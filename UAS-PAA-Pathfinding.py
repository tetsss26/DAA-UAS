import sys
import pygame
from queue import PriorityQueue

lebar = 400
screen = pygame.display.set_mode((lebar,lebar))
pygame.display.set_caption("Pathfinding Visualizer With A*")

maroon = (128,0,0) # Mulai Node
peachPuff = (255,218,185) # Node Status peachPuff
salmon = (250,128,114) # Node Akhir
slateGray = (112,128,144) # penghalang
grey = (142,166,180) #Pengisi Antar Node
firebrick = (178,34,34) # Pencarian Wilayah: jelajah
tomato = (255,99,71) # Pencarian Wilayah: pencarian
antiqueWhite = (250,235,215) # Jalur Node

class Node:
    def __init__(self, row, col, lebar, total_rows):
        self.row = row
        self.col = col
        self.x = row*lebar
        self.y = col*lebar
        self.color = peachPuff
        self.neighbors = []
        self.lebar = lebar
        self.total_rows = total_rows
    
    def get_pos(self):
        #mengembalikan posisi node sebagai (x,y)
        return self.row, self.col
    
    def is_closed(self):
        #kembali ketika tidak melihat node lagi
        return self.color == firebrick
    
    def is_open(self):
        #kembali jika simpul ada di node terbuka
        return self.color == tomato

    def is_wall(self):
        #kembali jika node tidak bisa dipertimbangkan
        return self.color == slateGray
    
    def is_end(self):
        #kembali jika telah mencapai tujuan akhir
        return self.color == salmon
    
    def reset(self):
        #mereset status node setelah traversal
        self.color = peachPuff

    def make_start(self):
        self.color = maroon

    def make_closed(self):
        self.color = firebrick

    def make_open(self):
        self.color = tomato
    
    def make_wall(self):
        self.color = slateGray
    
    def make_end(self):
        self.color = salmon
    
    def make_path(self):
        #jalur terakhir akan berwarna antiqueWhite
        self.color = antiqueWhite
    
    def draw(self,screen):
        #mengambar pygame rect untuk mewakili node
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.lebar,self.lebar))
    
    def update_neighbors(self,grid):
        #menemukan node terdekat untuk simpul yang diberikan
        self.neighbors = []
        # pergerakan ke bawah baris
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_wall():
            self.neighbors.append(grid[self.row+1][self.col])

        # pergerakan ke atas baris 
        if self.row > 0 and not grid[self.row-1][self.col].is_wall():
            self.neighbors.append(grid[self.row-1][self.col])

        # pergerakan ke kanan
        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_wall():
            self.neighbors.append(grid[self.row][self.col+1])

        # pergerakan ke kiri
        if self.col > 0 and not grid[self.row][self.col-1].is_wall():
            self.neighbors.append(grid[self.row][self.col-1])

    def __lt__(self):
        #membandingkan dua node
        return False

def heuristic(p1,p2):
    #perhitungan jarak Euclidean fungsi heuristik untuk pencarian jalur A*
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
          current = came_from[current]
          current.make_path()
          draw()

def algorithm(draw, grid, start, end):
    #algoritma pencarian jalan yang sebenarnya
    count = 0
    open_set = PriorityQueue()
    # menambahkan node awal ke P-Queue
    open_set.put((0, count, start))
    came_from = {}

    # mendefinisikan skor f dan g untuk pencarian jalan A*:
    # G: jarak dari node awal ke node saat ini
    # F: jarak yang diterima di akhir, menggunakan heuristic
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())
    
    # menambahkan node awal ke P-Queue
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    # mengakses node
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
        # membangun jalan
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
            
        for neighbor in current.neighbors:
            # mengansumsikan satu unit node terdekat sebagai satu unit node lebih jauh
            tmp_g = g_score[current] + 1

            if tmp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tmp_g
                f_score[neighbor] = tmp_g + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start:
            # pertimbangan node awal
            current.make_closed()
        
    return False

def make_grid(rows, lebar):
    #cara untuk mengelola semua node
    grid = []
    gap = lebar // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(screen, rows, lebar):
    gap = lebar // rows
    # garis horizontal diantara baris
    for i in range(rows):
        pygame.draw.line(screen, grey, (0, i*gap), (lebar, i*gap))
    # garis vertikal diantara kolom
        for j in range(rows):
            pygame.draw.line(screen, grey, (j*gap, 0), (j*gap, lebar))

def draw(screen, grid, rows, lebar):
    screen.fill(peachPuff)

    for row in grid:
        for spot in row:
            spot.draw(screen)
    
    draw_grid(screen, rows, lebar)
    pygame.display.update()

def get_clicked_pos(pos, rows, lebar):
    #mengembalikan node yang telah di klik
    gap = lebar // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(screen, lebar):
    ROWS = 15
    grid = make_grid(ROWS, lebar)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(screen, grid, ROWS, lebar)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
                        
            # mouse kiri
            if pygame.mouse.get_pressed()[0]:
                # mendapatkan posisi mouse
                pos = pygame.mouse.get_pos()
                # mendapatkan index node yang di klik
                row, col = get_clicked_pos(pos, ROWS, lebar)
                node = grid[row][col]
                # pembuatan posisi awal dan akhir
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()
                
                elif node != start and node != end:
                    node.make_wall()

            # mouse kanan
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos,ROWS, lebar)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    # menjalankan algoritma
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    
                    algorithm(lambda: draw(screen, grid, ROWS, lebar), grid, start, end)
                
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, lebar)

    sys.exit()

main(screen, lebar)
from queue import PriorityQueue
import pygame

width = 800
dis = pygame.display.set_mode((width, width))
pygame.display.set_caption("A* Path Finding Algorithm")

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (128, 0, 128)
orange = (255, 165, 0)
grey = (128, 128, 128)
turquoise = (64, 224, 208)

class Node():
    def __init__ (self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = white
        self.neighbours = []
        self.width = width
        self.total_rows= total_rows
    
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == red
    
    def is_open(self):
        return self.color == green
    
    def is_barrier(self):
        return self.color == black
    
    def is_start(self):
        return self.color == orange
    
    def is_end(self):
        return self.color == turquoise

    def reset(self):
        self.color = white

    def make_start(self):
        self.color = orange
    
    def make_close(self):
        self.color = red
    
    def make_open(self):
        self.color = green
    
    def make_barrier(self):
        self.color = black
    
    def make_end(self):
        self.color = turquoise

    def make_path(self):
        self.color = purple
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #DOWN
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #UP
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #LEFT
            self.neighbours.append(grid[self.row][self.col - 1])            

    def __lt__(self, other):
        return False



def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)



def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    q = []
    q.append(start)
    came_from = {}
    visited = {node: 0 for i in grid for node in i}
    visited[start] = 1

    while len(q) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr = q.pop(0)

        if curr == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return 1

        for i in curr.neighbours:
            if visited[i] != 1:
                visited[i] = 1
                came_from[i] = curr
                q.append(i)
                if i == end:
                    reconstruct_path(came_from, end, draw)
                    end.make_end()
                    return 1
                i.make_open()

        draw()
        if curr != start:
            curr.make_close()

    return 0

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid




def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, grey, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, grey, (j * gap, 0), (j * gap, width))





def draw(win, grid, rows, width):
    win.fill(white)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()




def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col





def main(win, width):
    rows = 50
    grid = make_grid(rows, width)

    start = None
    end = None

    run = True

    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()
                
                elif node != end and node != start:
                    node.make_barrier()
                
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start == None
                elif node == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    
                    algorithm(lambda: draw(win, grid, rows, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, width)
    pygame.quit()

main(dis, width)
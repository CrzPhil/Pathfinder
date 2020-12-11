from queue import PriorityQueue
import pygame
from pygame.locals import *
from tkinter import *

screen_width = 800
screen_height = 800
screen_color = (190, 190, 190)
grid_color = (0, 0, 0)

# PyGame Display Stuff
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Pathfinder")

# Colors for Nodes
gridlines = (133, 195, 207)
WHITE = (255, 255, 255)
GREEN = (42, 78, 83)
PURPLE = (248, 188, 36)
RED = (98, 199, 153)
ORANGE = (245, 136, 0)
BLACK = (5, 24, 33)
BLUE = (230, 57, 70)


class Node:
    def __init__(self, row, col, width, all_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.nextnode = []
        self.width = width
        self.all_rows = all_rows

    def getposition(self):
        return self.row, self.col

    def getclosed(self):
        return self.color == RED

    def getopen(self):
        return self.color == GREEN

    def getbarrier(self):
        return self.color == BLACK

    def getstart(self):
        return self.color == ORANGE

    def getend(self):
        return self.color == PURPLE

    def dostart(self):
        self.color = ORANGE

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.width))

    def res(self):
        self.color = WHITE

    def close(self):
        self.color = RED

    def open(self):
        self.color = GREEN

    def barrier(self):
        self.color = BLACK

    def doend(self):
        self.color = PURPLE

    def path(self):
        self.color = BLUE

    def up_neighbors(self, grid):
        self.nextnode = []
        if self.row < self.all_rows - 1 and not grid[self.row + 1][self.col].getbarrier():
            self.nextnode.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].getbarrier():
            self.nextnode.append(grid[self.row - 1][self.col])
        if self.col < self.all_rows - 1 and not grid[self.row][self.col + 1].getbarrier():
            self.nextnode.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].getbarrier():
            self.nextnode.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.path()
        draw()


def algo(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.getposition(), end.getposition())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.doend()
            return True

        for neighbor in current.nextnode:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.getposition(), end.getposition())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.open()

        draw()

        if current != start:
            current.close()

    return False


def heuristic(a, b):
    x1, y1 = a  # our 2 points a and b
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def makegrid(rows, width):
    grid = []
    sizebtwn = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, sizebtwn, rows)
            grid[i].append(node)
    return grid


def drawgrid(w, rows, surface):
    sizebtwn = w // rows
    for i in range(rows):
        pygame.draw.line(surface, gridlines, (0, i * sizebtwn), (w, i * sizebtwn))
        for j in range(rows):
            pygame.draw.line(surface, gridlines, (j * sizebtwn, 0), (j * sizebtwn, w))


def getclicked(position, rows, width):
    sizebtwn = width // rows
    y, x = position
    row = y // sizebtwn
    col = x // sizebtwn
    return row, col


def drawwindow(screen, grid, rows, width):
    screen.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(screen)
    drawgrid(width, rows, screen)
    pygame.display.update()


def main(screen, width):
    rows = 40

    running = True

    start = None
    end = None

    grid = makegrid(rows, width)

    while running:
        drawwindow(screen, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, col = getclicked(position, rows, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.dostart()
                elif not end and node != start:
                    end = node
                    end.doend()
                elif node != start and node != end:
                    node.barrier()
            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, col = getclicked(position, rows, width)
                node = grid[row][col]
                node.res()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.up_neighbors(grid)

                    algo(lambda: drawwindow(screen, grid, rows, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = makegrid(rows, width)

    pygame.quit()


main(screen, screen_width)

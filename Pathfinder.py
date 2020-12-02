import sys
import pygame
from pygame.locals import *
from tkinter import *
from tkinter import ttk


# Something about this being a standalone module, in order to avoid entanglements?

'''if __name__ == '__main__':
    main()'''


''' Takes arguments: size, flags, depth, display. Size is width and height,
 flags is collection of additional options, depth is number of bits to use for color'''


'''def callback():
    pass
'''
# Tkinter Prompt; Cannot store .Entries into a variable.
'''def prompt():
    global startNode, endNode
    window = Tk()
    window.title("Pathfinder")
    Label(window, text="Start Node (x,y)").grid(row=0)
    startNode = ttk.Entry(window)
    startNode.grid(row=0, column=1)
    Label(window, text="End Node (x,y)").grid(row=1)
    endNode = ttk.Entry(window)
    endNode.grid(row=1, column=1)
    Checkbutton(window, text="Show Process").grid(columnspan=2)
    Button(window, text="Start", width=10, command=callback).grid(columnspan=6)

    window.mainloop()


prompt()
print(startNode)'''
'''st = startNode.split(',')
ed = endNode.split(',')
print(''+st+' '+ed)'''

screen_width = 800
screen_height = 800
screen_color = (190, 190, 190)
grid_color = (0, 0, 0)
screen = pygame.display.set_mode([screen_width, screen_height])
screen.fill(screen_color)
pygame.display.set_caption("Pathfinder")
colorWhite = (255, 255, 255)
startGreen = (0, 255, 0)
endPurple = (128, 0, 128)


start = input("Choose start node (x,y): ").split(',')
end = input("Choose end node (x,y): ").split(',')
sx = 0
sy = 0
ex = 0
ey = 0

for i in range(0, int(start[0])):
    sx += 20
for i in range(0, int(start[1])):
    sy += 20
for i in range(0, int(end[0])):
    ex += 20
for i in range(0, int(end[1])):
    ey += 20

print(sx)
print(sy)


def drawgrid(w, rows, surface):
    sizebtwn = w // rows
    for i in range(0, w, sizebtwn):
        x, y = i, i
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global screen_width, row
    drawgrid(screen_width, row, surface)  # Will draw our grid lines
    pygame.display.update()  # Updates the screen


class Cube:
    def update(self, sizebtwn):
        x, y = pygame.mouse.get_pos()
        ix = x // sizebtwn
        iy = y // sizebtwn
        self.cx, self.cy = ix * sizebtwn, iy * sizebtwn
        self.square = pygame.Rect(self.cx, self.cy, sizebtwn, sizebtwn)

    def draw(self, surface, colour):
        click = pygame.mouse.get_pressed()
        if click[0]:
            pygame.draw.rect(surface, colour, self.square)


cube = Cube()


def main():
    pygame.init()
    global screen_width, screen_height, screen_color, row
    screen_width = 800
    screen_height = 800
    screen_color = (190, 190, 190)
    row = 40  # Rows in Grid
    running = True
    clock = pygame.time.Clock()
    pygame.draw.rect(screen, startGreen, pygame.Rect(sx, sy, 20, 20))
    pygame.draw.rect(screen, endPurple, pygame.Rect(ex, ey, 20, 20))
    while running:
        pygame.time.delay(50)
        clock.tick(60)
        redrawWindow(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        cube.update(screen.get_width() // 40)
        cube.draw(screen, colorWhite)
        pygame.display.flip()
        pygame.display.update()


main()


import sys
import pygame
from pygame.locals import *
import tkinter


# Something about this being a standalone module, in order to avoid entanglements?

'''if __name__ == '__main__':
    main()'''


'''# Takes arguments: size, flags, depth, display. Size is width and height,
 flags is collection of additional options, depth is number of bits to use for color'''


def callback():
    pass


def prompt():
    # global startnodex, startnodey, endnodex, endnodey
    window = tkinter.Tk()
    window.title("Pathfinder")
    tkinter.Label(window, text="Start Node (x, y)").grid(row=0)
    sx = tkinter.Entry(window).grid(row=0, column=1)
    sy = tkinter.Entry(window).grid(row=0, column=2)
    # startnodex = sx.get(), sy.get()
    tkinter.Label(window, text="End Node (x, y)").grid(row=1)
    ex = tkinter.Entry(window).grid(row=1, column=1)
    ey = tkinter.Entry(window).grid(row=1, column=2)
    # endnodex = ex.get(), ey.get()
    tkinter.Checkbutton(window, text="Show Process").grid(columnspan=2)
    tkinter.Button(window, text="Start", width=10, command=callback).grid(columnspan=6)

    window.mainloop()


prompt()


screen_width = 800
screen_height = 800
screen_color = (190, 190, 190)
grid_color = (0, 0, 0)
screen = pygame.display.set_mode([screen_width, screen_height])
screen.fill(screen_color)
pygame.display.set_caption("Pathfinder")


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

    def draw(self, surface):
        click = pygame.mouse.get_pressed()
        if click[0]:
            pygame.draw.rect(surface, (255, 255, 255), self.square)


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
        cube.draw(screen)
        pygame.display.flip()
        pygame.display.update()


main()


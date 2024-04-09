import pygame as pg
from pygame.locals import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)

def draw_background() -> None:
    screen.blit(bg, (0, 0))

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pg.Surface(screen.get_size())
bg.fill(WHITE)

clock = pg.time.Clock()
start_point = (0, 0)
end_point = (0, 0)
# size = (0, 0)
drawing = False

run = True
while run:
    # clock.tick(FPS)
    draw_background()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            start_point = event.pos
            end_point = event.pos
            # size = (0,0)
            drawing = True
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            end_point = event.pos
            # size = end_point[0] - start_point[0], end_point[1] - start_point[1]
            drawing = False
        elif event.type ==  MOUSEMOTION and drawing:
            end_point = event.pos
            # size = end_point[0] - start_point[0], end_point[1] - start_point[1]

    # rect = pg.Rect(rpos[0], rpos[1], pos2[0]-rpos[0], pos2[1]-rpos[1])
    rect = pg.Rect(start_point[0],start_point[1],end_point[0] - start_point[0], end_point[1] - start_point[1])
    rect.normalize()
    pg.draw.rect(screen, RED, rect, 2)
    pg.display.update()
pg.quit()


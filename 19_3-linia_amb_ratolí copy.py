import pygame as pg
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)

def draw_background() -> None:
    screen.blit(bg, (0, 0))

def ctrl_pressed() -> bool:
    return pg.key.get_pressed()[pg.K_LCTRL] or pg.key.get_pressed()[pg.K_RCTRL]

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pg.Surface(screen.get_size())
bg.fill(WHITE)

rect = pg.Rect(0,0,0,0)
drawing = False
rectangles = []
color = BLACK

run = True
while run:
    draw_background()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            x1,y1 = event.pos
            rect = pg.Rect((x1,y1), (0, 0))
            drawing = True
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            drawing = False
            if rect.width>0 and rect.height>0:
                rectangles.append(rect.copy())

    if drawing:
        x2, y2 = pg.mouse.get_pos()

        if ctrl_pressed():
            radius = math.hypot(rect.width, rect.height)
            pg.draw.circle(screen, BLACK, (x1,y1), radius, 2)
        else:
            pg.draw.line(screen, BLACK, (x1, y1), (x2, y2), 2 )

    for rectangle in rectangles:
        # pg.draw.rect(screen, color, rectangle, 2)
        pg.draw.ellipse(screen, color, rectangle, 2)

    pg.display.update()
    
pg.quit()


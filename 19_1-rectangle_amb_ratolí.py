import pygame as pg

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)

def draw_background() -> None:
    screen.blit(bg, (0, 0))

def sign(value:int) -> int:
    if value>=0:
        return 1
    return -1

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
            x1, y1 = event.pos
            rect = pg.Rect((x1,y1), (0, 0))
            drawing = True
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            drawing = False
            if rect.width>0 and rect.height>0:
                rectangles.append(rect.copy())

    if drawing:
        x2, y2 = pg.mouse.get_pos()
        rect.topleft = min(x1,x2), min(y1, y2)
        rect.width = abs(x2-x1)
        rect.height = abs(y2-y1)
        if ctrl_pressed():
            maxim = max(rect.width, rect.height)
            rect.width = maxim
            rect.height = maxim
            x, y = x1 + maxim * sign(x2-x1), y1 + maxim * sign(y2-y1)
            rect.topleft = min(x1,x), min(y1, y)
        pg.draw.rect(screen, color, rect, 2)

    for rectangle in rectangles:
        pg.draw.rect(screen, color, rectangle, 2)

    pg.display.update()
    
pg.quit()


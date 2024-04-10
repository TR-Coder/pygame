import pygame as pg
from enum import Enum
from typing import Tuple, List

pg.init()

info = pg.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)

class Figure_type(Enum):
    LINE=0
    CIRCLE=1
    ELLIPSE=2
    RECTANGLE=3
    TRIANGLE=4

Coord_ = Tuple[int,int]
Color_ = Tuple[int,int,int]
Group_ = pg.sprite.Group
Surface_ = pg.Surface

# class Figure:
#     def __init__(self, x1y1:Coord_, width:int, color:Color_) -> None:
#         self.x1 = x1y1[0]
#         self.y1 = x1y1[1]
#         self.width = width
#         self.color = color

class Rectangle():
    def __init__(self, rect:pg.Rect, width: int, color:Color_):
        self.rect = rect
        self.width = width
        self.color = color

class Ellipse():
    def __init__(self, rect:pg.Rect, width: int, color:Color_):
        self.rect = rect
        self.width = width
        self.color = color

figures:List[any] = []
current_figure:Figure_type = Figure_type.ELLIPSE
current_rect: pg.Rect
current_color:Color_ = BLACK
current_width:int = 2
selection:bool = False

def draw_background() -> None:
    screen.blit(bg, (0, 0))

def sign(value:int) -> int:
    if value>=0:
        return 1
    return -1

def ctrl_pressed() -> bool:
    return pg.key.get_pressed()[pg.K_LCTRL] or pg.key.get_pressed()[pg.K_RCTRL]

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pg.Surface(screen.get_size())
bg.fill(WHITE)
drawing = False

run = True
while run:
    draw_background()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            x1, y1 = event.pos
            if selection:
                pass
            else:
                if current_figure in [Figure_type.RECTANGLE, Figure_type.ELLIPSE]:
                    current_rect = pg.Rect((x1,y1), (0, 0))
                drawing = True

        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if current_figure == Figure_type.RECTANGLE:
                if current_rect.width>0 and current_rect.height>0:
                    rectangle = Rectangle(current_rect, current_width, current_color)
                    figures.append(rectangle)
            elif current_figure == Figure_type.ELLIPSE:
                if current_rect.width>0 and current_rect.height>0:
                    ellipse = Ellipse(current_rect, current_width, current_color)
                    figures.append(ellipse)
            drawing = False

    if drawing:
        x2, y2 = pg.mouse.get_pos()
        if current_figure == Figure_type.RECTANGLE:
            current_rect.topleft = min(x1,x2), min(y1, y2)
            current_rect.width = abs(x2-x1)
            current_rect.height = abs(y2-y1)
            if ctrl_pressed():
                maxim = max(current_rect.width, current_rect.height)
                current_rect.width = maxim
                current_rect.height = maxim
                x, y = x1 + maxim * sign(x2-x1), y1 + maxim * sign(y2-y1)
                current_rect.topleft = min(x1,x), min(y1, y)
            pg.draw.rect(screen, current_color, current_rect, 2)

    for figure in figures:
        if isinstance(figure, Rectangle):
            pg.draw.rect(screen, figure.color, figure.rect, figure.width)
        elif isinstance(figure, Ellipse):
            pg.draw.ellipse(screen, figure.color, figure.rect, figure.width)

    pg.display.update()
    
pg.quit()





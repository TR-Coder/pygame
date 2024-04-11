import pygame as pg
from enum import Enum
from typing import Tuple, List, Any

pg.init()
info = pg.display.Info()
SPACE_FOR_WINDOW_TITLE_BAR = 60
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h - SPACE_FOR_WINDOW_TITLE_BAR
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)

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

class Button_type(Enum):
    LINE=0
    ELLIPSE=1
    RECTANGLE=2
    NOT_FILL=3
    FILL=4
    SMALL=5
    MEDIUM=6
    LARGE=7
    UNDO=8

Coord_ = Tuple[int,int]
Color_ = Tuple[int,int,int]
Group_ = pg.sprite.Group
Surface_ = pg.Surface

class Button:
    side = 50
    color = (169, 169, 200)
    def __init__(self, type:Button_type) -> None:
        self.type = type
        self.surface = pg.Surface((self.side, self.side))
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        pg.draw.rect(self.surface, BLACK, self.rect, 1)
    
    def coord(self, xy:Coord_) -> None:
        self.rect.x = xy[0]
        self.rect.y = xy[1]

class TaskBar:
    color = (169, 169, 169)
    def __init__(self, buttons:List[Button]) -> None:
        width = pg.display.Info().current_w
        self.surface = pg.Surface((width, 101))
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        self.buttons:list[Button] = buttons


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

figures:List[Any] = []
current_figure:Figure_type = Figure_type.ELLIPSE
current_rect: pg.Rect
current_color:Color_ = BLACK
current_width:int = 2
old_width = 1

def draw_background() -> None:
    screen.fill(WHITE)

def Taskbar() -> TaskBar:
    bt1 = Button(Button_type.LINE)
    pg.draw.line(bt1.surface, BLACK, (10,40), (40,10), 2)
 
    bt2 = Button(Button_type.ELLIPSE)
    pg.draw.ellipse(bt2.surface, BLACK, bt2.rect.inflate(-10,-20), 2)

    bt3 = Button(Button_type.RECTANGLE)
    pg.draw.rect(bt3.surface, BLACK, bt3.rect.inflate(-20,-20), 2)

    bt4 = Button(Button_type.NOT_FILL)
    pg.draw.ellipse(bt4.surface, BLACK, bt4.rect.inflate(-20,-20), 2)

    bt5 = Button(Button_type.FILL)
    pg.draw.ellipse(bt5.surface, BLACK, bt5.rect.inflate(-20,-20))

    bt6 = Button(Button_type.SMALL)
    pg.draw.line(bt6.surface, BLACK, (10,25), (40,25), 1)    

    bt7 = Button(Button_type.MEDIUM)
    pg.draw.line(bt7.surface, BLACK, (10,25), (40,25), 3)

    bt8 =Button(Button_type.LARGE)
    pg.draw.line(bt8.surface, BLACK, (10,25), (40,25), 5)    

    bt9 = Button(Button_type.UNDO)
    font = pg.font.SysFont('calibri',30,bold=True)
    img_txt = font.render('←', True, BLACK)
    rect_txt = img_txt.get_rect(center=bt9.rect.center)
    bt9.surface.blit(img_txt, rect_txt)    

    buttons = [bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9]
    tb = TaskBar(buttons)
    
    bt1.rect.center = tb.rect.center
    for button,i in zip(buttons,[0,1,2, 4,5, 7,8,9, 11]):
        button.coord((30+(50+30)*i, bt1.rect.y))
        tb.surface.blit(button.surface, button.rect)

    return tb

def sign(value:int) -> int:
    return 1 if value>=0 else -1

def ctrl_pressed() -> bool:
    return pg.key.get_pressed()[pg.K_LCTRL] or pg.key.get_pressed()[pg.K_RCTRL]

drawing = False
taskbar:TaskBar
taskbar = Taskbar()

run = True
while run:

    draw_background()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            x1, y1 = event.pos
            if taskbar.rect.collidepoint((x1,y1)):
                for button in taskbar.buttons:
                    if button.rect.collidepoint((x1,y1)):
                        if button.type == Button_type.FILL:
                            old_width = current_width
                            current_width = 0
                        if button.type == Button_type.NOT_FILL:
                            if current_width == 0:
                                current_width = old_width
                        elif button.type == Button_type.SMALL:
                            current_width = 1
                        elif button.type == Button_type.MEDIUM:
                            current_width = 3
                        elif button.type == Button_type.LARGE:
                            current_width = 5
            else:
                if current_figure in [Figure_type.RECTANGLE, Figure_type.ELLIPSE]:
                    current_rect = pg.Rect((x1,y1), (0, 0))
                drawing = True

        if event.type == pg.MOUSEBUTTONUP and event.button == 1 and drawing:
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
            pg.draw.rect(screen, current_color, current_rect, current_width)
        if current_figure == Figure_type.ELLIPSE:
            current_rect.topleft = min(x1,x2), min(y1, y2)
            current_rect.width = abs(x2-x1)
            current_rect.height = abs(y2-y1)
            pg.draw.ellipse(screen, current_color, current_rect, current_width)

    for figure in figures:
        if isinstance(figure, Rectangle):
            pg.draw.rect(screen, figure.color, figure.rect, figure.width)
        elif isinstance(figure, Ellipse):
            pg.draw.ellipse(screen, figure.color, figure.rect, figure.width)

    screen.blit(taskbar.surface, (0,0))
    pg.display.update()
    
pg.quit()





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
    STROKE=4

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
    STROKE=9

Coord_ = Tuple[int,int]
Color_ = Tuple[int,int,int]
Group_ = pg.sprite.Group
Surface_ = pg.Surface

FPS=60
clock = pg.time.Clock()

undo_button_pressed = False
hold_time_undo_button:float = 0
dt = clock.tick(FPS) /1000               # FPS duration

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
        self.buttons:List[Button] = buttons


class Rectangle:
    def __init__(self, rect:pg.Rect, width: int, color:Color_):
        self.rect = rect
        self.width = width
        self.color = color

class Ellipse:
    def __init__(self, rect:pg.Rect, width: int, color:Color_):
        self.rect = rect
        self.width = width
        self.color = color

class Line:
    def __init__(self, x1y1:Coord_, x2y2:Coord_, width:int, color:Color_) -> None:
        self.x1y1 = x1y1
        self.x2y2 = x2y2
        self.width = width
        self.color = color

figures:List[Any] = []
current_figure:Figure_type = Figure_type.ELLIPSE
current_rect: pg.Rect
current_color:Color_ = BLACK
current_width:int = 1
current_line_width:int = 1
old_width = 1
x1:int
x2:int
y1:int
y2:int

def draw_background() -> None:
    screen.fill(WHITE)

def Taskbar() -> TaskBar:
    bt1 = Button(Button_type.LINE)
    pg.draw.line(bt1.surface, BLACK, (10,40), (40,10), 2)
 
    bt2 = Button(Button_type.ELLIPSE)
    pg.draw.ellipse(bt2.surface, BLACK, bt2.rect.inflate(-10,-20), 2)

    bt3 = Button(Button_type.RECTANGLE)
    pg.draw.rect(bt3.surface, BLACK, bt3.rect.inflate(-20,-20), 2)

    bt4 = Button(Button_type.STROKE)
    font = pg.font.SysFont('calibri', 50)
    img_txt = font.render('~', True, BLACK)
    rect_txt = img_txt.get_rect(center=bt4.rect.center)
    bt4.surface.blit(img_txt, rect_txt)

    bt5 = Button(Button_type.NOT_FILL)
    pg.draw.ellipse(bt5.surface, BLACK, bt4.rect.inflate(-20,-20), 2)

    bt6 = Button(Button_type.FILL)
    pg.draw.ellipse(bt6.surface, BLACK, bt5.rect.inflate(-20,-20))

    bt7 = Button(Button_type.SMALL)
    pg.draw.line(bt7.surface, BLACK, (10,25), (40,25), 1)    

    bt8 = Button(Button_type.MEDIUM)
    pg.draw.line(bt8.surface, BLACK, (10,25), (40,25), 3)

    bt9 =Button(Button_type.LARGE)
    pg.draw.line(bt9.surface, BLACK, (10,25), (40,25), 5)    

    bt10 = Button(Button_type.UNDO)
    font = pg.font.SysFont('calibri',30,bold=True)
    img_txt = font.render('←', True, BLACK)
    rect_txt = img_txt.get_rect(center=bt10.rect.center)
    bt10.surface.blit(img_txt, rect_txt)    

    buttons = [bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9, bt10]
    tb = TaskBar(buttons)
    
    bt1.rect.center = tb.rect.center
    for button,i in zip(buttons,[0,1,2,3, 5,6, 8,9,10, 11]):
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
    clock.tick(FPS)
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
                        elif button.type == Button_type.NOT_FILL:
                            if current_width == 0:
                                current_width = old_width
                        elif button.type == Button_type.SMALL:
                            current_width = 1
                            current_line_width = 1
                        elif button.type == Button_type.MEDIUM:
                            current_width = 3
                            current_line_width = 3
                        elif button.type == Button_type.LARGE:
                            current_width = 5
                            current_line_width = 5
                        elif button.type == Button_type.LINE:
                            current_figure = Figure_type.LINE
                        elif button.type == Button_type.ELLIPSE:
                            current_figure = Figure_type.ELLIPSE
                        elif button.type == Button_type.RECTANGLE:
                            current_figure = Figure_type.RECTANGLE
                        elif button.type == Button_type.STROKE:
                            current_figure = Figure_type.STROKE
                        elif button.type == Button_type.UNDO:
                            undo_button_pressed = True
                            if figures:
                                figures.pop()
            else:
                if current_figure in [Figure_type.RECTANGLE, Figure_type.ELLIPSE]:
                    current_rect = pg.Rect((x1,y1), (0, 0))
                drawing = True

        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            undo_button_pressed = False
            hold_time_undo_button = 0
            if drawing:
                if current_figure == Figure_type.RECTANGLE:
                    if current_rect.width>0 and current_rect.height>0:
                        rectangle = Rectangle(current_rect, current_width, current_color)
                        figures.append(rectangle)
                elif current_figure == Figure_type.ELLIPSE:
                    if current_rect.width>0 and current_rect.height>0:
                        ellipse = Ellipse(current_rect, current_width, current_color)
                        figures.append(ellipse)
                elif current_figure == Figure_type.LINE:
                    x2, y2 = pg.mouse.get_pos()
                    line = Line((x1,y1), (x2,y2), current_line_width, current_color)
                    figures.append(line)
            drawing = False

        if event.type == pg.MOUSEMOTION and drawing and current_figure==Figure_type.STROKE:
            x2, y2 = pg.mouse.get_pos()
            line = Line((x1,y1), (x2,y2), current_line_width, current_color)
            figures.append(line)
            x1, y1 = x2, y2

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

        elif current_figure == Figure_type.ELLIPSE:
            current_rect.topleft = min(x1,x2), min(y1, y2)
            current_rect.width = abs(x2-x1)
            current_rect.height = abs(y2-y1)
            pg.draw.ellipse(screen, current_color, current_rect, current_width)
            
        elif current_figure == Figure_type.LINE or current_figure == Figure_type.STROKE:
            pg.draw.line(screen, current_color, (x1,y1), (x2, y2), current_line_width)
    else:
        if undo_button_pressed:
            hold_time_undo_button += dt
            if hold_time_undo_button > 1:
                if figures:
                    figures.pop()


    for figure in figures:
        if isinstance(figure, Rectangle):
            pg.draw.rect(screen, figure.color, figure.rect, figure.width)
        elif isinstance(figure, Ellipse):
            pg.draw.ellipse(screen, figure.color, figure.rect, figure.width)
        elif isinstance(figure, Line):
            pg.draw.line(screen, figure.color, figure.x1y1, figure.x2y2, figure.width)

    screen.blit(taskbar.surface, (0,0))
    pg.display.update()
    
pg.quit()





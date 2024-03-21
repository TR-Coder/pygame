import pygame as pg
from enum import Enum
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)

pg.init()
font = pg.font.SysFont('Bauhaus 93', 60)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pg.Surface(screen.get_size())
bg.fill(WHITE)
clock = pg.time.Clock()

Coord_ = tuple[int,int]
Color_ = tuple[int,int,int]
Group_ = pg.sprite.Group
Surface_ = pg.Surface

class MouseClick(Enum):
    NOT_PRESSED=0
    DOWN=1
    UP=2

def draw_background() -> None:
    screen.blit(bg, (0, 0))

class Button(pg.sprite.Sprite):
    def __init__(self, x:int, y:int, radius:int, color: Color_, image:Surface_, group: Group_) -> None:
        super().__init__(group)
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color  
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def update(self, mouse_clicked: MouseClick):
        mouse_position = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_position) and mouse_clicked == MouseClick.DOWN:
            self.rect.move_ip(2,2)
            self.clicked = True
        elif self.clicked:
            self.rect.x, self.rect.y = self.x, self.y
            self.clicked = False

working_directory = os.path.split(os.path.abspath(__file__))[0]
assets_directory = os.path.join(working_directory, 'data')
images_list: list[pg.Surface] = []
img_path:str = os.path.join(assets_directory, 'push.png')
image:pg.Surface = pg.image.load(img_path).convert_alpha()   # convert_alpha() fa que funcione la transparència del .png
size:tuple[int, int] = image.get_size()
width, height = size[0], size[1]
scale = 0.1
image = pg.transform.scale(image, (width * scale, height * scale))         
images_list.append(image)

buttons_group:Group_ = pg.sprite.Group()
button1 = Button(x=100, y=100, radius=55, color=BLACK, image=images_list[0], group=buttons_group)
# button2 = Button(x=250, y=100, radius=55, color=BLUE, symbol='-', group=buttons_group)
# button2 = Button(x=400, y=100, radius=55, color=RED, symbol='#', group=buttons_group)

def main() -> None:
    pg.display.set_caption('Clock')
    mouse_click:MouseClick

    run = True
    while run:
        clock.tick(FPS)
        draw_background()
        mouse_click = MouseClick.NOT_PRESSED
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = MouseClick.DOWN
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                mouse_click = MouseClick.UP

        if mouse_click != MouseClick.NOT_PRESSED:
            buttons_group.update(mouse_click)
        buttons_group.draw(screen)
        pg.display.update()
    pg.quit()
    
if __name__ == '__main__':
    main()
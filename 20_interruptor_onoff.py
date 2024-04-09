import pygame as pg
import os
from enum import Enum

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)

class Switch(Enum):
    ON=0
    OFF=1

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

bg = pg.Surface(screen.get_size())
bg.fill(WHITE)


def load_image(name:str, scale:float) -> pg.Surface:
    working_directory = os.path.split(os.path.abspath(__file__))[0]
    assets_directory = os.path.join(working_directory, 'data')
    img_path:str = os.path.join(assets_directory, name)
    image:pg.Surface = pg.image.load(img_path).convert_alpha()
    size:tuple[int, int] = image.get_size()
    width, height = size[0], size[1]
    image = pg.transform.scale(image, (width * scale, height * scale))  
    return image

    

image_off = load_image('interruptor_off.png', 1)
image_on = load_image('interruptor_on.png', 1)
clock = pg.time.Clock()
switch:Switch = Switch.OFF


def draw_background(state:Switch) -> None:
    if state == Switch.OFF:
        bg.fill(BLACK)
        screen.blit(bg, (0, 0))
    else:
        bg.fill(WHITE)
        screen.blit(bg, (0, 0))


def draw_switch(state:Switch) -> None:
    if state == Switch.OFF:
        rect = image_off.get_rect(center=screen.get_rect().center)
        screen.blit(image_off, rect)
    else:
        rect = image_on.get_rect(center=screen.get_rect().center)
        screen.blit(image_on, rect)

def main() -> None:
    global switch
    run = True
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                switch = Switch.OFF if switch==Switch.ON else Switch.ON

        draw_background(state=switch)
        draw_switch(state=switch)
        pg.display.update()
    pg.quit()

if __name__ == '__main__':
    main()
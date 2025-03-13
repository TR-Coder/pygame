from __future__ import annotations
import pygame as pg
import os
from enum import Enum

W = 800
H = 400
FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)

class Switch(Enum):
    ON=0
    OFF=1


def load_image(name:str, scale:float=1) -> pg.Surface:
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),name)
    image:pg.Surface = pg.image.load(img_path).convert_alpha()
    width, height = image.get_size()
    image = pg.transform.scale(image, (width * scale, height * scale))  
    return image


def draw_background(state:Switch) -> None:
    if state == Switch.OFF:
        bg.fill(WHITE)
        screen.blit(bg, (0, 0))
    else:
        bg.fill(BLACK)
        screen.blit(bg, (0, 0))


def draw_switch(state:Switch) -> None:
    if state == Switch.OFF:
        # rect = image_off.get_rect(center=screen.get_rect().center)
        rect = image_off.get_rect()
        rect.center=screen.get_rect().center
        screen.blit(image_off, rect)
    else:
        rect = image_on.get_rect(center=screen.get_rect().center)
        screen.blit(image_on, rect)

def main() -> None:

    switch:Switch = Switch.OFF

    run = True
    while run:
        # clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                switch = Switch.OFF if switch==Switch.ON else Switch.ON

        draw_background(state=switch)
        draw_switch(state=switch)
        pg.display.update()

if __name__ == '__main__':
    pg.init()

    screen = pg.display.set_mode((W,H))
    bg = pg.Surface(screen.get_size())
    bg.fill(WHITE)

    image_off = load_image('data/interruptor_off.png')
    image_on = load_image('data/interruptor_on.png')

    clock = pg.time.Clock()

    main()

    pg.quit()
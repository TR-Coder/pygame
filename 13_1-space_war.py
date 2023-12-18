# https://www.youtube.com/watch?v=Mw81qlbBbqk&list=PLjcN1EyupaQkAQyBCYKyf1jt1M1PiRJEp&index=5

import pygame as pg
from math import ceil
import random

pg.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 60
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)
SPACECRAFT_SPEED = 5
TIME_BETWEEN_SHOTS = 300 # ms
INVIDER_ROWS = 5
INVIDER_COLUMNS = 4


screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Space war')
font = pg.font.SysFont('Bauhaus 93', 60)

# last_shot_time = pg.time.get_ticks()

clock = pg.time.Clock()
image = pg.image.load("data/space_war/bg.png")


# ===========================================================================================
def complete_stage(image: pg.Surface) -> pg.Surface:
    w = image.get_width()
    h = image.get_height()
    times = ceil(SCREEN_WIDTH / w)   
    combined_image = pg.Surface((w*times, h)).convert_alpha()
    for t in range(times):
        combined_image.blit(image, (w*t, 0))
    return combined_image

# ===========================================================================================
def draw_background():
    screen.blit(bg_img, (0,0))

# ===========================================================================================
def draw_text(text:str, x:int, y:int):
    img = font.render(text, True, WHITE_COLOR)
    image = complete_stage(img)
    screen.blit(image, (x,y))

# ===========================================================================================
class Spacecraft(pg.sprite.Sprite):
    def __init__(self, x:int, y:int, energy: int, *groups: pg.sprite.Group) -> None:
        super().__init__(*groups)
        self.image = pg.image.load('data/space_war/spaceship.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.energy = energy
        self.last_time = pg.time.get_ticks()

    def update(self):
        key = pg.key.get_pressed()
        if key[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= SPACECRAFT_SPEED
        if key[pg.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += SPACECRAFT_SPEED
        
        now = pg.time.get_ticks()
        if key[pg.K_SPACE] and (now - self.last_time) > TIME_BETWEEN_SHOTS:
            Shot(self.rect.centerx, self.rect.top, shot_group)
            self.last_time = now

# ===========================================================================================
class Shot(pg.sprite.Sprite):
    def __init__(self, x:int, y:int, *groups: pg.sprite.Group) -> None:
        super().__init__(*groups)
        self.image = pg.image.load('data/space_war/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        

bg_img = complete_stage(image)
spacecraft_group: pg.sprite.Group = pg.sprite.Group()
shot_group: pg.sprite.Group = pg.sprite.Group()
invider_group: pg.sprite.Group = pg.sprite.Group()
spacecraft = Spacecraft(SCREEN_WIDTH//2, SCREEN_HEIGHT-100, 3, spacecraft_group)


# ===========================================================================================
class Invider(pg.sprite.Sprite):
    def __init__(self, x:int, y:int, *groups: pg.sprite.Group) -> None:
        super().__init__(*groups)
        fate = str(random.randint(1,5))
        self.image = pg.image.load(f'data/space_war/alien{fate}.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x_increment = 2
        self.x_increment_counter = 0

    def update(self):
        self.rect.x += self.x_increment
        self.x_increment_counter += 1
        if self.x_increment_counter > 75:
            self.x_increment_counter = 0
            self.x_increment *= -1

# ===========================================================================================
def create_inviders():
    for r in range(INVIDER_ROWS):
        for c in range(INVIDER_COLUMNS):
            Invider(100+c*200, 100+r*70, invider_group)

# ===========================================================================================

create_inviders()

run = True
while run:
    clock.tick(FPS)
    draw_background()

    spacecraft_group.update()
    shot_group.update()
    invider_group.update()


    spacecraft_group.draw(screen)
    shot_group.draw(screen)
    invider_group.draw(screen)

    for event in pg.event.get():
        if event.type==pg.QUIT:
            run=False
    


    pg.display.update()

pg.quit()













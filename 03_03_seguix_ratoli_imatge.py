import pygame as pg
import math
import time
from typing import Tuple, Union, Optional, List

pg.init()

#game window
W = 800
H = 450
BLUE = pg.Color(0, 0, 255)

screen = pg.display.set_mode((W, H))
pg.display.set_caption('Following mouse')

mouse_x, mouse_y = W/2, H/2
sprite_x, sprite_y = W/2, H/2

img = pg.image.load('data/mosquit.png').convert_alpha()
size_x, size_y = img.get_size()
scaled_size = (size_x * 0.15, size_y * 0.15)
img = pg.transform.scale(img, scaled_size)
sprite_rect = img.get_rect()
  
speed = 1
dx, dy = 0.0, 0.0
counter = 0

run = True
while run:

  screen.fill("turquoise1")

  for event in pg.event.get():
    if event.type == pg.MOUSEMOTION:
        mouse_x, mouse_y =  event.pos
        dist = math.hypot(mouse_x - sprite_rect.centerx, mouse_y - sprite_rect.centery)
        dx, dy = (mouse_x - sprite_rect.centerx) / dist, (mouse_y - sprite_rect.centery) / dist

    if event.type == pg.QUIT:
      run = False

  counter += 1
  if counter == 5:
    sprite_x += 0 if int(sprite_x) == mouse_x else  dx * speed
    sprite_y += 0 if int(sprite_y) == mouse_y else  dy * speed
    counter = 0

  # -----
  sprite_rect.center = int(sprite_x), int(sprite_y)
  screen.blit(img, sprite_rect)
  # -----

  pg.display.flip()

pg.quit()
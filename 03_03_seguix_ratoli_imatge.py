import pygame as pg
import math
import time
from typing import Tuple, Union, Optional, List

pg.init()

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
BLUE = pg.Color(0, 0, 255)

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Following mouse')

target_x, target_y = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
x, y = SCREEN_WIDTH/2, SCREEN_HEIGHT/2

# -----------------
img = pg.image.load(f'data/mosquit.png').convert_alpha()
size:Tuple[int, int] = img.get_size()
scaled_size:Tuple[float, float] = (size[0] * 0.15, size[1] * 0.15)
img = pg.transform.scale(img, scaled_size)
rect = img.get_rect()
# -----------------
  
speed = 1
dx, dy = 0.0, 0.0
counter = 0

run = True
while run:

  screen.fill("turquoise1")

  for event in pg.event.get():
    if event.type == pg.MOUSEMOTION:
        target_x, target_y =  event.pos
        # ----
        dist = math.hypot(target_x - rect.centerx, target_y - rect.centery)
        dx, dy = (target_x - rect.centerx) / dist, (target_y - rect.centery) / dist
        # ----

    if event.type == pg.QUIT:
      run = False

  counter += 1
  if counter == 5:
    x += 0 if int(x) == target_x else  dx * speed
    y += 0 if int(y) == target_y else  dy * speed
    counter = 0

  # -----
  rect.center = int(x), int(y)
  screen.blit(img, rect)
  # -----

  pg.display.flip()

pg.quit()
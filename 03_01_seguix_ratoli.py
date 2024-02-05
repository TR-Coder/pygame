import pygame as pg
import math
import time

pg.init()

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
BLUE = pg.Color(0, 0, 255)

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Following mouse')

target_x, target_y = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
x, y = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
speed = 1
dx, dy = 0.0, 0.0
counter = 0

run = True
while run:

  screen.fill("turquoise1")
  pg.draw.circle(screen, BLUE, (int(x),int(y)), 20)

  for event in pg.event.get():
    if event.type == pg.MOUSEMOTION:
        target_x, target_y =  pg.mouse.get_pos()
        dist = math.hypot(target_x - x, target_y - y)
        dx, dy = (target_x - x) / dist, (target_y - y) / dist

    if event.type == pg.QUIT:
      run = False

  counter += 1
  if counter == 10:
    x += 0 if int(x) == target_x else  dx * speed
    y += 0 if int(y) == target_y else  dy * speed
    counter = 0


  pg.display.flip()

pg.quit()
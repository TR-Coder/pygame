import pygame as pg
import math
import random
from enum import Enum
from typing import Tuple, Union, Optional, List

pg.init()
clock = pg.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
BLUE = pg.Color(0, 0, 255)
RED = pg.Color(255, 0, 0)
BLACK = pg.Color(0,0,0)
YELLOW = pg.Color(255,255,0)
SIDE = 25

class Type(Enum):
    Reward=0
    Obstacle=1

class Timer():
    def __init__(self, ms: int):
        self.ticks = ms
        self.initial_time = pg.time.get_ticks()

    def is_over(self) -> bool:
        elapsed_time = pg.time.get_ticks() - self.initial_time
        if elapsed_time > self.ticks:
            self.initial_time += elapsed_time
            return True
        return False
    
def collides_with_figures(rect:pg.Rect, exclude: Union[pg.Rect,None] = None) -> bool:
  return any(rect.colliderect(f.rect) for f in figures if f.rect != exclude)

def calculate_position() -> pg.Rect:
  while True:
    rect = pg.Rect(random.randint(SIDE, SCREEN_WIDTH-SIDE), random.randint(SIDE, SCREEN_HEIGHT-SIDE), SIDE, SIDE)
    if not collides_with_figures(rect):
      return rect

class Figure:
    def __init__(self, type:Type) -> None:
      self.rect = calculate_position()
      self.timer =  Timer(ms=random.randint(1000,2000))
      self.color = random.choice([RED, BLACK, BLUE])
      self.type = type
  
    def move(self) -> None:
      # Per a limitar el valor d'una variable x a un interval [a,b] podem fer:  x = max(min(x, b), a)
      # min(x,b) assegura que x no supera b, si ho fa retorna b.
      # max(min(x, b), a) assegura que el valor resultant no és menor que a. 
      # Si el resultat de min(x, b) es menor que a, aleshores retorna a.
      new_rect = pg.Rect.copy(self.rect)
      x_min = y_min = 0
      x_max = SCREEN_WIDTH - SIDE
      y_max = SCREEN_HEIGHT - SIDE
      while True:
        new_rect.x = max(x_min, min(x_max, new_rect.x + random.randint(-20, 20)))
        new_rect.y = max(y_min, min(y_max, new_rect.y + random.randint(-20, 20)))
        if not collides_with_figures(new_rect, self.rect):
          self.rect = new_rect
          return

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Following mouse')

target_x, target_y = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
speed = 1
dx, dy = 0.0, 0.0
counter = 0

# list with obstacle figures and reward.
figures:List[Figure] = []
for _ in range(20):
   figures.append(Figure(type=Type.Obstacle))
figure_reward = Figure(type=Type.Reward)
figures.append(figure_reward)


rect = calculate_position()
x:float = rect.centerx
y:float = rect.centery
circle_rect = pg.Rect(x-SIDE, y-SIDE, SIDE*2, SIDE*2)

run = True
while run:
  screen.fill("turquoise1")
  pg.draw.circle(screen, BLUE, (int(x),int(y)), 20)

  for event in pg.event.get():
    if event.type == pg.MOUSEMOTION:
        target_x, target_y = event.pos
        dist = math.hypot(target_x - x, target_y - y)
        dx, dy = (target_x - x) / dist, (target_y - y) / dist

    if event.type == pg.QUIT:
      run = False

  counter += 1
  if counter == 10:
    x += 0 if int(x) == target_x else  dx * speed
    y += 0 if int(y) == target_y else  dy * speed
    circle_rect = pg.Rect(x-SIDE, y-SIDE, SIDE*2, SIDE*2)
    counter = 0
  
  for figure in figures:
      if figure.timer.is_over():
          figure.move()

      color = figure.color if figure.type == Type.Obstacle else YELLOW
      pg.draw.rect(screen, color, figure.rect)

      if figure.rect.colliderect(circle_rect):
          figures[-1] = Figure(type=Type.Reward)

  pg.display.update()

pg.quit()
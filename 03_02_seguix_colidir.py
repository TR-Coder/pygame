import pygame as pg
import math
import random
from enum import Enum

pg.init()
clock = pg.time.Clock()
FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
BLUE = pg.Color(0, 0, 255)
RED = pg.Color(255, 0, 0)
BLACK = pg.Color(0,0,0)
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
    
def collides_with_figures(rect:pg.Rect) -> bool:
  print(len(figures))
  return any(rect.colliderect(figure.rect) for figure in figures)

def calculate_position() -> pg.Rect:
  while True:
    rect = pg.Rect(random.randint(SIDE, SCREEN_WIDTH-SIDE), random.randint(SIDE, SCREEN_HEIGHT-SIDE), SIDE, SIDE)
    if not collides_with_figures(rect):
      return rect

class Figure:
    def __init__(self, type:Type) -> None:
      self.rect = calculate_position()
      self.timer =  Timer(ms=random.randint(2000,4000))
      self.color = random.choice([RED, BLACK, BLUE])
      self.type = type
    
    def move(self) -> None:
      # random_x, random_y = self.rect.x+random.randint(-20,20), self.rect.y+random.randint(-20,20)
      # if random_x>=0 and random_x<=SCREEN_WIDTH-SIDE:
      #   self.rect.x = random_x
      # if random_y>=0 and random_y<=SCREEN_HEIGHT-SIDE:
      #   self.rect.y = random_y
      self.rect.x = max(0, min(SCREEN_WIDTH - SIDE, self.rect.x + random.randint(-20, 20)))
      self.rect.y = max(0, min(SCREEN_HEIGHT - SIDE, self.rect.y + random.randint(-20, 20)))

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Following mouse')

target_x, target_y = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
speed = 1
dx, dy = 0.0, 0.0
counter = 0

# list with obstacle rectangles.
# figures:list[Figure] = []
figures = [Figure(type=Type.Obstacle) for _ in range(50)]
# for _ in range(50):
#    figures.append(Figure(type=Type.Obstacle))


rect = calculate_position()
x:float = rect.x
y:float = rect.y

run = True
while run:
  # clock.tick(FPS)
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
  if counter == 5:
    x += 0 if int(x) == target_x else  dx * speed
    y += 0 if int(y) == target_y else  dy * speed
    counter = 0
  
  for figure in figures:
    if figure.timer.is_over():
      figure.move()
    pg.draw.rect(screen, figure.color, figure.rect)

  pg.display.flip()

pg.quit()
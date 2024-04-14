import pygame as pg
import math
import random

pg.init()
clock = pg.time.Clock()
FPS = 60

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
BLUE = pg.Color(0, 0, 255)
RED = pg.Color(255, 0, 0)
BLACK = pg.Color(0,0,0)
SIDE = 25

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
    
class Obstacle:
    def __init__(self) -> None:
      self.rect = pg.Rect(random.randint(0, SCREEN_WIDTH-SIDE), random.randint(0, SCREEN_HEIGHT-SIDE), SIDE, SIDE)
      self.timer =  Timer(ms=random.randint(2000,4000))
      self.color = random.choice([RED, BLACK, BLUE])
    
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

#create empty list, then create 10 obstacle rectangles using a loop and add to list
obstacles:list[Obstacle] = [Obstacle() for _ in range(10)]

rect = pg.Rect(random.randint(SIDE, SCREEN_WIDTH-SIDE), random.randint(SIDE, SCREEN_HEIGHT-SIDE), SIDE, SIDE)

while any(rect.colliderect(obstacle.rect) for obstacle in obstacles):
    rect = pg.Rect(random.randint(SIDE, SCREEN_WIDTH-SIDE), random.randint(SIDE, SCREEN_HEIGHT-SIDE), SIDE, SIDE)

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
  
  for obstacle in reversed(obstacles):
    if obstacle.timer.is_over():
      obstacle.move()
    pg.draw.rect(screen, obstacle.color, obstacle.rect)
   
       

  pg.display.flip()

pg.quit()
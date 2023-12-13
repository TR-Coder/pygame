import pygame
import random

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Collision")

#create empty list, then create 16 obstacle rectangles using a loop and add to list
obstacles = []
for _ in range(16):
  obstacle_rect = pygame.Rect(random.randint(0, 500), random.randint(0, 300), 25, 25)
  obstacles.append(obstacle_rect)

#define line start point as the center of the screen
line_start = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

#define colours
BG = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

run = True
while run:

  #update background
  screen.fill(BG)

  #check mouse coordinates and draw a line to it
  pos = pygame.mouse.get_pos()
  pygame.draw.line(screen, WHITE, line_start, pos, 5)

  #check for line collision with each rectangle
  for obstacle in obstacles:
    if obstacle.clipline((line_start, pos)):        # clipline
      pygame.draw.rect(screen, RED, obstacle)
    else:
      pygame.draw.rect(screen, GREEN, obstacle)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  pygame.display.flip()

pygame.quit()
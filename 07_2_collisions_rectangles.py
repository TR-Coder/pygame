import pygame
import random

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Collision")

#create main rectangle
mouse_rect = pygame.Rect(0, 0, 25, 25)

#create empty list, then create 16 obstacle rectangles using a loop and add to list
obstacles = []
for _ in range(16):
  obstacle_rect = pygame.Rect(random.randint(0, 500), random.randint(0, 300), 25, 25)
  obstacles.append(obstacle_rect)

#define colours
BG = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#hide mouse cursor
pygame.mouse.set_visible(False)

run = True
while run:
  #update background
  screen.fill(BG)

  #check collision and change colour
  color = GREEN
  # for obstacle in obstacles:
  #   if mouse_rect.colliderect(obstacle):
  #     color = RED
  if mouse_rect.collidelist(obstacles)>=0:    # collidelist
    color = RED
    print(mouse_rect.collidelist(obstacles))

  #get mouse coordinates and use them to position the rectangle
  mouse_rect.center = pygame.mouse.get_pos()

  #draw all rectangles
  pygame.draw.rect(screen, color, mouse_rect)
  for obstacle in obstacles:
    pygame.draw.rect(screen, BLUE, obstacle)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  #update display
  pygame.display.update()

pygame.quit()
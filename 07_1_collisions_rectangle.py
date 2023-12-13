import pygame
import random

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Collision")

#create main rectangle & obstacle rectangle
mouse_rect = pygame.Rect(0, 0, 25, 25)
obstacle_rect = pygame.Rect(random.randint(0, 500), random.randint(0, 300), 25, 25)

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
  if mouse_rect.colliderect(obstacle_rect):
    color = RED

  #get mouse coordinates and use them to position the rectangle
  mouse_rect.center = pygame.mouse.get_pos()

  #draw both rectangles
  pygame.draw.rect(screen, color, mouse_rect)
  pygame.draw.rect(screen, BLUE, obstacle_rect)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  #update display
  pygame.display.update()

pygame.quit()
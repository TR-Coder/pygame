import pygame
import random
from typing import Tuple, Union, Optional

pygame.init()

W = 800
H = 450

screen = pygame.display.set_mode((W, H))

pygame.display.set_caption('Drag And Drop')

active_box:int|None = None

boxes = []
for i in range(5):
  x = random.randint(50, 700)
  y = random.randint(50, 350)
  w = random.randint(35, 65)
  h = random.randint(35, 65)
  box = pygame.Rect(x, y, w, h)
  boxes.append(box)

run = True
while run:

  screen.fill("turquoise1")

  for box in boxes:
    pygame.draw.rect(screen, "purple", box)

  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        for num, box in enumerate(boxes):
          if box.collidepoint(event.pos):
            active_box = num
            break          

    elif event.type == pygame.MOUSEBUTTONUP:
      if event.button == 1:
        active_box = None

    elif event.type == pygame.MOUSEMOTION:
      print(event.rel)
      if active_box is not None:
        
        
        boxes[active_box].move_ip(event.rel)

    elif event.type == pygame.QUIT:
      run = False

  pygame.display.flip()

pygame.quit()
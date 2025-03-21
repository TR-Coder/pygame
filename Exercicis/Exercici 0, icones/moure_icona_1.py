import pygame as pg
import random
import os


pg.init()

W = 800
H = 450
FPS = 60

screen = pg.display.set_mode((W, H))
pg.display.set_caption('Drag And Drop')

clock = pg.time.Clock()

bg = pg.Surface(screen.get_size())
bg.fill("turquoise1")

active_box:int|None = None


def load_image(relpath:str, scale:float=1) -> pg.Surface:
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),relpath)
    image:pg.Surface = pg.image.load(img_path).convert_alpha()
    width, height = image.get_size()
    image = pg.transform.scale(image, (width * scale, height * scale))  
    return image
  
icons:list[pg.Surface] = []
boxes:list[pg.Rect] = []

for i in range(5):
  img = load_image(relpath=f'assets/img{i}.svg',scale=0.1)
  img_rect = img.get_rect()
  img_rect.x = random.randint(50, 700)
  img_rect.y = random.randint(50, 350)
  icons.append(img)
  boxes.append(img_rect)

run = True
while run:
  clock.tick(FPS)
  screen.blit(bg, (0, 0))
    
  for event in pg.event.get():
    if event.type == pg.MOUSEBUTTONDOWN:
      if event.button == 1:
        for num, box in enumerate(boxes):
          if box.collidepoint(event.pos):
            active_box = num
            break          

    elif event.type == pg.MOUSEBUTTONUP:
      if event.button == 1:
        active_box = None

    elif event.type == pg.MOUSEMOTION:
      if active_box is not None:
        boxes[active_box].move_ip(event.rel)

    elif event.type == pg.QUIT:
      run = False

  for box,icon in zip(boxes,icons):
    screen.blit(icon, (box.x, box.y))

  pg.display.update()

pg.quit()
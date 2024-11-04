import pygame as pg

pg.init()

clock = pg.time.Clock()
FPS = 60
W = 1500
H = 600

to_left = True

#create game window
screen = pg.display.set_mode((W, H))
pg.display.set_caption("Endless Scroll")

#load image
bg = pg.image.load("data/bg_ciutat.png").convert()
bg_width = bg.get_width()
bg_rect = bg.get_rect()

dx = 0
run = True
while run:
  clock.tick(FPS)
  x = dx
  while x < W:
    screen.blit(bg, (x, 0))
    # bg_rect.x = x
    # pg.draw.rect(screen, (255, 0, 0), bg_rect, 1)
    x += bg_width

  #reset scroll
  if to_left:
    dx -= 5
    if abs(dx) > bg_width:
      dx = 0
  else:
    dx += 5
    if dx>0:
      dx = -bg_width

  #event handler
  for event in pg.event.get():
    if event.type == pg.QUIT:
      run = False
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_LEFT:
        to_left = True
      elif event.key == pg.K_RIGHT:
        to_left = False

  pg.display.update()

pg.quit()
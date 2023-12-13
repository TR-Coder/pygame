import pygame

pygame.init()

clock = pygame.time.Clock()
FPS = 60
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 600
RIGHT = 1
LEFT = -1

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Scroll")

#load image
bg = pygame.image.load("data/bg_ciutat.png").convert()
bg_width = bg.get_width()
bg_rect = bg.get_rect()

scroll_x = 0
right_left = LEFT

#game loop
run = True
while run:

  clock.tick(FPS)

  #draw scrolling background
  x = scroll_x
  while x < SCREEN_WIDTH:
    screen.blit(bg, (x, 0))
    bg_rect.x = x
    pygame.draw.rect(screen, (255, 0, 0), bg_rect, 1)
    x += bg_width

  #scroll background
  scroll_x += 5 * right_left

  #reset scroll
  if right_left == RIGHT  and scroll_x>0:
    print(scroll_x, bg_width)
    scroll_x -= bg_width
    print(scroll_x)
  elif right_left == LEFT and abs(scroll_x) > bg_width:
    scroll_x += bg_width

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        right_left = LEFT
      elif event.key == pygame.K_RIGHT:
        right_left = RIGHT

  pygame.display.update()

pygame.quit()
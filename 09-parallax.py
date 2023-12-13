import pygame

pygame.init()

clock = pygame.time.Clock()
FPS = 60
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
RIGHT = 1
LEFT = -1
SPEED_GROUND = 1

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("parallax")

#load ground image
ground = pygame.image.load("data/ground.png").convert()
ground_width = ground.get_width()
ground_y_position = SCREEN_HEIGHT - ground.get_height()


class Parallax(pygame.sprite.Sprite):
  def __init__(self, screen, left_right):
    pygame.sprite.Sprite.__init__(self)
    self.screen = screen
    self.left_right = left_right
    self.bg_images = []
    for i in range(1,6):
      image = pygame.image.load(f'data/plx-{i}.png').convert_alpha()
      bg_image = {
        'image': image,
        'scroll_x': 0
      }
      self.bg_images.append(bg_image)
    self.bg_width = self.bg_images[0]['image'].get_width()

  def update(self):
    speed = 1
    for img in self.bg_images:
      x = img['scroll_x']
      while x < screen.get_width():
        self.screen.blit(img['image'], (x, 0))
        x += self.bg_width

      img['scroll_x'] +=  self.left_right * speed
      speed += 0.2

      if self.left_right == RIGHT and img['scroll_x']>0:
        img['scroll_x'] -= self.bg_width
      elif self.left_right == LEFT and abs(img['scroll_x']) > self.bg_width:
        img['scroll_x'] += self.bg_width

  def go_left_right(self, left_right):
    self.left_right = left_right
      
      
scroll_x_ground = 0
right_left = LEFT
parallax = Parallax(screen, right_left)

def draw_image(image, x, y, width):
  while x < SCREEN_WIDTH:
    screen.blit(image, (x, y))
    x += width

#game loop
run = True
while run:

  clock.tick(FPS)

  parallax.update()
  draw_image(ground, scroll_x_ground, ground_y_position, ground_width)
  scroll_x_ground += right_left * SPEED_GROUND
 
  #reset scroll
  if right_left == RIGHT and scroll_x_ground>0:
      scroll_x_ground -= ground_width
  elif right_left == LEFT and abs(scroll_x_ground) > ground_width:
        scroll_x_ground += ground_width

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        right_left = LEFT
        parallax.go_left_right(right_left)
      elif event.key == pygame.K_RIGHT:
        right_left = RIGHT
        parallax.go_left_right(right_left)

  pygame.display.update()

pygame.quit()
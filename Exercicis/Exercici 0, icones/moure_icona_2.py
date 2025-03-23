import pygame as pg
import random
import os

pg.init()

W = 1000
H = 450
FPS = 60
WHITE = pg.Color(255,255,255)
BLACK = pg.Color(0,0,0)
BLUE = pg.Color(0,0,255)

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
  
texts:list[str] = ['ma','monstre','botella','campana','sol'] 
font:pg.font.Font = pg.font.SysFont('Calibri',40)
  
# # ramdom
# combined = list(zip(icons, text_imgs)) 
# random.shuffle(combined)
# tuples1, tuples2 = zip(*combined)
# icons = list(tuples1)
# text_imgs = list(tuples2)

icons_group:pg.sprite.Group = pg.sprite.Group()
texts_group:pg.sprite.Group = pg.sprite.Group()

class Icon(pg.sprite.Sprite):
  def __init__(self, x:int, y:int, path:str|None, text:str, *groups:pg.sprite.Group, scale:float=1):
    super().__init__(*groups)

    if path is not None:
      self.image = load_image(relpath=path, scale=scale)
    else:
      self.image = font.render(text, True, BLACK)

    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.rect_original_x = x
    self.rect_original_x = y
    self.text = text

  def collides_with_point(self, position: tuple[int, int]) -> bool:
    return self.rect.collidepoint(position)
  
  def update(self):
    pass

IMAGES_AMOUNT = 5

def create_sprites() -> tuple[int,int]:
  images_width = 0
  for i in range(IMAGES_AMOUNT):
    sprite = Icon(0, 50, f'assets/img{i}.png', texts[i], icons_group, scale=1)
    images_width += sprite.rect.width

  random_text = random.sample(texts, len(texts))
  texts_width = 0
  for i in range(IMAGES_AMOUNT):
    sprite = Icon(0, 350, None, random_text[i], texts_group, scale=1)
    texts_width += sprite.rect.width
  
  return (images_width, texts_width)
   

def distributes_distances_in_x(group:pg.sprite.Group, width:int):
  remainder = (W - width) // (IMAGES_AMOUNT+1)
  x = remainder
  for sprite in group:
    sprite.rect.x = x
    sprite.rect_original_x = x

    x += sprite.rect.width + remainder

# =========================================================>
images_width, texts_width = create_sprites()
distributes_distances_in_x(icons_group, images_width)
distributes_distances_in_x(texts_group, texts_width)

run = True
while run:
  clock.tick(FPS)
  screen.blit(bg, (0, 0))
    
  for event in pg.event.get():
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      for num, sprite in enumerate(icons_group):
        if sprite.collides_with_point(event.pos):
          active_box = num
          break 

    elif event.type == pg.MOUSEBUTTONUP:
      if event.button == 1:
        active_box = None

    elif event.type == pg.MOUSEMOTION:
      if active_box is not None:
        icon:Icon = icons_group.sprites()[active_box]
        icon.rect.move_ip(event.rel)

    elif event.type == pg.QUIT:
      run = False

  for sprite in icons_group:
    screen.blit(sprite.image, sprite.rect)

  for sprite in texts_group:
    screen.blit(sprite.image, sprite.rect)
  
  pg.display.update()

pg.quit()
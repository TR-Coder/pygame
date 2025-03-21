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

icons:list[pg.Surface] = []
icon_boxes:list[pg.Rect] = []

text_imgs:list[pg.Surface] = []
text_boxes:list[pg.Rect] = []


IMAGES_AMOUNT = 5
increment = W // IMAGES_AMOUNT
x = increment // 2

images_with = 0
for i in range(IMAGES_AMOUNT):
  img = load_image(relpath=f'assets/img{i}.svg', scale=0.1)
  icons.append(img)
  images_with += img.get_width()
  
font:pg.font.Font = pg.font.SysFont('Calibri',40)
texts_with = 0
for text in texts:
  img = font.render(text, True, BLACK)
  text_imgs.append(img)
  texts_with += img.get_width()
  
  
# ramdom
combined = list(zip(icons, text_imgs)) 
random.shuffle(combined)
tuples1, tuples2 = zip(*combined)
icons = list(tuples1)
text_imgs = list(tuples2)
    
remainder = (W - images_with) // (IMAGES_AMOUNT+1)
x = remainder
for img in icons:  
  rect = img.get_rect()
  rect.y = 50
  rect.x = x
  icon_boxes.append(rect)
  x += rect.width + remainder

  
remainder = (W - texts_with) // (IMAGES_AMOUNT+1)
x = remainder
for img in text_imgs:  
  rect = img.get_rect()
  rect.y = 350
  rect.x = x
  text_boxes.append(rect)
  x += rect.width + remainder

# aleatori
combined = list(zip())


# =========================================================>


class Icon(pg.sprite.Sprite):
  def __init__(self, x, y, path,scale=1, *groups:pg.sprite.Group):
    super().__init__(*groups)
    self.image = load_image(relpath=path, scale=scale)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    
icons_group:pg.sprite.Group = pg.sprite.Group()
text_group:pg.sprite.Group = pg.sprite.Group()

IMAGES_AMOUNT = 5
increment = W // IMAGES_AMOUNT
x = increment // 2

images_with = 0
for i in range(IMAGES_AMOUNT):
  sprite = Icon(x=0, y=0, path=f'assets/img{i}.svg', scale=0.1, group=icons_group)
  images_with += sprite.rect.width
 
   

print(a)
# =========================================================>

run = True
while run:
  clock.tick(FPS)
  screen.blit(bg, (0, 0))
    
  for event in pg.event.get():
    if event.type == pg.MOUSEBUTTONDOWN:
      if event.button == 1:
        for num, box in enumerate(icon_boxes):
          if box.collidepoint(event.pos):
            active_box = num
            break          

    elif event.type == pg.MOUSEBUTTONUP:
      if event.button == 1:
        active_box = None

    elif event.type == pg.MOUSEMOTION:
      if active_box is not None:
        icon_boxes[active_box].move_ip(event.rel)

    elif event.type == pg.QUIT:
      run = False

  for box,img in zip(icon_boxes,icons):
    screen.blit(img, (box.x, box.y))
    
  for box,img in zip(text_boxes, text_imgs):
    screen.blit(img, (box.x, box.y))

  pg.display.update()

pg.quit()
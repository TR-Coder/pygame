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
BG_COLOR = "turquoise1"
IMAGES_AMOUNT = 5

screen = pg.display.set_mode((W, H))
pg.display.set_caption('Drag And Drop')
clock = pg.time.Clock()

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

# ==================================================================================
class MouseSprite(pg.sprite.Sprite):
  def __init__(self):
      super().__init__()
      self.image = pg.Surface((1, 1))     # Sprite d'1 píxel
      self.rect = self.image.get_rect()

  def update(self):
      self.rect.topleft = pg.mouse.get_pos()

# ==================================================================================
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
    self.initial_x = x
    self.initial_y = y
    self.text = text
  
  def original_position(self):
    self.rect.x = self.initial_x
    self.rect.y = self.initial_y
 
  # Si sobreescrius __eq__ dona un Error: TypeError: unhashable type: 'Icon'
  # def __eq__(self, obj):                            
  #   return isinstance(obj, Icon) and (self.text == obj.text)
      
# =========================================================>
def clear_background() -> None:
    screen.fill(BG_COLOR)
  
# =========================================================>
def distributes_distances_in_x(group:pg.sprite.Group, width:int):
  margin = (W - width) // (IMAGES_AMOUNT+1)
  x = margin
  for sprite in group:
    sprite.rect.x = x
    sprite.initial_x = x
    x += sprite.rect.width + margin   
  
# =========================================================>
def create_sprites() -> None: 
  texts_random = random.sample(texts, len(texts)) 
  for i in range(IMAGES_AMOUNT):
    Icon(0, 50, f'assets/img{i}.png', texts[i], icons_group)      # Les imatges han d'estar en el mateix ordre que el text.
    Icon(0, 350, None, texts_random[i], texts_group)
    
  # Assumin que totes les imatges tenen les mateixes dimensions (width, height)
  images_width = sum(sprite.rect.width for sprite in icons_group)
  texts_width = sum(sprite.rect.width for sprite in texts_group)
  distributes_distances_in_x(texts_group, texts_width)
  distributes_distances_in_x(icons_group, images_width)
   
# =========================================================>
def same_text_collision(sprite1, sprite2):
    return sprite1.rect.colliderect(sprite2.rect) and sprite1.text == sprite2.text 
 
# =========================================================>
# spritecollideany(): Comprova si un sprite col·lideix amb algun sprite d'un group. Retorna el primer sprite amb 
#   què col·lidix o None si no hi ha col·lisió.

# spritecollide(): Comprova si un sprite col·lidix amb un o més sprites del group. Retorna una llista amb tots 
#   els sprites amb què l'sprite col·lidix. Si no hi ha cap col·lisió, retorna una llista buida. Té el paràmetre 'dokill'
#   que si és True, que fa que els sprites del grup amb què col·lidix s’esborren automàticament del grup.
#
# Una funció callback és una funció que es passa com a argument a una altra funció i que s’executa dins d'esta última en
# un moment determinat. Fixem-nos que es passa la refència a la funció (Sense parèntesis. És de tipus callable)
# =========================================================>

create_sprites()
mouse = MouseSprite()     # Sprite fictici (dummy)

score:int = IMAGES_AMOUNT
run = True
active_sprite:Icon|None = None

while run:
  clock.tick(FPS)
  clear_background()
    
  for event in pg.event.get():
    if event.type == pg.MOUSEBUTTONDOWN and  event.button == 1:
      mouse.update()
      active_sprite = pg.sprite.spritecollideany(mouse, icons_group)    
                    
    elif event.type == pg.MOUSEBUTTONUP and event.button == 1:          
      if active_sprite is not None:
        sprite = pg.sprite.spritecollideany(active_sprite, texts_group, collided=same_text_collision)
        if sprite:
          texts_group.remove(sprite)
          icons_group.remove(active_sprite)
          score -= 1
          if score == 0:
            run = False
        else:
          active_sprite.original_position()
      active_sprite = None

    elif event.type == pg.MOUSEMOTION and active_sprite is not None:
        active_sprite.rect.move_ip(event.rel)
        active_sprite.rect.clamp_ip(screen.get_rect())      # Limitar la posició de les icones dins de la pantalla.
        
    elif event.type == pg.QUIT:
      run = False

  texts_group.draw(screen)
  icons_group.draw(screen)
  pg.display.update()

pg.quit()
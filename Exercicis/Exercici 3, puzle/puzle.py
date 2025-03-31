from __future__ import annotations
import pygame as pg
import components
import random

W = 925
H = 800
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)

_Group = pg.sprite.Group
_Surface = pg.Surface
_Sprite = pg.sprite.Sprite
_Rect = pg.Rect

class Community(_Sprite):
  def __init__(self, image:_Surface, name:str, *groups:_Group):
    super().__init__(*groups)
    self.image = image 
    self.rect = image.get_rect()
    self.mask = pg.mask.from_surface(self.image)
    self.name = name
    self.highlight = pg.Surface(self.image.get_size(), pg.SRCALPHA)
    self.highlight.fill((255, 0, 0))                                            # Color de ressalt   
    self.highlight.blit(self.image, (0, 0), special_flags=pg.BLEND_RGBA_MULT)   # Aplicar la transparència original
   
class Mouse(_Sprite):
    def __init__(self):
        self.image = pg.Surface((1, 1))              # Punt de 1 píxel
        self.rect = self.image.get_rect()
        self.mask = pg.mask.Mask((1, 1), fill=True)  # Màscara d'1 píxel
        
class Text(_Sprite):
    def __init__(self, x:int, y:int, name:str):
        self.text = name
        self.image:_Surface = font.render(self.text, True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
   
# ------------------------------------------------------------------------------------------------------
def clear_screen() -> None:
    screen.blit(bg, (0, 0))

# ------------------------------------------------------------------------------------------------------
def main() -> None:   
    mouse_sprite = Mouse()      # Sprite 'fals' per a representar el punter del ratolí
    communities_name = ['Andalusia','Aragó','Astúries','Balears','Canàries','Cantàbria','Castella i Lleó','Castella la Manxa','Catalunya','Ceuta','Extremadura','Galícia','Madrid','Melilla','Múrcia','País Basc','Pamplona','La Rioja','València']
    communities_images:list[_Surface] = components.load_images(r'assets/comunitat*.png')
    spain_surface = components.load_image(r'assets/Espanya.png')
    communities:list[Community] = []
    communities_group:_Group = pg.sprite.Group()
    
    text = Text(W//2 ,H-75, random.choice(communities_name))
    
    for image, name in zip(communities_images, communities_name):
        communities.append(Community(image, name, communities_group))
            
    main_loop = True
    while main_loop:
        clear_screen()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                main_loop = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # print(communities[index_hover].name)
                    if communities_name[index_hover] == text.text:
                        text = Text(W//2 ,H-75, random.choice(communities_name))
        
        screen.blit(spain_surface, (0,0))
        
        mouse_sprite.rect.topleft = pg.mouse.get_pos()  # Actualitzar la posició de l'sprite' del ratolí.
        hovered_sprite = pg.sprite.spritecollide(mouse_sprite, communities_group, False, pg.sprite.collide_mask)
        if hovered_sprite:
            index_hover:int = communities_name.index(hovered_sprite[0].name)
            screen.blit(communities[index_hover].highlight, (0,0))  
                   
        screen.blit(text.image, text.rect.topleft)      
          
        pg.display.update()


# ------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((W,H))
    screen_center = screen.get_rect().center
    pg.display.set_caption("Mapa de comunitats d'Espanya")
    bg = pg.Surface(screen.get_size())
    bg.fill(WHITE)
    font = pg.font.Font(None, 36)
    main()
    pg.quit()
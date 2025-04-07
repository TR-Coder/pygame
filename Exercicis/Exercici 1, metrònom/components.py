import pygame as pg
from enum import Enum
import os

# ------------------------------------------------------------------------------------------------------
class MouseClick(Enum):
    NOT_PRESSED=0
    DOWN=1
    UP=2

# ------------------------------------------------------------------------------------------------------
class Button(pg.sprite.Sprite):
    def __init__(self, x:int, y:int, radius:int, group: pg.sprite.Group,  bg_color: tuple[int,int,int]|None = None, font_color: tuple[int,int,int]|None = None, image:pg.Surface|None = None, symbol:str|None = None) -> None:
        super().__init__(group)
        if image is None and symbol is None:
            raise Exception('Indica una imatge o un símbol')
        
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (0,0,0,0) if bg_color is None else bg_color 
        self.font_color = (255,255,255) if font_color is None else font_color 
        
        if image is not None:
            self.image = image
            self.rect = self.image.get_rect()    
        else:
            self.image = pg.Surface((radius*2, radius*2), pg.SRCALPHA)
            self.rect = self.image.get_rect()   
            pg.draw.circle(self.image, self.color, self.rect.center, radius)
            self.font = pg.font.SysFont('Calibri',80,bold=True)
            img_txt = self.font.render(symbol, True, self.font_color)
            rect_txt = img_txt.get_rect(center=self.rect.center)
            self.image.blit(img_txt, rect_txt)             
            
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def update(self, mouse_clicked: bool) -> None:
        mouse_position = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_position) and mouse_clicked == MouseClick.DOWN:
            self.rect.move_ip(2,2)
            self.clicked = True
        elif self.clicked:
            self.rect.x, self.rect.y = self.x, self.y
            self.clicked = False

# ------------------------------------------------------------------------------------------------------
# Nota: get_ticks() retorna el nombre de mil·lisegons que han passat des que es va iniciar el programa.
class Timer():
    def __init__(self, ms: int, first_time_over:bool=False):
        self.ms = ms
        self.first_time_over = first_time_over
        self.initial_ticks = pg.time.get_ticks()

    def is_over(self) -> bool:
        elapsed_time = pg.time.get_ticks() - self.initial_ticks
        if elapsed_time > self.ms or self.first_time_over:
            self.initial_ticks = pg.time.get_ticks()
            self.first_time_over = False
            return True
        return False
    
# ------------------------------------------------------------------------------------------------------
def load_image(relative_path_name:str, scale:float=1) -> pg.Surface:
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path_name)
    image:pg.Surface = pg.image.load(img_path).convert_alpha()
    image = pg.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
    return image

# ------------------------------------------------------------------------------------------------------
def load_sound(relative_path_name:str) -> pg.mixer.Sound:
    sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path_name)
    return pg.mixer.Sound(sound_path)

# ------------------------------------------------------------------------------------------------------

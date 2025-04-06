import pygame as pg
from enum import Enum
import os
import glob

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

TIMER_EVENT = pg.USEREVENT + 1 

class Timer():
    def __init__(self, ms: int, first_time_over:bool=False, raise_events_regularly:bool=False, loops:int=0):
        self.ms = ms
        self.first_time_over = first_time_over
        self.initial_ticks = pg.time.get_ticks()
        self.raise_events_regularly = raise_events_regularly
        self.loops = loops

        if self.raise_events_regularly:
            if first_time_over:
                pg.event.post(pg.event.Event(TIMER_EVENT))
                first_time_over = False
            pg.time.set_timer(TIMER_EVENT, ms, loops=self.loops)

    def is_over(self) -> bool:
        elapsed_time = pg.time.get_ticks() - self.initial_ticks
        if elapsed_time > self.ms or self.first_time_over:
            self.initial_ticks = pg.time.get_ticks()
            self.first_time_over = False
            return True
        return False
    
    def stop_raise_events_regularly(self) -> None:
        if self.raise_events_regularly:
            pg.time.set_timer(TIMER_EVENT, 0)
    
    def again(self, ms: int|None=None, loops:int|None=None) -> None:
        ms = ms or self.ms
        loops = loops or self.loops
        if self.raise_events_regularly:
            pg.time.set_timer(TIMER_EVENT, ms, loops)    

# ------------------------------------------------------------------------------------------------------
def load_image(relative_path_name:str, scale:float=1) -> pg.Surface:
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path_name)
    image:pg.Surface = pg.image.load(img_path).convert_alpha()
    image = pg.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
    return image

def load_images(relative_path_pattern_name:str, scale:float=1) -> list[pg.Surface]:
    surfaces:list[pg.Surface]  = []
    directory = os.path.dirname(os.path.abspath(__file__))
    pattern = os.path.join(directory, relative_path_pattern_name)
    matching_files = glob.glob(pattern)
    for file in sorted(matching_files):
        image:pg.Surface = pg.image.load(file).convert_alpha()
        image = pg.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        surfaces.append(image)
        
    return surfaces

# ------------------------------------------------------------------------------------------------------
def load_sound(relative_path_name:str) -> pg.mixer.Sound:
    sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path_name)
    return pg.mixer.Sound(sound_path)

# ------------------------------------------------------------------------------------------------------


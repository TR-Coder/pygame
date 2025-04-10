from __future__ import annotations
import pygame as pg
from enum import Enum
import components

W = 800
H = 800
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)

MAX_SPEED = 500
MIN_SPEED = 1500

_Group = pg.sprite.Group
_Surface = pg.Surface
_Rect = pg.Rect

# ------------------------------------------------------------------------------------------------------
class Metronome(pg.sprite.Sprite):
    def __init__(self, group: _Group):
        super().__init__(group)
        self.image = components.load_image(r'assets/metronom.png')
        self.rect = self.image.get_rect(center=screen_center)       # En el centre de la pantalla.

# ------------------------------------------------------------------------------------------------------
class Bar(pg.sprite.Sprite):

    class Position(Enum):
        LEFT=0
        RIGHT=1
 
    def __init__(self, ms:int, group: _Group):
        super().__init__(group)

        self.ms = ms
        self.timer = components.Timer(ms, first_time_over=True)
        
        self.image_bar = self.load_image()
        self.calculate_angle_and_image(ms)

        self.image = self.image_R
        self.rect = self.rect_R
        self.position = Bar.Position.LEFT

    
    def load_image(self) -> _Surface:
        img_first = components.load_image(r'assets/barra.png')
        rect = img_first.get_rect()
        img = pg.Surface((rect.width, rect.height*2), pg.SRCALPHA)
        img.blit(img_first, (0,0))  
        return img   

    def calculate_angle_and_image(self, ms:int) -> None:  
        self.degree:int = 45 if (ms>=800) else 10 if (ms<=400) else int(10 + (ms - 400) * (35/400))
        self.image_L:_Surface  = pg.transform.rotate(self.image_bar, self.degree)
        self.image_R:_Surface  = pg.transform.rotate(self.image_bar, -self.degree)
        self.rect_L:_Rect      = self.image_L.get_rect(center=screen_center)
        self.rect_R:_Rect      = self.image_R.get_rect(center=screen_center)

    def update(self) -> None:
        if self.position == Bar.Position.LEFT:
            self.position = Bar.Position.RIGHT
            self.image = self.image_R
            self.rect = self.rect_R
        else:
            self.position = Bar.Position.LEFT
            self.image = self.image_L
            self.rect = self.rect_L
            
    def increment_speed(self, ms:int) -> None:
        self.ms += ms
        if (self.ms <= MAX_SPEED):
            self.ms = MAX_SPEED
            return
        
        if (self.ms >= MIN_SPEED):
            self.ms = MIN_SPEED
            return
        
        self.timer = components.Timer(self.ms, first_time_over=True)
        self.calculate_angle_and_image(self.ms)

# ------------------------------------------------------------------------------------------------------
def clear_screen() -> None:
    screen.blit(bg, (0, 0))
    
# ------------------------------------------------------------------------------------------------------
def draw_speed(ms:int) -> None:
    surface = font.render(f'ms = {ms}', True, BLACK)
    screen.blit(surface, (50, 50))

# ------------------------------------------------------------------------------------------------------
def main() -> None: 
    miliseconds = 1000
    buttons_group:_Group   = pg.sprite.Group()
    metronome_group:_Group = pg.sprite.Group()
    button_plus  = components.Button(x=30, y=300, radius=55, bg_color=BLACK, symbol='+', group=buttons_group)
    button_minus = components.Button(x=30, y=450, radius=55, bg_color=BLUE,  symbol='-', group=buttons_group)
    tick_sound   = components.load_sound(r'assets/metronome.mp3')

    Metronome(group=metronome_group)
    bar = Bar(miliseconds, metronome_group)
    main_loop = True
    
    # --------------------- bucle principal ---------------------

    while main_loop:
        clear_screen()        
        mouse_click = components.MouseClick.NOT_PRESSED

        for event in pg.event.get():
            if event.type == pg.QUIT:
                main_loop = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = components.MouseClick.DOWN              
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                mouse_click = components.MouseClick.UP

        if bar.timer.is_over():  
            metronome_group.update()
            tick_sound.play()

        if mouse_click != components.MouseClick.NOT_PRESSED:
            buttons_group.update(mouse_click)
            if button_plus.clicked:
                bar.increment_speed(-100)
            elif button_minus.clicked:
                bar.increment_speed(100)                 

        metronome_group.draw(screen)
        buttons_group.draw(screen)
        draw_speed(bar.ms)

        pg.display.update()
        

# ------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((W,H))
    screen_center = screen.get_rect().center
    pg.display.set_caption('Metronome')
    bg = pg.Surface(screen.get_size())
    font = pg.font.Font(None, 36)
    bg.fill(WHITE)
    main()
    pg.quit()
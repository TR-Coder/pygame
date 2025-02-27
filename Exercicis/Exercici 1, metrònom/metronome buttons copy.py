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

# ------------------------------------------------------------------------------------------------------
class MetronomeBase(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group):
        super().__init__(group)
        self.image = components.load_image(r'assets/metronom.png')
        self.rect = self.image.get_rect(center=screen_center)       # En el centre de la pantalla.

# ------------------------------------------------------------------------------------------------------
class MetronomeBar(pg.sprite.Sprite):

    class Position(Enum):
        LEFT=0
        RIGHT=1
 
    def __init__(self, ms:int, group: pg.sprite.Group):
        super().__init__(group)
        self.group = group
        self.timer = components.Timer(ms, first_time_over=True)
        self.degree = self.calculate_angle(ms)
        img_bar = self.load_image()

        self.img_left  = pg.transform.rotate(img_bar, self.degree)
        self.img_right = pg.transform.rotate(img_bar, -self.degree)

        self.rect_left  = self.img_left.get_rect(center=screen_center)
        self.rect_right = self.img_right.get_rect(center=screen_center)

        self.position = MetronomeBar.Position.LEFT

    
    def load_image(self) -> pg.Surface:
        img_first = components.load_image(r'assets/barra.png')
        rect = img_first.get_rect()
        img = pg.Surface((rect.width, rect.height*2), pg.SRCALPHA)
        img.blit(img_first, (0,0))  
        return img   

    def calculate_angle(self, ms:int) ->int:
        # temps mínim de 400 ms i màxim de 800 ms,
        # A 800 ms o més lent (>=800) li corresponen 45º.
        # A 400 ms o més ràpid (<=400) li corresponen 10º.
        # Entre [400,800] ms l'angle serà proporcional:
        #   com 45º - 10º = 35graus  i   800 - 400 = 400ms
        #   són 35/400 graus/ms
        #   angle = 10º + (temps-400) * (35/400)
            if ms>=800:
                return 45
            if ms<=400:
                return 10
            return int(10 + (ms - 400) * (35/400))    

    def update(self) -> None:
        if self.position == MetronomeBar.Position.LEFT:
            self.image = self.img_left
            self.rect = self.rect_left
            self.position = MetronomeBar.Position.RIGHT
        else:
            self.image = self.img_right
            self.rect = self.rect_right
            self.position = MetronomeBar.Position.LEFT
            
    def new(self, speed:int) -> MetronomeBar:
        self.group.remove(self)
        return MetronomeBar(ms=speed, group=self.group)

# ------------------------------------------------------------------------------------------------------
def clear_screen() -> None:
    screen.blit(bg, (0, 0))
# ------------------------------------------------------------------------------------------------------
    
def draw_speed(ms:int) -> None:
    surface = font.render(f'ms = {ms}', True, BLACK)
    screen.blit(surface, (50, 50))


# ------------------------------------------------------------------------------------------------------
def main() -> None:
    
    MAX_SPEED = 500
    MIN_SPEED = 1500
    speed = 1000
     
    buttons_group:pg.sprite.Group = pg.sprite.Group()
    metronome_group:pg.sprite.Group = pg.sprite.Group()

    button_plus = components.Button(x=30, y=300, radius=55, bg_color=BLACK, symbol='+', group=buttons_group)
    button_minus =components.Button(x=30, y=450, radius=55, bg_color=BLUE, symbol='-', group=buttons_group)

    MetronomeBase(group=metronome_group)
    metronome_bar = MetronomeBar(ms=speed, group=metronome_group)

    tick_sound  = components.load_sound(r'assets/metronome.mp3')
    
    main_loop = True
    while main_loop:

        mouse_click = components.MouseClick.NOT_PRESSED

        for event in pg.event.get():
            if event.type == pg.QUIT:
                main_loop = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = components.MouseClick.DOWN
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                mouse_click = components.MouseClick.UP

        clear_screen()

        if metronome_bar.timer.is_over():  
            metronome_group.update()
            tick_sound.play()

        metronome_group.draw(screen)

        if mouse_click != components.MouseClick.NOT_PRESSED:
            buttons_group.update(mouse_click)
            if button_plus.clicked:
                if speed <= MAX_SPEED:
                    speed = MAX_SPEED
                else:
                    speed -= 100
                    metronome_bar = metronome_bar.new(speed)        # alternativa
            if button_minus.clicked:
                if speed >= MIN_SPEED:
                    speed = MIN_SPEED
                else:
                    speed += 100
                    metronome_bar = metronome_bar.new(speed)                 

        buttons_group.draw(screen)
        draw_speed(ms=speed)
        
        pg.display.update()
        

# ------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((W,H))
    screen_center = screen.get_rect().center
    pg.display.set_caption('Metronome')
    bg = pg.Surface(screen.get_size())
    bg.fill(WHITE)
    font = pg.font.Font(None, 36)
    main()
    pg.quit()
import pygame as pg
import os
from enum import Enum
import components

W = 800
H = 800
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)

class MouseClick(Enum):
    NOT_PRESSED=0
    DOWN=1
    UP=2

pg.init()
screen = pg.display.set_mode((W,H))
bg = pg.Surface(screen.get_size())
bg.fill(WHITE)


def load_image(name:str, scale:float=1) -> pg.Surface:
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', name)
    image:pg.Surface = pg.image.load(img_path).convert_alpha()
    image = pg.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
    return image


def load_sound(name: str) -> pg.mixer.Sound:
    sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', name)
    return pg.mixer.Sound(sound_path)


image_metronome = load_image('metronom.png')
image_bar_first = load_image('barra.png')

bar_rect = image_bar_first.get_rect()
image_bar = pg.Surface((bar_rect.width, bar_rect.height*2), pg.SRCALPHA)
image_bar.blit(image_bar_first, (0,0))


def draw_background() -> None:
    screen.blit(bg, (0, 0))


def draw_metronome(degree:int=0) -> None:
    screen_center = screen.get_rect().center
    center_metronome = image_metronome.get_rect(center=screen_center)
    screen.blit(image_metronome, center_metronome)

    rotated_bar = pg.transform.rotate(image_bar, degree)
    center_bar = rotated_bar.get_rect(center=screen_center)
    screen.blit(rotated_bar, center_bar.topleft)

def angle(ms:int) -> int:
# temps mínim de 400 ms i màxim de 800 ms,
# A 800 ms o més lent (>=800) li corresponen 45º.
# A 400 ms o més ràpid (<=400) li corresponen 10º.
# Entre [400,800] ms l'angle serà proporcional:
#   com 45º - 10º = 35graus i   800 - 400 = 400ms
#   són 35/400 graus/ms
#   angle = 10º + (temps-400) * (35/400)
    if ms>=800:
        return 45
    if ms<=400:
        return 10
    
    return int(10 + (ms - 400) * (35/400))

tick_sound  = load_sound('metronome.mp3')

buttons_group:pg.sprite.Group = pg.sprite.Group()
button1 = components.Button(x=30, y=300, radius=55, bg_color=BLACK, symbol='+', group=buttons_group)
button2 = components.Button(x=30, y=450, radius=55, bg_color=BLUE, symbol='-', group=buttons_group)

def main() -> None:
    pg.display.set_caption('Clock')
    mouse_click:MouseClick
    ms = 1000  
    degree = angle(ms)
    timer = components.Timer(ms, first_time_over=True)
    
    run = True
    while run:
        mouse_click = MouseClick.NOT_PRESSED
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = MouseClick.DOWN
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                mouse_click = MouseClick.UP

        if timer.is_over():  
            draw_background()
            draw_metronome(degree)
            tick_sound.play()
            degree *= -1      
        
        if mouse_click != MouseClick.NOT_PRESSED:
            buttons_group.update(mouse_click == MouseClick.DOWN)
        buttons_group.draw(screen)
        
        pg.display.update()

    pg.quit()

if __name__ == '__main__':
    main()
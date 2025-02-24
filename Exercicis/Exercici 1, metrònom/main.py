import pygame as pg
import os

W = 800
H = 800
FPS = 60
WHITE = (255,255,255)

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
image_bar = pg.Surface((bar_rect.width, bar_rect.height*2), pg.SRCALPHA).convert_alpha()
# image_bar.fill((0, 0, 0, 0))  # alternativa a  pg.SRCALPHA
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



def main() -> None:
    ms = 1000
    degree = angle(ms)
    run = True
    while run:
        draw_background()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                run = False

        pg.time.wait(ms)    
        draw_metronome(degree)
        degree *= -1
        pg.display.update()

    pg.quit()

if __name__ == '__main__':
    main()
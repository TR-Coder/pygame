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
clock = pg.time.Clock()

class Timer():
    def __init__(self, ms: int):
        self.ticks = ms
        self.initial_time = pg.time.get_ticks()

    def is_over(self) -> bool:
        elapsed_time = pg.time.get_ticks() - self.initial_time
        if elapsed_time > self.ticks:
            self.initial_time += elapsed_time
            return True
        return False
    

def load_image(name:str, scale:float=1) -> pg.Surface:
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', name)
    image:pg.Surface = pg.image.load(img_path).convert_alpha()
    image = pg.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
    return image


def load_sound(name: str) -> pg.mixer.Sound:
    sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', name)
    return pg.mixer.Sound(sound_path)


image_metronome = load_image('metronom.png')
image_bar = load_image('barra.png')



def draw_background() -> None:
    screen.blit(bg, (0, 0))


# def rotate_image(image:pg.Surface, angle:float, pivot:tuple[int,int]) -> tuple[pg.Surface, tuple[int, int]]:
#     rect = image.get_rect(center=pivot)  
#     rotated_image = pg.transform.rotate(image, angle)
#     rotated_rect = rotated_image.get_rect(center=rect.center)
#     return rotated_image, rotated_rect.topleft


def rotate_image(image: pg.Surface, angle: float, pivot: tuple[int, int]) -> tuple[pg.Surface, tuple[int, int]]:
    w, h = image.get_size()
    pivot_offset = (pivot[0] - w // 2, pivot[1] - h // 2)
    rotated_image = pg.transform.rotate(image, angle)
    new_w, new_h = rotated_image.get_size()
    new_x = pivot[0] - new_w // 2 + pivot_offset[0]
    new_y = pivot[1] - new_h // 2 + pivot_offset[1]
    return rotated_image, (new_x, new_y)



def draw_metronome() -> None:
    center_metronome = image_metronome.get_rect(center=screen.get_rect().center)
    screen.blit(image_metronome, center_metronome)
    
    center_bar = image_bar.get_rect(center=center_metronome.center)
    y = center_bar.y + image_bar.get_height()//2
    x = center_bar.x
    image_rotate_bar, (x, y) = rotate_image(image_bar, 0, (x,y))
    # image_rotate_bar = image_bar
    screen.blit(image_rotate_bar, (x,y))

    # screen.blit(image_rotate_bar, center_bar)


def main() -> None:
    timer_1 = Timer(ms=0)
    vibrate:bool = False
    run = True
    while run:
        clock.tick(FPS)
        draw_background()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pass
            
        if vibrate and timer_1.is_over():
            pass

        draw_metronome()
        pg.display.update()
    pg.quit()

if __name__ == '__main__':
    main()
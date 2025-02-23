import pygame as pg
import os
import random
import datetime as dt

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)

pg.init()
font = pg.font.Font(None, 36)
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


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


def load_image(name: str, scale: float) -> pg.Surface:
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', name)
    image:pg.Surface = pg.image.load(img_path).convert_alpha()
    image = pg.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
    return image


def load_sound(name: str) -> pg.mixer.Sound:
    sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', name)
    return pg.mixer.Sound(sound_path)


image = load_image('despertador.png', .25)
image_rect = image.get_rect(center=screen.get_rect().center)
alarm_sound = load_sound('alarm_ringing.mp3')
tic_sound = load_sound('slow_ticking.mp3')
        
def draw_background() -> None:
    screen.blit(bg, (0, 0))

def draw_alarmclock(vibrate:bool) -> None:
    if vibrate:
        alealt_x = random.randint(-5,5)
        alealt_y = random.randint(-5,5)
        new_position = image_rect.move(alealt_x, alealt_y)
        screen.blit(image, new_position)
    else:
        screen.blit(image, image_rect)

def draw_time() -> None:
    now = dt.datetime.now()
    hms = now.strftime("%H:%M:%S")
    surface = font.render(hms, True, BLACK)
    screen.blit(surface, (50, 50))

def main() -> None:
    timer_1 = Timer(ms=0)
    vibrate:bool = False
    run = True
    tic_sound.play(-1)      # -1 indica que sonarà de manera ininterrompuda.
    while run:
        clock.tick(FPS)
        draw_background()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if not vibrate:
                    timer_1 = Timer(ms=1000)
                    alarm_sound.play()
                    vibrate = True
                else:
                    alarm_sound.stop()
                    vibrate = False
            
        if vibrate and timer_1.is_over():
            alarm_sound.stop()
            vibrate = False

        draw_time()
        draw_alarmclock(vibrate)
        pg.display.update()
    pg.quit()

if __name__ == '__main__':
    main()

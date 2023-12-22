# https://www.youtube.com/watch?v=Mw81qlbBbqk&list=PLjcN1EyupaQkAQyBCYKyf1jt1M1PiRJEp&index=5

import pygame as pg
from math import ceil
import random
import ctypes
import sys
from enum import Enum

pg.init()

pg.mixer.pre_init()
pg.mixer.init()

# SCREEN_WIDTH = 1600
# SCREEN_HEIGHT = 1200

class GameStatus(Enum):
    START=0
    PLAYING=1
    PLAYER_WINS=2
    PLAYER_LOSES=3

FPS = 60
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (0, 0, 255)
SPACECRAFT_SPEED = 5
TIME_BETWEEN_SHOTS = 500 # ms
INVIDER_ROWS = 5
INVIDER_COLUMNS = 4


# ===================================================
def screen_scale_factor() -> float:
    if sys.platform.startswith('win32'):
        ctypes.windll.user32.SetProcessDPIAware()    # On some systems, high DPI settings can cause Pygame windows to appear larger than expected.
        return ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
    return 1

# ===================================================
# Perquè el joc es mostre amb unes dimensions agradables per pantalla apliquem un ajust que
# depen de la resoluió de la pantalla. Este ajust s'ha obtingut fent proves a diferents resolucions.
def screen_size_adjument(display_info) -> tuple[float, float]:
    if display_info.current_w >= 1600:
        return 0.9, 0.8
    return 1, 1

# ===================================================
def screen_resolution() -> tuple[int,int]:
    # La resolució que retorna display.Info() està dividida pel factor d'escala de la pantalla, 
    # per esta raó hem d'obtindre este factor d'escala i multiplicar-lo per la resolució.
    info_object = pg.display.Info()
    scale = screen_scale_factor()
    adjustment_x, adjustment_y = screen_size_adjument(info_object)
    width = int(info_object.current_w * scale * adjustment_x)
    height = int(info_object.current_h * scale * adjustment_y)
    return width, height

# ===================================================

SCREEN_WIDTH, SCREEN_HEIGHT = screen_resolution()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Space war')
font = pg.font.SysFont('Bauhaus 93', 60)
clock = pg.time.Clock()
image = pg.image.load("data/space_war/bg.png")
backspace_key_pressed = False
game_status = GameStatus.START

# Sprite groups
spacecraft_group = pg.sprite.Group()            # type: ignore
shot_spacecraft_group = pg.sprite.Group()       # type: ignore
invider_group = pg.sprite.Group()               # type: ignore
shot_invider_group = pg.sprite.Group()          # type: ignore
explosion_group = pg.sprite.Group()             # type: ignore

# Sounds
sound_explosion_1 = pg.mixer.Sound("data/space_war/explosion.wav")
sound_explosion_1.set_volume(0.25)

sound_explosion_2 = pg.mixer.Sound("data/space_war/explosion2.wav")
sound_explosion_2.set_volume(0.25)

sound_laser = pg.mixer.Sound("data/space_war/laser.wav")
sound_laser.set_volume(0.25)

# ===========================================================================================
def complete_stage(image: pg.Surface) -> pg.Surface:
    width = image.get_width()
    height = image.get_height()
    times_x = ceil(SCREEN_WIDTH / width)
    times_y = ceil(SCREEN_HEIGHT / height)
    combined_image = pg.Surface((width*times_x, height*times_y)).convert_alpha()
    
    for y in range(times_y):
        for x in range(times_x):
            combined_image.blit(image, (width*x, height*y))
    return combined_image

# ===========================================================================================
def draw_background():
    screen.blit(bg_img, (0,0))

# ===========================================================================================
def draw_text(text:str, x:int, y:int):
    image = font.render(text, True, WHITE_COLOR)
    screen.blit(image, (x,y))

# ===========================================================================================
def draw_energy_bar(energy: int):
    if energy > 10:
        color = GREEN_COLOR
    elif energy > 5:
        color = BLUE_COLOR
    else:
        color = RED_COLOR

    pg.draw.rect(screen, color, (10,SCREEN_HEIGHT - 10, energy * 10, 10), 10)

# ===========================================================================================
class Timer():
    def __init__(self, ms: int):
        self.ticks = ms
        self.initial_time = pg.time.get_ticks()

    def next_tick(self) -> bool:
        now = pg.time.get_ticks()
        if (now - self.initial_time) > self.ticks:
            self.initial_time = now
            return True
        return False

# ===========================================================================================
class Spacecraft(pg.sprite.Sprite):
    def __init__(self, xy_center: tuple[int,int], energy: int, *groups: pg.sprite.Group):
        super().__init__(*groups)
        self.image = pg.image.load('data/space_war/spaceship.png')
        self.rect = self.image.get_rect()
        self.rect.center = xy_center
        self.energy = energy
        self.timer = Timer(TIME_BETWEEN_SHOTS)
        self.backspace_key_pressed: bool = False

    def update(self):
        key = pg.key.get_pressed()
        if key[pg.K_SPACE]:
            self.backspace_key_pressed=True
        if key[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= SPACECRAFT_SPEED
        if key[pg.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += SPACECRAFT_SPEED
        
        time_out = self.timer.next_tick()
        if self.backspace_key_pressed and time_out:
            self.backspace_key_pressed=False
            ShotSpacecraft((self.rect.centerx, self.rect.top), shot_spacecraft_group)
            sound_laser.play()

        self.mask = pg.mask.from_surface(self.image)

        if spacecraft.energy == 0:
            Explosion(self.rect.center, 1.5, explosion_group)
            self.kill()

# ===========================================================================================
class ShotSpacecraft(pg.sprite.Sprite):
    def __init__(self, xy_center: tuple[int,int], *groups: pg.sprite.Group):
        super().__init__(*groups)
        self.image = pg.image.load('data/space_war/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = xy_center

    def update(self):
        global explosion_group
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pg.sprite.spritecollide(self, invider_group, True):
            spacecraft.energy += 1
            Explosion(self.rect.center, 1, explosion_group)
            sound_explosion_1.play()
            self.kill()

        
# ===========================================================================================
class ShotInvader(pg.sprite.Sprite):
    def __init__(self, xy_center: tuple[int,int], *groups: pg.sprite.Group):
        super().__init__(*groups)
        self.image = pg.image.load('data/space_war/alien_bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = xy_center

    def update(self):
        self.rect.y += 3
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        if pg.sprite.spritecollide(self, spacecraft_group, False, pg.sprite.collide_mask):
            spacecraft.energy -= 1
            sound_explosion_2.play()
            self.kill()
                    
# ===========================================================================================
class Invider(pg.sprite.Sprite):
    def __init__(self, xy_center: tuple[int,int], *groups: pg.sprite.Group):
        super().__init__(*groups)
        fate = str(random.randint(1,5))
        self.image = pg.image.load(f'data/space_war/alien{fate}.png')
        self.rect = self.image.get_rect()
        self.rect.center = xy_center
        self.x_increment = 2
        self.x_increment_counter = 0

    def update(self):
        self.rect.x += self.x_increment
        self.x_increment_counter += 1
        if self.x_increment_counter > 75:
            self.x_increment_counter = 0
            self.x_increment *= -1

# ===========================================================================================
class Explosion(pg.sprite.Sprite):
    def __init__(self, xy_center: tuple[int,int], scale:int, *groups: pg.sprite.Group):
        super().__init__(*groups)
        self.images = []
        for i in range(1,6):
            img = pg.image.load(f'data/space_war/exp{i}.png')
            x,y = img.get_size()
            img = pg.transform.scale(img, (x*scale,y*scale))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = xy_center
        self.timer = Timer(50)
     
    def update(self):    
        time_out = self.timer.next_tick()
        if time_out:
            if self.index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.index]
                self.index += 1



# ===========================================================================================
def create_inviders():
    for r in range(INVIDER_ROWS):
        for c in range(INVIDER_COLUMNS):
            Invider((100+c*200, 100+r*70), invider_group)

# ===========================================================================================

bg_img = complete_stage(image)
spacecraft = Spacecraft((SCREEN_WIDTH//2, SCREEN_HEIGHT-100), 15, spacecraft_group)
timer_invader_shot = Timer(1000)
create_inviders()

run = True
while run:
    clock.tick(FPS)
    draw_background()

    time_out = timer_invader_shot.next_tick()
    if time_out: # and invider_group.sprites().len()>0
        invider = random.choice(invider_group.sprites())
        shot_invider = ShotInvader(invider.rect.center)
        shot_invider_group.add(shot_invider)

    spacecraft_group.update()
    shot_spacecraft_group.update()
    invider_group.update()
    shot_invider_group.update()
    explosion_group.update()

    spacecraft_group.draw(screen)
    shot_spacecraft_group.draw(screen)
    invider_group.draw(screen)
    shot_invider_group.draw(screen)
    explosion_group.draw(screen)
    draw_energy_bar(spacecraft.energy)

    if game_status == GameStatus.START:
        draw_text('GET READY, PRESS ANY KEY', 100,100)
        game_status = GameStatus.PLAYING

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.update()

pg.quit()













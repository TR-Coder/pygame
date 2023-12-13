# https://github.com/russs123/flappy_bird/blob/main/Part_3-Game_Physics/flappy_bird_tut3.py
# https://www.youtube.com/watch?v=_7er9kqWpG4&list=PLjcN1EyupaQkz5Olxzwvo1OzDNaNLGWoJ&index=3
# https://iconify.design/docs/icons/


import pygame as pg
import math
import random
from enum import Enum

pg.init()

SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 900
GROUND_SPEED = 5
PIPE_FREQUENCY = 1500   # milliseconds
GRAVITY_UP   = 5
GRAVITY_DOWN = 0.5
FPS = 60
PIPE_GAP = 250
WHITE_COLOR = (255, 255, 255)
IMAGES_PATH = 'data'

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Flappy bird')
font = pg.font.SysFont('Bauhaus 93', 60)
clock = pg.time.Clock()

last_time:int
run: bool
game_over: bool
bird_collided: bool
had_touched_gap: bool
score: int

# ==========================================================================================
class Position(Enum):
    TOP=0,
    BOTTOM=1

# ==========================================================================================
class StageImage():
    def __init__(self, image_path:str, speed: int):
        img = pg.image.load(image_path).convert()
        self.image = self.complete_stage(img)
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.rect = self.image.get_rect()
        self.speed = speed
        self.scroll_x = 0
    
    def complete_stage(self, image: pg.Surface) -> pg.Surface:
        w = image.get_width()
        h = image.get_height()
        times = math.ceil(SCREEN_WIDTH / w)   
        combined_image = pg.Surface((w*times, h)).convert_alpha()
        for t in range(times):
            combined_image.blit(image, (w*t, 0))
        return combined_image
    
    def blit(self, screen: pg.Surface, y:int) -> None:
        x = self.scroll_x
        while x < SCREEN_WIDTH:
            screen.blit(self.image, (x, y))
            self.rect.x = x
            x += self.width

        self.scroll_x -= self.speed
        if abs(self.scroll_x) > self.width:
            self.scroll_x += self.width

# ==========================================================================================
class Bird(pg.sprite.Sprite):
    MAX_GRAVITY = 8
    MAX_SPRITE_COUNTER = 5

    def __init__(self, rect_center:tuple[int,int], *groups: pg.sprite.Group):
        super().__init__(*groups)
        self.images = []
        self.index = 0
        for i in range(3):
            img = pg.image.load(f'{IMAGES_PATH}/bird{i}.png').convert_alpha()
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = rect_center
        self.sprite_counter = 0
        self.gravity = 0
        self.clicked_before = False
        self.rotation = -2

    def mouse_left_bottom_pressed(self) -> bool:
        left, _, _ = pg.mouse.get_pressed()
        if not left:
            self.clicked_before = False
        elif not self.clicked_before:
            self.clicked_before = True
        return self.clicked_before
    

    def next_sprite(self) -> pg.Surface:
        self.sprite_counter += 1
        if self.sprite_counter > self.MAX_SPRITE_COUNTER:
            self.sprite_counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        return self.images[self.index]


    def update(self):
        global game_over
        if self.gravity <= Bird.MAX_GRAVITY:
            self.gravity += GRAVITY_DOWN

        if self.rect.bottom >= background.rect.bottom:
            self.image = pg.transform.rotate(self.image, -80)
            game_over = True
            return
               
        self.rect.y += self.gravity
            
        if self.mouse_left_bottom_pressed() and not bird_collided:
            self.gravity = -GRAVITY_UP

        self.image = self.next_sprite()

        if bird_collided:
            self.rotation = -80

        self.image = pg.transform.rotate(self.image, self.gravity * self.rotation)


# ==========================================================================================
pipe_img_bottom = pg.image.load(f'{IMAGES_PATH}/pipe.png').convert_alpha()
pipe_img_top = pg.transform.flip(pipe_img_bottom , False, True)

class Pipe(pg.sprite.Sprite):
    SCROLL_SPEED = 4

    def __init__(self, x:int, y:int, position: Position, gap:int, *groups: pg.sprite.Group):
        super().__init__(*groups)
        if position == Position.TOP:
            self.image = pipe_img_top.copy()
            self.rect = self.image.get_rect()
            # pg.draw.rect(self.image, (255, 0, 0), self.rect, 4)
            y -= gap
            self.rect.bottomleft = (x, y)
        elif position == Position.BOTTOM:
            self.image = pipe_img_bottom.copy()
            self.rect = self.image.get_rect()
            # pg.draw.rect(self.image, (255, 0, 0), self.rect, 4)
            y += gap
            self.rect.topleft = (x, y)
     
    def update(self):
        self.rect.x -= self.SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()

# ==========================================================================================
class Gap(pg.sprite.Sprite):
    SCROLL_SPEED = 4

    def __init__(self, x:int, y:int, width:int, height:int, *groups: pg.sprite.Group):
        super().__init__(*groups)
        s = pg.Surface((width, height),pg.SRCALPHA)
        self.image = s
        self.rect = s.get_rect()
        self.rect.topleft = (x,y)
    
    def update(self):
        self.rect.x -= self.SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()

# ==========================================================================================
def draw_score():
    x = SCREEN_WIDTH / 2
    y= 20
    img = font.render(str(score), True, WHITE_COLOR)
    screen.blit(img, (x, y))

# ==========================================================================================
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def pressed(self):
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return pg.mouse.get_pressed()[0] == 1
        return False


# ==========================================================================================
background = StageImage(f'{IMAGES_PATH}/bg_ciutat.png', 0)
ground = StageImage(f'{IMAGES_PATH}/ground_flappy.png', GROUND_SPEED)
restart_button_img = pg.image.load(f'{IMAGES_PATH}/restart.png')
restart_button = Button(SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT // 2 - 100, restart_button_img)

bird_group: pg.sprite.Group
pipe_group: pg.sprite.Group
gap_group: pg.sprite.Group

def init_game():
    global run
    global last_time
    global game_over
    global bird_collided
    global had_touched_gap
    global score
    global bird_group
    global pipe_group
    global gap_group
    
    last_time = pg.time.get_ticks() - PIPE_FREQUENCY
    run = True
    game_over = False
    bird_collided = False
    had_touched_gap = False
    score = 0  

    bird_group = pg.sprite.Group()                     # type: ignore
    pipe_group = pg.sprite.Group()                     # type: ignore
    gap_group  = pg.sprite.Group()                     # type: ignore

    Bird((SCREEN_WIDTH//3, SCREEN_HEIGHT//2), bird_group)

# ==========================================================================================

init_game()

while run:
    clock.tick(FPS)
    
    if game_over:
        restart_button.draw()
        if restart_button.pressed():
            init_game()
    else:
        if pg.sprite.groupcollide(bird_group, pipe_group, False, False):
            bird_collided = True

        if not bird_collided:
            bird_collids_gap = pg.sprite.groupcollide(bird_group, gap_group, False, False)
            if bird_collids_gap:
                if not had_touched_gap:
                    had_touched_gap = True
            elif had_touched_gap:
                had_touched_gap = False
                score += 1  
    
        screen.blit(background.image, (0,0))
        ground.blit(screen, background.height)

        time_now:int = pg.time.get_ticks()              # miliseconds
        if time_now - last_time > PIPE_FREQUENCY:
            ramdom_height = random.randint(-100, 100)
            x = SCREEN_WIDTH
            y = SCREEN_HEIGHT//2 + ramdom_height
            gap = PIPE_GAP//2
            Pipe(x, y, Position.TOP, gap, pipe_group)
            Pipe(x, y, Position.BOTTOM, gap, pipe_group)
            Gap(x, y-gap, pipe_img_bottom.get_width(), gap*2, gap_group)
            last_time = time_now

        pipe_group.update()
        pipe_group.draw(screen)

        gap_group.update()
        gap_group.draw(screen)

        bird_group.update()
        bird_group.draw(screen)

        draw_score()
         
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
           
    pg.display.update()

pg.quit()
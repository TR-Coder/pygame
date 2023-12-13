# https://github.com/russs123/flappy_bird/blob/main/Part_3-Game_Physics/flappy_bird_tut3.py
# https://www.youtube.com/watch?v=_7er9kqWpG4&list=PLjcN1EyupaQkz5Olxzwvo1OzDNaNLGWoJ&index=3

import pygame as pg
import math

pg.init()
SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 900
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Flappy bird')
run = True
GROUND_SPEED = 5

clock = pg.time.Clock()
fps = 60
game_over = False

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
        combined_image = pg.Surface((w*times, h))
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


class Bird(pg.sprite.Sprite):

    MAX_GRAVITY = 8
    MAX_SPRITE_COUNTER = 5

    def __init__(self, rect_center:tuple[int,int], *groups: pg.sprite.Group):
        super().__init__(*groups)
        self.images = []
        self.index = 0
        for i in range(3):
            img = pg.image.load(f'data/bird{i}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = rect_center
        self.sprite_counter = 0
        self.gravity = 0
        self.clicked_before = False

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
            self.gravity += 0.5

        if self.rect.bottom >= background.rect.bottom:
            self.image = pg.transform.rotate(self.image, -40)
            game_over = True
            return
            
        self.rect.y += self.gravity
            
        if self.mouse_left_bottom_pressed():
            self.gravity = -10

        self.image = self.next_sprite()
        self.image = pg.transform.rotate(self.image, self.gravity * -2)

background = StageImage('data/bg_ciutat.png', 0)
ground = StageImage('data/ground_flappy.png', GROUND_SPEED)

bird_group  = pg.sprite.Group()                     # type: ignore
bird = Bird((100,SCREEN_HEIGHT//2), bird_group)

while run:
    clock.tick(fps)
    
    if not game_over:
        screen.blit(background.image, (0,0))
        ground.blit(screen, background.height)
        bird_group.update()
        bird_group.draw(screen)
    

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    pg.display.update()

pg.quit()
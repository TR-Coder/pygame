#
#       ████████╗██████╗        ██████╗ ██████╗ ██████╗ ███████╗██████╗ 
#       ╚══██╔══╝██╔══██╗      ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗
#          ██║   ██████╔╝█████╗██║     ██║   ██║██║  ██║█████╗  ██████╔╝
#          ██║   ██╔══██╗╚════╝██║     ██║   ██║██║  ██║██╔══╝  ██╔══██╗
#          ██║   ██║  ██║      ╚██████╗╚██████╔╝██████╔╝███████╗██║  ██║
#          ╚═╝   ╚═╝  ╚═╝       ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
#
#

import pygame as pg
from typing import Tuple, Union, Optional, List

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800
FPS = 30
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)

pg.init()
font = pg.font.SysFont('Bauhaus 93', 60)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pg.Surface(screen.get_size())
bg.fill(WHITE)
clock = pg.time.Clock()
jumping_img_path = 'data/salt/salt_{}.png'
running_img_path = 'data/salt/correr_{}.png'

# ===========================================================================================
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

# ===========================================================================================
class Rock(pg.sprite.Sprite):
    def __init__(self,x:int, y_minimun:int, *groups: pg.sprite.Group) -> None:
        super().__init__(*groups)
        img = pg.image.load('data/salt/roca_1.png')
        x_size, y_size = img.get_size()
        scale = .1
        self.image = pg.transform.scale(img, (x_size*scale, y_size*scale))

        self.rect:pg.Rect = self.image.get_rect()
        self.rect.bottom = y_minimun
        self.rect.x = x

        self.timer = Timer(30)
        self.mask = pg.mask.from_surface(self.image)

    def update(self) -> None:
        if self.timer.is_over():
            self.rect.x -= 10

# ===========================================================================================
class Runner(pg.sprite.Sprite):
    def __init__(self, x:int, y_minimum:int,  *groups: pg.sprite.Group) -> None:
        super().__init__(*groups)
        self.jumping = False
        self.running = True
        # self.y_inc = [5,4,3,2,1,0,-1,-2,-3,-4,-5]
        self.images_jumping, self.mask_jumping = self.get_images(jumping_img_path, 12, 0.5)
        self.images_running, self.mask_running = self.get_images(running_img_path, 6, 0.5)
        self.index = 0
        self.image = self.images_running[self.index]
        self.rect:pg.Rect = self.image.get_rect()
        self.rect.bottom = y_minimum
        self.rect.x = x
        self.y_minimum = y_minimum
        self.timer = Timer(60)
        self.runner_mask:pg.Mask = self.mask_running[0]
  

    def get_images(self, path: str, images_number: int, scale: float) ->  Tuple[List[pg.Surface], List[pg.Mask]]:
        images:list[pg.Surface] = []
        masks:list[pg.Mask] = []
        for i in range(1,images_number):
            img = pg.image.load(path.format(i))
            x_size, y_size = img.get_size()
            img = pg.transform.scale(img, (x_size*scale, y_size*scale))
            mask = pg.mask.from_surface(img)
            images.append(img)
            masks.append(mask)
        return images, masks


    def update(self) -> None:
        if self.running:
            if self.timer.is_over():
                self.image = self.images_running[self.index]
                self.runner_mask = self.mask_running[self.index]
                self.index = (self.index + 1) % len(self.images_running)
                if self.jumping:
                    self.running=False
                    self.index = 0

        elif self.jumping:
            if self.timer.is_over():
                self.image = self.images_jumping[self.index]
                self.runner_mask = self.mask_jumping[self.index]
                self.index = (self.index + 1) % len(self.images_jumping)
                if self.index == 0:
                    self.jumping = False
                    self.running = True

    
    def collide_with(self, rock_group:pg.sprite.Group) -> bool:
        for rock in rock_group:
            offset_x = rock.rect.x - self.rect.x
            offset_y = rock.rect.y - self.rect.y
            if self.runner_mask.overlap(rock.mask, (offset_x, offset_y)):
                return True
        return False
                   
# ===============================================================================
def draw_background() -> None:
    screen.blit(bg, (0, 0))

# ===============================================================================
def draw_floor() -> None:
    y_floor = SCREEN_HEIGHT - SCREEN_HEIGHT//8
    pg.draw.rect(screen, BLACK, [0,y_floor, SCREEN_WIDTH,5])

# ===============================================================================
def main() -> None:
    pg.display.set_caption('Jumping')

    y_min = SCREEN_HEIGHT - SCREEN_HEIGHT//8
    x:int = SCREEN_WIDTH // 8

    runner_group = pg.sprite.Group()            # type: ignore
    rock_group = pg.sprite.Group()              # type: ignore
    runner = Runner(x,y_min,runner_group)
    Rock(SCREEN_WIDTH//2, y_min, rock_group)


    stop = False
    run = True
    while run:
        clock.tick(FPS)
        draw_background()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    if not runner.jumping:
                        runner.jumping = True
            if event.type == pg.QUIT:
                run = False

        draw_floor()
        if not stop:
            runner_group.update()
            rock_group.update()

        runner_group.draw(screen)
        rock_group.draw(screen)

        pg.display.update()

        stop = runner.collide_with(rock_group)

    pg.quit()
if __name__ == '__main__':
    main()
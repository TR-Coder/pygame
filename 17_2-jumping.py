#
#       ████████╗██████╗        ██████╗ ██████╗ ██████╗ ███████╗██████╗ 
#       ╚══██╔══╝██╔══██╗      ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗
#          ██║   ██████╔╝█████╗██║     ██║   ██║██║  ██║█████╗  ██████╔╝
#          ██║   ██╔══██╗╚════╝██║     ██║   ██║██║  ██║██╔══╝  ██╔══██╗
#          ██║   ██║  ██║      ╚██████╗╚██████╔╝██████╔╝███████╗██║  ██║
#          ╚═╝   ╚═╝  ╚═╝       ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
#
import pygame as pg
import random
import os

SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 800
FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)

pg.init()
font = pg.font.SysFont('Bauhaus 93', 60)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pg.Surface(screen.get_size())
bg.fill(WHITE)
clock = pg.time.Clock()


stop = False

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
class Rock(pg.sprite.Sprite):
    def __init__(self,x:int, y_minimun:int, *groups: pg.sprite.Group) -> None:
        super().__init__(*groups)
        img = pg.image.load('data/salt/roca_1.png')
        x_size, y_size = img.get_size()
        scale = .1
        self.image = pg.transform.scale(img, (x_size*scale, y_size*scale))
        self.rect:pg.Rect = self.image.get_rect()
        self.rect.bottom = y_minimun
        self.rect.right = x
        self.timer = Timer(30)
        self.mask = pg.mask.from_surface(self.image)

    def update(self) -> None:
        time_out = self.timer.next_tick()
        if time_out:
            self.rect.right -= 10

# ===========================================================================================
class Runner(pg.sprite.Sprite):
    def __init__(self, x:int, y_minimun:int,  *groups: pg.sprite.Group) -> None:
        super().__init__(*groups)
        self.jumping = False
        self.running = True
        self.y_inc = [5,4,3,2,1,0,-1,-2,-3,-4,-5]

        self.images_jumping = []
        self.mask_jumping = []

        for i in range(1,12):
            img = pg.image.load(f'data/salt/salt_{i}.png')
            x_size, y_size = img.get_size()
            scale = .5
            img = pg.transform.scale(img, (x_size*scale, y_size*scale))
            self.images_jumping.append(img)
            mask = pg.mask.from_surface(img)
            self.mask_jumping.append(mask)

        self.images_running = []
        self.mask_running = []
        for i in range(1,6):
            img = pg.image.load(f'data/salt/correr_{i}.png')
            x_size, y_size = img.get_size()
            scale = .5
            img = pg.transform.scale(img, (x_size*scale, y_size*scale))
            self.images_running.append(img)
            mask = pg.mask.from_surface(img)
            self.mask_running.append(mask)

        self.index = 0
        self.image = self.images_running[self.index]
        self.rect:pg.Rect = self.image.get_rect()
        self.y_min = y_minimun - self.rect.height//2
        self.x = x
        self.y = self.y_min
        self.rect.center = self.x, self.y
        self.timer = Timer(60)
        self.index_ant = 0
        self.running_ant = False
        self.jumping_ant = False

    def update(self, *args) -> None:
        rock_group:pg.sprite.Group = args[0]
        if self.running:
            time_out = self.timer.next_tick()
            if time_out:
                self.image = self.images_running[self.index]
                self.rect.center = self.x, self.y
                self.collide_with(rock_group)
                self.index += 1
                if self.index==len(self.images_running):
                    self.index = 0
                    self.rect.center = self.x, self.y
                    if self.jumping:
                        self.running=False
                    return

        if self.jumping:
            time_out = self.timer.next_tick()
            if time_out:
                self.image = self.images_jumping[self.index]
                self.y -= self.y_inc[self.index]
                self.rect.center = self.x, self.y
                self.collide_with(rock_group)
                self.index += 1
                if self.index==len(self.images_jumping):
                    self.index = 0
                    self.y = self.y_min
                    self.rect.center = self.x, self.y
                    self.jumping = False
                    self.running = True
                    return
    
    def collide_with(self, rock_group:pg.sprite.Group) -> bool:
        global stop
        i = self.index - 1
        if self.jumping:
            if i<0:
                i = len(self.images_jumping) - 1
            runner_mask = self.mask_jumping[i]
        else:
            i = self.index -1 
            if i<0:
                i = len(self.images_running) - 1
            runner_mask = self.mask_running[i]

        for rock in rock_group:
            offset_x = rock.rect.x - self.rect.x
            offset_y = rock.rect.y - self.rect.y
            if runner_mask.overlap(rock.mask, (offset_x, offset_y)):
                print(self.jumping, i)
                stop = True
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
    global stop

    pg.display.set_caption('Jumping')

    y_min = SCREEN_HEIGHT - SCREEN_HEIGHT//8
    x:int = SCREEN_WIDTH // 8

    runner_group = pg.sprite.Group()            # type: ignore
    rock_group = pg.sprite.Group()              # type: ignore
    runner = Runner(x,y_min,runner_group)
    rock = Rock(SCREEN_WIDTH//2, y_min, rock_group)


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
            runner_group.update(rock_group)
            rock.update()

        runner_group.draw(screen)
        rock_group.draw(screen)

        pg.display.update()

    pg.quit()
if __name__ == '__main__':
    main()
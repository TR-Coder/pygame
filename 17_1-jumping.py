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
bg.fill(BLACK)
clock = pg.time.Clock()


# ===============================================================================
def draw_background() -> None:
    screen.blit(bg, (0, 0))

# ===============================================================================
def draw_floor() -> None:
    y_floor = SCREEN_HEIGHT - SCREEN_HEIGHT//8
    pg.draw.rect(screen, WHITE, [0,y_floor, SCREEN_WIDTH,5])

# ===============================================================================
def draw_runner(x:int, y:int) -> None:
    size = 20
    # rect = pg.Rect(0,0,size,size)
    # rect.center = (x,y)
    rect = pg.Rect(0, 0, size, size).move(x - size // 2, y - size // 2)
    pg.draw.rect(screen, GREEN, rect)

# ===============================================================================
y_min = (SCREEN_HEIGHT - SCREEN_HEIGHT//8) - 10
x:int = SCREEN_WIDTH // 8
y:int = y_min
jumping = False
y_max = y_min - 100
y_inc = 18
gravity = 1

def jump() -> None:
    global jumping
    global x
    global y
    global gravity
    global y_inc
    if jumping:
        y -= y_inc
        y_inc -= gravity
        if y>y_min:
            y = y_min
            y_inc = 18
            jumping = False

# ===============================================================================

def main() -> None:
    global jumping
    global x
    global y
    pg.display.set_caption('Jumping')

    run = True
    while run:
        clock.tick(FPS)
        draw_background()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    if not jumping:
                        jumping = True
            if event.type == pg.QUIT:
                run = False

        draw_floor()
        if jumping:
            jump()
        draw_runner(x,y)
        pg.display.update()

    pg.quit()
if __name__ == '__main__':
    main()
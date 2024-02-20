#
#       ████████╗██████╗        ██████╗ ██████╗ ██████╗ ███████╗██████╗ 
#       ╚══██╔══╝██╔══██╗      ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗
#          ██║   ██████╔╝█████╗██║     ██║   ██║██║  ██║█████╗  ██████╔╝
#          ██║   ██╔══██╗╚════╝██║     ██║   ██║██║  ██║██╔══╝  ██╔══██╗
#          ██║   ██║  ██║      ╚██████╗╚██████╔╝██████╔╝███████╗██║  ██║
#          ╚═╝   ╚═╝  ╚═╝       ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
#

# https://www.youtube.com/watch?v=W-3okcjOFnY&list=PLsFyHm8kJsx32EFcsJNt5sDI_nKsanRUu&index=20

import pygame as pg
import random

SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 900
FPS = 60

RECTANGLE_WIDTH = 20
MARGIN = 10

pg.init()
font = pg.font.SysFont('Bauhaus 93', 60)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pg.Surface(screen.get_size())
bg.fill((170, 238, 187))
clock = pg.time.Clock()

def draw_background() -> None:
    screen.blit(bg, (0, 0))


''' La idea per a crear el túnel és:
    Generem intervals de longitud aleatoria.
    Durant cada interval el túnel va pujant o baixant amb una inclinació determinada.
    En cada nou interval el sentit de pujada és el contrari a la del interval anterior.
'''
def create_tunnel() -> list[pg.Rect]:
    rectangles:list[pg.Rect] = []
    NUMBER_OF_RECTANGLES = SCREEN_WIDTH // RECTANGLE_WIDTH
    GAP = 300
    MIN_HEIGHT = 40
    sign = -1
    x = 0
    height = MARGIN +  200
    i = 0

    while i < NUMBER_OF_RECTANGLES:
        interval_length = random.randint(15,25)      # number of rectangles per interval.
        slope = random.randint(10, 20) * sign        # The units are pixels.
        sign = -sign
        print(interval_length, slope, sign)
        for j in range(interval_length):
            height = (height + slope) if height>=MIN_HEIGHT else MIN_HEIGHT
            rect_sup = pg.Rect(x, MARGIN, RECTANGLE_WIDTH, height)
            rect_inf = pg.Rect(x, MARGIN+height+GAP, RECTANGLE_WIDTH, SCREEN_HEIGHT-(MARGIN+height+GAP))
            rectangles.append(rect_sup)
            rectangles.append(rect_inf)
            x = x + RECTANGLE_WIDTH
        i = i + j
    print(len(rectangles))
    return rectangles



def draw_tunnel(rectangles:list[pg.Rect]) -> None:
    for rectangle in rectangles:
        pg.draw.rect(screen, 'blue', rectangle)      
    pg.draw.rect(screen, 'dark gray', [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT], MARGIN)

def move_tunnel(rectangles:list[pg.Rect]) -> list[pg.Rect]:
    SPEED = 5
    for i in range(len(rectangles)):
        rectangles[i].x -= SPEED
        if rectangles[i].x + RECTANGLE_WIDTH < 0:
            rectangles.pop(0)
            rectangles.pop(1)
            rect_sup = pg.Rect(0, MARGIN, RECTANGLE_WIDTH, 100)
            rect_sup1 = pg.Rect(0, MARGIN, RECTANGLE_WIDTH, 100)
            rectangles.append(rect_sup)
            rectangles.append(rect_sup1)
    return rectangles



def main() -> None:

    rectangles:list[pg.Rect] = create_tunnel()
    

    pg.display.set_caption('Missile')


    run = True
    while run:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        draw_tunnel(rectangles)
        rectangles = move_tunnel(rectangles)
        pg.display.update()
    
    pg.quit()



if __name__ == '__main__':
    main()
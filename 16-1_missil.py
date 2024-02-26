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

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
FPS = 60

RECTANGLE_WIDTH = 10
MARGIN = 10
NUMBER_OF_RECTANGLES = SCREEN_WIDTH // RECTANGLE_WIDTH

pg.init()
font = pg.font.SysFont('Bauhaus 93', 60)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pg.Surface(screen.get_size())
bg.fill((170, 238, 187))
clock = pg.time.Clock()

def draw_background() -> None:
    screen.blit(bg, (0, 0))


sign = -1
upper_height = MARGIN +  200
def create_interval(rectangles:list[pg.Rect]) -> int:
    global sign
    global upper_height
    GAP = 300
    MIN_HEIGHT = 30
    interval_length = random.randint(30,40)      # number of rectangles per interval.
    slope = random.randint(5, 15) * sign        # The units are pixels.
    sign = -sign
    for j in range(interval_length):

        upper_height = (upper_height + slope) if upper_height>=MIN_HEIGHT else MIN_HEIGHT + slope      
        upper_rect = pg.Rect(0, MARGIN, RECTANGLE_WIDTH, upper_height)
        rectangles.append(upper_rect)

        lower_height = SCREEN_HEIGHT - 2*MARGIN - GAP - upper_height
        if lower_height < MIN_HEIGHT - MARGIN:
            upper_height = lower_height = SCREEN_HEIGHT - MARGIN - GAP - MIN_HEIGHT

        lower_rect = pg.Rect(0, MARGIN+upper_height+GAP, RECTANGLE_WIDTH, lower_height)
        rectangles.append(lower_rect)

    return interval_length

        

''' La idea per a crear el túnel és:
    Generem intervals de longitud aleatoria.
    Durant cada interval el túnel va pujant o baixant amb una inclinació determinada.
    En cada nou interval el sentit de pujada és el contrari a la del interval anterior.
'''
def create_tunnel() -> list[pg.Rect]:
    rectangles:list[pg.Rect] = []
    i = 0
    while i < NUMBER_OF_RECTANGLES:
        interval_length = create_interval(rectangles)
        i = i + interval_length
    return rectangles



def draw_tunnel(x:int, rectangles:list[pg.Rect]) -> None:
    for upper_rect, lower_rect in zip(rectangles[0::2], rectangles[1::2]):
        upper_rect.x = lower_rect.x = x
        pg.draw.rect(screen, 'blue', upper_rect)      
        pg.draw.rect(screen, 'blue', lower_rect)
        x = x + RECTANGLE_WIDTH
    pg.draw.rect(screen, 'dark gray', [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT], MARGIN)



def main() -> None:
    pg.display.set_caption('Missile')
    rectangles:list[pg.Rect] = create_tunnel()
    x = 0

    run = True
    while run:
        clock.tick(FPS)
        draw_background()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        draw_tunnel(x, rectangles)
        if abs(x) >= RECTANGLE_WIDTH:
            x += RECTANGLE_WIDTH - 6
            rectangles.pop(0)
            rectangles.pop(0)
        else:
            x -= 6

        if len(rectangles)<=NUMBER_OF_RECTANGLES*2:
            create_interval(rectangles)

        pg.display.update()
    
    pg.quit()



if __name__ == '__main__':
    main()
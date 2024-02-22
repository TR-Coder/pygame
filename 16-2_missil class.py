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

class Tunnel:
    def __init__(self) -> None:
        self.sign = -1
        self.upper_height = MARGIN +  200
        self.rectangles:list[pg.Rect] = []
        self.x = 0
        self.delta_x = 6
        self.create()


    def create_interval(self) -> int:
        GAP = 300
        MIN_HEIGHT = 30
        interval_length = random.randint(15,25)      # number of rectangles per interval.
        slope = random.randint(5, 15) * self.sign        # The units are pixels.
        self.sign = -self.sign
        for j in range(interval_length):
            self.upper_height = (self.upper_height + slope) if self.upper_height>=MIN_HEIGHT else MIN_HEIGHT + slope      
            upper_rect = pg.Rect(0, MARGIN, RECTANGLE_WIDTH, self.upper_height)
            self.rectangles.append(upper_rect)

            lower_height = SCREEN_HEIGHT - 2*MARGIN - GAP - self.upper_height
            if lower_height < MIN_HEIGHT - MARGIN:
                self.upper_height = lower_height = SCREEN_HEIGHT - MARGIN - GAP - MIN_HEIGHT

            lower_rect = pg.Rect(0, MARGIN+self.upper_height+GAP, RECTANGLE_WIDTH, lower_height)
            self.rectangles.append(lower_rect)

        return interval_length

        

    ''' La idea per a crear el túnel és:
        Generem intervals de longitud aleatoria.
        Durant cada interval el túnel va pujant o baixant amb una inclinació determinada.
        En cada nou interval el sentit de pujada és el contrari a la del interval anterior.
    '''
    def create(self) -> None:
        i = 0
        while i < NUMBER_OF_RECTANGLES:
            interval_length = self.create_interval()
            i = i + interval_length


    def draw(self) -> None:
        for upper_rect, lower_rect in zip(self.rectangles[0::2], self.rectangles[1::2]):
            upper_rect.x = lower_rect.x = self.x
            pg.draw.rect(screen, 'blue', upper_rect)      
            pg.draw.rect(screen, 'blue', lower_rect)
            self.x = self.x + RECTANGLE_WIDTH
        pg.draw.rect(screen, 'dark gray', [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT], MARGIN)
        # self.update()

    def update(self) -> None:
        if abs(self.x) >= RECTANGLE_WIDTH:
            self.x += RECTANGLE_WIDTH - self.delta_x
            self.rectangles.pop(0)
            self.rectangles.pop(0)
        else:
            self.x -= self.delta_x

        if len(self.rectangles)<=NUMBER_OF_RECTANGLES*2:
            self.create_interval()

def main() -> None:
    tunnel = Tunnel()
    pg.display.set_caption('Missile')
 
    run = True
    while run:
        clock.tick(FPS)
        draw_background()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        tunnel.draw()
        pg.display.update()
    
    pg.quit()



if __name__ == '__main__':
    main()
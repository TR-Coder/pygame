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
import os

SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 800
FPS = 60

pg.init()
font = pg.font.SysFont('Bauhaus 93', 60)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pg.Surface(screen.get_size())
bg.fill((170, 238, 187))
clock = pg.time.Clock()


# ===============================================================================
def load_image(name: str, scale:float=1) -> pg.Surface:
    working_directory = os.path.split(os.path.abspath(__file__))[0]
    assets_directory = os.path.join(working_directory, 'data')
    img_path:str   = os.path.join(assets_directory, name)
    img:pg.Surface = pg.image.load(img_path).convert_alpha()    # convert_alpha() fa que funcione la transparència del .png
    size:tuple[int, int] = img.get_size()
    scaled_size:tuple[float, float] = (size[0] * scale, size[1] * scale)
    return pg.transform.scale(img, scaled_size)

# ===============================================================================
def draw_background() -> None:
    screen.blit(bg, (0, 0))

# ===============================================================================
class Missil(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('rocketship.svg', scale=1) 
        self.rect = self.image.get_rect()
        x = SCREEN_WIDTH // 4
        y = Tunnel.missile_initial_y_position()
        self.rect.center = (x, y)

    def draw(self):
        key = pg.key.get_pressed()
        if key[pg.K_UP]:
            self.rect.y -= 5
        if key[pg.K_DOWN]:
            self.rect.y += 5
        screen.blit(self.image, self.rect)

# ===============================================================================
#   -------------------------
#           MARGIN
#   -------------------------
#           HEIGHT
#   -------------------------
#           GAP
#   -------------------------
#           MARGIN
#   -------------------------
# ===============================================================================
class Tunnel:
    GAP = 300
    MIN_HEIGHT = 30
    MARGIN = 10
    RECTANGLE_WIDTH = 10
    NUMBER_OF_RECTANGLES = SCREEN_WIDTH // RECTANGLE_WIDTH
    INC_X = 6
    INITIAL_HEIGHT = 100

    def __init__(self) -> None:
        self.upper_height = self.MARGIN +  self.INITIAL_HEIGHT
        self.rectangles:list[pg.Rect] = []
        self.x = 0
        self.create()

    @classmethod
    def missile_initial_y_position(cls) -> int:
        return cls.INITIAL_HEIGHT + cls.GAP//2


    def create_interval(self) -> int:
        interval_length = random.randint(15,25)                     # number of rectangles per interval.
        slope = random.randint(5, 15) * random.choice([1, -1])      # The units are pixels.

        for j in range(interval_length):
            self.upper_height = (self.upper_height + slope) if self.upper_height>=self.MIN_HEIGHT else self.MIN_HEIGHT + slope      

            upper_rect = pg.Rect(0, self.MARGIN, self.RECTANGLE_WIDTH, self.upper_height)
            self.rectangles.append(upper_rect)

            lower_height = SCREEN_HEIGHT - 2*self.MARGIN - self.GAP - self.upper_height
            if lower_height < self.MIN_HEIGHT - self.MARGIN:
                self.upper_height = lower_height = SCREEN_HEIGHT - self.MARGIN - self.GAP - self.MIN_HEIGHT

            lower_rect = pg.Rect(0, self.MARGIN+self.upper_height+self.GAP, self.RECTANGLE_WIDTH, lower_height)
            self.rectangles.append(lower_rect)

        return interval_length   


    def create_straight_interval(self, interval: int) -> int:   
        for i in range(interval):
            upper_rect = pg.Rect(0, self.MARGIN, self.RECTANGLE_WIDTH, self.upper_height)
            self.rectangles.append(upper_rect)

            lower_height = SCREEN_HEIGHT - 2*self.MARGIN - self.GAP - self.upper_height
            lower_rect = pg.Rect(0, self.MARGIN+self.upper_height+self.GAP, self.RECTANGLE_WIDTH, lower_height)
            self.rectangles.append(lower_rect)
        return self.upper_height
        

    ''' La idea per a crear el túnel és:
        Generem intervals de longitud aleatoria.
        Durant cada interval el túnel va pujant o baixant amb una inclinació determinada.
        En cada nou interval el sentit de pujada és el contrari a la del interval anterior.
    '''
    def create(self) -> None:
        INITIAL_INTERVAL = 100
        self.create_straight_interval(INITIAL_INTERVAL)
        i = 0
        while i < self.NUMBER_OF_RECTANGLES-100:
            interval_length = self.create_interval()
            i = i + interval_length


    def draw_rounded_rect(self, surface, rect, color, corner_radius):
        ''' Draw a rectangle with rounded corners '''
        if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
            raise ValueError(f"Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})")

        # draw rectangles
        pg.draw.rect(surface, color, rect.inflate(-2*corner_radius, 0))
        pg.draw.rect(surface, color, rect.inflate(0, -2*corner_radius))

        # draw circles for the corners
        pg.draw.circle(surface, color, (rect.topleft[0] + corner_radius, rect.topleft[1] + corner_radius), corner_radius)
        pg.draw.circle(surface, color, (rect.topright[0] - corner_radius, rect.topright[1] + corner_radius), corner_radius)
        pg.draw.circle(surface, color, (rect.bottomleft[0] + corner_radius, rect.bottomleft[1] - corner_radius), corner_radius)
        pg.draw.circle(surface, color, (rect.bottomright[0] - corner_radius, rect.bottomright[1] - corner_radius), corner_radius)

    def draw(self) -> None:
        x = self.x
        for upper_rect, lower_rect in zip(self.rectangles[0::2], self.rectangles[1::2]):
            upper_rect.x = lower_rect.x = x
            # pg.draw.rect(screen, 'blue', upper_rect)      
            # pg.draw.rect(screen, 'blue', lower_rect)
            self.draw_rounded_rect(screen, upper_rect, 'blue', 5)
            self.draw_rounded_rect(screen, lower_rect, 'blue', 5)
            x = x + self.RECTANGLE_WIDTH
        pg.draw.rect(screen, 'dark gray', [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT], self.MARGIN)
        self.update()

    def update(self) -> None:
        if abs(self.x) >= self.RECTANGLE_WIDTH:
            self.x += self.RECTANGLE_WIDTH - self.INC_X
            self.rectangles.pop(0)
            self.rectangles.pop(0)
        else:
            self.x -= self.INC_X

        if len(self.rectangles)<=self.NUMBER_OF_RECTANGLES*2:
            self.create_interval()

    def collide_with(self, missil:Missil) -> bool:
        for rect in self.rectangles:
            if missil.rect.colliderect(rect):
                return True
        return False
    
# ===============================================================================

def main() -> None:
    pg.display.set_caption('Missile')
    tunnel = Tunnel()
    missil = Missil()
 
    run = True
    while run:
        clock.tick(FPS)
        draw_background()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        tunnel.draw()
        missil.draw()
        if tunnel.collide_with(missil):
            run = False
        pg.display.update()
    pg.quit()

if __name__ == '__main__':
    main()
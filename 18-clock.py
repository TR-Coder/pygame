import pygame as pg
import pygame.gfxdraw as gfx

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800
FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

pg.init()
font = pg.font.SysFont('Bauhaus 93', 60)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pg.Surface(screen.get_size())
bg.fill(WHITE)
clock = pg.time.Clock()

Coord_ = tuple[int,int]
Color_ = tuple[int,int,int]
Group_ = pg.sprite.Group

def draw_background() -> None:
    screen.blit(bg, (0, 0))


# class Button():
#     def __init__(self, screen: pg.Surface, center: Coord_, radius:int, color: Color_, symbol: str) -> None:
#         self.screen = screen
#         self.center = center
#         self.radius = radius
#         self.color = color
#         self.symbol = symbol
#         self.font = pg.font.SysFont('Calibri',40,bold=True)
    
#     def draw(self) -> None:
#         # pg.draw.circle(self.screen, self.color, self.center, self.radius)
#         gfx.aacircle(self.screen, *self.center, self.radius, self.color)
#         gfx.filled_circle(self.screen, *self.center, self.radius, self.color)

#         img_txt = self.font.render(self.symbol, True, WHITE)
#         # x = self.center[0] - img_txt.get_width() / 2
#         # y = self.center[1] - img_txt.get_height() / 2
#         # self.screen.blit(img_txt, (x,y))
#         rect = img_txt.get_rect(center=self.center)
#         self.screen.blit(img_txt, rect)
    
class Button(pg.sprite.Sprite):
    def __init__(self, x:int, y:int, radius:int, color: Color_, symbol: str, group: Group_) -> None:
        super().__init__(group)
        self.image = pg.Surface((radius*2, radius*2), pg.SRCALPHA)      # .convert_alpha(), no funciona.
        # self.image.fill((255,0,0))

        self.rect = self.image.get_rect()
        pg.draw.circle(self.image, BLACK, self.rect.center, radius)
        # gfx.aacircle(self.image, radius, radius, radius-1, color)
        # gfx.filled_circle(self.image, radius, radius, radius-1, color)

        self.font = pg.font.SysFont('Calibri',80,bold=True)
        img_txt = self.font.render(symbol, True, WHITE)
        rect = img_txt.get_rect(center=self.rect.center)
        self.image.blit(img_txt, rect)
        self.rect.x = x
        self.rect.y = y

    # def update(self, *arg):
    #     clicked = arg[0]
    #     mouse_position = arg[1]
    #     if 

        

def button() -> None:
    rect = pg.Rect(50, 50, 200, 100)
    pg.draw.rect(screen, RED, rect,  width=0,  border_radius=5)

# button1= Button(screen, center=(400,400), radius=30, color=BLACK, symbol='+')
buttons_group:Group_ = pg.sprite.Group()
button1 = Button(x=400, y=400, radius=55, color=BLACK, symbol='+', group=buttons_group)



def main() -> None:
    pg.display.set_caption('Clock')

    clicked = False
    mouse_position = (-1, -1)

    run = True
    while run:
        clock.tick(FPS)
        draw_background()
        button()
        # button1.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = event.pos
                # if button1.rect.collidepoint(mouse_position):
                if button1.rect.collidelist()
                    clicked = True
                    button1.rect.move_ip(5,5)
            if event.type == pg.MOUSEBUTTONUP and event.button == 1 and clicked:
                clicked = False
                button1.rect.move_ip(-5,-5)

        buttons_group.update()
        buttons_group.draw(screen)
        pg.display.update()
    pg.quit()
    
if __name__ == '__main__':
    main()
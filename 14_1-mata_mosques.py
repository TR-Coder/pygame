from typing import Any
import pygame as pg
import os
import random

SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 900
FPS = 60
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

pg.init()
font = pg.font.SysFont('Bauhaus 93', 60)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pg.Surface(screen.get_size()).convert()
bg.fill((170, 238, 187))
clock = pg.time.Clock()

working_directory = os.path.split(os.path.abspath(__file__))[0]
assets_directory = os.path.join(working_directory, 'data')

def load_image(name: str, scale:float=1) -> pg.Surface:
    img_path:str   = os.path.join(assets_directory, name)
    img:pg.Surface = pg.image.load(img_path).convert_alpha()    # convert_alpha() fa que funcione la transparència del .png
    size:tuple[int, int] = img.get_size()
    scaled_size:tuple[float, float] = (size[0] * scale, size[1] * scale)
    return pg.transform.scale(img, scaled_size)

# -----------------------------------------------------------------------------------------------
class Fly(pg.sprite.Sprite):
    def __init__(self, rect_center: tuple[int,int], *groups: pg.sprite.Group):
        super().__init__(*groups)
        self.image = load_image('mosquit.png', scale=0.15)   
        self.rect = self.image.get_rect()
        self.rect.center = rect_center
        self.hunted = False
    
    def update(self):
        if self.hunted:
            self.pass_away()
        else:
            self.flap()
    
    def flap(self):
        area_screen = screen.get_rect()
        alealt_x = random.randint(-5,5)
        alealt_y = random.randint(-5,5)
        new_position = self.rect.move(alealt_x, alealt_y)
        if area_screen.contains(new_position):
            self.rect = new_position

    def pass_away(self):
        self.image = self.original
        self.hunted = False
        print()

    def hitted(self):
        if not self.hunted:
            self.hunted = True
            self.original = self.image
    

# -----------------------------------------------------------------------------------------------
class FlySwatter(pg.sprite.Sprite):
    def __init__(self, rect_center: tuple[int,int], *groups: pg.sprite.Group):
        super().__init__(*groups)
        self.image = load_image('mata_mosques.png', scale=0.35)   
        self.rect = self.image.get_rect()
        self.rect.center = rect_center
        self.hitting = False
    
    def update(self) -> None:
        self.rect.topleft = pg.mouse.get_pos()
        if self.hitting:
            self.rect.move_ip(15, 25)

    def hit(self, fly: Fly) -> bool:
        if not self.hitting:
            self.hitting = True
            hitbox = self.rect.inflate(-5,-5)
            return hitbox.colliderect(fly.rect)
        return False
    
    def unhit(self):
        self.hitting = False

# -----------------------------------------------------------------------------------------------
def draw_score(score:int) -> None:
    img = font.render(f'{str(score)} points', True, BLACK_COLOR)
    screen.blit(img, (10, 10))

# -----------------------------------------------------------------------------------------------
def draw_background() -> None:
    screen.blit(bg, (0, 0))

# ==============================================================================================
def main() -> None:
    run = True
    score: int = 0

    pg.display.set_caption('Matamosques')
    pg.mouse.set_visible(False)
    sprite_group = pg.sprite.Group()        # type: ignore

    fly = Fly((SCREEN_WIDTH//4, SCREEN_HEIGHT//15), sprite_group)
    fly_swatter = FlySwatter((SCREEN_WIDTH//2, SCREEN_HEIGHT//2), sprite_group)

    while run:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if fly_swatter.hit(fly):
                    fly.hitted()
                    score += 1
            elif event.type == pg.MOUSEBUTTONUP:
                fly_swatter.unhit()
            elif event.type == pg.QUIT:
                run = False

        draw_background()
        draw_score(score)
        sprite_group.update()
        sprite_group.draw(screen)

        pg.display.update()
    
    pg.quit()

if __name__ == '__main__':
    main()



# Notes
# (1) La classe RenderPlain és un contenidor d'sprites. És paregut a la classe Group.
# Com en la classe Group, la classe RenderPlain proporciona els mètodes update() i draw().
# El mètode update() crida als mètodes update() de tots els sprites. Hem d'implemetar el mètode
#   update() en tots els sprites.
# El mètode draw() dibuixa sobre la Surface que li passem els sprites utilitzant els atributs image i rect dels sprites,
#
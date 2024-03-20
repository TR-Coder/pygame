import pygame as pg

# La col·lisió entre un un sprite i un grup d'sprites es fa amb:
# sprite.spritecollide(), sprite.groupcollide() i sprite.spritecollideany().
# En estos mètodes, l'argument 'collided' permet especificar l'algoritme de col·lisió. 'collided' és una funció callback que
# s'utilitza per a calcular si 2 sprites estan col·lidint. Podem utilitzar:  collide_rect, collide_rect_ratio, collide_circle, collide_circle_ratio, collide_mask.


Coord_ = tuple[int,int]
Surface_ = pg.Surface
Rect_ = pg.Rect
Color_ = tuple[int,int,int]

pg.init()

WHITE:Color_ = (255,255,255)
RED:Color_ = (255,0,0)
GREEN:Color_ = (0,255,0)

window:Surface_ = pg.display.set_mode((250, 250))
xy_center:Coord_ = window.get_rect().center

class Circle(pg.sprite.Sprite):
    def __init__(self, color:Color_) -> None:
        super().__init__()
        # Provar a llevar el pg.SRCALPHA
        self.image = pg.Surface((80, 80), pg.SRCALPHA)
        pg.draw.circle(self.image, color, center=(40, 40), radius=40)
        self.rect = pg.Rect(*xy_center, 0, 0).inflate(80,80)


sprite1 = Circle(color=RED)
sprite2 = Circle(color=GREEN)

all_group = pg.sprite.Group([sprite2, sprite1])
test_group = pg.sprite.Group(sprite2)

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    # Col·loca el centre de sprite1 en el punter del ratolí.
    sprite1.rect.center = pg.mouse.get_pos()
    window.fill('black')
    collide_list:list[Circle] = pg.sprite.spritecollide(sprite1, test_group, False)

    all_group.draw(window)

    for sprite in collide_list:
        pg.draw.circle(window, WHITE, sprite.rect.center, sprite.rect.width // 2, 5)

    pg.display.flip()

pg.quit()
exit()
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

class Rectangle(pg.sprite.Sprite):
    def __init__(self, color:Color_) -> None:
        super().__init__()
        self.image = pg.Surface((75, 75))
        self.image.fill(color)
        self.rect = pg.Rect(*xy_center, 0, 0).inflate(75, 75)


sprite1 = Rectangle(color=RED)
sprite2 = Rectangle(color=GREEN)

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

    # sprite.spritecollide(): Find sprites in a group that intersect another sprite.
    # Return a list containing all Sprites in a Group that intersect with another Sprite.
    # Intersection is determined by comparing the Sprite.rect attribute of each Sprite.
    # The dokill argument is a bool. If set to True, all Sprites that collide will be removed from the Group.
    # The collided argument is a callback function used to calculate if two sprites are colliding. it should take two sprites as values,
    # and return a bool value indicating if they are colliding. If collided is not passed, all sprites must have a "rect" value, which is
    # a rectangle of the sprite area, which will be used to calculate the collision.
    # collided callables: collide_rect, collide_rect_ratio, collide_circle,collide_circle_ratio, collide_mask
    collide_list:list[Rectangle] = pg.sprite.spritecollide(sprite1, test_group, False)

    all_group.draw(window)

    for sprite in collide_list:
        pg.draw.rect(window, WHITE, sprite.rect, 5, 1)

    pg.display.flip()

pg.quit()
exit()
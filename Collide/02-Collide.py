import pygame as pg

# A provar:
# Podem detectar la col·lisió entre un rectangle i una llista de rectangles amb Rect.collidelist i  Rect.collidelistall.
# També entre un rectangle i un diccionari de rectangles amb Rect.collidedict i pygame.Rect.collidedictall.

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

rect1 = pg.Rect(*xy_center, 0, 0).inflate(75, 75)
rect2 = pg.Rect(0, 0, 75, 75)

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    # Col·loquem rect2 centrat en el punter del ratolí.
    rect2.center = pg.mouse.get_pos()

    # Rect.colliderect() : test if two rectangles overlap. Returns true if any portion of either rectangle overlap (except the top+bottom or left+right edges)
    collide = rect1.colliderect(rect2)
    color = RED if collide else WHITE

    window.fill('black')
    pg.draw.rect(window, color, rect1)
    pg.draw.rect(window, GREEN, rect2, 6, 1)
    pg.display.flip()

pg.quit()
exit()
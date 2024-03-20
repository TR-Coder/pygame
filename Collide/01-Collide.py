#  https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_collision_and_intesection.md

import pygame as pg

# La col·lisió bàsica es fa amb l'objecte pg.Rect
# Es tracta d'una detecció aproximada ja que detecta la col·lisió entre la regió rectangular de 2 objetes.
# Així, encara que la imatge siga d'una pilota, la detecció es fa amb el delimitador rectangular de la pilota.


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
# Rect.inflate() : Returns a new rectangle with the size changed by the given offset. The rectangle remains centered around its current center.
rect:Rect_ = pg.Rect(*xy_center, 0, 0).inflate(100, 100)

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    point = pg.mouse.get_pos()
    # Rect.Collidepoint test if a point is inside a rectangle. Returns true if the given point is inside the rectangle. A point along the right or bottom edge is not considered to be inside the rectangle.
    collide = rect.collidepoint(point)
    color = RED if collide else WHITE

# Surface.fill() : Fill the Surface with a solid color. If no rect argument is given the entire Surface will be filled. The rect argument will limit the fill to a specific area
# The color argument can be either a RGB sequence, a RGBA sequence or a mapped color index. If using RGBA, the Alpha (A part of RGBA) is ignored unless the surface uses per pixel alpha (Surface has the SRCALPHA flag).
    window.fill('black')
    pg.draw.rect(window, color, rect)
    pg.display.flip()

pg.quit()
exit()
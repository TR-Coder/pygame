import pygame as pg
from typing import Tuple

W, H = 600, 400
WxH = (W,H)
FPS = 60
WHITE = pg.Color(255, 255, 255)
BLACK = pg.Color(0, 0, 0)
BLUE = pg.Color(0, 0, 255)

running, playing = True, False
screen = pg.display.set_mode(WxH)       # dimensions de la pantalla
font_name = pg.font.get_default_font()
BG_color = BLACK
clock = pg.time.Clock()
pg.init()


def surface_text(text:str, background_color: pg.Color) -> pg.Surface:
    font:pg.font.Font = pg.font.SysFont('Calibri',40)

    # Covertim el text en una imatge (surface) amb font.render()
    txt_img:pg.Surface = font.render(text, True, WHITE)

    # Posem el text sobre un fons quadrat. Creem una surface i la pintem d'un color.
    aux = txt_img.get_rect()
    
    print(aux.top, aux.left, aux.width, aux.height)
    rect = txt_img.get_rect().inflate(100,100)
    print(rect.top, rect.left, rect.width, rect.height)
    canvas = pg.Surface((rect.width, rect.height))

    canvas.fill(background_color)
 
    # Centrem el txt_img dins de la surface anterior.
    coordinate:pg.Rect = txt_img.get_rect(center=canvas.get_rect().center)

    # Volquem la imatge del text en el fons quadrat.
    canvas.blit(txt_img, coordinate)
    return canvas
     
txt = surface_text(text='Text per pantalla', background_color=BLUE)
rect = txt.get_rect(center=(W/2, H/2))
screen.blit(txt, rect)

running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.update()


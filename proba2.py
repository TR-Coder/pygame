import pygame as pg

W, H = 600, 400
FPS = 60
WHITE = pg.Color(255,255,255)
BLACK = pg.Color(0,0,0)
BLUE = pg.Color(0,0,255)

screen = pg.display.set_mode((W,H))
BG_color = BLUE
clock = pg.time.Clock()
pg.init()

font:pg.font.Font = pg.font.SysFont('Calibri',40)

txt:pg.Surface = font.render('Hola què tal?', True, WHITE)
txt_rect = txt.get_rect()

img_bg = pg.Surface((txt_rect.width + 250,txt_rect.height + 50))
img_bg.fill(BG_color)

txt_rect.center = img_bg.get_rect().center
img_bg.blit(txt, txt_rect)

img_bg_rect = img_bg.get_rect()
img_bg_rect.center = (W//2, H//2)
screen.blit(img_bg, img_bg_rect)

run = True
while run:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    pg.display.update()


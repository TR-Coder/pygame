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

# txt_rect = txt.get_rect().inflate(250,50)
# bg = pg.Surface((txt_rect.width,txt_rect.height))
txt_rect = txt.get_rect()
bg = pg.Surface((txt_rect.width+250,txt_rect.height+50))
bg.fill(BG_color)
bg_rect = bg.get_rect()

# txt_rect = txt.get_rect(center=bg.get_rect().center)
txt_rect.center = bg_rect.center
bg.blit(txt, txt_rect)

bg_rect.center = (W//2, H//2)
screen.blit(bg, bg_rect)

run = True
while run:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    pg.display.update()


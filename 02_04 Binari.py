import pygame as pg

W,H = 600, 300
FPS = 60

WHITE = pg.Color(255,255,255)
BLAU = pg.Color(0,0,255)
BLACK = pg.Color(0,0,0)

screen = pg.display.set_mode((W,H))
clock = pg.time.Clock()
pg.init()

font:pg.font.Font = pg.font.SysFont('Calibri',40)
binari = list('00000000')
decimal:int = 0

# Dividim el W en len(number)+2 parts. El 2 es per a deixar un espai a dreta i esquerra
rects:list[pg.Rect] = []
number_width = W // (len(binari)+2)
x, y = 0, 0
for _ in range(len(binari)):
    x += number_width
    rects.append(pg.Rect(x,y,number_width,H//3))


def draw_binari(number) -> pg.Surface:
    surface = pg.Surface((W,H//3))
    for i, rect in enumerate(rects):
        text = font.render(str(number[i]), True, WHITE)
        text_rect = text.get_rect(center=rect.center)
        pg.draw.rect(surface,WHITE,rects[i],1)
        surface.blit(text, text_rect)

    pg.draw.rect(surface,WHITE,surface.get_rect(),1)
    return surface

def draw_decimal(decimal:int) -> pg.Surface:
    surface = pg.Surface((W,H//3))
    text = font.render(str(decimal), True, WHITE)
    text_rect = text.get_rect(center=(W//2,H//6))
    surface.blit(text, text_rect)
    return surface


def get_number_clicked(point: tuple[float,float]) ->tuple[int,bool]:
    for i,rect in enumerate(rects):
        if rect.collidepoint(point):
            return i,True
    return -1,False


run = True
while run:
    clock.tick(FPS)
    screen.fill(BLACK)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            i,ok = get_number_clicked(event.pos)
            if ok:
                binari[i] = '0' if binari[i]=='1' else '1'
                decimal = int(''.join(binari), 2)
    
    binari_surface = draw_binari(binari)
    screen.blit(binari_surface,(0,0))
    decimal_surface = draw_decimal(decimal)
    screen.blit(decimal_surface,(0,H//3))
    pg.display.update()




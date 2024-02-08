import pygame as pg

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

class MenuOption():
    def __init__(self, text:str, bg_color: pg.Color|None = None) -> None:
        self.text = text
        self.bg_color = bg_color
        self.clicked = False

    def draw(self, x:int, y:int) -> None:
        # Covertim el text en una imatge (surface) amb font.render()
        font = pg.font.Font('font/Workbench-Regular-VariableFont_BLED,SCAN.ttf', 40)
        txt:pg.Surface = font.render(self.text, True, WHITE)

        # Posarem el text sobre una surface quadrada (box).
        # Obtenim el rectangle que ocupa txt i el fem un poc més gran amb inflate.
        rect = txt.get_rect().inflate(50,10)
        box = pg.Surface((rect.width, rect.height))

        # Calculem les coordenades de box respecte la finestra.
        rect_box = box.get_rect(center=(x, y))

        pos = pg.mouse.get_pos()
        if rect_box.collidepoint(pos) and self.bg_color:
            font = pg.font.Font('font/Workbench-Regular-VariableFont_BLED,SCAN.ttf', 45)
            if pg.mouse.get_pressed()[0] == 1:
                txt = font.render(self.text, True, BLACK)
                box.fill(WHITE)
                self.clicked = True
            if pg.mouse.get_pressed()[0] == 0:
                txt = font.render(self.text, True, WHITE)
                box.fill(self.bg_color)
                self.clicked = False
                if self.clicked:
                    print(self.text)

        # Volquem la imatge del text en el fons quadrat.
        rect_center:pg.Rect = txt.get_rect(center=box.get_rect().center)
        box.blit(txt, rect_center)

        screen.blit(box, rect_box)

menu_option_1 = MenuOption(text='MENÚ')
menu_option_2 = MenuOption(text='- Opció 1 -', bg_color=BLUE)
menu_option_3 = MenuOption(text='- Opció 2 -', bg_color=BLUE)

running = True
while running:
    clock.tick(FPS)

    y = H // 6
    menu_option_1.draw(W//2, y)
    y += 60
    menu_option_2.draw(W//2, y)
    y += 60
    menu_option_3.draw(W//2, y)


    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.flip()

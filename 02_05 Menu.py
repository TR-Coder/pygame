import pygame as pg

W, H = 600,400
FPS = 60
WHITE = pg.Color(255,255,255)
BLACK = pg.Color(0,0,0)
BLUE  = pg.Color(0,0,255)

screen = pg.display.set_mode((W,H))
clock = pg.time.Clock()
pg.init()

menu:list[str] = [' File ', ' Selection ', ' Edit ', ' View ']
submenu: list[list[str]] = [
    ['New text file', 'New file', 'New windows','open file','open folder','Save'],
    ['Select all', 'Expand selection', 'Shrink slection','Copy Line up'],
    ['Undo', 'Redo', 'Cut','Copy','Paste','Find','Replace'],
    ['Command palette','Open view','Appereance','Editor layout']
]
mouse_button_clicked = False

class MainMenu():
    def __init__(self, menu:list[str]) -> None:
        self.menu = menu
        self.font = pg.font.Font('font/Workbench-Regular-VariableFont_BLED,SCAN.ttf', 30)
        self.menu_box_list:list[pg.Rect] = []
        self.menu_box = None
        self.option_selected:None|int = None    # Indica la opció sobre la que hem fet click amb el ratolí.
        self.index:None|int = None              # Indica la opció sobre la que està el ratolí.
        self.clicked = False                    # Commuta entre False i True quan fem click estant sobre qualsevol opció del menú.

    
    def draw(self) -> None:
        # Pintar com a fons del menú un requadre de color blanc:
        #   El requadre ocuparà tot l'ample (W) de la pantalla
        #   L'alçaria serà l'alçaria de la font (get_height) per un factor d'escala (1.75)
        font_height = self.font.get_height()
        print(font_height * 1.75)
        surface = pg.Surface((W,font_height * 1.75))
        surface.fill(WHITE)
        screen.blit(surface, (0,0))
        self.menu_box = surface.get_rect()

        # Pintem les opcions del menú dins del requadre
        lletra_width, lletra_height = self.font.size('M')   # Separació (em) entre les paraules del menú.
        delta:int = lletra_width//2                         # delta indica la posició x inicial de cada opció del menú.

        for i, option in enumerate(self.menu):
            txt:pg.Surface = self.font.render(option, True, BLACK)
            if (self.index is not None) and (i == self.index):
                txt = self.font.render(option, True, BLUE)
            txt_box:pg.Rect = txt.get_rect()
            txt_box.centery = self.menu_box.centery
            txt_box.x += delta
            screen.blit(txt, txt_box)
            self.menu_box_list.append(txt_box)
            pg.draw.rect(screen,BLUE,txt_box,1)
            delta += txt_box.width

        # Si hem clicat sobre alguna opció del menú mostre el seu submenú.
        if self.clicked:
            self.draw_submenu(self.index)



    def draw_submenu(self, index: int):
        print(f'Mostrar menú {self.index}')
        # Pintar com a fons del menú un requadre de color blanc:
        max_number_of_characters = max(len(cadena) for cadena in submenu[index])
        max_width, font_height = self.font.size("M" * max_number_of_characters)
        surface = pg.Surface((max_width,font_height * len(submenu[index])))
        surface.fill(BLUE)
        x = self.menu_box_list[index].left
        screen.blit(surface, (x,self.menu_box_list[index].bottom))

        # surface_box = surface.get_rect()
        # delta:int = int(font_height*1.75)
        delta:int = self.menu_box.bottom

        for i, option in enumerate(submenu[index]):
            txt:pg.Surface = self.font.render(option, True, WHITE)
            # if (self.index is not None) and (i == self.index):
            #     txt = self.font.render(option, True, BLUE)
            txt_box:pg.Rect = txt.get_rect()
            txt_box.x = x
            txt_box.y += delta
            screen.blit(txt, txt_box)
            self.menu_box_list.append(txt_box)
            pg.draw.rect(screen,BLUE,txt_box,1)
            delta += font_height 
    
    def collidepoint(self, point:tuple[int,int], rectangles:list[pg.Rect]) -> tuple[int,bool]:
        for i, rect in enumerate(rectangles):
            if rect.collidepoint(point):
                return i,True
        return -1,False
    
    # Quan el ratolí està sobre alguna de les opcions del menú principal anotem el seu index.
    # Esté index servirà quan pintem el menú per a canviar el seu color i ressaltar l'opció.
    # Anotem si hem fet click amb el ratolí (servirà per mostrar o ocultar submenús).
    def get_selected_option(self):
        mouse_position:tuple[int,int] = pg.mouse.get_pos()                         # type: ignore
        index, mouse_over_menu = self.collidepoint(mouse_position, self.menu_box_list)
        if mouse_over_menu:
            self.index = index
            if mouse_button_clicked:
                self.clicked = not self.clicked
        else:
            # self.index = None
            if mouse_button_clicked:
                # hem de mirar si hem fet clic sobre alguna opcio d'un submenú.
                self.clicked = False


    # Si estem sobre una opció del menú principal.
    #   Ressaltar esta opció del menú.
    # Si hem fet click sobre una opcíó del menú.
    #   Si els submenús estan actius desactivar-los sinó activar-los.

# Crear background
bg = pg.Surface(screen.get_size()).convert()
bg.fill(BLACK)
main_menu = MainMenu(menu)

run = True
while run:
    clock.tick(FPS)

    screen.blit(bg, (0,0))
    main_menu.draw()
    main_menu.get_selected_option()

    mouse_button_clicked = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_button_clicked = True

    pg.display.update()
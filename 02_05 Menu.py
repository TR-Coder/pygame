import pygame as pg
from dataclasses import dataclass
from typing import Optional

W, H = 800,600
FPS = 60
WHITE = pg.Color(255,255,255)
BLACK = pg.Color(0,0,0)
BLUE  = pg.Color(0,0,255)
RED   = pg.Color(255,0,0)

clock = pg.time.Clock()
pg.init()


# -------------------------------------------------------------------------------------------------------

@dataclass
class Option:
    text: str
    rect: pg.Rect
    surface_off: pg.Surface
    surface_on: pg.Surface
    submenu: Optional['Submenu'] = None

# -------------------------------------------------------------------------------------------------------

class Menu():
    def __init__(self, W: int, menu_items:list[str], submenu_items: list[list[str]]) -> None:
        self.menu_items = menu_items
        self.submenu_items = submenu_items

        self.font = pg.font.Font('font/Workbench-Regular-VariableFont_BLED,SCAN.ttf', 30)
        self.font_width, self.font_height = self.font.size('M')
        
        self.bg = pg.Surface((W,self.font_height * 1.75))   # El fons (bg) del menú és un requadre blanc W x l'alçaria de la font (font_height) per 
        self.bg.fill(WHITE)                                 # un factor d'escala (1.75) per a crear un espai per damunt i avall.
        self.bg_rect:pg.Rect = self.bg.get_rect()

        self.options:list[Option] = self.generate_menu_options()
        self.options_rect:list[pg.Rect] = [item.rect for item in self.options]      # Ho extraem per rapidesa

        self.index_menu:None|int = None         # Indica la opció del menú activa.
        self.index_submenu:None|int = None      # Indica la opció del submenú activa.
        self.submenu_activated = False          # Submenú desplegat


    def generate_menu_options(self) -> list:
        '''Generem (que no pintar en screen) el menú principal. Omplim un objecte Option per cada item de menú.
        '''       
        option:list[Option] = []
        initial_space = self.font_width//2                              # Espai inicial abans de la primera opció del menú.
        delta_x:int =  initial_space                                    # Posició x inicial de que cada item del menú.

        for i, txt in enumerate(self.menu_items):                       # Generem un Option per cada item del menú.
            surface_off:pg.Surface = self.font.render(txt, True, BLACK) # Imatge d'un item no seleccionat.
            surface_on :pg.Surface = self.font.render(txt, True, BLUE)  # Imatge d'un item selecionat.
            rect:pg.Rect = surface_off.get_rect()
            rect.x = delta_x                        # x de l'item
            rect.centery = self.bg_rect.centery     # y de l'item. Centrem els items verticalment dins del bg del menú.  

            x, y = rect.x, rect.bottom      # Coordenades del submenú
            submenu = Submenu(x, y, self.submenu_items[i]) if self.submenu_items[i] else None    # Creem els submenús. None si no hi ha items.

            option.append(Option(txt, rect, surface_off, surface_on, submenu))      # Generem un option i l'afegim a la llista d'Option del menu.
            self.bg.blit(surface_off, rect)                                         # Anem afegint al bg del menú els items que anem generant.
            delta_x += rect.width

        return option 


    def draw(self, screen:pg.Surface, mouse_clicked:bool) -> tuple[bool,int|None,int|None]:
        '''Dibuxem sobre la pantalla (screen) el menú. Accedim a les imatges que hem creat a l'inicialitzar la classe i que tenim en la list de Option.
           Passem per paràmetres la pantalla i la pulsació del ratolí per a fer la classe independent del programa principal.
        '''
        screen.blit(self.bg, (0,0))
        mouse_is_over_menu, index_menu = self.is_mouse_over_menu()
        if mouse_is_over_menu:
            if mouse_clicked:                                           # Si cliquem sobre un item...
                self.submenu_activated = not self.submenu_activated     # ...és que volem mostrar o ocultar el seu submenú. 
            self.index_menu = index_menu
            self.index_submenu = None 
            item = self.options[index_menu] 
            img = item.surface_on                   # Imatge 'on' de l'item sobre el que estem.
            img_rect = item.rect
            screen.blit(img, img_rect)              # Repintem a 'on' l'item del menú en la pantalla.

        mouse_is_over_submenu = False
        if self.submenu_activated and self.index_menu is not None and (submenu := self.options[self.index_menu].submenu) is not None:
            mouse_is_over_submenu, index_submenu = self.is_mouse_over_submenu(submenu)
         
            submenu.draw(screen)                                        # ... pintem el submenú sobre la pantalla.

            if mouse_is_over_submenu:                                   # Si el ratolí està sobre l'item d'un submenú. 
                self.index_submenu = index_submenu   
                img = submenu.submenu[index_submenu].surface_on         # Imatge 'on' de l'item sobre el que estem.
                img_rect = submenu.submenu[index_submenu].rect
                screen.blit(img, img_rect)                              # Repintem a 'on' l'item del menú en la pantalla.
                if mouse_clicked:                                       
                    index_menu = self.index_menu
                    self.index_menu = None              # Tanquem el menú
                    self.index_submenu = None
                    self.submenu_activated = False
                    return True, index_menu, index_submenu
        
        if not mouse_is_over_menu and not mouse_is_over_submenu and mouse_clicked:
            self.index_menu = None                  # Tanquem el menú
            self.index_submenu = None
            self.submenu_activated = False 

        return False,None,None


    def is_mouse_over_menu(self) -> tuple[bool,int]:
        mouse_position:tuple[int,int] = pg.mouse.get_pos()  
        if self.bg_rect.collidepoint(mouse_position):                   # Comprovem si el ratolí està sobre el menú principal...
            for i,rect in enumerate(self.options_rect):                 # ...i sobren quin item està (index_menu).
                if rect.collidepoint(mouse_position):
                    return True, i
        return False, -1
      
    def is_mouse_over_submenu(self, submenu:'Submenu') -> tuple[bool,int]:
        mouse_position:tuple[int,int] = pg.mouse.get_pos() 
        if submenu.bg_rect and submenu.bg_rect.collidepoint(mouse_position):     # Comprovem si el ratolí està sobre el submenú desplegat...
            for i,rect in enumerate(submenu.submenu_rect_list):
                if rect.collidepoint(mouse_position):
                    return True, i
        return False, -1

# -------------------------------------------------------------------------------------------------------

class Submenu():
    def __init__(self, x:int, y:int, submenu_items:list[str]) -> None:
        self.x = x
        self.y = y
        self.submenu_items = submenu_items      
        self.font = pg.font.Font('font/Workbench-Regular-VariableFont_BLED,SCAN.ttf', 30)
        self.font_width, self.font_height = self.font.size('M')
        self.line_spacing = 8

        max_number_of_characters = max(len(cadena) for cadena in self.submenu_items) + 2    # Afegim 1 espai a l'inici i 1 al final. Visualment queda millor.
        w = self.font_width * max_number_of_characters
        h = self.line_spacing + (self.font_height + self.line_spacing) * len(self.submenu_items)

        self.bg = pg.Surface((w,h))      # Dibuixem el fons del menú
        self.bg.fill(BLUE)
        self.bg_rect = self.bg.get_rect()
        self.bg_rect.topleft = (self.x,self.y)
        self.submenu:list[Option] = self.generate_submenu_options()
        self.submenu_rect_list = [item.rect for item in self.submenu]           # Ho extraem per rapidesa

    def generate_submenu_options(self) -> list:
        '''Generem (que no pintar en screen) el menú principal. Omplim l'estructura de dades class Option per cada punt de menú'''
        menu:list[Option] = []
        delta_y = 0
        for i, txt in enumerate(self.submenu_items):
            surface_off: pg.Surface = self.font.render(txt, True, WHITE)
            surface_on: pg.Surface = self.font.render(txt, True, RED)
            rect:pg.Rect = surface_off.get_rect()
            rect.x = self.font_width                # espai inicial
            rect.y += delta_y + self.line_spacing
            self.bg.blit(surface_off, rect)
            rect.x += self.x
            rect.y += self.y
            menu.append(Option(txt, rect, surface_off,surface_on,None))

            delta_y += self.font_height + self.line_spacing        
            
        return menu
    
    def draw(self, screen:pg.Surface) -> None:
        screen.blit(self.bg, (self.x, self.y))

# -------------------------------------------------------------------------------------------------------

# Crear background
screen_ = pg.display.set_mode((W,H))
bg = pg.Surface(screen_.get_size()).convert()
bg.fill(BLACK)

menu_options:list[str] = [' File ', ' Selection ', ' Edit ', ' View ', ' Terminal ']             # Text de les opción del menú.
submenu_options: list[list[str]] = [
    ['New text file', 'New file', 'New windows','open file','open folder','Save'],
    ['Select all', 'Expand selection', 'Shrink slection','Copy Line up'],
    ['Undo', 'Redo', 'Cut','Copy','Paste','Find','Replace'],
    [], # Sense submenú
    ['Command palette','Open view','Appereance','Editor layout']
]
main_menu = Menu(W, menu_options, submenu_options)

mouse_button_clicked = False
run = True
while run:
    clock.tick(FPS)

    screen_.blit(bg, (0,0))
    menu_option_selected, index, subindex = main_menu.draw(screen_, mouse_button_clicked)
    if menu_option_selected:
        print(index,subindex)
        
    mouse_button_clicked = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_button_clicked = True

    pg.display.update()
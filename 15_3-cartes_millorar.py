#
#       ████████╗██████╗        ██████╗ ██████╗ ██████╗ ███████╗██████╗ 
#       ╚══██╔══╝██╔══██╗      ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗
#          ██║   ██████╔╝█████╗██║     ██║   ██║██║  ██║█████╗  ██████╔╝
#          ██║   ██╔══██╗╚════╝██║     ██║   ██║██║  ██║██╔══╝  ██╔══██╗
#          ██║   ██║  ██║      ╚██████╗╚██████╔╝██████╔╝███████╗██║  ██║
#          ╚═╝   ╚═╝  ╚═╝       ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
#
from __future__ import annotations
import pygame as pg
import os
import random
import math

SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 900
FPS = 60

# -----------------------------------------------------------------------------------------------

pg.init()
font = pg.font.SysFont('Bauhaus 93', 60)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pg.Surface(screen.get_size())
# bg.fill((170, 238, 187))
clock = pg.time.Clock()

working_directory = os.path.split(os.path.abspath(__file__))[0]
assets_directory = os.path.join(working_directory, 'data')
card_images_list: list[pg.Surface] = []

# -----------------------------------------------------------------------------------------------
class Group(pg.sprite.Sprite):
    def __init__(self) -> None:
        self.cards:list[Card] = []
        self.rect:pg.Rect = pg.Rect(0,0,0,0)
        self.selected = False

    def add_cards_from(self, group) -> None:
        '''Afegix a este grup les cartes del grup que li passem'''
        y_init = self.cards[-1].rect.y          # Posem les noves cartes a l'altura de l'última carta del grup...
        x_init = self.cards[-1].rect.x + 30     # ...i un poc a la dreta.
        for card in group.cards:
            self.cards.append(card)
            card.group = self                   # Les cartes canvien de grup
            card.rect.y = y_init
            card.rect.x = x_init
            x_init += 30
        self.update_rect()
        group.cards = []                        # El grup d'on venen les cartes es buida.
        group.rect = None  

    def update_rect(self) -> None:
        ''' Crea un rect que engloba tots els rect del group.'''    
        rects:list[pg.Rect] = [card.rect for card in self.cards]
        self.rect = rects[0].unionall(rects) if rects else pg.Rect(0,0,0,0)
    
    def append(self, card:'Card') -> None:
        self.cards.append(card)
        self.update_rect()

    def __change_group(self) -> None:
        for card in self.cards:
            card.group = self

    def update_cards(self, cards: list[Card]) -> None:
        self.cards = cards
        self.__change_group()
        self.update_rect()
    
    
    def unselect_all_cards(self) -> None:
        for card in self.cards:
            card.selected = False

    def split(self, card:Card, groups: Groups) -> Group:     
        '''Dividix el grup en dos. Deixa en este grup les cartes per davall de card i retorna
        el altre grup amb les cartes amb card i per damunt d'ella'''       
        index = self.cards.index(card)
        new_cards = self.cards[index:]

        self.cards = self.cards[:index]
        self.update_rect()
        self.unselect_all_cards()

        group_number = new_cards[0].number - 1
        selected_group = groups.list[group_number]
        selected_group.update_cards(new_cards)

        return selected_group
    
    def trying_split(self, mouse_y: int) -> bool:
        '''Considerem que volem separar un grup de cartes en dos quan hen clitat en la part superior de les cartes'''
        return (mouse_y - self.rect.y < 50) 
    

    def put_on_top_level(self, sprites: pg.sprite.LayeredUpdates) -> None:
        '''Col·loca en les capes superiors les cartes del grup a què pertany Card.
        La resta de cartes baixen de nivell per a fer lloc.
        '''
        n = len(self.cards)
        new_layer = 14
        for sprite in reversed(list(sprites)):
            if sprite in self.cards:
                sprites.change_layer(sprite, new_layer)
                new_layer -= 1
            else:
                sprites.change_layer(sprite, sprite._layer-n)

     
    def __str__(self) -> str:
        s:str  = ''
        for card in self.cards:
            s += str(card.number) + ' '
        return s
    
    
# -----------------------------------------------------------------------------------------------
class Groups(pg.sprite.Sprite):
    def __init__(self) -> None:
        self.list: list[Group] = []
    
    def __str__(self) -> str:
        s = ''
        for i,group in enumerate(self.list):
            s += '  '+f'{i+1}=>'
            for card in group.cards:
                s += f'{card.number},'
        return s
    
    def __distance(self, rect1: pg.Rect|None, rect2: pg.Rect|None) -> int:
        if not rect1 or not rect2:
            return 1000
        x1, y1 = rect1.topleft
        x2, y2 = rect2.topleft
        dx = x2 - x1
        dy = y2 - y1
        return int(math.sqrt(dx**2 + dy**2))

    def __closest_grup(self, group:Group, groups:list[Group]) -> Group:
        distances = [self.__distance(group.rect,g.rect) for g in groups]
        minim = min(enumerate(distances), key=lambda x: x[1])[0]
        return groups[minim]

    def search_nearest_group_to(self, group: Group) -> Group|None:
        '''Busca d'entre tots els grups aquell que està més a prop del grup que li passem'''
        groups_collide_with_group:list[Group] = [g for g in self.list if g!=group and g.rect and group.rect.colliderect(g.rect)]
        return self.__closest_grup(group, groups_collide_with_group) if groups_collide_with_group else None
    
      
# -----------------------------------------------------------------------------------------------
class Card(pg.sprite.Sprite):
    def __init__(self, i:int, group: Group, *groups: pg.sprite.Group) -> None:
        super().__init__(*groups)
        self.image = card_images_list[i]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.random_coordenates()
        self.number = i+1
        self.x_relative = 0
        self.y_relative = 0
        self._layer = i
        self.selected = False
        self.group = group
        group.append(self)

    def random_coordenates(self) -> tuple[int,int]:
        x = random.randint(0, SCREEN_WIDTH-self.rect.width)
        y = random.randint(0, SCREEN_HEIGHT-self.rect.height)
        return x,y
    

    def update(self, *args) -> None:
        selected_group = args[0]
        if selected_group and self in selected_group.cards:
            if not self.selected:
                self.selected = True
                x, y = pg.mouse.get_pos()
                self.x_relative = x - self.rect.topleft[0]
                self.y_relative = y - self.rect.topleft[1]
            else:
                x, y = pg.mouse.get_pos()
                self.rect.topleft = x - self.x_relative, y - self.y_relative        


# -----------------------------------------------------------------------------------------------
def load_card_images_list(name:str, scale:float = 1):
    img_path:str = os.path.join(assets_directory, name)
    card_image:pg.Surface = pg.image.load(img_path).convert_alpha()   # convert_alpha() fa que funcione la transparència del .png
    size:tuple[int, int] = card_image.get_size()
    width, height = size[0]/7, size[1]/2
    for i in range(2):
        for j in range(7):
            image = pg.Surface((width, height))
            image.blit(card_image, (0, 0), ((j * width), i*height, width, height))
            image = pg.transform.scale(image, (width * scale, height * scale))         
            card_images_list.append(image)
   

# -----------------------------------------------------------------------------------------------
def draw_background() -> None:
    screen.blit(bg, (0, 0))

# -----------------------------------------------------------------------------------------------
def info(selected_group: Group, selected_card: Card, groups: Groups) -> None:
    print()
    print(f"Grup seleccionat: {selected_group}")
    print(f"Carta seleccionada: {selected_card.number}")
    print(groups)

       
# ==============================================================================================
# Les estructures de dades són:
#   - sprites_group: llista de Cards
#   - Group: un group és una agrupació de cartes que es mouen juntes.
#   - Groups: conjunt de tots el groups. 
#   Tenim 14 imatges. Tenim 14 Groups inicialment formats per una única carta.
#   El programa treballa amb grups i no amb cards individuals.
#   Quan unim dos groups pasem les cards d'un grup a un altre grup. El mateix quan els separem.
#   Els groups no s'esborren, encara que podem tindre groups buits on la seua llista de cards està buida.
# ==============================================================================================
def main() -> None:
    pg.display.set_caption('Card Game')
    load_card_images_list('cartes.png', 0.5)

    selected_group: Group|None = None       # Grup de cartes seleccionat.
    selected_card: Card|None = None         # Carta seleccionada (dins del grup de cartes seleccionat).
    nearest_group: Group|None = None        # Grup de cartes més a prop del grup de cartes seleccionat:
                                            #   És necessari perquè el grup seleccionat podria solapar-se al mateix temps
                                            #   amb més d'un grup de cartes. La idea és que s'unisca al que està més a prop.
    draging = False                         # A True quan estinc arrosegant.
    is_splitting = False                       # A True quan estic separant un grup de cartes en dos parts.


    sprites = pg.sprite.LayeredUpdates()    # type: ignore
                                            # LayeredUpdate és com pg.Group però treballa amb capes. Propietat _layer de l'sprite.
    groups = Groups()

    for i in range(14):
        group = Group()
        card = Card(i, group)
        sprites.add(card)
        groups.list.append(group)           # Inicialment creem 14 grups formats per una carta.
                                            # Cada grup està és una capa. El grup 0 es la capa inferior, la 14 en la superior.
 
    run = True
    while run:
        clock.tick(FPS)

        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:               # Clic principal ratolí
                    mouse_x, mouse_y = event.pos
                    for card in reversed(list(sprites)):                        # Recorrem les capes de cartes de la capa superior a l'inferior...
                        if card.rect.collidepoint(mouse_x, mouse_y):            # ...així, si estan solapades, seleccionarem la que està per damunt.
                            selected_card, selected_group = card, card.group    # Considerem que volem separar un grup de cartes en dos quan estem clitant sobre la part superior de les cartes.
                            is_splitting = selected_group.trying_split(mouse_y)
                            info(selected_group, selected_card, groups)
                            selected_group.put_on_top_level(sprites)       # Col·loca en les capes superiors les cartes del grup seleccionat.
                            draging = True
                            break

            elif event.type == pg.MOUSEBUTTONUP:
                if selected_group:
                    selected_group.selected = False
                    selected_group.unselect_all_cards()
                    if nearest_group:
                        print(f'Grups més pròxim {nearest_group}')
                        nearest_group.add_cards_from(selected_group)
                selected_card, selected_group, nearest_group = None, None, None
                draging, is_splitting = False, False

            elif event.type == pg.MOUSEMOTION:
                if draging and selected_group:
                    if is_splitting and selected_card:
                        # Si estem dividint un grup separem les cartes per grup i retornem el grup que estem separant,
                        selected_group = selected_group.split(selected_card, groups)
                        is_splitting = False
                    else:
                        selected_group.update_rect()
                        nearest_group = groups.search_nearest_group_to(selected_group)

            elif event.type == pg.QUIT:
                run = False

        draw_background()

        sprites.update(selected_group)
        sprites.draw(screen)

        # if nearest_group:
        #     pg.draw.rect(screen, (0, 0, 255), nearest_group.rect, 2)

        # if selected_group:
        #     pg.draw.rect(screen, (0, 0, 255), selected_group.rect, 2)
            

        pg.display.update()
    
    pg.quit()

if __name__ == '__main__':
    main()
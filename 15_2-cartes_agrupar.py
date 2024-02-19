
from __future__ import annotations
import pygame as pg
import os
import random
import math

SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 900
FPS = 60
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

# -----------------------------------------------------------------------------------------------

pg.init()
font = pg.font.SysFont('Bauhaus 93', 60)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pg.Surface(screen.get_size())
bg.fill((170, 238, 187))
clock = pg.time.Clock()

working_directory = os.path.split(os.path.abspath(__file__))[0]
assets_directory = os.path.join(working_directory, 'data')
card_images_list: list[pg.Surface] = []

# -----------------------------------------------------------------------------------------------
class Group(pg.sprite.Sprite):
    def __init__(self) -> None:
        self.cards: list[Card] = []
        self.rect: pg.Rect = self.join_rectangles()
        self.selected = False

    def move_to(self, group) -> None:
        '''Afegix a este grup les cartes del grup que li passem'''
        x_init = self.cards[-1].rect.x + 30
        y_init = self.cards[-1].rect.y
        for card in group.cards:
            self.cards.append(card)
            card.group = self
            card.rect.y = y_init
            card.rect.x = x_init
            x_init += 30
        group.cards = []
        group.rect = pg.Rect(0,0,0,0)
        self.update_rect()

    def append(self, card:'Card') -> None:
        self.cards.append(card)
        self.rect =  self.join_rectangles()


    def __change_group(self) -> None:
        for card in self.cards:
            card.group = self

    def update(self, cards: list[Card]) -> None:
        self.cards = cards
        self.__change_group()
        self.rect = self.join_rectangles()
        
    def join_rectangles(self) -> pg.Rect:
        ''' Crea un rect que engloba tots els rect del group.'''    
        rects:list[pg.Rect] = [card.rect for card in self.cards]
        return rects[0].unionall(rects) if rects else pg.Rect(0,0,0,0)
    
    def update_rect(self):
        self.rect = self.join_rectangles()
    
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
        selected_group.update(new_cards)

        return selected_group
    
    def trying_split(self, mouse_y: int) -> bool:
        '''Considerem que volem serparar un grup de cartes en dos quan hen clitat en la part superior de les cartes'''
        return (mouse_y - self.rect.y < 50) 
     
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
        groups_collide_with_group:list[Group] = [g for g in self.list if g!=group and group.rect.colliderect(g.rect)]
        return self.__closest_grup(group, groups_collide_with_group) if groups_collide_with_group else None
    
      
# -----------------------------------------------------------------------------------------------
# selected_group: Group|None = None
# -----------------------------------------------------------------------------------------------

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
def draw_score(score:int) -> None:
    pass

# -----------------------------------------------------------------------------------------------
def draw_background() -> None:
    screen.blit(bg, (0, 0))

# -----------------------------------------------------------------------------------------------
def put_on_top_level(sprites_group: pg.sprite.LayeredUpdates, selected_group: Group) -> None:
    '''Col·loca en els nivell superiors totes les cartes del grup a què pertany Card.
       La resta de cartes baixen de nivell per a fer lloc.
    '''
    n = len(selected_group.cards)
    new_layer = 14
    for s in reversed(list(sprites_group)):
        if s in selected_group.cards:
            sprites_group.change_layer(s, new_layer)
            new_layer -= 1
        else:
            sprites_group.change_layer(s, s._layer-n)
        
# ==============================================================================================
def main() -> None:
    selected_group: Group|None = None
    selected_card:Card|None = None
    nearest_group: Group|None = None
    draging = False
    splitting = False

    run = True
    score: int = 0

    pg.display.set_caption('Card Game')
    sprites_group = pg.sprite.LayeredUpdates()      # type: ignore
    load_card_images_list('cartes.png', 0.5)

    groups = Groups()
    for i in range(14):
        group = Group()
        card = Card(i, group)
        sprites_group.add(card)
        groups.list.append(group)
 
    while run:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic principal
                    mouse_x, mouse_y = event.pos
                    for card in reversed(list(sprites_group)):
                        if card.rect.collidepoint(mouse_x, mouse_y):
                            selected_card, selected_group = card, card.group
                            splitting = selected_group.trying_split(mouse_y)
                            print(f"Grup seleccionat {selected_group}")
                            print(f"Carta seleccionada{card.number}")
                            print(groups)
                            if selected_group:
                                put_on_top_level(sprites_group, selected_group)
                            draging = True
                            break
            elif event.type == pg.MOUSEBUTTONUP:
                if selected_group:
                    selected_group.selected = False
                    selected_group.unselect_all_cards()
                    if nearest_group is not None:
                        print(f'Grups més pròxim {nearest_group}')
                        nearest_group.move_to(selected_group)
                selected_group = None
                selected_card = None
                nearest_group = None
                draging = False
                splitting = False
            elif event.type == pg.MOUSEMOTION:
                if draging:
                    if selected_group and draging:
                        if splitting and selected_card:
                            selected_group = selected_group.split(selected_card, groups)
                            splitting = False
                            nearest_group = None
                            print(groups)
                        else:
                            selected_group.update_rect()
                            nearest_group = groups.search_nearest_group_to(selected_group)
            elif event.type == pg.QUIT:
                run = False

        draw_background()
        draw_score(score)

        sprites_group.update(selected_group)
        sprites_group.draw(screen)
        if nearest_group:
            pg.draw.rect(screen, (0, 0, 255), nearest_group.rect, 2)

        # if selected_group:
        #     pg.draw.rect(screen, (0, 0, 255), selected_group.rect, 2)
            

        pg.display.update()
    
    pg.quit()

if __name__ == '__main__':
    main()
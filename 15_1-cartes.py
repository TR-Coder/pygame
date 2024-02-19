
import pygame as pg
import os
import random

SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 900
FPS = 60
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

pg.init()
font = pg.font.SysFont('Bauhaus 93', 60)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pg.Surface(screen.get_size())
bg.fill((170, 238, 187))
clock = pg.time.Clock()

working_directory = os.path.split(os.path.abspath(__file__))[0]
assets_directory = os.path.join(working_directory, 'data')
card_images_list: list[pg.Surface] = []


class Card(pg.sprite.Sprite):
    def __init__(self, i:int,  *groups: pg.sprite.Group):
        super().__init__(*groups)
        self.image = card_images_list[i]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.random_coordenates()
        self.number = i+1
        self.selected = False
        self.x_relative = 0
        self.y_relative = 0
        self._layer = i

    def random_coordenates(self) -> tuple[int,int]:
        x = random.randint(0, SCREEN_WIDTH-self.rect.width)
        y = random.randint(0, SCREEN_HEIGHT-self.rect.height)
        return x,y
    

    def update(self) -> None:
        if selected_card and selected_card.number == self.number:
            if not self.selected:
                self.selected = True
                x, y = pg.mouse.get_pos()
                self.x_relative = x - self.rect.topleft[0]
                self.y_relative = y - self.rect.topleft[1]
            else:
                x, y = pg.mouse.get_pos()
                self.rect.topleft = x - self.x_relative, y - self.y_relative
      
selected_card: Card | None = None

# -----------------------------------------------------------------------------------------------
def load_card_images_list(name:str, scale:int = 1):
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
def layer_reorder(sprite_group: pg.sprite.LayeredUpdates, card: Card) -> None:
    # pos:int = sprite_group.get_layer_of_sprite(sprite)
    for s in reversed(sprite_group.sprites()):
        if s._layer == card._layer:
            sprite_group.change_layer(s, 14)
            return
        sprite_group.change_layer(s, s._layer-1)
        


# ==============================================================================================
def main() -> None:
    global selected_card

    run = True
    score: int = 0

    pg.display.set_caption('Card Game')
    # sprite_group = pg.sprite.OrderedUpdates()      # type: ignore
    sprite_group = pg.sprite.LayeredUpdates()      # type: ignore
    load_card_images_list('cartes.png')

    for i in range(14):
        sprite_group.add(Card(i))

    while run:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic esquerre
                    x, y = event.pos
                    print('----------------')
                    for sprite in reversed(list(sprite_group)):
                        if sprite.rect.collidepoint(x, y):
                            selected_card = sprite
                            layer_reorder(sprite_group,sprite)
                            print(f"Se hizo clic en {sprite.number}")
                            break
            elif event.type == pg.MOUSEBUTTONUP:
                if selected_card:
                    selected_card.selected = False
                selected_card = None
            elif event.type == pg.QUIT:
                run = False

        draw_background()
        draw_score(score)
        sprite_group.update()
        sprite_group.draw(screen)

        pg.display.update()
    
    pg.quit()

if __name__ == '__main__':
    main()
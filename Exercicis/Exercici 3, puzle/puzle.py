from __future__ import annotations
import pygame as pg
from enum import Enum
import components
import glob
import os

W = 925
H = 800
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)

_Group = pg.sprite.Group

# ------------------------------------------------------------------------------------------------------
def clear_screen() -> None:
    screen.blit(bg, (0, 0))

# ------------------------------------------------------------------------------------------------------
def main() -> None:

    
    spain_surface = components.load_image(r'assets/Espanya.png')

    comunities:list[pg.Surface] = components.load_images(r'assets/comunitat*.png')
    spain_surface = comunities[1]

    provinces_group:_Group = pg.sprite.Group()

    main_loop = True
    while main_loop:
        clear_screen()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                main_loop = False
        
        screen.blit(spain_surface, (0,0))
        pg.display.update()

# ------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    directory = os.path.dirname(os.path.abspath(__file__))
    pattern = os.path.join(directory, 'assets/comunitat*.png')
    matching_files = glob.glob(pattern)
    for file in matching_files:
        print(os.path.basename(file), file)

    pg.init()
    screen = pg.display.set_mode((W,H))
    screen_center = screen.get_rect().center
    pg.display.set_caption("Mapa de províncies d'Espanya")
    bg = pg.Surface(screen.get_size())
    bg.fill(WHITE)
    font = pg.font.Font(None, 36)
    main()
    pg.quit()
import pygame as pg
import math
import components

pg.init()

W = 800
H = 450
BLUE = pg.Color(0, 0, 255)

_Group = pg.sprite.Group
_Sprite = pg.sprite.Sprite


screen = pg.display.set_mode((W, H))
pg.display.set_caption('Following mouse')

mouse_x, mouse_y = W/2, H/2
sprite_x, sprite_y = W/2, H/2

class Follower(_Sprite):
        
        




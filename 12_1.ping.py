import pygame as pg
import math
import random
from enum import Enum

pg.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
FPS = 60
BG_COLOR = (50, 25, 25)
WHITE_COLOR = (255, 255, 255)

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Ping Pong')
font = pg.font.SysFont('Bauhaus 93', 40)
clock = pg.time.Clock()
run = True
computer_score = 0
player_score = 0
level = 0

class Paddle():
    pass

def init_game():
    pass


def draw_text(text:str, x:int, y:int):
    img = font.render(text, True, WHITE_COLOR)
    screen.blit(img, (x,y))


def draw_score():
    draw_text(f'Computer: {computer_score}', 50, 10)
    draw_text(f'Player: {player_score}', SCREEN_WIDTH-200, 10)
    draw_text(f'Level: {level}', SCREEN_WIDTH//2 - 50, 10)


def draw_background():
    screen.fill(BG_COLOR)
    pg.draw.line(screen, WHITE_COLOR, (0,50), (SCREEN_WIDTH, 50), 2)
    pg.draw.line(screen, WHITE_COLOR, (0,SCREEN_HEIGHT - 15), (SCREEN_WIDTH, SCREEN_HEIGHT - 15), 2)
    pg.draw.line(screen, WHITE_COLOR, (0,SCREEN_HEIGHT - 15), (SCREEN_WIDTH, SCREEN_HEIGHT - 15), 2)



init_game()

while run:
    clock.tick(FPS)

    draw_background()
    draw_score()
    
    # if game_over:
    #     restart_button.draw()
    #     if restart_button.pressed():
    #         init_game()
    # else:
        
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
           
    pg.display.update()

pg.quit()
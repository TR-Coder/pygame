import pygame
from enum import Enum


class Direction(Enum):
    UP=1,
    RIGHT=2,
    DOWN=3,
    LEFT=4


class Segmet():
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

pygame.init()
screen_witdh = 600
screen_height = 600
diameter = 20

background_color = (255, 200, 150)
segment_inner_color = (57, 175, 25)
segment_outer_color = (100, 100, 200)
red_color = (255, 0, 0)

screen = pygame.display.set_mode((screen_witdh, screen_height))
pygame.display.set_caption('Snake')

direction = Direction.UP
x_init = screen_witdh // 2
y_init = screen_height // 2

s1 = Segmet(x_init, y_init + diameter*0)
s2 = Segmet(x_init, y_init + diameter*1)
s3 = Segmet(x_init, y_init + diameter*2)
s4 = Segmet(x_init, y_init + diameter*3)
snake = [s1,s2,s3,s4]


def draw_segment(s:Segmet, head:bool=False) -> None:
    color = segment_inner_color
    if head:
        color= red_color
    pygame.draw.circle(screen, color, (s.x, s.y), diameter//2 )

wait = 0
run = True
while run:
    screen.fill(background_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != Direction.DOWN:
                direction = Direction.UP
            if event.key == pygame.K_RIGHT and direction != Direction.LEFT:
                direction = Direction.RIGHT
            if event.key == pygame.K_DOWN and direction != Direction.UP:
                direction = Direction.DOWN
            if event.key == pygame.K_LEFT and direction != Direction.RIGHT:
                direction = Direction.LEFT


    if wait > 500:
        wait = 0
        head, *body, tail = snake

        if direction == Direction.UP:
            x = head.x
            y = head.y - diameter
        elif direction == Direction.RIGHT:
            x = head.x + diameter
            y = head.y
        elif direction == Direction.DOWN:
            x = head.x
            y = head.y + diameter
        elif direction == Direction.LEFT:
            x = head.x - diameter
            y = head.y

        new_head = Segmet(x,y)
        snake = [new_head, head, *body]

    wait += 1

    draw_segment(snake[0], head=True)
    for s in snake[1:]:
        draw_segment(s)

    pygame.display.update()

pygame.quit()
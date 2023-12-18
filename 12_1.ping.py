# https://www.youtube.com/watch?v=HdUAUlX9P2Y&list=PLjcN1EyupaQnB9-Ovkisq0Ss-1u0gOAv4&index=3

import pygame as pg
from enum import Enum
import random

pg.init()

SCREEN_WIDTH = 1000 # Don't change
SCREEN_HEIGHT = 500 # Don't change
TOP_MARGIN = 50
BOTTOM_MARGIN = 15
HALF_BOARD_Y = (SCREEN_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN) // 2

RADIUS = 10
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
BG_COLOR = (50, 25, 25)
FPS = 60
SPEED = 5

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Ping Pong')
font = pg.font.SysFont('Bauhaus 93', 60)
clock = pg.time.Clock()
run = True
number_of_players = 2
number_of_bounces = 0

# ==========================================================================================
class Score(Enum):
    NONE=0
    USER1=1
    USER2=2

class Player(Enum):
    USER1=1
    USER2=2

class Direction(Enum):
    LEFT=-1
    RIGHT=1

# ===========================================================================================
def stop():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN :
                return
            
# ===========================================================================================
class Paddle():
    # ------------------------------------------------------------------
    def __init__(self, x:int, y:int, player: Player):
        self.rect = pg.Rect(x, y, 20, 100)
        self.y_increment = 5
        self.player = player
    
    # ------------------------------------------------------------------
    def move(self):
        paddle_below_top_margin = (self.rect.top > TOP_MARGIN + 2)
        paddle_over_bottom_margin = (self.rect.bottom < SCREEN_HEIGHT - BOTTOM_MARGIN)

        key = pg.key.get_pressed()

        if number_of_players == 2:
            key_up = (self.player==Player.USER2 and key[pg.K_UP]) or (self.player==Player.USER1 and key[pg.K_w])
            key_down = (self.player==Player.USER2 and key[pg.K_DOWN]) or (self.player==Player.USER1 and key[pg.K_s])
        else:
            key_up = key[pg.K_UP]
            key_down = key[pg.K_DOWN]

        if key_up and paddle_below_top_margin:
            self.rect.move_ip(0, -1 * self.y_increment)

        if key_down and paddle_over_bottom_margin:
            self.rect.move_ip(0, self.y_increment)

    # ------------------------------------------------------------------
    def draw(self):
        pg.draw.rect(screen, WHITE_COLOR, self.rect)

# ===========================================================================================
class Ball():
    # ------------------------------------------------------------------
    def __init__(self, x:int, y:int, direction: Direction):
        self.rect = pg.Rect(x, y, RADIUS*2, RADIUS*2)
        self.x_increment:float = SPEED * direction.value
        self.y_increment:float = random.choice([-1, 1]) * random.uniform(1.75, 3)
        self.sign = lambda x: 1 if x>=0 else -1

    # ------------------------------------------------------------------
    def move(self) -> Score:
        global level
        global number_of_bounces
        
        ball_hits_top_margin = (self.rect.top < TOP_MARGIN)
        ball_hits_bottom_margin = (self.rect.bottom > SCREEN_HEIGHT - BOTTOM_MARGIN)
        ball_scores_user2 = (self.rect.left < 0)
        ball_scores_user1 = (self.rect.right > SCREEN_WIDTH)

        user1_line_start = (user1_paddle.rect.x + 20, user1_paddle.rect.y + 5)
        user1_line_end = (user1_paddle.rect.x + 20, user1_paddle.rect.y + 95)

        user2_line_start = (user2_paddle.rect.x, user2_paddle.rect.y + 5)
        user2_line_end = (user2_paddle.rect.x, user2_paddle.rect.y + 95)

        ball_hits_any_paddle = self.rect.clipline(user1_line_start, user1_line_end) or self.rect.clipline(user2_line_start, user2_line_end)
        
        pg.draw.line(screen, RED_COLOR, user1_line_start, user1_line_end, 5)
        pg.draw.line(screen, RED_COLOR, user2_line_start, user2_line_end, 5)

        if ball_hits_top_margin or ball_hits_bottom_margin:
            self.y_increment *= -1
        elif ball_hits_any_paddle:
            # change the bounce angle a little randomly
            self.x_increment *= -1
            self.y_increment = self.sign(self.y_increment) * random.uniform(1.5, 2.5)

            # prevent the ball from bouncing inside the paddle
            ball_direction_to_right = (self.x_increment >= 0)
            if ball_direction_to_right:
                if self.rect.x + self.x_increment <= 40:
                    self.rect.x = 41
            else:
                if self.rect.x + 2*RADIUS + self.x_increment>= 960:
                    self.rect.x = 960 - 2*RADIUS

            # increases the level every certain number of bounces
            number_of_bounces += 1
            if number_of_bounces == 2:
                number_of_bounces = 0
                self.x_increment = self.sign(self.x_increment) * (abs(self.x_increment) + 0.25)
                level += 1

        self.rect.x += round(self.x_increment)
        self.rect.y += round(self.y_increment)
        print(self.x_increment)

        if ball_scores_user1:
            return Score.USER1
        elif ball_scores_user2:
            return Score.USER2
        return Score.NONE
        
    # ------------------------------------------------------------------
    def draw(self):
        ball_center = (self.rect.x + RADIUS, self.rect.y + RADIUS)
        pg.draw.circle(screen, WHITE_COLOR, ball_center, RADIUS)

# ===========================================================================================
user2_paddle: Paddle
user1_paddle: Paddle
ball: Ball

playing = False
level = 0
user1_score = 0
user2_score = 0

initial_ball_user2_x = SCREEN_WIDTH - 65
initial_ball_user1_x = 55
initial_ball_y = HALF_BOARD_Y + 50

# ===========================================================================================
def draw_text(text:str, x:int, y:int):
    img = font.render(text, True, WHITE_COLOR)
    screen.blit(img, (x,y))

# ===========================================================================================
def draw_score():
    draw_text(f'user1: {user1_score}', 40, 10)
    draw_text(f'user2: {user2_score}', SCREEN_WIDTH-200, 10)
    draw_text(f'Level: {level}', SCREEN_WIDTH//2 - 50, 10)

# ===========================================================================================
def draw_background():
    screen.fill(BG_COLOR)
    pg.draw.line(screen, WHITE_COLOR, (0,TOP_MARGIN), (SCREEN_WIDTH, TOP_MARGIN), 2)
    pg.draw.line(screen, WHITE_COLOR, (0,SCREEN_HEIGHT - BOTTOM_MARGIN), (SCREEN_WIDTH, SCREEN_HEIGHT - BOTTOM_MARGIN), 2)

# ===========================================================================================
def draw_screen():
    draw_background()
    draw_score()
    user1_paddle.draw()
    user2_paddle.draw()
   
# ===========================================================================================
def init_game(player: Player):
    global user1_paddle
    global user2_paddle
    global ball
    global level
    global playing
    user1_paddle = Paddle(20, HALF_BOARD_Y, Player.USER1)
    user2_paddle = Paddle(SCREEN_WIDTH - 40, HALF_BOARD_Y, Player.USER2)
    level = 0
    playing = False
    if player == Player.USER2:
        ball = Ball(initial_ball_user2_x, initial_ball_y, Direction.LEFT)
    else:
        ball = Ball(initial_ball_user1_x, initial_ball_y, Direction.RIGHT)

# ===========================================================================================
init_game(Player.USER2)

while run:
    clock.tick(FPS)
    draw_screen()

    if playing:
        state = ball.move()
        if state == Score.USER2:
            user2_score += 1
            init_game(Player.USER2)
        elif state == Score.USER1:
            user1_score += 1
            init_game(Player.USER1)
        else:
            ball.draw()

        user2_paddle.move()
        user1_paddle.move()
    else:
        draw_text('press any key', SCREEN_WIDTH//3, HALF_BOARD_Y)
            
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN and not playing:
            playing = True
           
    pg.display.update()

pg.quit()
import pygame as pg
from enum import Enum
import random

W = 1000            # Don't change
H = 500             # Don't change

TOP_MARGIN = 50                                       # We leave room at the top for the score and the level we are at.
BOTTOM_MARGIN = 15                                    # We leave room at the bottom for aesthetic reasons. So that the ball does'nt bounce off the edge of the window.
HALF_BOARD_Y = (H - TOP_MARGIN - BOTTOM_MARGIN) // 2  # Half of the playing field

STARTING_X_BALL_PLAYER_1 = 55
STARTING_X_BALL_PLAYER_2 = W - 65
STATING_Y_BALL = HALF_BOARD_Y + 50

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BG_COLOR = (50, 25, 25)

FPS = 60
SPEED = 5
BALL_RADIUS = 10
NUMBER_OF_PLAYERS = 2


_Group = pg.sprite.Group
_Sprite = pg.sprite.Sprite
_Color = tuple[int,int,int]

# ============================================================================
class Score(Enum):          # It is used to know which player has scored.
    NONE=0
    PLAYER_1=1
    PLAYER_2=2

class Player(Enum):         # Reference to a player
    ONE=1
    TWO=2

class Direction(Enum):      # Ball direction
    LEFT=-1
    RIGHT=1

# ============================================================================
class Paddle(_Sprite):
    def __init__(self, x:int, y:int, player:Player, color:_Color,  group: pg.sprite.Group, width:int=20, height:int=100):
        super().__init__(group)
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.initial_coordinates = (x,y)
        self.width = width
        self.height = height
        self.player = player
        self.y_increment = 5
        self.score = 0
        self.restart()
      
     
       
        # mouse_rect.colliderect(obstacle_rect)

    def restart(self) -> None:
        self.rect = self.image.get_rect(topleft=self.initial_coordinates)

    def update(self) -> None:
        key = pg.key.get_pressed()
        key_up_pressed:bool   = key[pg.K_UP]   if NUMBER_OF_PLAYERS == 1 else key[pg.K_w] if self.player == Player.ONE else key[pg.K_UP]
        key_down_pressed:bool = key[pg.K_DOWN] if NUMBER_OF_PLAYERS == 1 else key[pg.K_s] if self.player == Player.ONE else key[pg.K_DOWN]

        if key_up_pressed:
            self.rect.move_ip(0, -1 * self.y_increment)     # Equival a: self.rect.y = self.rect.y - self.y_increment    
                  
        if key_down_pressed:
            self.rect.move_ip(0, self.y_increment)
        
        self.rect.y = max(TOP_MARGIN, min(self.rect.y, H - BOTTOM_MARGIN - self.height))    # No usem clamp_ip ja que és un Rect i no podem posar limits superior i inferior diferents.
        
class Ball(_Sprite):
    def __init__(self, radius:int, color:_Color, group: pg.sprite.Group):
        super().__init__(group)
        self.image = pg.Surface((radius*2, radius*2), pg.SRCALPHA)
        pg.draw.circle(self.image, color, (radius, radius), radius)
        self.restart()
        self.sign = lambda x: 1 if x>=0 else -1
        self.ball_hits_top_margin    = property(lambda self: self.rect.top < self.TOP_MARGIN)
        self.ball_hits_bottom_margin = property(lambda self: self.rect.bottom > H - BOTTOM_MARGIN)
    
    def restart(self) -> None:
        self.player = random.choice(list(Player))
        self.y = STATING_Y_BALL
        self.x = STARTING_X_BALL_PLAYER_1 if self.player==Player.ONE else STARTING_X_BALL_PLAYER_2
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
    def update(self) -> None:
        if self.ball_hits_top_margin or self.ball_hits_bottom_margin:
            self.y_increment *= -1  

        
        self.rect.x += round(self.x_increment)
        self.rect.y += round(self.y_increment)
        
        
        

    
    
    def update(self) -> None:
        # En general:
        # La pilota es mou sumant la velocitat a ball.x i ball.y.
        # Si toca les vores esquerra/dreta, s’invertix speed_x.
        # Si toca les vores superior/inferior, s’invertix speed_y.
        #
        pass


# ===========================================================================================
def draw_text(text:str, x:int, y:int):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x,y))

def draw_score():
    draw_text(f'Player 1: {paddle_1.score}', 40, 10)
    draw_text(f'Player 2: {paddle_2.score}', W-240, 10)
    draw_text(f'Level: {level}', W//2 - 50, 10)

# ============================================================================
def draw_background():
    screen.fill(BG_COLOR)
    pg.draw.line(screen, WHITE, (0, TOP_MARGIN), (W, TOP_MARGIN), 2)
    pg.draw.line(screen, WHITE, (0, H - BOTTOM_MARGIN), (W, H - BOTTOM_MARGIN), 2)

# ============================================================================
def start_new_game(player: Player) -> None:
    '''Quan s'inicia un nova partida hem d'indicar el jugador que la inicia'''
    paddle_1.restart()
    paddle_2.restart()
    ball.restart()


def main():
    clock = pg.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        draw_background()
        draw_score()

        paddle_group.update()
        ball_group.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        
        paddle_group.draw(screen)
        ball_group.draw(screen)
        pg.display.update()


# ------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((W,H))
    pg.display.set_caption('Ping Pong')
    font = pg.font.SysFont('Bauhaus 93', 50)

    ball_group:_Group = pg.sprite.Group()
    paddle_group:_Group = pg.sprite.Group()
    paddle_1 = Paddle(x=20, y=HALF_BOARD_Y, player=Player.ONE, color=WHITE, group=paddle_group)
    paddle_2 = Paddle(x=W-40, y=HALF_BOARD_Y, player=Player.TWO, color=WHITE, group=paddle_group)
    ball = Ball(radius=BALL_RADIUS, color=WHITE, group=ball_group)
    level = 0

    main()

    pg.quit()

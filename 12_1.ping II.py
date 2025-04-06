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
STARTING_Y_BALL = HALF_BOARD_Y + 50

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
# class Score(Enum):          # It is used to know which player has scored.
#     NONE=0
#     PLAYER_1=1
#     PLAYER_2=2

class Player(Enum):         # Reference to a player
    LEFT=1                   # 1 is right direction
    RIGHT=-1                  # -1 is left direction

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

    def restart(self) -> None:
        margin = 5
        self.rect = self.image.get_rect(topleft=self.initial_coordinates)
        self.collision_rect = pg.Rect(
            self.rect.left + margin,
            self.rect.top + margin,
            self.rect.width - 2 * margin,
            self.rect.height - 2 * margin
        )

    def collide_with(self, ball:"Ball") -> bool:
        return self.rect.colliderect(ball.rect)

    def update(self) -> None:
        key = pg.key.get_pressed()
        key_up_pressed:bool   = key[pg.K_UP]   if NUMBER_OF_PLAYERS == 1 else key[pg.K_w] if self.player == Player.LEFT else key[pg.K_UP]
        key_down_pressed:bool = key[pg.K_DOWN] if NUMBER_OF_PLAYERS == 1 else key[pg.K_s] if self.player == Player.LEFT else key[pg.K_DOWN]

        if key_up_pressed:
            self.rect.move_ip(0, -1 * self.y_increment)     # Equival a: self.rect.y = self.rect.y - self.y_increment    
                  
        if key_down_pressed:
            self.rect.move_ip(0, self.y_increment)
        
        self.rect.y = max(TOP_MARGIN, min(self.rect.y, H - BOTTOM_MARGIN - self.height))    # No usem clamp_ip ja que és un Rect i no podem posar limits superior i inferior diferents.

        self.collision_rect.center = self.rect.center
        
class Ball(_Sprite):
    def __init__(self, radius:int, color:_Color, group: pg.sprite.Group):
        super().__init__(group)
        self.image = pg.Surface((radius*2, radius*2), pg.SRCALPHA)
        pg.draw.circle(self.image, color, (radius, radius), radius)
        self.sign = lambda x: 1 if x>=0 else -1
        self.restart(random.choice(list(Player)))

    def ball_hits_the_top_or_bottom_edge(self) -> bool:
        return (self.rect.top < TOP_MARGIN) or (self.rect.bottom > H - BOTTOM_MARGIN)
    
   
    def ball_hits_any_paddle(self) -> Paddle|None:
        for paddle in paddle_group.sprites():
            if ball.collision_rect.colliderect(paddle.collision_rect):
                return paddle
        return None


    def check_if_any_player_has_scored_a_goal(self) -> Player|None:
        if (self.rect.left < 0):
            return Player.LEFT
        if (self.rect.right > W):
            return Player.RIGHT
        return None
    
    def restart(self, player: Player) -> None:
        self.y = STARTING_Y_BALL
        self.x = STARTING_X_BALL_PLAYER_1 if player==Player.LEFT else STARTING_X_BALL_PLAYER_2
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.x_increment:float = SPEED * player.value
        self.y_increment:float = random.choice([-1, 1]) * random.uniform(1.75, 3)
        w, h = self.rect.size
        self.collision_rect = pg.Rect(0, 0, int(w * 0.5), int(h * 0.5))
        self.collision_rect.center = self.rect.center
        
    def update(self) -> None:   
        if self.ball_hits_the_top_or_bottom_edge():
            self.y_increment *= -1

        elif paddle:= self.ball_hits_any_paddle():
                 
            self.x_increment *= -1
            self.y_increment = self.sign(self.y_increment) * random.uniform(1.5, 2.5)   # Change the bounce angle a little randomly

            # prevent the ball from bouncing inside the paddle
            if paddle.player == Player.LEFT:
                self.rect.left = paddle.rect.right
            elif paddle.player == Player.RIGHT:
                self.rect.right = paddle.rect.left          

        self.rect.x = round(self.rect.x + self.x_increment)
        self.rect.y = round(self.rect.y + self.y_increment)

        self.collision_rect.center = self.rect.center



# ===========================================================================================
def draw_text(text:str, x:int, y:int):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x,y))


def draw_score():
    draw_text(f'Player 1: {paddle_Left.score}', 40, 10)
    draw_text(f'Player 2: {paddle_Right.score}', W-240, 10)
    draw_text(f'Level: {level}', W//2 - 50, 10)

# ============================================================================
def draw_background():
    screen.fill(BG_COLOR)
    pg.draw.line(screen, WHITE, (0, TOP_MARGIN), (W, TOP_MARGIN), 2)
    pg.draw.line(screen, WHITE, (0, H - BOTTOM_MARGIN), (W, H - BOTTOM_MARGIN), 2)

# ============================================================================
def start_new_game(player: Player) -> None:
    '''Quan s'inicia un nova partida hem d'indicar el jugador que la inicia'''
    paddle_Left.restart()
    paddle_Right.restart()
    # ball.restart()


def main():
    clock = pg.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        draw_background()
        draw_score()

        paddle_group.update()
        ball_group.update()

        player = ball.check_if_any_player_has_scored_a_goal()
        if player:
            run = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        
        paddle_group.draw(screen)
        ball_group.draw(screen)

        # pl = paddle_group.sprites()[0].collision_rect
        # pr = paddle_group.sprites()[1].collision_rect
        # b =  ball_group.sprites()[0].collision_rect
        # pg.draw.rect(screen, (255, 0, 0), pl, 1)
        # pg.draw.rect(screen, (255, 0, 0), pr, 1)
        # pg.draw.rect(screen, (255, 0, 0), b, 2) 

        pg.display.update()


# ------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((W,H))
    pg.display.set_caption('Ping Pong')
    font = pg.font.SysFont('Bauhaus 93', 50)

    ball_group:_Group = pg.sprite.Group()
    paddle_group:_Group = pg.sprite.Group()
    paddle_Left = Paddle(x=20, y=HALF_BOARD_Y, player=Player.LEFT, color=WHITE, group=paddle_group)
    paddle_Right = Paddle(x=W-40, y=HALF_BOARD_Y, player=Player.RIGHT, color=WHITE, group=paddle_group)
    ball = Ball(radius=BALL_RADIUS, color=WHITE, group=ball_group)
    level = 0

    main()

    pg.quit()

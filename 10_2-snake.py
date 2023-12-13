import pygame
from enum import Enum
import random

pygame.init()
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')

class Direction(Enum):
    UP=1,
    RIGHT=2,
    DOWN=3,
    LEFT=4

class Answer(Enum):
    NEW_GAME=0,
    EXIT=1

class Segment():
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
    
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, diameter, diameter)
    
    def __eq__(self, obj):
        return obj.x == self.x and obj.y == self.y


class Fruit(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.image = image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width * random.randint(0, (screen_width // self.rect.width)-1)
        self.rect.y = self.rect.height * random.randint(0, (screen_height // self.rect.height)-1)

    def delete(self):
        self.kill()

background_color = (255, 200, 150)
circle_color = (50, 170, 25)
red_color = (255, 0, 0)
blue_color = (0, 0, 255)
diameter = 20
font = pygame.font.SysFont(None, 35)
SPEED = 400

apple_image = pygame.image.load('data/apple.png').convert_alpha()
apple_image = pygame.transform.scale(apple_image, (30,30))
apple_image.set_colorkey(background_color)

x_init = screen_width // 2
y_init = screen_height // 2
s1 = Segment(x_init, y_init + diameter*0)
s2 = Segment(x_init, y_init + diameter*1)
s3 = Segment(x_init, y_init + diameter*2)
s4 = Segment(x_init, y_init + diameter*3)

score = 0

def init_game() -> None:
    global direction
    global create_new_food
    global fruit
    global snake
    global score
    direction = Direction.UP
    create_new_food = True
    fruit = Fruit(apple_image)
    snake:list[Segment] = [s1,s2,s3,s4]
    score = 0



def draw_segment(s:Segment, head:bool=False) -> None:
    radius = diameter // 2
    if head:
        pygame.draw.rect(screen, circle_color, (s.x, s.y, radius, radius))
    else: 
        pygame.draw.circle(screen, red_color, (s.x + radius , s.y + radius), radius)

def draw_snake():
    draw_segment(snake[0], head=True)
    for s in snake[1:]:
        draw_segment(s)

def draw_score():
    score_txt = 'Score: ' + str(score)
    score_img = font.render(score_txt, True, blue_color)
    screen.blit(score_img, (0, 0))


def is_snake_eaten_itself() -> bool:
    head_snake = snake[0]
    for s in snake[1:]:
        if s==head_snake:
            return True
    return False

def is_snake_out_of_bounds() -> bool:
    head_snake = snake[0]
    return head_snake.x<0 or head_snake.x>screen_width or head_snake.y<0 or head_snake.y>screen_height

def is_game_over() -> bool:
    return is_snake_eaten_itself() or is_snake_out_of_bounds()

def draw_game_over() -> Answer:
    mouse_clicked = False
    while True:
        screen.fill(background_color)

        score_img = font.render('Game Over', True, blue_color)
        screen.blit(score_img, (screen_width // 2 - 80, screen_height // 2 - 60))

        play_again_img = font.render('PLAY AGAIN', True, blue_color)
        play_again_rect = play_again_img.get_rect()
        play_again_rect.left = screen_width // 2 - 200
        play_again_rect.top = screen_height // 2 - 20
        screen.blit(play_again_img, play_again_rect)

        exit_img = font.render('EXIT', True, blue_color)
        exit_img_rect = exit_img.get_rect()
        exit_img_rect.left = screen_width // 2 + 50
        exit_img_rect.top = screen_width // 2 - 20
        screen.blit(exit_img, exit_img_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Answer.EXIT
            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_clicked:
                mouse_clicked = True
            if event.type == pygame.MOUSEBUTTONUP and mouse_clicked:
                mouse_clicked = False
                mouse_position = pygame.mouse.get_pos()

                if play_again_rect.collidepoint(mouse_position):
                    return Answer.NEW_GAME
                
                if exit_img_rect.collidepoint(mouse_position):
                    return Answer.EXIT
        pygame.display.update()


wait = 0

init_game()

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

    if wait > SPEED:
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

        new_head = Segment(x,y)
        snake:list[Segment] = [new_head, head, *body]

        if is_game_over():
            if draw_game_over() == Answer.EXIT:
                run = False
            else:
                init_game()

    wait += 1

    draw_snake()
    draw_score()

    if create_new_food:
        create_new_food = False
        if fruit:
            fruit.delete()
        fruit = Fruit(apple_image)
    
    # draw fruit
    screen.blit(fruit.image, fruit.rect)

    head_snake = snake[0].rect()
    pygame.draw.rect(screen, (0, 0, 255), head_snake)

    if fruit.rect.colliderect(head_snake):
        score += 1
        create_new_food = True

        tail_segment = snake[-1]

        if direction == Direction.UP:
            x = tail_segment.x
            y = tail_segment.y + diameter
        elif direction == Direction.RIGHT:
            x = tail_segment.x - diameter
            y = tail_segment.y
        elif direction == Direction.DOWN:
            x = tail_segment.x
            y = tail_segment.y - diameter
        elif direction == Direction.LEFT:
            x = tail_segment.x + diameter
            y = tail_segment.y
        snake.append(tail_segment)

    pygame.display.update()

pygame.quit()
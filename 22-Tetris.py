import pygame as pg
import sys
import random
from dataclasses import dataclass
import copy

WHITE = 0xFFFFFF
BLACK = 0x000000
RED = 0xFF0000
FPS = 60

BG_COLOR = 0x000270

pg.init()
rows, columns = 15,10
tetromino_pixels_width = 30                                # Mida de cada peça, per exemple: 40x40 píxels.
W, H = columns*tetromino_pixels_width, rows*tetromino_pixels_width

screen = pg.display.set_mode((W,H))
clock = pg.time.Clock()
bg = pg.Surface(screen.get_size())

@dataclass
class Tetromino:
    def __init__(self, color:int, shape:list[list[str]], ):
        self.shape = shape
        self.color = color


i = Tetromino(0x00f0f0,[
     ['X···',
      'X···',
      'X···',
      'X···'
     ],
     ['····',
      '····',
      'XXXX'
      '····',
     ]
    ])

s = Tetromino(0x00f000,[
     ['···',
      '·XX',
      'XX·'
     ],
     ['X··',
      'XX·',
      '·X·'
     ]
    ])

t = Tetromino(0xa100f0,[
     ['···',
      'XXX',
      '·X·'
     ],
     ['·X·',
      'XX·',
      '·X·'
     ],
     ['···',
      '·X·',
      'XXX'
     ],
     ['X··',
      'XX·',
      'X··'
     ]
    ])

z = Tetromino(0xf00000,[
     ['···',
      'XX·',
      '·XX',
     ],
     ['·X·',
      'XX·',
      'X··'
     ]
    ])


j = Tetromino(0x0000f0,[
     ['·X·',
      '·X·',
      'XX·'
     ],
     ['···',
      'X··',
      'XXX'
     ],
     ['XX·',
      'X·',
      'X··'
     ],
     ['···',
      'XXX',
      '··X'
     ]
    ])


o = Tetromino(0xf0f000,[
     ['XX',
      'XX'
     ]
    ])


l = Tetromino(0xf0a100,[
     ['X··',
      'X··',
      'XX·'
     ],
     ['···',
      'XXX',
      'X··'
     ],
     ['XX·',
      '·X·',
      '·X·'
     ],
     ['···',
      '··X',
      'XXX'
     ]
    ])


tetrominos = [i,s,t,z,j,o,l]
tetrominos2 = [i]

class Timer():
    def __init__(self, ms: int):
        self.end_time = ms
        self.initial_time = pg.time.get_ticks()
        self.stop = False

    def is_time_out(self) -> bool:
        now = pg.time.get_ticks()
        if self.stop:
            self.initial_time = now
            self.stop = False
            return True

        if (now - self.initial_time) <= self.end_time:
            return False

        self.initial_time = now
        self.stop = False
        return True
  
    
    def reset(self) -> None:
        self.stop = True
        

class Piece:
    def __init__(self, initial_column:int, tetromino:Tetromino):
        self.initial_row = -2
        self.column:int = initial_column
        self.tetromino:Tetromino = tetromino
        self.position:int = 0
        self.orientation:list[str] = self.tetromino.shape[self.position]
        self.color:int = self.tetromino.color
        self.last_line:str = self.orientation[-1]           
        self.width:int = len(self.orientation[0])
        self.height = self.width
        self.row:int = self.initial_row
        self.real_width = max([len(c.rstrip('·')) for c in self.orientation])
        self.real_height = self.get_real_height()
    
    def next_position(self) -> None:
        number_of_positions = len(self.tetromino.shape)
        self.position = (self.position + 1) % number_of_positions
        self.orientation = self.tetromino.shape[self.position]
        self.last_line = self.orientation[-1]
        self.real_width = max([len(c.rstrip('·')) for c in self.orientation])
        self.real_height = self.get_real_height()

    def get_real_height(self) -> int:
        real_height = len(self.orientation)
        for line in reversed(self.orientation):
            if '·' * len(line) != line:
                break
            real_height -= 1
        return real_height
    

class Tetris:
    def __init__(self, rows, columns, tetromino_pixels_width, tetrominos) -> None:
        self.jjj = 0
        self.rows = rows
        self.columns = columns
        self.tetromino_width = tetromino_pixels_width
        self.tetrominos = tetrominos
        self.grid = [[BG_COLOR for _ in range(columns)] for _ in range(rows)]
        self.current:Piece = self.random_piece()
        self.score = 0
        self.game_over = False
        self.key_pressed = 0
        

    def random_piece(self) -> Piece:
        # tetromino = random.choice(self.tetrominos)
        tetromino = tetrominos2[self.jjj]
        self.jjj = (self.jjj + 1)%1
        # tetromino = tetrominos[0]
        # random_colum = random.randint(0,self.columns - 3)
        return Piece(self.columns//2, tetromino) 

    def draw_grid(self):
        for r, row in enumerate(self.grid):
            for c, color in enumerate(row):
                pg.draw.rect(screen, color, (c * self.tetromino_width, r * self.tetromino_width, self.tetromino_width - 1 , self.tetromino_width - 1))
                pg.draw.rect(screen, WHITE, (c * self.tetromino_width, r * self.tetromino_width, self.tetromino_width , self.tetromino_width), 1)

    def draw_current_piece(self):
        for r, line in enumerate(self.current.orientation):
            if self.current.row + r < 0:
                continue
            for c,square in enumerate(line):
                if square == 'X':
                    row = (self.current.row + r) * self.tetromino_width 
                    column = (self.current.column + c) * self.tetromino_width
                    color = self.current.color
                    pg.draw.rect(screen, color, (column, row, tetromino_pixels_width - 1 , tetromino_pixels_width - 1))     

    
    def save_current_position_in_grid(self) -> None:
        r = self.current.row
        for i, line in enumerate(self.current.orientation):
            c = self.current.column
            for j,cell in enumerate(line):
                if j+c<self.columns and self.grid[i+r][j+c] == BG_COLOR and cell=='X':
                    # print(">>>>", j,c,j+c)
                    self.grid[i+r][j+c] = self.current.color
                    if r+i == 0:
                        self.game_over = True
                        return
  

    def is_this_position_valid(self, row:int, column: int) -> bool:
        for r, line in enumerate(self.current.orientation):
            for c,cell in enumerate(line):
                if r+row>=0 and c+column<self.columns and self.grid[r+row][c+column] != BG_COLOR and cell=='X':
                    return False                
        return True
        

    def is_next_position_of_piece_valid(self, direcction: int) -> bool:  

        if  self.current.row + self.current.real_height >= self.rows:
            return False     

        if (direcction == 0):
            row = self.current.row + 1
            column = self.current.column
        elif (direcction == pg.K_LEFT):
            row = self.current.row
            column = self.current.column - 1          
        elif (direcction == pg.K_RIGHT):
            row = self.current.row
            column = self.current.column + 1

        return self.is_this_position_valid(row, column)


    def create_new_piece(self):
        self.current = self.random_piece()


    def move(self, direction: int, increment:int) -> None:
        self.draw_grid()
        self.draw_current_piece()

        if self.is_next_position_of_piece_valid(direction):
            if direction == pg.K_LEFT:
                if self.current.column - increment >= 0:
                    self.current.column -= increment
                else:
                    pass

            elif direction == pg.K_RIGHT:
                if self.current.column + self.current.real_width < self.columns:
                    self.current.column += increment

            elif direction == 0:
                self.current.row += increment

            return
  
        if direction == 0:
            self.save_current_position_in_grid()
            if not self.game_over:
                self.create_new_piece() 
                print(self.current.real_width)


    def draw(self):     
        if horizontal_timer.is_time_out():
            if self.key_pressed == pg.K_LEFT:
                self.move(pg.K_LEFT, increment=-1)
            elif self.key_pressed == pg.K_RIGHT:
                self.move(pg.K_RIGHT, increment=1)
            elif self.key_pressed == pg.K_UP:            
                current_copy = copy.deepcopy(self.current)
                self.current.next_position()
                # if not self.is_this_position_valid(self.current.row, self.current.column):
                #     self.current = current_copy
                # else:
                #     self.draw_grid()
                #     self.draw_current_piece()
                if (self.current.column - 1 >= 0) and (self.current.column + self.current.real_width < self.columns):
                    pass
                else:
                   if (self.current.column - 1 >= 0):
                       
                   self.current = current_copy 
                    
        
        if fall_timer.is_time_out():
            self.move(direction=0, increment=0)

            
tetris = Tetris(rows, columns, tetromino_pixels_width, tetrominos)
fall_timer = Timer(350)
horizontal_timer = Timer(50)
stop = False

run = True
while run:
    clock.tick(FPS)
      
    tetris.key_pressed = 0
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                tetris.key_pressed = pg.K_UP
                horizontal_timer.reset()
                fall_timer.reset()

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        tetris.key_pressed = pg.K_LEFT
    elif keys[pg.K_RIGHT]:
        tetris.key_pressed = pg.K_RIGHT
    elif keys[pg.K_DOWN]:
        print("Fletxa avall mantinguda")
    
    if not tetris.game_over:
        tetris.draw()
    else:
        print('game over')
        run = False

    pg.display.update()
       
pg.quit()










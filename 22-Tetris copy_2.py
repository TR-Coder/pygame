import pygame as pg
import sys
import random
from dataclasses import dataclass

WHITE = 0xFFFFFF
BLACK = 0x000000
RED = 0xFF0000
FPS = 60

BG_COLOR = 0x000270

pg.init()
rows, columns = 15,10
tetromino_width = 30                                # Mida de cada peça, per exemple: 40x40 píxels.
W, H = columns*tetromino_width, rows*tetromino_width

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
      'XXXX',
      '····'
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
tetrominos2 = [i,z]

class Timer():
    def __init__(self, ms: int):
        self.ticks = ms
        self.initial_time = pg.time.get_ticks()

    def time_out(self) -> bool:
        now = pg.time.get_ticks()
        if (now - self.initial_time) > self.ticks:
            self.initial_time = now
            return True
        return False

class Piece:
    def __init__(self, column:int, tetromino:Tetromino):
        self.tetromino:Tetromino = tetromino
        self.position:int = 0
        self.orientation:list[str] = self.tetromino.shape[self.position]
        self.color:int = self.tetromino.color
        self.last_line:str = self.orientation[-1]           
        self.width:int = len(self.orientation[0])
        self.height = self.width
        self.initial_position = -2
        self.column:int = column
        self.row:int = self.initial_position

class Tetris:
    def __init__(self, rows, columns, tetromino_width, tetrominos) -> None:
        self.jjj = 0
        self.rows = rows
        self.columns = columns
        self.tetromino_width = tetromino_width
        self.tetrominos = tetrominos
        self.grid = [[BG_COLOR for _ in range(columns)] for _ in range(rows)]
        self.current:Piece = self.random_piece()
        self.score = 0
        self.game_over = False
        self.key_pressed = 0
        

    def random_piece(self) -> Piece:
        tetromino = random.choice(self.tetrominos)
        tetromino = tetrominos2[self.jjj]
        self.jjj = (self.jjj + 1)%2
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
                    pg.draw.rect(screen, color, (column, row, tetromino_width - 1 , tetromino_width - 1))     
    
    def save_current_position_in_grid(self) -> None:
        r = self.current.row
        for i, line in enumerate(self.current.orientation):
            c = self.current.column
            for j,cell in enumerate(line):
                if self.grid[i+r][j+c] == BG_COLOR and cell=='X':
                    self.grid[i+r][j+c] = self.current.color
                    if r+i == 0:
                        self.game_over = True
                        return
  
    def is_next_position_of_piece_valid(self, direcction: int) -> bool:  
        if  self.current.row + self.current.height >= self.rows:
            return False     

        if (direcction == 0):
            r = self.current.row + 1
            c = self.current.column

        if (direcction == pg.K_LEFT):
            r =  r = self.current.row
            c = self.current.column - 1

        for i, line in enumerate(self.current.orientation):
            for j,cell in enumerate(line):
                if i+r>=0 and self.grid[i+r][j+c] != BG_COLOR and cell=='X':
                    return False
                
        return True

    def create_new_piece(self):
        self.current = self.random_piece()
        self.current.row = self.current.initial_position


    def move(self, direction: int) -> None:
        self.draw_grid()
        self.draw_current_piece()
        if self.is_next_position_of_piece_valid(direction):
            if direction == 0:
                self.current.row += 1
            elif direction == pg.K_LEFT:
                self.current.column -= 1
            return
        self.save_current_position_in_grid()
        if not self.game_over:
            self.create_new_piece()        


    def draw(self):
        
        if self.key_pressed == pg.K_LEFT:
            self.move(pg.K_LEFT)

        if timer.time_out():
                self.move(direction=0)

            

tetris = Tetris(rows, columns, tetromino_width, tetrominos)
timer = Timer(150)
stop = False

run = True
while run:
    clock.tick(FPS)
      
    tetris.key_pressed = 0
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                tetris.key_pressed = pg.K_LEFT
            if event.key == pg.K_RIGHT:
                tetris.key_pressed = pg.K_RIGHT
    

    if not tetris.game_over:
        tetris.draw()

    pg.display.update()
       
pg.quit()










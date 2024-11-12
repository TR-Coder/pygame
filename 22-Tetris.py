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
rows, columns = 20,10
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
    def __init__(self, row:int, column:int, tetromino:Tetromino):
        self.row:int = row
        self.column:int = column
        self.tetromino:Tetromino = tetromino
        self.position:int = 0

        self.orientation:list[str] = self.tetromino.shape[self.position]
        self.color:int = self.tetromino.color
        self.last_line:str = self.orientation[-1]
               
        self.width:int = len(self.orientation[0])
        # line = self.orientation[0]
        # for e in line[::-1]:
        #     if e == '·':
        #         self.width -= 1
                          
        self.height = 0
        for line in self.orientation:
            if line != '···' and line != '····':
                self.height += 1  

class Tetris:
    def __init__(self, rows, columns, tetromino_width, tetrominos) -> None:
        self.rows = rows
        self.columns = columns
        self.tetromino_width = tetromino_width
        self.tetrominos = tetrominos
        self.grid = [[BG_COLOR for _ in range(columns)] for _ in range(rows)]
        self.current_piece:Piece = self.random_piece()
        self.score = 0
        self.top_row = self.rows
        self.game_over = False
        
        self.grid[19][7] = RED

    def random_piece(self) -> Piece:
        tetromino = random.choice(self.tetrominos)
        tetromino = self.tetrominos[1]
        return Piece(0, self.columns//2, tetromino) 


    def draw_grid(self):
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                pg.draw.rect(screen, color, (x * self.tetromino_width, y * self.tetromino_width, self.tetromino_width - 1 , self.tetromino_width - 1))

        if self.current_piece:
            r = 0
            for line in self.current_piece.orientation:
                if line != '···' and line != '····':
                    for c,square in enumerate(line):
                        if square == 'X':
                            row = (self.current_piece.row + r) * self.tetromino_width 
                            column = (self.current_piece.column + c) * self.tetromino_width
                            color = self.current_piece.color
                            pg.draw.rect(screen, color, (column, row, tetromino_width - 1 , tetromino_width - 1))
                    r += 1
        

    def save_piece(self) -> None:
        r = self.current_piece.row
        for i, line in enumerate(self.current_piece.orientation):
            c = self.current_piece.column
            for j,cell in enumerate(line):
                if self.grid[i+r][j+c] == BG_COLOR and cell=='X':
                    self.grid[i+r][j+c] = self.current_piece.color

        # if self.current_piece.row < self.top_row:
        #     self.top_row = self.current_piece.row
        #     if self.top_row < 3:
        #         self.game_over = True
        #         print('>>>>>>>', r, self.top_row)
        #         print(self.grid)
        #         return
         
    
    def move_tetro(self, timer:Timer) -> None:
        next_row = self.current_piece.row + 1
        if timer.time_out():
            r = next_row + self.current_piece.height
            if r >= self.rows:
                self.save_piece()
                self.current_piece.row = 0
                return         

            c = self.current_piece.column
            w = self.current_piece.width
            next_grid = self.grid[r][c:c+w]
            last_line = self.current_piece.last_line
            for l,g in zip(last_line, next_grid):
                if l=='X' and g != BG_COLOR:
                    self.save_piece()
                    self.current_piece.row = 0
                    return
            self.current_piece.row += 1
            print(last_line,next_grid,r,c,c+w)
               

tetris = Tetris(rows, columns, tetromino_width, tetrominos)
timer = Timer(150)

run = True
while run:
    clock.tick(FPS)
    screen.fill(BLACK)  
       
    for event in pg.event.get():
        if event.type == pg.QUIT:
            print('********************************')
            run = False
    

    tetris.move_tetro(timer)
    tetris.draw_grid()
        
    pg.display.update()
    
    if tetris.game_over:
        break

print('----------------------------------')
pg.quit()










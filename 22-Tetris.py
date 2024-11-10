import pygame as pg
import sys
import random
from dataclasses import dataclass

WHITE = pg.Color(255,255,255)
BLACK = pg.Color(0,0,0)
FPS = 60

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


class Tetro:
    def __init__(self, x:int, y:int, tetromino:Tetromino):
        self.x:int = x
        self.y:int = y
        self.tetromino:Tetromino = tetromino
        self.position:int = 0    


class Tetris:
    def __init__(self, rows, columns, tetromino_width, tetrominos) -> None:
        self.rows = rows
        self.columns = columns
        self.tetromino_width = tetromino_width
        self.tetrominos = tetrominos
        self.grid = [[0 for _ in range(columns)] for _ in range(rows)]
        self.current:Tetro = self.random_tetro()
        self.score = 0

    def random_tetro(self) -> Tetro:
        tetromino = random.choice(self.tetrominos)
        return Tetro(self.columns//2, 0, tetromino) 


    def draw_grid(self):
        # for y, row in enumerate(self.grid):
        #     for x, cell in enumerate(row):
        #         if cell == 0:
        #             pg.draw.rect(screen, WHITE, (x * self.tetromino_width, y * self.tetromino_width, self.tetromino_width - 1 , self.tetromino_width - 1), 2)

        if self.current:
            current_shape = self.current.tetromino.shape[self.current.position]
            i = 0
            for line in current_shape:
                if line != '···' and line != '····':
                    for j,square in enumerate(line):
                        if square=='X':
                            x = (self.current.x + j) * self.tetromino_width 
                            y = (self.current.y + i) * self.tetromino_width
                            color = self.current.tetromino.color
                            pg.draw.rect(screen, color, (x, y, tetromino_width - 1 , tetromino_width - 1))
                    i += 1
        

    
    def move_tetro(self):
        pass
                

tetris = Tetris(rows, columns, tetromino_width, tetrominos)

run = True
while run:
    clock.tick(FPS)
    screen.fill(BLACK)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    tetris.draw_grid()

    pg.display.update()












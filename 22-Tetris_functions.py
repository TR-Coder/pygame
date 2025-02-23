import pygame as pg
from typing import Literal

WHITE = 0xFFFFFF
BLACK = 0x000000
RED = 0xFF0000
GREEN = 0x00FF00
FPS = 60    
BG_COLOR = 0x000270

pg.init()
rows, columns = 15,10
tetromino_pixels_width = 30
W, H = columns*tetromino_pixels_width, rows*tetromino_pixels_width
screen = pg.display.set_mode((W,H))
clock = pg.time.Clock()
bg = pg.Surface(screen.get_size())
grid = [[BG_COLOR for _ in range(columns)] for _ in range(rows)]

class Figure:
    def __init__(self, shape:list[list[str]]):
        self.shape = shape
        self.rotation_point = self.get_rotation_point(self.shape)

    def rotate(self, direcction:Literal['R', 'L']) -> tuple[list[list[str]], tuple[int,int]]:
        shape = [list(e) for e in zip(*self.shape)]
        if direcction == 'R':
            shape.reverse()
        rp = self.get_rotation_point(shape)
        return shape, rp
    
    def get_rotation_point(self, tmp_shape: list[list[str]]) -> tuple[int,int]:
        for i, fila in enumerate(tmp_shape):
            for j, valor in enumerate(fila):
                if valor == 'C':
                    return (i,j)
        return (0,0)


    def translate(self, tmp_shape:list[list[str]], tmp_rotation_point: tuple[int,int], i: int, j: int) -> tuple[tuple[int, int], bool]:
        """
        Mou la figura sobre el grid situant el seu punt de rotació en (i, j).
        Si el punt (i, j) fa que la figura se n'isca del grid, ajusta la posició per mantindre-la dins.
        Retorna el punt de rotació (i, j): Si la figura no se n'ha eixit coincidirà amb el paràmetre (i, j).
        """
        grid_rows, grid_cols = len(grid), len(grid[0])
        shape_rows, shape_cols = len(tmp_shape), len(tmp_shape[0])

        # Calcular l'offset inicial
        row_offset = i - tmp_rotation_point[0]
        col_offset = j - tmp_rotation_point[1]

        # Ajustar per a mantindre's dins del grid
        row_offset = max(0, min(row_offset, grid_rows - shape_rows))
        col_offset = max(0, min(col_offset, grid_cols - shape_cols))

        # Comprovar si la posició ajustada és vàlida (no col·lidis)
        if not self.is_valid_position(tmp_shape, row_offset, col_offset):
            return (i, j), False
        
        self.shape = tmp_shape
        self.rotation_point = tmp_rotation_point

        # Actualitzar el grid amb els valors corresponents
        for y in range(shape_rows):
            for x in range(shape_cols):
                if self.shape[y][x] == 'C':
                    grid[row_offset + y][col_offset + x] = GREEN
                    i, j = row_offset + y, col_offset + x
                else:
                    grid[row_offset + y][col_offset + x] = RED
                    
        return (i, j), True

    
    def is_valid_position(self, tmp_shape:list[list[str]], r:int, c:int) -> bool:
        for x, cell in enumerate(tmp_shape[0]):
            for y in range(len(tmp_shape)):
                if grid[r+y][c+x] != BG_COLOR and tmp_shape[y][x]!='·':
                    return False
        return True
    

    def new_position(self, row:int, column:int, direcction:Literal['R', 'L'] | None = None) -> None:
        '''La posició (row,columns) fa referència sempre a la del rotation_point'''
        if direcction is not None:
            tmp_shape, tmp_rotation_point = self.rotate(direcction)
        else:
            tmp_shape, tmp_rotation_point = self.shape, self.rotation_point

        (current_row, current_column), collision = self.translate(tmp_shape,tmp_rotation_point, row, column)

        if not collision:
            print('**************** Error')

def draw_grid():
    for r, row in enumerate(grid):
        for c, color in enumerate(row):
            pg.draw.rect(screen, color, (c * tetromino_pixels_width, r * tetromino_pixels_width, tetromino_pixels_width - 1 , tetromino_pixels_width - 1))
            pg.draw.rect(screen, WHITE, (c * tetromino_pixels_width, r * tetromino_pixels_width, tetromino_pixels_width , tetromino_pixels_width), 1)

figure3 = [[1],
           [2],
           [3],
           [4]]       

figure4 = [['1','2','3','4'],
           ['5','C','7','8']]

f1 = Figure(figure4)   
# f1.new_position(5,-2,'R')
print(f1.rotation_point)
f1.new_position(0,0)
print(f1.rotation_point)

run = True
while run:
    clock.tick(FPS)    

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    draw_grid()

    pg.display.update()
       
pg.quit()















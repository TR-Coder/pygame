import pygame as pg

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
        self.rotation_point = (0,0)

    def rotate(self) -> None:
        self.shape = [list(e) for e in zip(*self.shape)]
        self.shape.reverse()
        self.get_rotation_point()
    
    def get_rotation_point(self) -> None:
        for i, fila in enumerate(self.shape):
            for j, valor in enumerate(fila):
                if valor == 'C':
                    self.rotation_point = (i,j)
                    return               
        self.rotation_point = (0,0)


    def translate(self, i: int, j: int) -> tuple[int, int]:
        """
        Mou la figura sobre el grid situant el seu punt de rotació en (i, j).
        Si el punt (i, j) fa que la figura se n'isca del grid, ajusta la posició perquè no se n'isca.
        Retorna el punt de rotació (i, j): Si la figura no se n'ha eixit coincidirà amb el paràmetre (i, j).
        """
        grid_rows, grid_cols = len(grid), len(grid[0])
        shape_rows, shape_cols = len(self.shape), len(self.shape[0])

        # Calcular l'offset inicial
        row_offset = i - self.rotation_point[0]
        col_offset = j - self.rotation_point[1]

        # Ajustar per a mantindre's dins del grid
        row_offset = max(0, min(row_offset, grid_rows - shape_rows))
        col_offset = max(0, min(col_offset, grid_cols - shape_cols))

        # Comprovar si la posició ajustada és vàlida
        if not self.is_valid_position(row_offset, col_offset):
            return i, j

        # Actualitzar el grid amb els valors corresponents
        for y in range(shape_rows):
            for x in range(shape_cols):
                if self.shape[y][x] == 'C':
                    grid[row_offset + y][col_offset + x] = GREEN
                    i, j = row_offset + y, col_offset + x
                else:
                    grid[row_offset + y][col_offset + x] = RED

        return i, j

    
    def is_valid_position(self, r:int, c:int) -> bool:
        for x, cell in enumerate(self.shape[0]):
            for y in range(len(self.shape)):
                if grid[r+y][c+x] != BG_COLOR and self.shape[y][x]!='·':
                    print('******************************************** Error')
                    return False
        return True

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
# print(f1.shape)
f1.rotate()
print('rotation point = ', f1.rotation_point)
# print(f1.shape)
print('Translate',f1.translate(2,10))
print('rotation point = ', f1.rotation_point)

run = True
while run:
    clock.tick(FPS)    

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    draw_grid()

    pg.display.update()
       
pg.quit()















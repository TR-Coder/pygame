import pygame as pg

Coord_ = tuple[int,int]
Surface_ = pg.Surface
Rect_ = pg.Rect
Color_ = tuple[int,int,int]
Group_ = pg.sprite.Group

pg.init()

WHITE:Color_ = (255,255,255)
RED:Color_ = (255,0,0)
GREEN:Color_ = (0,255,0)
BLUE:Color_ = (0,0,255)
BLACK:Color_ = (0,0,0)

window:Surface_ = pg.display.set_mode((800, 600))

class Circle(pg.sprite.Sprite):
    def __init__(self, x:int, y:int, radius:int, color:Color_) -> None:
        super().__init__()
        self.radius = radius
        self.color = color
        self.x = x
        self.y = y
        self.selected = False
        self.image = self.get_unselected_img(radius, color)
        self.rect = pg.Rect(x, y, 0, 0).inflate(radius*2,radius*2)

    def get_unselected_img(self, radius, color) -> Surface_:
        image = pg.Surface((radius*2, radius*2), pg.SRCALPHA)
        pg.draw.circle(image, color, center=(radius, radius), radius=radius)  
        return image 
    
    def get_selected_img(self, radius, color) -> Surface_:
        image = self.get_unselected_img(radius, color)
        pg.draw.circle(image, WHITE, center=(radius, radius), radius=radius, width=2)
        return image
    
    def get_surface_text(self, number:str) -> Surface_:
        font = pg.font.Font(None, 50)
        text:Surface_ = font.render(number, True, BLACK, WHITE)
        return text

    def update(self, number:int) -> None:       
        mouse_position = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            if self.selected:
                self.image = self.get_unselected_img(self.radius, self.color)
            else:
                self.image = self.get_selected_img(self.radius, self.color)
            self.selected = not self.selected

            number_surface = self.get_surface_text(str(number))
            image_center = self.image.get_rect().center
            number_rect = number_surface.get_rect(center=image_center)
            self.image.blit(number_surface, number_rect)


container = pg.Surface((240,100))
rect_container = container.get_rect(center= window.get_rect().center)
x,y = rect_container.x,rect_container.y
sprite1 = Circle(50+x,50+y,radius=30,color=RED)
print(50+x,50+y)
sprite2 = Circle(120+x,50+y,radius=30,color=GREEN)
sprite3 = Circle(190+x,50+y,radius=30,color=BLUE)
group = pg.sprite.Group([sprite1, sprite2, sprite3])
number = 1

run = True
while run:
    mouse_clicked = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_clicked = True

    window.fill('gray')
    container.fill('black')    

    if mouse_clicked:
        group.update(number)
        number = (number+1)%10

    window.blit(container, rect_container)
    group.draw(window)
    pg.display.flip()

pg.quit()
exit()


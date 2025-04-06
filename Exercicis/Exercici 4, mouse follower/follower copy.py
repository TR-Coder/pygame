import pygame as pg
import os

pg.init()

# Configuració
W, H = 800, 600
screen = pg.display.set_mode((W, H))
pg.display.set_caption("Sprite segueix el ratolí")
clock = pg.time.Clock()

# Colors
WHITE = (255, 255, 255)

# Carrega imatge
def load_image(path:str, scale:float=1) -> pg.Surface:
    img_path = os.path.join(os.path.dirname(__file__), path)
    img = pg.image.load(img_path).convert_alpha()
    if scale != 1:
        w, h = img.get_size()
        img = pg.transform.scale(img, (int(w * scale), int(h * scale)))
    return img

# Classe del Sprite
class Follower(pg.sprite.Sprite):
    def __init__(self, image_path, scale=1):
        super().__init__()
        self.image = load_image(image_path, scale)
        self.rect = self.image.get_rect(center=(W//2, H//2))
        self.speed = 10  # píxels per frame

    def update(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        dist = (dx**2 + dy**2)**0.5

        if dist > 1:  # només es mou si la distància és prou gran
            move_x = dx / dist * min(self.speed, dist)
            move_y = dy / dist * min(self.speed, dist)
            self.rect.move_ip(move_x, move_y)

# Inicialitza sprite
follower = Follower("assets/mosquit.png", scale=0.2)
sprites = pg.sprite.Group(follower)

# Bucle principal
running = True
while running:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    sprites.update()

    screen.fill(WHITE)
    sprites.draw(screen)
    pg.display.flip()

pg.quit()


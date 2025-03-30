import pygame as pg
# Un sprite és un objecte gràfic en moviment dins d’un joc (personatge, enemic, objecte, etc.).
# Es defineix amb una classe que hereta de pg.sprite.Sprite.

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50, 50))                    # Crear un quadrat
        self.image.fill((0, 255, 0))
        # self.image = pg.image.load("imatge.png").convert_alpha() 
        self.rect = self.image.get_rect(topleft=(100, 100))  # Posició inicial

# 
# En lloc de gestionar cada sprite manualment, Pygame té pg.sprite.Group(), que permet actualitzar i dibuixar tots els sprites junts.
grup = pg.sprite.Group()
player = Player()
grup.add(player)

# En el bucle principal:
grup.update()
grup.draw(screen)


# update(): S’encarrega de modificar les propietats de l'sprite, com ara la seva posició, velocitat, animació, etc.
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50, 50))  
        self.image.fill((0, 255, 0))  
        self.rect = self.image.get_rect(topleft=(100, 100))  
        self.speed = 5  

    def update(self):
        self.rect.x += self.speed  # Es mou cap a la dreta
 
# Un altre exemple d'update que permet al jugador moure’s amb les fletxes esquerra/dreta.
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:  
            self.rect.x -= 5  
        if keys[pg.K_RIGHT]:  
            self.rect.x += 5  
# 
# 
# draw(): Dibuixa tots els sprites d’un grup sobre la pantalla o una altra superfície.
# Mestre blit() es fa servir per pintar una única imatge,draw() pinta tots els sprites d’un grup alhora.
# Fixem-nos que li passem la sufarfe sobre la que es pitaran tots els sprites del grup.
grup.draw(screen)
#
# 
# Una estructura típica d'un joc amb update() i draw() és:
# Bucle principal del joc
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    screen.fill((0, 0, 0))  # Netejar pantalla
    
    all_sprites.update()        # Actualitzar tots els sprites
    all_sprites.draw(screen)    # Dibuixar-los

    pg.display.flip()           # Actualitzar la pantalla





















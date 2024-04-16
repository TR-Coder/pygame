import pygame as pg

# pg.init()                                 # Inicialitza pygame
# screen = pg.display.set_mode((500,400))   # Crea una finestra de 500x400
# screen.fill((255,0,0))                    # Pinta la finestra de color roig
# input()
# pg.quit()                                 # Tanca la finestra i pygame

# --------------------------------

# pg.init()
# surface = pg.Surface((100,100))             # Creem una surface de 100x100
# surface.fill((0,255,0))                     # La pintem de verd
# screen = pg.display.set_mode((500,400))
# screen.fill((255,0,0))
# screen.blit(surface, (0,0))                 # Volquen la surface sobre la pantalla en la posició (0,0)
# pg.display.update()                         # Actualizem la finestra.
# input()
# pg.quit()

# --------------------------------

# pg.init()
# surface = pg.image.load('data/apple.png')     # Creem una surface a partir d'una imatge des d'un arxiu
# screen = pg.display.set_mode((500,400))
# screen.fill((255,0,0))
# screen.blit(surface, (0,0))
# pg.display.update()
# input()
# pg.quit()

# ----------------------------------

# pg.init()
# screen = pg.display.set_mode((500,400))
# pg.draw.circle(screen, (0,0,255), (50,50), 20, 2)      # Dibuixem un cercle directament en la pantalla.
# pg.display.update()
# input()
# pg.quit()

# ----------------------------------

# pg.init()
# surface = pg.Surface((100,100))                         # Creem una surface de 100x100
# pg.draw.circle(surface, (0,0,255), (50,50), 20, 2)      # Dibuixem en ella un cercle.
# screen = pg.display.set_mode((500,400))
# screen.fill((255,0,0))
# screen.blit(surface, (0,0))
# pg.display.update()
# input()
# pg.quit()

# ----------------------------------

# pg.init()
# surface = pg.image.load('data/apple.png')               # Creem una surface a partir d'una imatge des d'un arxiu 
# pg.draw.circle(surface, (0,0,255), (50,50), 20, 2)      # Dibuixem en ella un cercle.
# screen = pg.display.set_mode((500,400))
# screen.fill((255,0,0))
# screen.blit(surface, (0,0))
# pg.display.update()
# input()
# pg.quit()

# ----------------------------------

# pg.init()
# surface = pg.image.load('data/apple.png')
# surface = pg.transform.scale(surface, (150,150))          # escalem la imatge
# pg.draw.circle(surface, (0,0,255), (50,50), 20, 2)
# screen = pg.display.set_mode((500,400))
# screen.fill((255,0,0))
# screen.blit(surface, (0,0))
# pg.display.update()
# input()
# pg.quit()

# ----------------------------------

# pg.init()
# apple = pg.image.load('data/apple.png')
# screen = pg.display.set_mode((500,400))
# screen.fill((255,0,0))

# ## x1,y1,w1,h1 = surface.get_rect()       # recuperar els valors de get_rect()
# ## x2,y2,w2,h2 = screen.get_rect()

# rect_apple = apple.get_rect()
# rect_screen = screen.get_rect()
# rect_apple.center = rect_screen.center    # Modificar els valors de get_rect()
# screen.blit(apple, rect_apple)

# pg.display.update()
# input()
# pg.quit()

# ----------------------------------

# pg.init()
# apple = pg.image.load('data/apple.png')
# screen = pg.display.set_mode((500,400))
# screen.fill((255,0,0))

# rect_apple = apple.get_rect()
# rect_screen = screen.get_rect()
# rect_apple.center = rect_screen.center
# rect_apple.move_ip(100,100)                # Moure una imatge es canviar el seu rect.
# screen.blit(apple, rect_apple)

# pg.display.update()
# input()
# pg.quit()




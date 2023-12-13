#
# Delta time and framerate independence
# https://www.construct.net/en/tutorials/delta-time-framerate-23
#
# Suposem que movem un sprite 1 píxel cada frame: x = x + 1
# Un joc a 100fps implica que el moura a 100 pixels en un segon.
# El mateix joc a 50fps mourà el mateix sprite a 50 pixels per segon.
# Com en veu, la velocitat del moviment depen dels fps.
#
# Definim dt (delta time) com el temps que ha transcorregut des del tick anterior.
# Un joc a 100fps té un dt=1/100s
# Un joc a 50fps té un dt=1/50s
# Obsevem que, cada segon la suma dels dt=1.
#
# Suposem que ens volem moure a un velocitat v de 75px/s.
# Si enlloc de fer x=x+1, fem x=x+75·dt, significa que:
# En el joc a 100fps, en 1 segon ens mourem 75 pixels.
# En el joc a 50fps, en 1 segon ens mourem també 75 pixels.

# O siga, per aconseguir una velocitat de desplaçament v independent dels fps farem:
#  x = x + v·dt,  on dt=1/fps

# Podem afegir un factor d'escala, de manera que un factor 1 significa velocitat normal, 
# 0.5 el doble de lent, i 2 el doble de ràpid. A més, un factor de 0 significa pausar el moviment.
#  x = x + v·escala·dt,  on dt=1/fps

# Si modifiquen v, estem cambiant la velocitat, és a dir que accelerem el moviment.

# Enlloc d'utilitzar un dt general per a tot el joc podem que cada sprite tinga el seu propi dt.



# Interpolació línial (lerp)
# Si volem anar del punt a al punt b 



import pygame
import time

################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Calibri',40)
DISPLAY_W, DISPLAY_H = 480, 270
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
running = True
clock = pygame.time.Clock()
TARGET_FPS = 60
WHITE = (255,255,255)

################################# LOAD VARIABLES AND OBJECTS###################################
rect_pos = 0
timer:float = 0
prev_time = time.time()
dt:float = 0
record:float = 0
passed, start = False, False

velocity = 300
FPS = 70

################################# GAME LOOP ##########################
while running:
    # Limit framerate
    clock.tick(FPS)

    # Compute delta time
    now = time.time()
    dt = now - prev_time
    prev_time = now
   
    # Update the timer and move the rectangle
    if start:
        timer += dt
        rect_pos += int(velocity * dt)

    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = True

    if rect_pos > DISPLAY_W and not passed:
        record = timer
        passed = True

    ################################# UPDATE/ Animate SPRITE #################################
    countdown = font.render("Time: " +str(round(timer,5)), False, (255,255,255))
    fps_text = font.render("FPS: " +str(round(clock.get_fps(),2)), False, (255,255,255))

    ################################# UPDATE WINDOW AND DISPLAY #################################
    canvas.fill((0, 0, 0)) # Fills the entire screen with light blue
    canvas.blit(countdown, (0,0))
    canvas.blit(fps_text, (0, 50))
    pygame.draw.rect(canvas,WHITE,(rect_pos,DISPLAY_H/2 + 30,40,40))
    if record:
        record_text = font.render("Time: " +str(round(record,5)), False, (255,255,255))
        canvas.blit(record_text, (DISPLAY_W/4, DISPLAY_H/2))
    window.blit(canvas, (0,0))
    pygame.display.update()








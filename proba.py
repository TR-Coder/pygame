import pygame
import sys
import os

# Inicialitza Pygame
pygame.init()

# Crea una finestra
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Rotació d'Imatge amb Punt Personalitzat")

# Carrega una imatge
img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exercicis\\Exercici 1, metrònom\\assets', "barra.png")
image = pygame.image.load(img_path)
image_rect = image.get_rect(center=screen.get_rect().center)

# Punt de rotació personalitzat
pivot_x, pivot_y = 400, 300  # Canvia aquests valors segons les teves necessitats
angle = 0

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Augmenta l'angle
    angle += 1
    if angle >= 360:
        angle = 0

    # Crear una imatge més gran que conté la imatge original amb el punt de rotació al centre
    bigger_image = pygame.Surface((image_rect.width * 2, image_rect.height * 2), pygame.SRCALPHA)
    bigger_rect = bigger_image.get_rect()

    # Copiar la imatge original en la imatge més gran de manera que el punt de rotació estiga al centre
    offset_x = bigger_rect.width // 2 - pivot_x
    offset_y = bigger_rect.height // 2 - pivot_y
    bigger_image.blit(image, (offset_x, offset_y))

    # Rota la imatge més gran
    rotated_image = pygame.transform.rotate(bigger_image, angle)
    rotated_rect = rotated_image.get_rect(center=image_rect.center)

    # Dibuixa la imatge rotada
    screen.fill((0, 0, 0))
    screen.blit(rotated_image, rotated_rect.topleft)
    pygame.display.flip()

    # Controla la velocitat de rotació
    pygame.time.delay(30)
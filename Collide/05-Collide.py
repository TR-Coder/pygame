import pygame as pg

pg.init()
window = pg.display.set_mode((200, 200))
clock = pg.time.Clock()


rect = pg.Rect(0, 0, 40, 40)
rect.center = window.get_rect().center
speed = 5
outer = pg.display.get_surface().get_rect()

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False    

    if keys := pg.key.get_pressed():
        rect.x += (keys[pg.K_RIGHT] - keys[pg.K_LEFT]) * speed
        rect.y += (keys[pg.K_DOWN] - keys[pg.K_UP]) * speed  
        
        # x_ant = rect.x
        # rect.clamp(): moves the rectangle inside another
        # Si el rectangle interior se'n ix del exterior, es recalculen les coordenades de l'interior
        # per a fer-lo caure dins de l'exterior.
        # x_ant, y_ant = rect.x, rect.y
        rect.clamp_ip(outer)
        # if x_ant!=rect.x or y_ant!=rect.y:
        #     print(x_ant, rect.x, y_ant, rect.y)
        #     run = False

    window.fill(0)
    pg.draw.rect(window, (255, 0, 0), rect)
    pg.display.flip()
    clock.tick(60)

pg.quit()
exit()
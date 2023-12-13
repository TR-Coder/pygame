# Counter strike keycaps set
# Gateron G Pro 2.0 Switch
# glorious gmmk pro

# ==========
# Surface
# ==========
# Una surface és una imatge (llenç) sobre la qual podem dibuixar. Disposa del seu sitema de coordenades propi.
# 
# surface.blit(source, dest, area=None, special_flags=0)
#   - Pinta una imatge (la surface apuntada per source) sobre la surface.
#   - La coloca en la posició indicaca per les coordenades dest.
#   - area permet dibuixar només una zona específica de la imatge source. Per exemple, si source és una imatge de 100x100 de la qual
#     només volem dibuixar un quadrat de 50x50 en la mitat de la imatge, farem: screen.blit(image, (0, 0), (25, 25, 50, 50))
#
# Exemples
import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
image = pygame.image.load('mi_imagen.png')
screen.blit(image, (0, 0))
pygame.display.flip()

# ==========
# display
# ==========
# per a crear una finestra per al joc utilitzem display.set_mode(size, flags, depth, display, vsync)
# Size són les seues dimesions segons una tupla (with, height)
# Els flags són unes constants que indiquen el tipus de finestra com:
#   - pygame.FULLSCREEN	create a fullscreen display
#   - pygame.RESIZABLE	display window should be sizeable
#   - pygame.NOFRAME	display window will have no border or controls
#   - pygame.SHOWN	window is opened in visible mode (default)
#   - pygame.HIDDEN	window is opened in hidden mode
#   - etc.
#   
# amb pygame.display.set_mode((0, 0), pygame.FULLSCREEN) creem una finestra a pantalla completa.
# Per a crear una finestra que mantiga la barra de títols amb els controls de la finestra farem:
infoObject = pygame.display.Info()
screen_width, screen_height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((screen_width, screen_height))

# ===================
# mòdul pygame.locals
# ===================
# from pygame.locals import *
# Per comoditat utilitzarem les constants definides en el mòdul locals enlloc de les definides en els altres mòduls.

# =============
# Objecte Color
# =============
# color = pygame.Color(r, g, b, a=255)

# =============
# Esdeveniments
# =============
# Tots els esdeveniments són instàncies de la classe pygame.event.EventType
# Event Type	    attributes
# QUIT	            None
# ACTIVEEVENT	    gain, state
# KEYDOWN	        unicode, key, mod
# KEYUP	            key, mod
# MOUSEMOTION	    pos, rel, buttons
# MOUSEBUTTONUP	    pos, button
# MOUSEBUTTONDOWN	pos, button
# JOYAXISMOTION	    joy, axis, value
# JOYBALLMOTION	    joy, ball, rel
# JOYHATMOTION	    joy, hat, value
# JOYBUTTONUP	    joy, button
# JOYBUTTONDOWN	    joy, button
# VIDEORESIZE	    size, w, h
# VIDEOEXPOSE	    None
# USEREVENT	        Code


# ========================
# Esdeveniments del teclat
# ========================
# Pygame detecta els esdeveniments KEYUP i KEYDOWN
#
# Els atributs més útils de pygame.key
# .name(key:int)                                key attribute is an integer ID representing every key on the keyboard.
# .get_pressed()->ScancodeWrapper               get the state of all keyboard buttons
# .get_mods()->int                              determine which modifier keys are being held
# .set_repeat(delay:int, interval:int)->None	control how held keys are repeated
# .get_repeat()->Tuple(int,int)	                see how held keys are repeated
# .key_code(name:str)->int	                    get the key identifier from a key name
# .start_text_input()->None 	                start handling Unicode text input events
# .stop_text_input()->None  	                stop handling Unicode text input events
# #
# while True:
#    for event in pygame.event.get():
#         if event.type == pygame.KEYDOWN:
#             key=pygame.key.stop_text_input()
#             print (key, "Key is pressed")


# ========================
# Esdeveniments del ratolí
# ========================
# Pygame detecta els esdeveniments MOUSEMOTION, MOUSEBUTTONUP i MOUSEBUTTONDOWN.
# Els atributs més útils de pygame.mouse
# pygame.key.get_pressed()->ScancodeWrapper	        get the state of the mouse buttons
# pygame.mouse.get_pos()->Tuple[int, int]	        get the mouse cursor position
# pygame.mouse.get_rel()->Tuple[int, int]	        get the amount of mouse movement
# pygame.mouse.set_pos(x,y)->None	                set the mouse cursor position
# pygame.mouse.set_visible(bool)->int     	        hide or show the mouse cursor
# pygame.mouse.get_visible()->bool	                get the current visibility state of the mouse cursor
# pygame.mouse.get_focused()->bool	                check if the display is receiving mouse input
# pygame.mouse.set_cursor(...)->None	            set the image for the mouse cursor


# pygame.mouse.set_system_cursor(cursor:int)->None	set the mouse cursor to a system variant
#   Disposem de diferents cursors, pe:
#       pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)


# ============================
# Dibuixar formes geomètriques
# ============================
# Estan en el mòdul pygame.draw module
#
# draw a rectangle	        rect(surface, color, rect)
# draw a polygon	        polygon(surface, color, points)
# draw a circle	            circle(surface, color, center, radius)
# draw an ellipse	        ellipse(surface, color, rect)
# draw an elliptical arc	arc(surface, color, rect, start_angle, stop_angle)
# draw a straight line	    line(surface, color, start_pos, end_pos, width)
#
# Exemple: pygame.draw.polygon(screen, blue, ((25,75),(76,125),(275,200),(350,25),(60,280)))


# ============================
# Carregar imatges
# ============================
# img = pygame.image.load('pygame.png')

# import pygame
# pygame.init()
# screen = pygame.display.set_mode((400, 300))
# img = pygame.image.load('pygame.png')
# done = False
# bg = (127,127,127)
# while not done:
#    for event in pygame.event.get():
#       screen.fill(bg)
#       rect = img.get_rect()
#       rect.center = 200, 150
#       screen.blit(img, rect)          # Surface.blit() function to render the image −
#       if event.type == pygame.QUIT:
#       done = True
#    pygame.display.update()


# ============================
# Mostrar text
# ============================
# font = pygame.font.SysFont("Arial", 36)
# txtsurf = font.render("Hello, World", True, white)
# screen.blit(txtsurf,(200 - txtsurf.get_width() // 2, 150 - txtsurf.get_height() // 2))
#
# Els atributs més útils de pygame.font.
#
# bold()	        Gets or sets whether the font should be rendered in bold.
# italic()	        Gets or sets whether the font should be rendered in italics.
# underline()	    Gets or sets whether the font should be rendered with an underline.
# render()	        draw text on a new Surface
# size()	        calculate size needed to render text
# set_underline()	control if text is rendered with an underline
# get_underline()	check if text will be rendered with an underline
# set_bold()	    enable fake rendering of bold text
# get_bold()	    check if text will be rendered bold
# set_italic()	    enable fake rendering of italic text
# metrics()	        gets the metrics for each character
# get_italic()	    check if the text will be rendered italic
# get_linesize()	get the line space of the font text
# get_height()	    get the height of the font
# get_ascent()	    get the ascent of the font
# get_descent()	    get the descent of the font
#

# ==============================
# Moure una imatge amb el ratolí
# ==============================
# A computer game creates illusion of movement by drawing and erasing an object at incremental position.
# (mx,my) = pygame.mouse.get_pos()
# 


# ==============================
# Manejar objectes rectangulars
# ==============================
# La classe Pygame.Rect permet emmagatzemar i manipular àrees rectangulars.
# Disposa dels següents mètodes:
#
# copy()	            Returns a new rectangle having the same position and size as the original.
# move()	            Returns a new rectangle that is moved by the given offset. The x and y arguments can be any integer value, positive or negative.
# move_ip()	            Same as the Rect.move() method, but operates in place.
# inflate(x,y)	        Returns a new rectangle with the size changed by the given offset. Negative values will shrink the rectangle.
# inflate_ip(x, y)	    Same as the Rect.inflate() method, but operates in place.
# clamp(Rect)     	    Returns a new rectangle that is moved to be completely inside the argument Rect.
# clip(Rect)	        Returns a new rectangle that is cropped to be completely inside the argument Rect.
# union(Rect)	        Returns a new rectangle that completely covers the area of the two provided rectangles.
# union_ip(Rect)	    Same as the Rect.union() method, but operates in place.
# contains(Rect)	    Returns true when the argument is completely inside the Rect.
# collidepoint((x,y))	Returns true if the given point is inside the rectangle.
# colliderect(Rect) 	Returns true if any portion of either rectangle overlap





# https://www.tutorialspoint.com/pygame/pygame_display_modes.htm
# https://www.pygame.org/docs/#tutorials-reference-label
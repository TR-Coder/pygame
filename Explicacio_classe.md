
# Conceptes sobre videojocs
Els flux de dades que genera un vídeojoc seguix una jerarquia de capes que fluix des del codi font del llenguatge de programació fins arribar al monitor del jugador. Estos passos són:

    Codi del joc (Python, C++, C#, etc.)            # Un videojoc utilitza un motor gràfic (per exemple, Unity).
            ↓
    Motor gràfic (Pygame, Unity, Unreal)            # El motor gràfic crida funcions d’una API gràfica (ex.: OpenGL).
            ↓
    API gràfica (OpenGL, DirectX, Vulkan, SDL)      # L’API gràfica envia ordres al driver de la GPU.
            ↓
    Driver de la targeta gràfica                    # El driver traduïx les ordres en un llenguatge que la targeta gràfica entén.
            ↓
    Targeta gràfica (GPU)                           # La targeta gràfica processa la informació i envia el resultat a la pantalla.
            ↓
    Pantalla (Monitor)


Per a entendre-ho millor possem un símil: El motor gràfic enten ordres visuals com pinta un quadrat de tals dimensions en tal posició amb un color o una textura de fons determinada. L'API gràfica trandirira estes ordres an un llenguatque que el driver de la gràfica puga entrendre. El driver de la GPU ajustarà i optimitzarà este ordres perquè la targeta gràfica les execute de la manera més eficient. Finalment la GPU generarà els pixels que es mostraran per pantalla.


Per exemple:

- Nosaltres programarem en Python i utilitzarem una llibreria gràfica anomenada pygame. Pygame no és un motor gràfic complet com Unity o Unreal, sinó una col·lecció de mòduls que utilitza SDL per a gestionar gràfics, so i entrades.

- Pygame utilitza com a motor gràfic SDL (simple directmedia layer). SDL és un conjunt de llibreries multiplataforma (Windows, Linux, MacOS) desenvolupades amb C que proporciona funcions bàsiques per a realitzar operacions de dibuix 2D, gestió d'efectes de so i música, i càrrega i gestió d'imatges. Pygame actua com una capa d’abstracció sobre SDL, simplificant el seu ús en Python. Quan s'utilizen funcions de Pygame (per exemple, dibuixar una línia per pantalla), en realitat s’estan fent crides a SDL en segon pla.
 
- Els motors gràfics fan servir APIs gràfiques per a dibuixar a la pantalla. Per exemple, Unity pot utilitzar OpenGL o DirectX segons la plataforma.
Per defecte, SDL intenta utilitzar l'API més eficient disponible al sistema. En Windows 11, SDL per defecte farà servir Direct3D (DirectX) i en Ubuntu OpenGL o Vulkan si esta instal·lat i l'aplicació ho demana explícitament.


## Motor gràfic
Un motor gràfic és un conjunt de llibreries i eines que faciliten la creació de videojocs. Alguns exemples de motors gràfics són Unreal Engine, Godot, Pygame (tot i que Pygame és més una llibreria que un motor complet).

El motor gràfic permet crear els objectes que es dibuxaram per pantalla (com línies, rectangles, polígons, corbes, imatges, etc.). Proporciona també eines per a simular la física dels objectes com és el moviment i la detecció de col·lisions. També s'encarrega de l'àudio (efectes sonors i música). Els videojocs són programes dirigits per esdeveniments. El motor gràfic captura esdeveniments, com les polsacions del tecla i el moviment del ratolí, que el programa pot detecter i modificar l'estat del programa.

## API gràfica (Application Programming Interface)
La funció principal d'una API gràfica és actuar com una interfície estàndard entre el motor gràfic i el driver de la targeta gràfica, evitant que cada motor haja de comunicar-se de manera específica amb cada model de targeta. Fa de pont entre el codi del joc i el maquinari de la GPU. Les més conegudes són OpenGL (multiplataforma), Vulkan (successors d'OpenGL) i DirectX (API de Microsoft, usada en Windows i Xbox).


## Driver
Un driver és un programari que permet al sistema operatiu i les aplicacions comunicar-se directament amb la targeta gràfica. Hi ha moltes targetes gràfiques diferents (NVIDIA, AMD, Intel) i cadascuna té el seu propi driver. Si un motor gràfic haguera de parlar directament amb cada driver, hauria d’implementar codi específic per a cada fabricant i cada model de targeta. Això seria impracticable.Una API gràfica unifica la manera d’accedir al mauinari, fent que el motor gràfic funcione igual en qualsevol targeta

Els fabricants de targetes gràfiques optimitzen els seus drivers per a una API gràfica (OpenGL, Vulkan o Direct3D) el que permet que el motor gràfic es preocupe només de generar els gràfics, i deixe al driver la feina d’optimitzar-los per la targeta gràfica específica.

Sense una API gràfica, cada joc o motor hauria de conéixer detalls interns del maquinari. Amb una API gràfica, el motor només ha d’enviar ordres generals (com dibuixa un triangle) i la API s'encarrega de convertir-ho en ordres específiques per cada targeta.

## Targeta gràfica
Disposa d'un processador anomentat GPU (Graphics Processing Unit) especialitzat en el processament de gràfics.

## FPS (frames per segon)
Nombre d'imatges que la gràfica genera per segons i que envia al monitor per a la seua visualització.

## Shader
És un programa que executa la GPU i determina com es representen els píxels a la pantalla (llum, ombres, textures, etc.).


## V-Sync (Vertical Sync)
Sincronitza els FPS amb la taxa de refresc del monitor per evitar l’efecte "screen tearing".

## Renderitzar
Procés de generar la imatge final a partir d’un conjunt de dades (models 3D, textures, llums, càmeres, etc.), amb la finalitat de crear una imatge que es mostrarà en la pantalla. La renderització sol ser realitzada per l'API gràfica (OpenGL, DirectX, Vulkan) i implica tota una sèrie de càlculs intensius per transformar models 3D en les imatges que es mostraran.

La renderització implica una sèrie d'estapes:
    
+ __Transformacions geomètriques__: Transformar els models 3D a coordenades de càmera (matrius de transformació).
+ Aplicació de __textures__: Mapejar textures a la geometria del model.
+ Càlculs d'__il·luminació__: S’aplicaran efectes d'il·luminació per a determinar com la llum interactua amb la superfície.
+ __Sombrejat__: Determinar el color final de cada píxel o fragment.
+ __Rasterització__: Convertir la informació en una matriu de píxels (2D).
+ __Postprocessat__: Afegir efectes com difuminat, bloom, etc.

## Dibuix per pantalla
És el procés de mostrar la imatge generada per la renderització en la pantalla. Té dos etapes:

+ __Emmagatzemar la imatge renderitzada__\
Esta imatge (o frame) es guarda en una memòria intermèdia o "buffer" (doble buffer).

+ __Mostrar la imatge__\
Esta imatge es copia del buffer a la pantalla. En pygame es fa mitjançant la funció _pygame.display.flip()_.

## Doble buffer
És una tècnica usada en gràfics 2D i 3D per a evitar que els usuaris vegen processos de dibuix inacabats o defectes visuals en la pantalla. Funciona de la següent manera:

+ __Buffer primari__ (_front buffer_)\
    És el buffer visible, el que realment es veu a la pantalla. Esta imatge conté l'últim fotograma complet que l'usuari veu. La pantalla només pot mostrar el que hi ha en este buffer.

+ __Buffer secundari__ (_back buffer_)\
És el buffer intern que no es veu directament. En este buffer és on es genera el següent fotograma. Quan el sistema dibuixa o renderitza la nova imatge, ho fa en este buffer intern abans de mostrar-lo a l consumidor (usuari).

En un moment donat hi ha un intercanvi de buffers (__flip__ o swap) intercanviant el _back buffer_ amb el _front buffer_. Ara que el _front buffer_ conté la nova imatge, es mostra a la pantalla. Mentrestant, el _back buffer_ es queda lliure per a preparar el següent fotograma. Este procés es repetix contínuament.


# Pygame

## Estructura bàsica
El passos bàsics a considerar a l'hora de crear un joc en pygame són:
- Instal·lar la llibreria de pygame en el sistema.
- Importar la lliberia amb _import pygame_.
- Inicialitar pygame amb un _pygame.init()_.
- Crear la finestra on es pintarà el joc amb _display.set_mode()_.
- Crear el bucle principal del joc:
    - Conté la lògica del joc, manté el seu estat i genera les imatges.
    - Captura els esdeveniments del teclat i el ratolí.
    - Manté un velocitat constat d'imatges que s'envien a la pantalla (FPS).
    - En cada iteració del bucle es redibuixa la pantalla per a mostrar els canvis en el joc. 
- Tancar la finestra i pygame amb _pygame.quit()_.


## Surface(), fill(), blit() i update()
Una __Surface__ es un objecte que representa un llenç que s'utilitza per a representar qualsevol imatge. Es pot crear una amb el constructor _pygame.Surface()_ encara que en moltes ocasions són el retorn de cridar algun mètode. Els únics arguments necessaris són les dimensions d'una tupla (width, height). Sense arguments addicionals, la Surface es crearà en un format que s'ajuste millor a la superfície de la pantalla. El color inicial serà negre (0,0,0) i sense canal alfa. Si volem canal alfa ho inidiquem amb _pygame.SRCALPHA_.

Per a pintar una Surface amb un color sòlid tenim __pg.Surface.fill(color, rect=None)__, on color és una tupla (r,g,b,a). Si no es dóna cap argument _rect_, s'omplirà tota la superfície.

```python
surface = pg.Surface((200, 100))        # Surface sense canal alfa.
surface.fill((255, 0, 0))               # Roig pur, sense canal alfa
print(surface.get_at((0, 0)))           # Sense SRCALPHA → (255, 0, 0, 255)

surface_alpha = pg.Surface((200, 100), pygame.SRCALPHA)     # Amb canal alfa.
surface_alpha.fill((255, 0, 0, 128))                        # Roig amb 50% de transparència
print(surface_alpha.get_at((0, 0)))                         # Amb SRCALPHA  → (255, 0, 0, 128)
```

El mètode __blit(source, dest)__: dibuixa una imatge sobre una altra. El dibuix es pot posicionar amb l'argument _dest_. L'argument _dest_ pot ser un parell de coordenades (x,y) que representen la posició de la cantonada superior esquerra del blit o un __Rect__, on la cantonada superior esquerra del rectangle s'utilitzarà com a posició del blit.

Si volem mantindre la transparència d'una imatge, tant la imatge com la Surface sobre la que es bolca han de tindre canal alfa. Si la imatge té canal alfa però la Surface no, la imatge perdrà la transparència ja que la Surface no la sabrà gestionar. 

Pygame utilitza per defecte _single buffering_ el que significa que tot es dibuixa (amb sentencies de dibuix com blit(), fill(), circle(), etc.) en un únic buffer. Quan cridem a pg.display.update() o a pg.display.flip() és quan s'actualiza la pantalla. Amb flip() s'actualitza tota la pantalla mentre que amb update() podem indicar que només s'actualitze una zona en concret, per la qual cosa és útil per a optimitzar el rendiment en escenes amb pocs canvis. Amb _single buffering_ com que el dibuix es fa directament sobre la pantalla, poden hi haveri parpellejos (flickering) si el dibuix no es completa en un sol frame. També poden passar parpellejos en animacions ràpides, quan una imatge es dibuixa en diverses etapes (per exemple, primer el contorn i després l’interior) ja que el jugador pot vore frames incomplets.

Podem fer que Pygame utilitze doble buffer al crear la finestra amb el flag pygame.DOUBLEBUF. Els dibuixos es faran sobre una Surface situada en el _back buffer_.  Quan s'executa el mètode pg.display.flip(), es copia el contingut de la Surface del _back buffer_ al _front buffer_ i s'actualitza automàticament tota la pantalla. Convé usar doble buffer amb animacions o es dibuixa cada frame, ja que evita parpelleigs i millora el rendiment. Si a més s'afegixen els flags HWSURFACE i FULLSCREEN, Pygame intentarà accelerar el dibuix amb la GPU (si és compatible).
```python
screen = pg.display.set_mode((800, 600), pg.DOUBLEBUF | pg.HWSURFACE | pg.FULLSCREEN)
```

```python
import pygame as pg
pg.init()                                   # Inicialitza pygame
surface = pg.Surface((100,100))             # Creem una surface de 100x100
surface.fill((0,255,0))                     # La pintem de verd
screen = pg.display.set_mode((500,400))     # Crea una finestra de 500x400
screen.fill((255,0,0))                      # Pinta la finestra de color roig
screen.blit(surface, (0,0))                 # Volquen la surface sobre la pantalla en la posició (0,0)
pg.display.update()                         # Actualizem la finestra.
input()
pg.quit()                                   # Tanca la finestra i pygame
```


# load(), convert(), convert_alpha()
Per a carregar una imatge des d'un arxiu utilitzem load(ruta/imatge) la qual genera una Surface amb els colors i transparències tal i com estan en l'arxiu. En general, al carregar una imatge convé amplicar la funció convert() o convert_alpha(). 

El mètode __convert()__ crea una copia dels píxels d’una imatge i els adapta al format de la finestra on la dibuixarem. Per exemple, si la pantalla utilitza un model RGBA (32 píxels) i la imatge té 24 bits (RGB) sense canal alfa, sense convert, cada vegada que férem un blit(), pygame hauria de fer la conversió de 24 bits a 32 bits. Amb el convert() ho farem una vegada. A l’utilitzar convert(), és perd el canal alfa de la imatge original. Si no volem perdre’l hem d’utilitzar __convert_alpha()__.

```python
import pygame as pg
pg.init()
surface = pg.image.load('data/apple.png').convert()     # Creem una surface a partir d'una imatge des d'un arxiu
screen = pg.display.set_mode((500,400))
screen.fill((255,0,0))
screen.blit(surface, (0,0))
pg.display.update()
input()
pg.quit()
```

# Dibuixar formes geomètriques
Podem pintar formes geomètriques directament sobre una Surface amb funcions com pg.draw.circle() i pg.draw.rect().

```python
import pygame as pg
pg.init()
screen = pg.display.set_mode((500,400))
pg.draw.circle(screen, (0,0,255), (50,50), 20, 2)      # Dibuixem un cercle directament en la pantalla.
pg.display.update()
input()
pg.quit()
```


```python
import pygame as pg
pg.init()
surface = pg.Surface((100,100))                         # Creem una surface de 100x100
pg.draw.circle(surface, (0,0,255), (50,50), 20, 2)      # Dibuixem en ella un cercle.
screen = pg.display.set_mode((500,400))
screen.fill((255,0,0))
screen.blit(surface, (0,0))
pg.display.update()
input()
pg.quit()
```


```python
import pygame as pg
pg.init()
surface = pg.image.load('data/apple.png')               # Creem una surface a partir d'una imatge des d'un arxiu 
pg.draw.circle(surface, (0,0,255), (50,50), 20, 2)      # Dibuixem en ella un cercle.
screen = pg.display.set_mode((500,400))
screen.fill((255,0,0))
screen.blit(surface, (0,0))
pg.display.update()
input()
pg.quit()
```

# Escalat
Pygame permet fer una sèrie de transformacions sobre una Surface com escalar-la i rotar-la. Amb pg.transform,scale(surface, (w,h) indiquem la Surface i les seues noves dimensions. Amb pg.transform.rotate(Surface, degree) rotem degree graus antihorari.


```python
import pygame as pg
pg.init()
surface = pg.image.load('data/apple.png')
surface = pg.transform.scale(surface, (150,150))          # escalem la imatge
pg.draw.circle(surface, (0,0,255), (50,50), 20, 2)
screen = pg.display.set_mode((500,400))
screen.fill((255,0,0))
screen.blit(surface, (0,0))
pg.display.update()
input()
pg.quit()
```

# get_rect()
Un objecte Surface té una funció get_rect() que retorna un objecte pg.Rect(). Un àrea rectangular que representa les dimensions i cobrix tota la Surface començant en la posició (0,0) amb l’ample i l’alt de la Surface. A la funció get_rect() li podem passar uns arguments que s’aplicaran als atributs del rectangle abans de ser retornat.

Pygame utilitza objectes Rect per a emmagatzemar i manipular àrees rectangulars. Un objecte Rect es crea combinant els valors de left, top, width i height.

Rect disposa de diversos atributs que utilitzem per a moure i alinear un Rect.
    x,y
    top, left, bottom, right
    topleft, bottomleft, topright, bottomright
    midtop, midleft, midbottom, midright
    center, centerx, centery
    size, width, height
    w,h

L'assignació de size, width or height canvia les dimensions del rectangle.Totes les altres assignacions mouen el rectangle sense canviar-ne la mida. Alguns atributs són nombres enters i d'altres són parells de nombres enters.

Alguns mètodes molt emprats són:

- copy() -> Rect\
Retorna un rectangle nou amb la mateixa posició i mida que l'original.

- move() -> Rect\
Retorna un rectangle nou que es mou pel desplaçament donat. Els arguments x i y poden ser qualsevol valor enter, positiu o negatiu.

- move_ip(x, y) -> None\
Igual que el mètode Rect.move(), però no retorna un nou rectangle sinó que mou sobre el que s'aplica el mètode.

- inflate(x, y) -> Rect\
Retorna un nou rectangle nou amb la mida canviada pel desplaçament donat. El rectangle roman centrat al voltant del seu centre actual. Els valors negatius reduiran el rectangle. De manera anàloga tenim inflate_ip(x,y) que no retorna un nou rectangle sinó que unfla sobre el que s'aplica el mètode.

```python
import pygame as pg
pg.init()
apple = pg.image.load('data/apple.png')
screen = pg.display.set_mode((500,400))
screen.fill((255,0,0))

## x1,y1,w1,h1 = surface.get_rect()       # recuperar els valors de get_rect()
## x2,y2,w2,h2 = screen.get_rect()

rect_apple = apple.get_rect()
rect_screen = screen.get_rect()
rect_apple.center = rect_screen.center    # Modificar els valors de get_rect()
screen.blit(apple, rect_apple)

pg.display.update()
input()
pg.quit()
```

```python
import pygame as pg
pg.init()
apple = pg.image.load('data/apple.png')
screen = pg.display.set_mode((500,400))
screen.fill((255,0,0))

rect_apple = apple.get_rect()
rect_screen = screen.get_rect()
rect_apple.center = rect_screen.center
rect_apple.move_ip(100,100)                # Moure una imatge es canviar el seu rect.
screen.blit(apple, rect_apple)

pg.display.update()
input()
pg.quit()
```


# Cua d'esdeveniment tipus Event

```python
import pygame as pg
pg.init()
apple = pg.image.load('data/apple.png')
screen = pg.display.set_mode((500,400))


rect_apple = apple.get_rect()
rect_screen = screen.get_rect()
rect_apple.center = rect_screen.center

run = True
while run:
    screen.fill((255,0,0))
    for event in pg.event.get():        # Recorrer bucle esdeveniments
        if event.type == pg.QUIT:       # Verificar tipus esdeveniment
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                rect_apple.y -= 10
            elif event.key == pg.K_DOWN:
                rect_apple.y += 10
            elif event.key == pg.K_RIGHT:
                rect_apple.x += 10
            elif event.key == pg.K_LEFT:
                rect_apple.x -= 10

    screen.blit(apple, rect_apple)
    pg.display.update()

pg.quit()
```


# ----------------------------------

```python
import pygame as pg
pg.init()
apple = pg.image.load('data/apple.png')
screen = pg.display.set_mode((500,400))


rect_apple = apple.get_rect()
rect_screen = screen.get_rect()
rect_apple.center = rect_screen.center

run = True
while run:
    screen.fill((255,0,0))
    for event in pg.event.get():        # Recorrer bucle esdeveniments
        if event.type == pg.QUIT:       # Verificar tipus esdeveniment
            run = False
        elif event.type == pg.MOUSEMOTION:
            ## target_x, target_y =  pg.mouse.get_pos()
            x, y =  event.pos
            rect_apple.center = x,y

    screen.blit(apple, rect_apple)
    pg.display.update()

pg.quit()
```
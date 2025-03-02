from __future__ import annotations
import pygame as pg
from enum import Enum
import components

W = 800
H = 800
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)

# ------------------------------------------------------------------------------------------------------
class Color(Enum):
    RED=(0, 2000)
    YELLOW=(1, 1000)
    GREEN=(3, 2000)

    @property
    def ms(self) -> int:
        return self.value[1]


# ------------------------------------------------------------------------------------------------------
class TrafficLight(pg.sprite.Sprite):

    def __init__(self, group: pg.sprite.Group, initial_color:Color=Color.RED):
        super().__init__(group)
        self.group = group
        self.color = initial_color

        self.traffic_light_red    = components.load_image(r'assets/semafor_roig.png', scale=0.5)
        self.traffic_light_yellow = components.load_image(r'assets/semafor_grog.png', scale= 0.5)
        self.traffic_light_green  = components.load_image(r'assets/semafor_verd.png', scale=0.5)

        self.set_color(self.color)

    
    def next_color(self) -> Color:
        match self.color:
            case Color.RED:
                self.color = Color.YELLOW
            case Color.YELLOW:
                self.color = Color.GREEN
            case Color.GREEN:
                self.color = Color.RED      
        
        self.set_color(self.color)
        return self.color


    def set_color(self,  color:Color) -> None:
        match color:
            case Color.RED:
                self.image = self.traffic_light_red
            case Color.YELLOW:
                self.image = self.traffic_light_yellow
            case Color.GREEN:
                self.image = self.traffic_light_green
        
        self.rect = self.image.get_rect(center=screen_center) 

# ------------------------------------------------------------------------------------------------------
def clear_screen() -> None:
    screen.blit(bg, (0, 0))

# ------------------------------------------------------------------------------------------------------
def draw_speed(ms:int) -> None:
    surface = font.render(f'ms = {ms}', True, BLACK)
    screen.blit(surface, (50, 50))

# ------------------------------------------------------------------------------------------------------
def main() -> None:   
    traffic_light_group:pg.sprite.Group = pg.sprite.Group()
    traffic_light = TrafficLight(traffic_light_group, initial_color=Color.RED)

    buttons_group:pg.sprite.Group = pg.sprite.Group()
    button_right_img = components.load_image(r'assets/boto_fletxa_dreta.png', scale=0.3)
    button_left_img = components.load_image(r'assets/boto_fletxa_esquerra.png', scale=0.3)

    xright = screen_center[0] + screen.get_width()//4 - button_right_img.get_rect().width//2
    xleft  = screen_center[0] - screen.get_width()//4 - button_right_img.get_rect().width//2
    yright = 4 * screen.get_height()//5
    yleft  = 4 * screen.get_height()//5
    button_right = components.Button(x=xright, y=yright, radius=55, bg_color=BLACK, image=button_right_img, group=buttons_group)
    button_left  = components.Button(x=xleft,  y=yleft,  radius=55, bg_color=BLUE,  image=button_left_img,  group=buttons_group)

    timer = components.Timer(ms=Color.RED.ms, raise_events_regularly=True)

    main_loop = True
    while main_loop:

        mouse_click = components.MouseClick.NOT_PRESSED

        for event in pg.event.get():
            if event.type == pg.QUIT:
                main_loop = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = components.MouseClick.DOWN
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                mouse_click = components.MouseClick.UP
            if event.type == components.TIMER_EVENT:
                color = traffic_light.next_color()
                timer.again(ms=color.ms)

        clear_screen()

        if mouse_click != components.MouseClick.NOT_PRESSED:
            buttons_group.update(mouse_click)
            if button_right.clicked:
                color = traffic_light.next_color()
                timer.again(ms=color.ms)
            if button_left.clicked:
                color = traffic_light.next_color()
                timer.again(ms=color.ms)                

        traffic_light_group.draw(screen)
        buttons_group.draw(screen)
        
        pg.display.update()
        

# ------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((W,H))
    screen_center = screen.get_rect().center
    pg.display.set_caption('Traffic light')
    bg = pg.Surface(screen.get_size())
    bg.fill(WHITE)
    font = pg.font.Font(None, 36)
    main()
    pg.quit()
import pygame as pg

pg.init()

clock = pg.time.Clock()
fps = 1000

W = 600
H = 800

screen = pg.display.set_mode((W, H))
icon = pg.image.load('data/exp1.png')
pg.display.set_caption('Explosion Demo')
pg.display.set_icon(icon)

#define colours
bg_color = (50, 50, 50)

def draw_bg():
	screen.fill(bg_color)


#create Explosion class
class Explosion(pg.sprite.Sprite):
	def __init__(self, x, y):
		
		pg.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pg.image.load(f'data/exp{num}.png')
			img = pg.transform.scale(img, (100, 100))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 20
		self.counter += 1
		
		if self.counter >= explosion_speed:
			if self.index < len(self.images):
				self.image = self.images[self.index]
				self.index += 1
				self.counter = 0
			else:
				self.kill()


explosion_group:pg.sprite.Group = pg.sprite.Group()		

run = True
while run:
	clock.tick(fps)
	draw_bg()
	for event in pg.event.get():
		if event.type == pg.QUIT:
			run = False
		if event.type == pg.MOUSEBUTTONDOWN:
			x,y = pg.mouse.get_pos()
			explosion = Explosion(x,y)
			explosion_group.add(explosion)

	explosion_group.draw(screen)
	explosion_group.update()
	
	pg.display.update()

pg.quit()	
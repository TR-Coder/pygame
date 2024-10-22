import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 1000

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
icon = pygame.image.load('data/exp1.png')
pygame.display.set_caption('Explosion Demo')
pygame.display.set_icon(icon)

#define colours
bg = (50, 50, 50)

def draw_bg():
	screen.fill(bg)


#create Explosion class
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y):
		
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f'data/exp{num}.png')
			img = pygame.transform.scale(img, (100, 100))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 3
		self.counter += 1
		
		if self.counter >= explosion_speed:
			if self.index < len(self.images):
				self.image = self.images[self.index]
				self.index += 1
				self.counter = 0
			else:
				self.kill()


explosion_group = pygame.sprite.Group()			# type: ignore


run = True
while run:

	clock.tick(fps)
	draw_bg()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			explosion = Explosion(pos[0], pos[1])
			explosion_group.add(explosion)

	explosion_group.update()
	explosion_group.draw(screen)
	
	pygame.display.update()

pygame.quit()	
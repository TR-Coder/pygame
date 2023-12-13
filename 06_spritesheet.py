import pygame

class SpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame, width, height, scale, colour):
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)

		return image
	

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

sprite_sheet_image = pygame.image.load('data/doux.png').convert_alpha()
sprite_sheet = SpriteSheet(sprite_sheet_image)

BG = (50, 50, 50)
BLACK = (0, 0, 0)

animation_list = []
animation_steps = [4,6,3,4]
action = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 250
frame = 0
step_counter = 0


for animation in animation_steps:
	tmp_list = []
	for _ in range(animation):
		tmp_list.append(sprite_sheet.get_image(step_counter, 24, 24, 3, BLACK))
		step_counter += 1
	animation_list.append(tmp_list)

run = True
while run:

	#update background
	screen.fill(BG)

	current_time = pygame.time.get_ticks()
	if current_time - last_update >= animation_cooldown:
		frame += 1
		last_update = current_time
		if frame >= len(animation_list[action]):
			frame = 0

	#show frame image
	screen.blit(animation_list[action][frame], (0, 0))

	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN  and action>0:
				action -= 1
				frame = 0
			if event.key == pygame.K_UP  and action<len(animation_list)-1:
				action += 1
				frame = 0				

	pygame.display.update()

pygame.quit()

















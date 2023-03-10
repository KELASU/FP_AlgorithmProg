import pygame 

#button class
class Button():
	def __init__(self, surface, x, y, image, width, height):
		self.image = pygame.transform.scale(image, (width, height))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.surface = surface

	def draw(self):
		action = False

		#get the position of the mouse
		pos = pygame.mouse.get_pos()

		#check mouse click condition over a certain button
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw the buttons
		self.surface.blit(self.image, (self.rect.x, self.rect.y))

		return action
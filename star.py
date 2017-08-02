import pygame
from pygame.sprite import Sprite

class Star(Sprite):

	def __init__(self,ai_settings,screen):
		super(Star,self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		self.image = pygame.image.load('images/star.png')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.centery

	def blitme(self):
		self.screen.blit(self.image,self.rect)
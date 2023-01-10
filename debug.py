import pygame

class Debug_menu(object):
	def __init__(self) -> None:
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont("Verdana", 12)
		self.text = ""

	def render(self, surface, text):
		self.text = self.font.render(text, True, 'white')
		surface.blit(self.text, (10,10))


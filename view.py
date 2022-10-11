import pygame
import main
from monster import *

class View:
	def __init__(self, target=None):
		self.rect = pygame.Rect(0, 0, main.SCREEN_WIDTH, main.SCREEN_HEIGHT)
		self.target = target
		self.bg = main.backgrounds['stage1']
		self.bg_rect = self.bg.get_rect()
		self.font = pygame.font.SysFont("Verdana", 20)
		self.debug_text = []

	def update(self):
		if self.target:
			self.rect.center = self.target.pos

	def draw(self, screen):
		screen.fill('#71ddee')

		screen_rect = self.bg_rect.move(-self.rect.left, -self.rect.top)
		screen.blit(self.bg, screen_rect)

		for sprite in main.group.sprites():
			main.group.change_layer(sprite, sprite.pos.y)
			sprite.rect.center = sprite.pos - self.rect.topleft
		
		main.group.draw(screen)
		
		for sprite in main.group.sprites():
			if isinstance(sprite, Tree):
				hp_rect = pygame.Rect(sprite.rect.left, sprite.rect.bottom, sprite.rect.width, 8)
				pygame.draw.rect(screen, (0, 0, 0), hp_rect, 0, 5)
				
				border = main.HP_BAR_BORDER
				hp_rect = pygame.Rect(sprite.rect.left + border, sprite.rect.bottom + border,
									(sprite.rect.width - border * 2) * sprite.hp / sprite.mhp, 8 - border * 2)
				pygame.draw.rect(screen, (255, 0, 0), hp_rect, 0, 5)

		if main.DEBUG:
			for body in main.world.bodies:
				for fixture in body.fixtures:
					vertices = [body.transform * v * main.PPM - self.rect.topleft for v in fixture.shape.vertices]
					pygame.draw.polygon(screen, (192, 32, 32), vertices, 2)
				
		if main.DEBUG:
			# self.debug_text.append(round(self.clock.get_fps(), 2))
			self.debug_text.append(len(main.group))

			for idx, text in enumerate(self.debug_text):
				text = self.font.render(str(text), True, (0, 0, 0))
				screen.blit(text, (10, 10 + idx * 20))
			self.debug_text.clear()
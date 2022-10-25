import pygame
import ww
from instance import Instance
from monster import *

class Bullet(Instance):
	def __init__(self, pos):
		super().__init__(pos)
		self.speed = 80
		self.mhp = 20
		self.hp = self.mhp
		self.vel = pygame.math.Vector2(pygame.mouse.get_pos()) + ww.view.rect.topleft - pos
		self.vel.scale_to_length(self.speed)
		deg = pygame.math.Vector2().angle_to(self.vel)
		self.image_rad = (360 - deg) / 360 * 3.141592 * 2
		self.attack = 5
		
	def update(self):
		super().update()
		self.body.linearVelocity = self.vel

		for ce in self.body.contacts:
			if isinstance(ce.other.userData, Tree):
				ce.other.userData.hp -= self.attack
				self.hp = 0
				break

		if self.hp:
			self.hp -= 1
		else:
			self.kill()
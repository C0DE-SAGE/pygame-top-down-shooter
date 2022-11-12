import pygame
import ww
from instance import BulletInstance, BrightInstance
from monster import *
import numpy as np
from particle import Particle

class Bullet(BulletInstance, BrightInstance):
	def __init__(self, pos):
		super().__init__(pos)
		self.sprite_index = ww.sprites['bullet_idle']
		self.attack = 2
		self.dur = 20
		deg = pygame.math.Vector2().angle_to(self.vel)
		self.image_angle = deg / 360 * 3.141592 * 2
		
	def update(self):
		x = 1 - np.cos(self.t / self.dur * 2 * np.pi)
		self.light_diffuse = x * 0.05

		for ce in self.body.contacts:
			if isinstance(ce.other.userData, Tree):
				ce.other.userData.hp -= self.attack
				ce.other.userData.render_hit = True
				self.t = self.dur
				for _ in range(np.random.randint(2, 4)):
					ww.group.add(Particle(self.pos, self.vel))
				break

		super().update()
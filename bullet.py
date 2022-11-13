import pygame
import ww
from instance import BulletInstance, BrightInstance
from monster import *
import numpy as np
from particle import Particle
from vector import *

class Bullet(BulletInstance, BrightInstance):
	def __init__(self, pos):
		super().__init__(pos)
		self.sprite_index = ww.sprites['bullet_idle']
		self.attack = 2
		self.dur = 20
		self.image_angle = -(np.arctan2(*self.vel)) + np.pi / 2

	def update(self):
		x = 1 - np.cos(self.t / self.dur * 2 * np.pi)
		self.light_diffuse = x * 0.05

		for ce in self.body.contacts:
			if isinstance(ce.other.userData, Tree):
				ce.other.userData.hp -= self.attack
				ce.other.userData.render_hit = True
				ce.other.userData.image_color_mul = Vec4(0, 0, 0, 1)
				ce.other.userData.image_color_add = Vec4(1, 1, 1, 0)
				self.t = self.dur
				for _ in range(np.random.randint(2, 4)):
					ww.group.add(Particle(ww.sprites['particle'], self.pos, self.vel))
				break

		super().update()
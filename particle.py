from instance import TemporaryInstance, DrawableInstance
import ww
import pygame
import numpy as np

class Particle(TemporaryInstance, DrawableInstance):
	def __init__(self, pos, vel):
		super().__init__(pos)
		self.sprite_index = ww.sprites['particle']
		self.dur = 10
		vel.x += np.random.normal(scale=4)
		vel.y += np.random.normal(scale=4)
		pos += vel
		self.vel = vel
		self.image_angle = pygame.math.Vector2().angle_to(self.vel) / 360 * 3.141592 * 2
		self.image_xscale = 2
		self.image_yscale = 1
		self.image_speed = 0
		self.image_index = 0
		
	def update(self):
		self.pos += self.vel
		self.vel *= 0.5
		self.image_xscale *= 0.8
		super().update()

class Particle2(TemporaryInstance, DrawableInstance):
	def __init__(self, pos, vel):
		super().__init__(pos)
		self.sprite_index = ww.sprites['particle']
		self.dur = 25
		vel.x += np.random.normal(scale=4)
		vel.y += np.random.normal(scale=4)
		pos += vel
		self.vel = vel
		self.image_angle = pygame.math.Vector2().angle_to(self.vel) / 360 * 3.141592 * 2
		self.image_xscale = 2
		self.image_yscale = 1
		self.image_speed = 0
		self.image_index = 1
		
	def update(self):
		self.pos += self.vel
		self.vel *= 0.8
		self.image_xscale *= 0.8
		super().update()
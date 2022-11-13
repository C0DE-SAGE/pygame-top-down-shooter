from instance import DrawableInstance
import numpy as np

import pygame
class Particle(DrawableInstance):
	def __init__(self, sprite_index, pos, vel=(0,0), dur=10, image_color_mul=(1,1,1,1), dspd=0.5):
		super().__init__(pos)
		self.sprite_index = sprite_index
		self.dur = dur
		vel = pygame.Vector2(vel)
		vel += np.random.normal(scale=4), np.random.normal(scale=4)
		pos += vel
		self.vel = vel
		self.image_angle = pygame.Vector2().angle_to(self.vel) / 360 * 3.141592 * 2
		self.image_scale = pygame.Vector2(2, 1)
		self.image_speed = 0
		self.image_index = 0
		self.image_color_mul = image_color_mul
		self.dspd = dspd
		
	def update(self):
		self.pos += self.vel
		self.vel *= self.dspd
		self.image_scale.x *= 0.8
		if np.linalg.norm(self.vel) < 0.1:
			self.kill()
		super().update()
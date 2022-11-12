from instance import LifeInstance
import ww
from Box2D import *
import numpy as np
from particle import Particle2
import pygame

class Tree(LifeInstance):
	def __init__(self, pos):
		super().__init__(pos)
		self.sprite_index = ww.sprites['tree_idle']
		self.normals_index = ww.sprites['tree_idle_normal']
		self.speed = 5
		self.mhp = 30
		self.hp = self.mhp

	def update(self):
		vel = ww.player.pos - self.pos
		vel.Normalize()
		self.body.linearVelocity = vel * self.speed
		super().update()

	def kill(self):
		for _ in range(np.random.randint(15, 20)):
			dir = np.random.uniform(0, 360)
			spd = abs(np.random.normal(0, 6))
			vel = pygame.Vector2(np.cos(dir) * spd, np.sin(dir) * spd)
			ww.group.add(Particle2(self.pos, vel))
		super().kill()
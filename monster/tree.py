from instance import LifeInstance
import ww
from Box2D import *
import numpy as np
from particle import Particle2
import pygame
# from player import Player

class Tree(LifeInstance):
	def __init__(self, pos):
		super().__init__(pos)
		self.sprite_index = ww.sprites['tree_idle']
		self.normals_index = ww.sprites['tree_idle_normal']
		self.speed = 5
		self.mhp = 5
		self.hp = self.mhp
		self.attack = 1

	def update(self):
		vel = ww.player.pos - self.pos
		vel.Normalize()
		self.body.linearVelocity = vel * self.speed

		for ce in self.body.contacts:
			if ce.other.userData is ww.player:
				ce.other.userData.hp -= self.attack
				ce.other.userData.render_hit = True
				break

		super().update()

	def kill(self):
		for _ in range(np.random.randint(15, 20)):
			dir = np.random.uniform(0, 360)
			spd = abs(np.random.normal(0, 6))
			vel = pygame.Vector2(np.cos(dir) * spd, np.sin(dir) * spd)
			ww.group.add(Particle2(self.pos, vel))
			ww.view.add_shake(0.15, 0.15)
		super().kill()
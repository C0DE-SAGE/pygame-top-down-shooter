from instance import LifeInstance
import ww
from Box2D import *
import numpy as np
from particle import Particle
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
		self.gold = 5

	def update(self):
		if ww.phase == ww.PHASE.PLAY:
			vel = ww.player.pos - self.pos
		elif ww.phase == ww.PHASE.SHOP:
			vel = -(ww.player.pos - self.pos)
		# 	if not ww.view.rect.colliderect(self.aabb_rect):
		# 		self.kill()
		vel.Normalize()
		self.body.linearVelocity = vel * self.speed

		for ce in self.body.contacts:
			if ce.other.userData is ww.player:
				ce.other.userData.hp -= self.attack
				ce.other.userData.render_hit = True
				ce.other.userData.image_color_mul = 0, 0, 0, 1
				ce.other.userData.image_color_add = 1, 1, 1, 0
				break

		super().update()

	def dead(self):
		for _ in range(np.random.randint(15, 20)):
			dir = np.random.uniform(0, 360)
			spd = abs(np.random.normal(0, 6))
			vel = pygame.Vector2(np.cos(dir) * spd, np.sin(dir) * spd)
			ww.group.add(Particle(ww.sprites['particle'], self.pos, vel, dur=10, image_color_mul=(1, 0, 0, 1), dspd=0.8))
			ww.view.add_shake(0.15, 0.15)
		ww.player.gold += self.gold * ww.player.stat.gold_earn
		super().dead()
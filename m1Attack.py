import pygame
import ww
from instance import BulletInstance, BrightInstance, CollidableInstance, DrawableInstance
from monster import *
import numpy as np
from particle import Particle
from damage_number import DamageNumber
from random import random
from item import *

class M1Attack(BulletInstance, BrightInstance):
	def __init__(self, pos, stat: Status):
		super().__init__(pos)
		self.sprite_index = ww.sprites['skill_effect_m1']
		self.atk_multiplier = 1.1 # 스킬 공격력 계수
		self.dur = stat.atk_duration # 지속 시간
		self.speed = stat.atk_velocity # 탄속
		self.image_angle = -(np.arctan2(*self.vel)) + np.pi / 2
		self.image_scale = (1.5, 1.5)
		pygame.mixer.find_channel(True).play(ww.sounds['shot'])

	def update(self):
		x = 1 - np.cos(self.t / self.dur * 2 * np.pi)
		self.light_diffuse = x * 0.05

		for ce in self.body.contacts:
			if isinstance(ce.other.userData, Tree):
				crit = random() < ww.player.stat.crit
				damage = ww.player.stat.atk * self.atk_multiplier
				if crit:
					damage *= ww.player.stat.crit_atk
				ce.other.userData.hp -= damage
				ce.other.userData.render_hit = True
				ce.other.userData.image_color_mul = 0, 0, 0, 1
				ce.other.userData.image_color_add = 1, 1, 1, 0
				self.t = self.dur
				pygame.mixer.find_channel(True).play(ww.sounds['hit'])
				ww.group.add(DamageNumber(self.pos, damage, crit))
				for _ in range(np.random.randint(2, 4)):
					ww.group.add(Particle(ww.sprites['particle'], self.pos, self.vel))
				break

		super().update()

class M2Attack(CollidableInstance, DrawableInstance, BrightInstance):
	def __init__(self, pos, stat: Status):
		super().__init__(pos)
		self.sprite_index = ww.sprites['skill_effect_m2']
		self.atk_multiplier = 1.7 # 스킬 공격력 계수
		self.dur = stat.atk_duration # 지속 시간
		self.vel = (0, 0) # 탄속
		self.image_scale = (1.5, 1.5)
		self.image_speed = len(self.sprite_index) / stat.atk_duration
		self.t = 0
		pygame.mixer.find_channel(True).play(ww.sounds['번개떨구기'])

	def update(self):
		self.t += 1
		x = 1 - np.cos(self.t / self.dur * 2 * np.pi)
		self.light_color = 0, 1, 0
		self.light_diffuse = x * 0.3

		for ce in self.body.contacts:
			if isinstance(ce.other.userData, Tree):
				crit = random() < ww.player.stat.crit
				damage = ww.player.stat.atk * self.atk_multiplier
				if crit:
					damage *= ww.player.stat.crit_atk
				ce.other.userData.hp -= damage
				ce.other.userData.render_hit = True
				ce.other.userData.image_color_mul = 0, 0, 0, 1
				ce.other.userData.image_color_add = 1, 1, 1, 0
				self.t = self.dur
				pygame.mixer.find_channel(True).play(ww.sounds['hit'])
				ww.group.add(DamageNumber(self.pos, damage, crit))
				for _ in range(np.random.randint(2, 4)):
					ww.group.add(Particle(ww.sprites['particle'], self.pos, self.vel))
				break

		if self.image_index >= len(self.sprite_index) - .5:
			self.kill()
		super().update()
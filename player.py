import pygame
from instance import LifeInstance, BrightInstance
import ww
from bullet import Bullet

class Player(LifeInstance, BrightInstance):
	def __init__(self, pos):
		super().__init__(pos)
		self.sprite_index = ww.sprites['player_idle']
		self.speed = 8
		self.mhp = 100
		self.hp = self.mhp
		self.attack_time = 0
		self.attack_delay = 4
		self.image_index = 0

		self.light_ambient = 0.5
		self.light_diffuse = 0.5

	def update(self):
		super().update()
		self.direction = ww.controller.direction
		self.body.linearVelocity = self.direction * self.speed
			
		if ww.controller.mouse_left_down and self.attack_time == 0:
			ww.group.add(Bullet(self.pos))
			self.attack_time = self.attack_delay
		
		if ww.controller.horizontal == 1:
			self.image_xscale = 1
		if ww.controller.horizontal == -1:
			self.image_xscale = -1

		if ww.controller.direction and self.sprite_index == ww.sprites['player_idle']:
			self.sprite_index = ww.sprites['player_run']
			self.image_index = 0

		if not ww.controller.direction and self.sprite_index == ww.sprites['player_run']:
			self.sprite_index = ww.sprites['player_idle']
			self.image_index = 0
			
		self.attack_time = max(self.attack_time - 1, 0)

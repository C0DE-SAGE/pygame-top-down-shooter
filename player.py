from instance import LifeInstance, BrightInstance, DrawableInstance
import ww
from bullet import Bullet
import pygame
from monster import *
from monster_constuctor import MonsterConstuctor
from vector import *

class Player(LifeInstance, BrightInstance):
	def __init__(self, pos):
		super().__init__(pos)
		self.sprite_index = ww.sprites['player_idle']
		self.speed = 8
		self.mhp = 1000000
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
			self.image_scale.x = 1
		if ww.controller.horizontal == -1:
			self.image_scale.x = -1
			
		if ww.controller.direction and self.sprite_index == ww.sprites['player_idle']:
			self.sprite_index = ww.sprites['player_run']
			self.image_index = 0

		if not ww.controller.direction and self.sprite_index == ww.sprites['player_run']:
			self.sprite_index = ww.sprites['player_idle']
			self.image_index = 0
			
		self.attack_time = max(self.attack_time - 1, 0)

	def kill(self):
		ww.group.add(PlayerDeath(self))
		ww.view.add_flash()
		for sprite in ww.group:
			if isinstance(sprite, Tree):
				sprite.kill()
		ww.phase = ww.PHASE.DEAD
		super().kill()


class PlayerDeath(DrawableInstance, BrightInstance):
	def __init__(self, player):
		super().__init__(player.pos)
		self.sprite_index = ww.sprites['player_death']
		self.image_index = 0
		self.image_speed = 0.05
		self.image_scale = player.image_scale

		self.light_ambient = 0.5
		self.light_diffuse = 0.5
		self.light_color = Vec3(1, 1, 1)
	
	def update(self):
		self.light_color.yz *= 0.995
		if self.image_index >= len(self.sprite_index.images) - 1:
			self.image_speed = 0
		super().update()
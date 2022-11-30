from instance import LifeInstance, BrightInstance, DrawableInstance
import ww
from bullet import Bullet
import pygame
from monster import *
from item import *

class Player(LifeInstance, BrightInstance):
	def __init__(self, pos):
		super().__init__(pos)
		self.sprite_index = ww.sprites['player_idle']

		self.stat = Status()
		self.base_stat = Status()

		# 변동된 값 #
		self.hp = self.stat.mhp # 현재 체력
		self.gold = 0 # 현재 골드
		self.items_tier3 = [0 for _ in range(len(items_tier3_name))] # 획득한 아이템

		self.attack_time = 0
		self.image_index = 0

		self.light_diffuse = 0.5

	def apply_item(self):
		# 아이템 능력치를 적용하여 최종능력치를 갱신 #
		self.stat = self.base_stat
		self.stat.atk += self.items_tier3[0]
		self.stat.atk *= (1 + self.items_tier3[1] * 0.05)
		self.stat.mhp *= self.items_tier3[2] * 10
		self.stat.mhp *= (1 + self.items_tier3[3] * 0.05)

		## TODO

	def update(self):
		super().update()

		if ww.phase == ww.PHASE.PLAY:
			self.direction = ww.controller.direction
			self.body.linearVelocity = self.direction * self.stat.speed
				
			if ww.controller.mouse_left_down and self.attack_time <= 0:
				ww.group.add(Bullet(self.pos, self.stat))
				self.attack_time += 1
		else:
			self.body.linearVelocity = (0, 0)
		
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
			
		self.attack_time = max(self.attack_time - self.stat.atk_firerate / ww.FPS, 0)
		ww.view.debug_text.append(f'골드: {ww.player.gold}')

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

		self.light_diffuse = 0.5
		self.light_color = pygame.Vector3(1, 1, 1)
	
	def update(self):
		self.light_color.yz *= 0.995
		if self.image_index >= len(self.sprite_index.images) - 1:
			self.image_speed = 0
		super().update()
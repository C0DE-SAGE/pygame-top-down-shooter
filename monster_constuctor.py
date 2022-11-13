import ww
from monster import *
import numpy as np
import pygame

class MonsterConstuctor:
	def __init__(self):
		super().__init__()
		self.monster_list = ['Tree']
		self.pos = ww.view.rect.center
		self.t = 0
		self.dur = 14

	def update(self):
		self.t += 1
		if self.t == self.dur:
			sprite = ww.sprites['tree_idle']
			r = pygame.Vector2(sprite.images[0].get_bounding_rect().size)
			size = ww.SCREEN_SIZE + r
			line = np.random.uniform(0, (size.x + size.y) * 2)
			pos = -(r - (sprite.x, sprite.y))
			l = min(line, size.x)
			line = max(0, line - size.x)
			pos.x += l
			l = min(line, size.y)
			line = max(0, line - size.y)
			pos.y += l
			l = min(line, size.x)
			line = max(0, line - size.x)
			pos.x -= l
			l = min(line, size.y)
			line = max(0, line - size.y)
			pos.y -= l
			pos += ww.view.rect.topleft
			ww.group.add(Tree(pos))
			self.t = 0

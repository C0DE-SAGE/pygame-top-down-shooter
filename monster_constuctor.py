import ww
from monster import *
import numpy as np

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
			rw = sprite.images[0].get_bounding_rect().width
			rh = sprite.images[0].get_bounding_rect().height
			w = ww.SCREEN_SIZE[0] + rw
			h = ww.SCREEN_SIZE[1] + rh
			line = np.random.uniform(0, (w + h) * 2)
			x = -(rw - sprite.x)
			y = -(rh - sprite.y)
			l = min(line, w)
			line = max(0, line - w)
			x += l
			l = min(line, h)
			line = max(0, line - h)
			y += l
			l = min(line, w)
			line = max(0, line - w)
			x -= l
			l = min(line, h)
			line = max(0, line - h)
			y -= l
			x += ww.view.rect.left
			y += ww.view.rect.top
			ww.group.add(Tree((x, y)))
			self.t = 0

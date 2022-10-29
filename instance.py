import pygame
import ww
import Box2D

class Instance(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.sprite_index = None
		self.image_index = 0
		self.image_speed = 0.2
		self.image_angle = 0
		self.image_xflip = False

		self.pos = Box2D.b2Vec2(pos)
		self.body = ww.world.CreateDynamicBody(position=self.pos/ww.PPM)
		self.body.CreateFixture(ww.fixture_defs[self.__class__])
		self.body.fixedRotation = True
		self.body.userData = self

	def update(self):
		self.pos = self.body.transform.position * ww.PPM
		self.image_index = (self.image_index + self.image_speed) % len(self.sprite_index)

	def get_image(self):
		return self.sprite_index[int(self.image_index)]
	
	def kill(self):
		ww.world.DestroyBody(self.body)
		super().kill()
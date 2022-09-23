import random
import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((500,500))

class Star(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.image = pygame.image.load('oie_transparent.png').convert_alpha()
		self.rect = self.image.get_rect()
		alpha = pygame.Surface(self.rect.size, SRCALPHA)
		alpha.fill((255, 255, 255, 90))
		self.image.blit(alpha, (0, 0), special_flags=BLEND_RGBA_MULT)
		self.pos = pygame.math.Vector2(pos)
		direction = random.random() * 360
		speed = random.random() * 1 + 0.5
		self.dpos = pygame.math.Vector2(0, speed).rotate(direction)
		self.duration = random.random() * 5 + 100
		self.timer = 0
	
	def update(self):
		if self.timer < self.duration:
			self.timer += 1
			self.pos += self.dpos
		else:
			self.kill()
		

class ParticleEmitter:
	def __init__(self, pos, ctor, delay):
		self.pos = pos
		self.ctor = ctor
		self.delay = delay
		self.particles = pygame.sprite.Group()
		self.timer = 0
	
	def update(self):
		self.timer += 1
		if self.timer == self.delay:
			self.particles.add(self.ctor(self.pos))
			self.timer = 0
		self.particles.update()
	
	def render(self):
		surf = pygame.Surface((500, 500), SRCALPHA)
		surf.fill((0, 0, 0, 0))
		for particle in self.particles:
			surf.blit(particle.image, particle.pos, special_flags=BLEND_RGBA_ADD)
		screen.blit(surf, (0, 0))

emitter = ParticleEmitter(pygame.math.Vector2(150, 150), Star, 5)
clock = pygame.time.Clock()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill((0, 0, 0))
	emitter.update()
	emitter.render()
	pygame.display.update()
	clock.tick(60)
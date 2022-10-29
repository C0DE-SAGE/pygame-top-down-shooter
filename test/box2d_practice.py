import random
import pygame
from Box2D import *

screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()
FPS = 60
PPM = 10

world = b2World(gravity=(0, 0))

bodies = []
for i in range(1000):
	monster_body = b2BodyDef(position=(random.random() * 160, random.random() * 90), type=b2_dynamicBody)
	monster_body.angularVelocity = random.random() * 30 - 15
	monster_body.angle = random.random() * 3.14 * 2
	monster_body = world.CreateBody(monster_body)
	monster_shape = b2PolygonShape()
	monster_shape.SetAsBox(5, 0.1)
	monster_fixture = b2FixtureDef(shape=monster_shape, density=1, friction=0.5)
	monster_fixture = monster_body.CreateFixture(monster_fixture)
	bodies.append(monster_body)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			break
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				for body in bodies:
					body.angularVelocity -= 1
			if event.key == pygame.K_RIGHT:
				for body in bodies:
					body.angularVelocity += 1

	screen.fill((0, 0, 0, 0))

	for body in bodies:
		for fixture in body.fixtures:
			shape = fixture.shape
			vertices = [(body.transform * v) * PPM for v in shape.vertices]
			pygame.draw.polygon(screen, (128, 128, 128), vertices)

	world.Step(1 / FPS, 10, 10)
	pygame.display.flip()
	clock.tick(FPS)

pygame.quit()

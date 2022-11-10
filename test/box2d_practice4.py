import math
import random
import pygame
from Box2D import *

screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()
FPS = 60
PPM = 10

world = b2World(gravity=(0, 0))

vertices = []
for i in range(16):
	angle = math.pi * 2 / 16 * i
	x = math.cos(angle)
	y = math.sin(angle)
	vertices.append(b2Vec2(x, y))
shape = b2PolygonShape()
shape.vertices = vertices
fixture_def = b2FixtureDef(density=1.0, friction=0.1, restitution=0.1, isSensor=False)
fixture_def.shape = shape

bodies = []
for i in range(100):
	body = world.CreateBody(position=(random.random() * 160, random.random() * 90), type=b2_dynamicBody)
	body.CreateFixture(fixture_def)
	body.fixedRotation = True
	bodies.append(body)

shape = b2PolygonShape()
shape.SetAsBox(30, 1)
fixture_def = b2FixtureDef(density=1.0, friction=1.0, restitution=0.1, isSensor=False)
fixture_def.shape = shape
body = world.CreateBody(position=(80, 45), type=b2_staticBody)
body.CreateFixture(fixture_def)
bodies.append(body)

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
			color = (128, 128, 128)
			shape = fixture.shape
			if isinstance(shape, b2CircleShape):
				pygame.draw.circle(screen, color, center=body.transform * shape.pos * PPM, radius=shape.radius * PPM)
			elif isinstance(shape, b2PolygonShape):
				vertices = [(body.transform * v) * PPM for v in shape.vertices]
				pygame.draw.polygon(screen, color, vertices)
			elif isinstance(shape, b2ChainShape):
				vertices = [(body.transform * v) * PPM for v in shape.vertices]
				pygame.draw.polygon(screen, color, vertices)

	for body in bodies:
		a = (b2Vec2(pygame.mouse.get_pos()) - body.transform * body.fixtures[0].shape.centroid * PPM)
		a.Normalize()
		body.linearVelocity = a * 10
	world.Step(1 / FPS, 10, 10)
	pygame.display.flip()
	clock.tick(FPS)

pygame.quit()

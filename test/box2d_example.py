import pygame
from pygame.locals import *
from Box2D import *
from Box2D.b2 import *
SCREEN_WD = 600
SCREEN_HT = 400
TARGET_FPS = 60
PPM = 20.0
screen = pygame.display.set_mode((SCREEN_WD, SCREEN_HT), 0, 32)
pygame.display.set_caption("PyBox2D_Example")
clock = pygame.time.Clock()
world = b2World(gravity = (0, -10), doSleep = True)

ground1BodyDef = b2BodyDef()
ground1BodyDef.position.Set(0, 1)
ground1Body = world.CreateBody(ground1BodyDef)
ground1Shape = b2PolygonShape()
ground1Shape.SetAsBox(50, 5)
ground1Fixture = ground1Body.CreateFixture(shape = ground1Shape)

box1BodyDef = b2BodyDef()
box1BodyDef.type = b2_dynamicBody
box1BodyDef.position.Set(10, 15)
box1BodyDef.linearVelocity.Set(4, 0)
box1BodyDef.angularVelocity = 30
box1Body = world.CreateBody(box1BodyDef)
box1Shape = b2PolygonShape()
box1Shape.SetAsBox(2, 0.1)
box1FixtureDef = b2FixtureDef(shape=box1Shape)
box1FixtureDef.shape = box1Shape
box1FixtureDef.density = 1
box1FixtureDef.friction = 0.5
box1Fixture = box1Body.CreateFixture(box1FixtureDef)

timeStep = 1.0 / 60
velIters = 10
posIters = 10
colors = {b2_staticBody : (255,255,255,255), b2_dynamicBody : (127,127,127,255),}
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
            break

    screen.fill((0, 0, 0, 0))
    
    overlap = False
    for body in (ground1Body, box1Body):
        for fixture in body.fixtures:
            shape = fixture.shape
            vertices = [(body.transform * v) * PPM for v in shape.vertices]
            color = colors[body.type]
            if body.type == b2_dynamicBody:
                overlap = box1Body.contacts
                if overlap:
                    color = (255, 0, 0)

            pygame.draw.polygon(screen, color, vertices)

    world.Step(timeStep, velIters, posIters)
    pygame.display.flip()
    clock.tick(TARGET_FPS)

pygame.quit()
print("done")
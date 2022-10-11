import pygame
import Box2D
import main

class Instance(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        pos = Box2D.b2Vec2(pos)
        self.image = main.images[self.__class__]
        self.body = main.world.CreateDynamicBody(position=pos / main.PPM)
        self.body.CreateFixture(main.fixture_defs[self.__class__])
        self.body.fixedRotation = True
        self.body.userData = self
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.pos = self.body.transform.position * main.PPM
    
    def kill(self):
        main.world.DestroyBody(self.body)
        super().kill()
import random
import pygame
import moderngl
import ctypes
import sys

class SpriteObject(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() 
        self.image = image
        self.rect = self.image.get_rect(center = (x, y))
       
    def update(self, surface):
        keys = pygame.key.get_pressed()
        vel = 5
        if keys[pygame.K_LEFT]:
            self.rect.left = max(0, self.rect.left-vel)
        if keys[pygame.K_RIGHT]:
            self.rect.right = min(surface.get_width(), self.rect.right+vel)
        if keys[pygame.K_UP]:
            self.rect.top = max(0, self.rect.top-vel)
        if keys[pygame.K_DOWN]:
            self.rect.bottom = min(surface.get_height(), self.rect.bottom+vel)

pygame.init()
window = pygame.display.set_mode((500, 500))
image = pygame.image.load('test\graphics\VEkp8.png').convert_alpha()
clock = pygame.time.Clock()

# sprite_object = SpriteObject(*window.get_rect().center)

sprite_object = [SpriteObject(random.random() * window.get_rect().width, random.random() * window.get_rect().height) for _ in range(1000)]
group = pygame.sprite.LayeredUpdates(sprite_object)

t = 0
while True:
    if t == 60:
        print(clock.get_fps())
        t = 0
    else:
        t += 1
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    group.update(window)

    for sprite in group:
        group.change_layer(sprite, sprite.rect.centery)
    window.fill((0.2, 0.2, 0.2))
    group.draw(window)
    pygame.display.update()
    clock.tick(120)

pygame.quit()
exit()
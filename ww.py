import pygame

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

pygame.init()

group = pygame.sprite.Group()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Images:
    player = pygame.image.load('test/graphics/pixil-frame-0.png').convert_alpha()
    tree = pygame.image.load('test/graphics/tree.png').convert_alpha()
    bullet = pygame.image.load('test/graphics/bullet.png').convert_alpha()
    view = pygame.image.load('test/graphics/ground.png').convert_alpha()
import pygame
import Box2D
import math
from pygame.locals import *
from monster import *
from player import Player
from bullet import Bullet
from enum import IntEnum

WINDOW_SIZE = (1920, 1080)
SCREEN_SIZE = (1920, 1080)
# SCREEN_SIZE = (640, 360)
HP_BAR_BORDER = 2
FPS = 60
PPM = 20
DEBUG = True

pygame.init()

pygame.display.set_mode(WINDOW_SIZE, flags=pygame.DOUBLEBUF | pygame.OPENGL)

world = Box2D.b2World(gravity=(0, 0))

images = {
    Player: pygame.image.load('test/graphics/KakaoTalk_20221026_024937996.png').convert_alpha(),
    Tree: pygame.image.load('test/graphics/tree_origin.png').convert_alpha(),
    Bullet: pygame.image.load('test/graphics/bullet.png').convert_alpha(),
    'stage1': pygame.image.load('test/graphics/ground.png').convert_alpha()
}

normals = {
    Tree: pygame.image.load('test/graphics/tree_normal4_origin.png').convert_alpha(),
}

def _get_ellipsis_vertices(cls, pos, size):
    precision = 4
    vertices = []
    rect_size = images[cls].get_rect().size if cls else (1, 1)
    for i in range(precision):
        angle = math.pi * 2 / precision * i
        x = (math.cos(angle) * size[0] + pos[0]) * rect_size[0] / PPM
        y = (math.sin(angle) * size[1] + pos[1]) * rect_size[1] / PPM
        vertices.append(Box2D.b2Vec2(x, y))
    return vertices

class category_bits(IntEnum):
    PLAYER  = 0b0000_0000_0000_0001
    BULLET  = 0b0000_0000_0000_0010
    MONSTER = 0b0000_0000_0000_0100

fixture_defs = {
    Player: Box2D.b2FixtureDef(
        density=100.0, categoryBits=category_bits.PLAYER, maskBits=category_bits.MONSTER,
        shape=Box2D.b2PolygonShape(vertices=_get_ellipsis_vertices(Player, (0, 0.3), (0.4, 0.2))),
    ),
    Tree: Box2D.b2FixtureDef(
        density=0.1, categoryBits=category_bits.MONSTER, maskBits=category_bits.PLAYER | category_bits.MONSTER | category_bits.BULLET,
        shape=Box2D.b2PolygonShape(vertices=_get_ellipsis_vertices(Tree, (0, 0.3), (0.4, 0.2))),
    ),
    Bullet: Box2D.b2FixtureDef(
        density=0.1, categoryBits=category_bits.BULLET, maskBits=category_bits.MONSTER,
        shape=Box2D.b2PolygonShape(vertices=_get_ellipsis_vertices(Bullet, (0, 0), (0.5, 0.5))),
    ),
}
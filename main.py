import pygame
from pathlib import Path
import moderngl
import moderngl_window
from moderngl_window import geometry

from player import Player
from monster import *
from bullet import Bullet
import math
from enum import IntEnum
import Box2D

from monster_constuctor import MonsterConstuctor
from view import View
import random


SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
HP_BAR_BORDER = 2
FPS = 60
PPM = 20
DEBUG = True

class Runner(moderngl_window.WindowConfig):
	title = "이세계에 <강제 소환>당해서 스테이터스 체크를 해봤더니 8서클 대마법사였습니다?(임시) ~소환된 김에 마왕토벌하는 이세계 라이프~"
	window_size = (1600, 900)
	resolution = (1600, 900)
	resource_dir = (Path(__file__) / '../test/graphics').absolute()

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		pygame.init()
		self.screen = pygame.Surface(self.resolution, flags=pygame.SRCALPHA)
		self.texture = self.ctx.texture(self.resolution, 4)
		self.texture.filter = (moderngl.NEAREST, moderngl.NEAREST)

		self.texture_program = self.load_program('texture.glsl')
		# self.quad_texture = self.load_texture_2d('python-bg.png')
		self.quad_fs = geometry.quad_fs()

		global world
		global images
		global backgrounds
		global fixture_defs

		world = Box2D.b2World(gravity=(0, 0))

		images = {
			Player: pygame.image.load('test/graphics/pixil-frame-0.png').convert_alpha(),
			Tree: pygame.image.load('test/graphics/tree.png').convert_alpha(),
			Bullet: pygame.image.load('test/graphics/bullet.png').convert_alpha()
		}

		backgrounds = {
			'stage1': pygame.image.load('test/graphics/ground.png').convert_alpha()
		}

		def _get_ellipsis_vertices(cls, pos, size):
			precision = 16
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

		global group
		global player
		global view
		global monster_constructor

		group = pygame.sprite.LayeredUpdates()
		player = Player((640,360))
		group.add(player)
		view = View(target=player)
		monster_constructor = MonsterConstuctor()

		for i in range(50):
			random_x = random.randint(0,1000)
			random_y = random.randint(0,1000)
			group.add(Tree((random_x, random_y)))

	def render(self, time, frametime):
		world.Step(1 / FPS, 1, 1)
		group.update()
		view.update()

		self.ctx.enable(moderngl.BLEND)
		# Render background graphics
		# self.quad_texture.use()
		# self.texture_program['texture0'].value = 0
		# self.quad_fs.render(self.texture_program)

		# Render foreground objects
		self.texture.use()
		view.draw(self.screen)
		texture_data = self.screen.get_view('1')
		self.texture.write(texture_data)

		self.quad_fs.render(self.texture_program)

		self.ctx.disable(moderngl.BLEND)

moderngl_window.run_window_config(Runner, args=('--window', 'pygame2'))
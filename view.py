import pygame
import ww
from monster import *
import moderngl
import numpy as np

class View:
	def __init__(self, target=None):
		self.rect = pygame.Rect(0, 0, ww.SCREEN_WIDTH, ww.SCREEN_HEIGHT)
		self.target = target
		self.bg = ww.backgrounds['stage1']
		self.bg_rect = self.bg.get_rect()
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont("Verdana", 20)
		self.debug_text = []

		vshader = """
		#version 330
		in vec2 in_position;
		in vec2 in_uv;
		out vec2 v_uv;
		void main()
		{
			v_uv = in_uv;
			gl_Position = vec4(in_position, 0.0, 1.0);
		}
		"""

		fshader = """
		#version 330
		out vec4 fragColor;
		uniform sampler2D u_texture;
		in vec2 v_uv;
		void main() 
		{
			fragColor = texture(u_texture, v_uv);
		}
		"""
		self.ctx = moderngl.create_context()
		self.ctx.enable(moderngl.BLEND)
		program = self.ctx.program(vertex_shader=vshader, fragment_shader=fshader)
		self.vbo = self.ctx.buffer(None, reserve=6 * 5 * 4)
		self.vao = self.ctx.vertex_array(program, [(self.vbo, "2f4 2f4", "in_position", "in_uv")])
		self.textures = {}

		bg_texture = self.ctx.texture(self.bg_rect.size, 4, self.bg.get_buffer())
		bg_texture.swizzle = 'BGRA'
		self.textures[self.bg] = bg_texture

		vshader_prim = """
		#version 330
		in vec2 in_position;
		in vec4 in_color;
		out vec4 color;
		void main()
		{
			gl_Position = vec4(in_position, 0.0, 1.0);
			color = in_color;
		}
		"""

		fshader_prim = """
		#version 330
		in vec4 color;
		out vec4 fragColor;
		void main() 
		{
			fragColor = color;
		}
		"""
		program_prim = self.ctx.program(vertex_shader=vshader_prim, fragment_shader=fshader_prim)
		self.vbo_prim = self.ctx.buffer(None, reserve=8 * 6 * 4)
		self.vao_prim = self.ctx.vertex_array(program_prim, [(self.vbo_prim, "2f4 4f4", "in_position", "in_color")])


		self.pg_screen = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
		self.pg_texture = self.ctx.texture(self.rect.size, 4)
		self.pg_texture.filter = moderngl.NEAREST, moderngl.NEAREST

	def update(self):
		if self.target:
			self.rect.center = self.target.pos

	def draw_debug_text(self):
		for idx, text in enumerate(self.debug_text):
			text = self.font.render(str(text), True, (0, 0, 0))
			self.pg_screen.blit(text, (10, 10 + idx * 20))
		self.debug_text.clear()

	def draw(self):
		self.ctx.clear(0.5, 0.9, 0.95)

		screen_rect = self.bg_rect.move(-self.rect.left, -self.rect.top)

		def convert_vertex(pt, surface):
			return pt[0] / surface.get_width() * 2 - 1, 1 - pt[1] / surface.get_height() * 2 
		corners = [
			convert_vertex(screen_rect.bottomleft, self.pg_screen),
			convert_vertex(screen_rect.bottomright, self.pg_screen),
			convert_vertex(screen_rect.topright, self.pg_screen),
			convert_vertex(screen_rect.topleft, self.pg_screen)
		] 
		vertices_quad_2d = np.array([
			*corners[0], 0.0, 1.0, 
			*corners[1], 1.0, 1.0, 
			*corners[2], 1.0, 0.0,
			*corners[0], 0.0, 1.0, 
			*corners[2], 1.0, 0.0, 
			*corners[3], 0.0, 0.0
		], dtype=np.float32)
		self.vbo.write(vertices_quad_2d)
		self.textures[self.bg].use()
		self.vao.render()
		

		for sprite in ww.group.sprites():
			ww.group.change_layer(sprite, sprite.pos.y)
			sprite.rect.center = sprite.pos - self.rect.topleft
		
		# ww.group.draw(self.pg_screen)
		for sprite in ww.group:
			corners = [
				convert_vertex(sprite.rect.bottomleft, self.pg_screen),
				convert_vertex(sprite.rect.bottomright, self.pg_screen),
				convert_vertex(sprite.rect.topright, self.pg_screen),
				convert_vertex(sprite.rect.topleft, self.pg_screen)
			] 
			vertices_quad_2d = np.array([
				*corners[0], 0.0, 1.0, 
				*corners[1], 1.0, 1.0, 
				*corners[2], 1.0, 0.0,
				*corners[0], 0.0, 1.0, 
				*corners[2], 1.0, 0.0, 
				*corners[3], 0.0, 0.0
			], dtype=np.float32)
			
			self.vbo.write(vertices_quad_2d)

			if sprite.image not in self.textures:
				texture = sprite.image
				texture = self.ctx.texture(texture.get_size(), 4, texture.get_buffer())
				texture.swizzle = 'BGRA'
				self.textures[sprite.image] = texture
			self.textures[sprite.image].use()
			self.vao.render()
		

		
		self.pg_screen.fill((0, 0, 0, 0))
		for sprite in ww.group.sprites():
			if isinstance(sprite, Tree):
				hp_rect = pygame.Rect(sprite.rect.left, sprite.rect.bottom, sprite.rect.width, 8)
				pygame.draw.rect(self.pg_screen, (0, 0, 0), hp_rect, 0, 5)
				
				border = ww.HP_BAR_BORDER
				hp_rect = pygame.Rect(sprite.rect.left + border, sprite.rect.bottom + border,
									(sprite.rect.width - border * 2) * sprite.hp / sprite.mhp, 8 - border * 2)
				pygame.draw.rect(self.pg_screen, (255, 0, 0), hp_rect, 0, 5)

		if ww.DEBUG:
			for body in ww.world.bodies:
				for fixture in body.fixtures:
					vertices = [body.transform * v * ww.PPM - self.rect.topleft for v in fixture.shape.vertices]
					pygame.draw.polygon(self.pg_screen, (192, 32, 32), vertices, 2)
					# vertices = np.array([
					# 	[*convert_vertex(v, self.pg_screen), 1.0, 0.0, 0.0, 1.0]
					# 	for v in vertices
					# ], dtype=np.float32)
					# vertices = vertices.flatten()
					# # print(vertices)
					# self.vbo_prim.write(vertices)
					# self.vao_prim.render(moderngl.LINE_LOOP)
				
		if ww.DEBUG:
			self.debug_text.append(round(self.clock.get_fps(), 2))
			self.debug_text.append(len(ww.group))

			self.draw_debug_text()


		corners = [
			convert_vertex((0, ww.SCREEN_HEIGHT), self.pg_screen),
			convert_vertex((ww.SCREEN_WIDTH, ww.SCREEN_HEIGHT), self.pg_screen),
			convert_vertex((ww.SCREEN_WIDTH, 0), self.pg_screen),
			convert_vertex((0, 0), self.pg_screen)
		] 
		vertices_quad_2d = np.array([
			*corners[0], 0.0, 1.0, 
			*corners[1], 1.0, 1.0, 
			*corners[2], 1.0, 0.0,
			*corners[0], 0.0, 1.0, 
			*corners[2], 1.0, 0.0, 
			*corners[3], 0.0, 0.0
		], dtype=np.float32)
		self.vbo.write(vertices_quad_2d)
		self.pg_texture.use()
		self.pg_texture.write(self.pg_screen.get_view('1'))
		self.pg_texture.swizzle = 'BGRA'
		self.vao.render()

		self.clock.tick(ww.FPS)
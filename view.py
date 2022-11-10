import pygame
import ww
from monster import *
import moderngl
import numpy as np

class View:
	def __init__(self, target=None):
		self.rect = pygame.Rect((0, 0), ww.SCREEN_SIZE)
		self.target = target
		self.bg = ww.backgrounds['stage1']
		self.screen_quad = np.array([[-1, 1], [1, 1], [1, -1], [-1, -1]])
		self.font = pygame.font.SysFont("Verdana", 20)
		self.debug_text = []

		self.ctx = moderngl.create_context()
		self.ctx.enable_only(moderngl.BLEND)
		self.program = self.ctx.program(
			vertex_shader="""
				#version 330
				layout (location = 0) in vec2 in_uv;
				layout (location = 1) in vec2 in_position;
				out vec2 v_uv;
				void main()
				{
					gl_Position = vec4(in_position, 0.0, 1.0);
					v_uv = in_uv;
				}
			""",
			fragment_shader="""
				#version 330
				out vec4 fragColor;
				uniform sampler2D u_texture;
				in vec2 v_uv;
				void main() 
				{
					fragColor = texture(u_texture, v_uv);
				}
			"""
		)
		self.program2 = self.ctx.program(
			vertex_shader="""
				#version 330
				in vec2 in_position;
				in vec2 in_uv;
				out vec2 v_uv;
				out vec2 pos;
				void main()
				{
					gl_Position = vec4(in_position, 0.0, 1.0);
					v_uv = in_uv;
					pos = in_position;
				}
			""",
			fragment_shader="""
				#version 330
				in vec2 v_uv;
				in vec2 pos;
				out vec4 fragColor;
				uniform sampler2D u_texture;
				uniform sampler2D u_normal;
				uniform vec3 lightPos[60];

				void main() 
				{
					vec3 lightColor = vec3(1, 1, 1);
					vec3 col = texture(u_texture, v_uv).rgb;
					vec3 normal = normalize(texture(u_normal, v_uv).rgb - vec3(0.5, 0.5, 0.5));
					normal.x = -normal.x;
					vec3 lightDir = normalize(vec3(0, 0, 0.1) - vec3(pos, 0.0));

					float ambientStrength = 0.1;
					vec3 ambient = ambientStrength * lightColor;

					float diff = max(dot(normal, lightDir), 0.0);
					vec3 diffuse = diff * lightColor;

					vec3 result = (ambient + diffuse) * col;


					// result = normal;
					fragColor = vec4(result, 1.0);

					lightPos;
					u_normal;
					{
						fragColor = texture(u_texture, v_uv);
						vec3 lightColor = vec3(1, 1, 1);
						float ambientStrength = 0.5;
						vec3 ambient = ambientStrength * lightColor;
						fragColor.xyz *= ambient;
						u_normal * u_texture;

						float value = 1;
						value *= max(0.9, min(1, (distance(vec2(0.5, 0.5), v_uv) + 0.8) * 1));
						for (int i = 0; i < 60; ++i) {
							value *= max(0.2, min(1, distance(lightPos[i].xy, v_uv) * 10));
						}
						fragColor.rgb *= 1 - value;
					}
					
				}
			"""
		)
		self.program2['u_texture'] = 0
		self.program2['u_normal'] = 1

		self.vbo = self.ctx.buffer(None, reserve=4 * 4 * 4)
		self.vao = self.ctx.vertex_array(self.program, [(self.vbo, "2f4 2f4", "in_position", "in_uv")])
		
		images = []
		for image in ww.backgrounds.values():
			images.append(image)
		for sprite in ww.sprites.values():
			for image in sprite:
				images.append(image)

		self.textures = {}
		for image in images:
			texture = self.ctx.texture(image.get_size(), 4, image.get_buffer())
			texture.swizzle = 'BGRA'
			self.textures[image] = texture

		self.pg_screen = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
		self.pg_texture = self.ctx.texture(self.rect.size, 4)
		self.pg_texture.filter = moderngl.NEAREST, moderngl.NEAREST

		self.texture_layer = self.ctx.texture(self.rect.size, 4)
		self.texture_layer.filter = moderngl.NEAREST, moderngl.NEAREST
		self.texture_layer_fbo = self.ctx.framebuffer(self.texture_layer)
		self.normal_layer = self.ctx.texture(self.rect.size, 4)
		self.normal_layer.filter = moderngl.NEAREST, moderngl.NEAREST
		self.normal_layer_fbo = self.ctx.framebuffer(self.normal_layer)
		self.vao2 = self.ctx.vertex_array(self.program2, [(self.vbo, "2f4 2f4", "in_position", "in_uv")])

	def update(self):
		if self.target:
			self.rect.center = self.target.pos

	def draw_debug_text(self):
		for idx, text in enumerate(self.debug_text):
			text = self.font.render(str(text), True, (0, 0, 0))
			self.pg_screen.blit(text, (10, 10 + idx * 20))
		self.debug_text.clear()

	def draw(self):
		def get_gl_coord(pt, screen, rad=0, center=None):
			if rad != 0:
				center = center or (0, 0)
				rot = np.array([
					[np.cos(rad), -np.sin(rad)],
					[np.sin(rad), np.cos(rad)],
				])
				pt = rot.dot((pt[0] - center[0], pt[1] - center[1])) + center
			return pt[0] / screen.get_width() * 2 - 1, pt[1] / screen.get_height() * 2 - 1

		def get_gl_corner(rect, screen, rad=0, center=None):
			center = center or rect.center
			return [
				get_gl_coord(rect.bottomleft, screen, rad, center),
				get_gl_coord(rect.bottomright, screen, rad, center),
				get_gl_coord(rect.topright, screen, rad, center),
				get_gl_coord(rect.topleft, screen, rad, center)
			]

		def get_vertices_quad(rect, screen, rad=0, center=None, flip=False):
			corners = get_gl_corner(rect, screen, rad, center=center)
			if flip:
				return np.array([
					*corners[0], 1.0, 1.0,
					*corners[1], 0.0, 1.0,
					*corners[2], 0.0, 0.0,
					*corners[3], 1.0, 0.0,
				], dtype=np.float32)
			return np.array([
				*corners[0], 0.0, 1.0,
				*corners[1], 1.0, 1.0,
				*corners[2], 1.0, 0.0,
				*corners[3], 0.0, 0.0,
			], dtype=np.float32)

		def get_quad(rect):
			return np.array([rect.topleft, rect.topright, rect.bottomright, rect.bottomleft])

		def gl_scaling(quad):
			quad = (quad - self.rect.topleft) / ww.SCREEN_SIZE * 2 - 1
			return quad
		
		def attach_uv(quad):
			uv = np.array([
				[0, 0], [1, 0], [1, 1], [0, 1],
			])
			return np.hstack([quad, uv]).astype(np.float32)

		def draw_texture(quad, texture):
			if isinstance(quad, pygame.rect.Rect):
				quad = get_quad(quad)
			quad = gl_scaling(quad)
			quad = attach_uv(quad)
			self.vbo.write(quad)
			texture.use()
			self.vao.render(moderngl.TRIANGLE_FAN)

		def draw_screen(texture):
			quad = attach_uv(self.screen_quad)
			self.vbo.write(quad)
			texture.use()
			self.vao.render(moderngl.TRIANGLE_FAN)
		
		# Render Texture Layer
		self.texture_layer_fbo.clear(0.5, 0.9, 0.95, 1)
		self.texture_layer_fbo.use()
		draw_texture(self.bg.get_rect(), self.textures[self.bg])
		
		for sprite in ww.group:
			ww.group.change_layer(sprite, sprite.pos.y)
		for sprite in ww.group:
			draw_texture(sprite.get_quad(), self.textures[sprite.get_image()])

		# Render Pygame Layer
		self.pg_screen.fill((0, 0, 0, 0))
		for sprite in ww.group:
			if isinstance(sprite, Tree):
				hp_rect = sprite.get_aabb_rect().move(-self.rect.left, -self.rect.top)
				hp_rect = hp_rect.move(0, hp_rect.height + 2)
				hp_rect.height = 4
				pygame.draw.rect(self.pg_screen, (0, 0, 0), hp_rect, 0, 5)
				
				hp_rect = hp_rect.inflate(-2, -2)
				hp_rect.width *= sprite.hp / sprite.mhp
				pygame.draw.rect(self.pg_screen, (255, 0, 0), hp_rect, 0, 5)

		if ww.DEBUG:
			for sprite in ww.group:
				vertices = sprite.get_vertices() - self.rect.topleft
				pygame.draw.polygon(self.pg_screen, (192, 32, 32), vertices, 1)
			self.draw_debug_text()

		self.pg_texture.write(self.pg_screen.get_view('1'))
		self.pg_texture.swizzle = 'BGRA'

		# Render Normal Layer
		self.normal_layer_fbo.clear(0.5, 0.5, 1, 1)
		self.normal_layer_fbo.use()
		for sprite in ww.group:
			normal = sprite.get_normali()
			if normal:
				draw_texture(sprite.get_quad(), self.textures[normal])
		
		# Lighting
		lightPos = []
		for sprite in ww.group:
			lightPos.append(gl_scaling(np.array(sprite.pos)))
			lightPos[-1] = (lightPos[-1][0] / 2 + .5, lightPos[-1][1] / 2 + .5, 0)

		# lightPos = [gl_scaling(ww.player.pos, self.pg_screen)]
		# lightPos[-1] = (lightPos[-1][0] / 2 + .5, lightPos[-1][1] / 2 + .5, 0.1)
		
		if len(lightPos) > 60:
			lightPos = lightPos[:60]
		else:
			lightPos.extend([(-2, -2, 0) for i in range(60 - len(lightPos))])
		self.program2['lightPos'].value = lightPos

		# Integrate Layers
		self.ctx.screen.use()
		self.vbo.write(attach_uv(self.screen_quad))

		self.texture_layer.use(location=0)
		self.normal_layer.use(location=1)
		self.vao2.render(moderngl.TRIANGLE_FAN)

		self.pg_texture.use()
		self.vao.render(moderngl.TRIANGLE_FAN)
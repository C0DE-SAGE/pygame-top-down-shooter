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
		self.bg_rect = self.bg.get_rect()
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
					pos = in_position;
					pos.y = -pos.y;
					gl_Position = vec4(pos, 0.0, 1.0);
					v_uv = in_uv;
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
					

					float ambientStrength = 0.5;
					vec3 ambient = ambientStrength * lightColor;

					float diff = max(dot(normal, lightDir), 0.0);
					vec3 diffuse = diff * lightColor;

					vec3 result = (ambient + diffuse) * col;


					// result = normal;
					fragColor = vec4(result, 1.0);

					lightPos;
					u_normal;
					
					// fragColor = texture(u_texture, v_uv);
					// vec3 lightColor = vec3(1, 1, 1);
					// float ambientStrength = 0.1;
					// vec3 ambient = ambientStrength * lightColor;
					// fragColor.xyz *= ambient;
					// lightPos;
					// u_normal * u_texture;

					// float value = 1;
					// value *= max(0.9, min(1, (distance(vec2(0.5, 0.5), v_uv) + 0.8) * 1));
					// for (int i = 0; i < 60; ++i) {
					// 	value *= max(0.9, min(1, distance(lightPos[i], v_uv) * 10));
					// }
					// fragColor.rgb *= 1 - value;
				}
			"""
		)
		self.program2['u_texture'] = 0
		self.program2['u_normal'] = 1
		self.program3 = self.ctx.program(
			vertex_shader="""
				#version 330
				attribute vec3 inputPosition;
				attribute vec2 inputTexCoord;
				attribute vec3 inputNormal;

				uniform mat4 projection, modelview, normalMat;

				varying vec3 normalInterp;
				varying vec3 vertPos;

				void main() {
					gl_Position = projection * modelview * vec4(inputPosition, 1.0);
					vec4 vertPos4 = modelview * vec4(inputPosition, 1.0);
					vertPos = vec3(vertPos4) / vertPos4.w;
					normalInterp = vec3(normalMat * vec4(inputNormal, 0.0));
				}
			""",
			fragment_shader="""
				#version 330
				precision mediump float;

				in vec3 normalInterp;
				in vec3 vertPos;

				uniform int mode;

				const vec3 lightPos = vec3(1.0, 1.0, 1.0);
				const vec3 lightColor = vec3(1.0, 1.0, 1.0);
				const float lightPower = 40.0;
				const vec3 ambientColor = vec3(0.1, 0.0, 0.0);
				const vec3 diffuseColor = vec3(0.5, 0.0, 0.0);
				const vec3 specColor = vec3(1.0, 1.0, 1.0);
				const float shininess = 16.0;
				const float screenGamma = 2.2; // Assume the monitor is calibrated to the sRGB color space

				void main() {

				vec3 normal = normalize(normalInterp);
				vec3 lightDir = lightPos - vertPos;
				float distance = length(lightDir);
				distance = distance * distance;
				lightDir = normalize(lightDir);

				float lambertian = max(dot(lightDir, normal), 0.0);
				float specular = 0.0;

				if (lambertian > 0.0) {

					vec3 viewDir = normalize(-vertPos);

					// this is blinn phong
					vec3 halfDir = normalize(lightDir + viewDir);
					float specAngle = max(dot(halfDir, normal), 0.0);
					specular = pow(specAngle, shininess);
					
					// this is phong (for comparison)
					if (mode == 2) {
					vec3 reflectDir = reflect(-lightDir, normal);
					specAngle = max(dot(reflectDir, viewDir), 0.0);
					// note that the exponent is different here
					specular = pow(specAngle, shininess/4.0);
					}
				}
				vec3 colorLinear = ambientColor +
									diffuseColor * lambertian * lightColor * lightPower / distance +
									specColor * specular * lightColor * lightPower / distance;
				// apply gamma correction (assume ambientColor, diffuseColor and specColor
				// have been linearized, i.e. have no gamma correction in them)
				vec3 colorGammaCorrected = pow(colorLinear, vec3(1.0 / screenGamma));
				// use the gamma corrected color in the fragment
				gl_FragColor = vec4(colorGammaCorrected, 1.0);
				}
			"""
		)

		self.vbo = self.ctx.buffer(None, reserve=4 * 4 * 4)
		self.vao = self.ctx.vertex_array(self.program, [(self.vbo, "2f4 2f4", "in_position", "in_uv")])
		
		self.textures = {}
		for image in ww.backgrounds.values():
			texture = self.ctx.texture(image.get_size(), 4, image.get_buffer())
			texture.swizzle = 'BGRA'
			self.textures[image] = texture

		for sprite in ww.sprites.values():
			for image in sprite:
				texture = self.ctx.texture(image.get_size(), 4, image.get_buffer())
				texture.swizzle = 'BGRA'
				self.textures[image] = texture

		self.pg_screen = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
		self.pg_texture = self.ctx.texture(self.rect.size, 4)
		self.pg_texture.filter = moderngl.NEAREST, moderngl.NEAREST

		self.texture_layer = self.ctx.texture(ww.SCREEN_SIZE, 4)
		self.texture_layer.filter = moderngl.NEAREST, moderngl.NEAREST
		self.texture_layer_fbo = self.ctx.framebuffer(self.texture_layer)
		self.normal_layer = self.ctx.texture(ww.SCREEN_SIZE, 4)
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

		self.texture_layer_fbo.clear(0.5, 0.9, 0.95, 1)
		self.texture_layer_fbo.use()

		screen_rect = self.bg_rect.move(-self.rect.left, -self.rect.top)
		vertices_quad_2d = get_vertices_quad(screen_rect, self.pg_screen)
		self.vbo.write(vertices_quad_2d)
		self.textures[self.bg].use()
		self.vao.render(moderngl.TRIANGLE_FAN)
		
		for sprite in ww.group:
			pos = sprite.body.transform * sprite.body.fixtures[0].shape.centroid * ww.PPM - self.rect.topleft
			ww.group.change_layer(sprite, pos[1])
		
		for sprite in ww.group:
			image = sprite.sprite_index[int(sprite.image_index)]
			vertices_quad_2d = get_vertices_quad(image.get_rect(center=sprite.pos - self.rect.topleft), self.pg_screen, rad=3.14 * 2 - sprite.image_angle, flip=sprite.image_xflip)
			self.vbo.write(vertices_quad_2d)
			self.textures[image].use()
			self.vao.render(moderngl.TRIANGLE_FAN)
		
		self.pg_screen.fill((0, 0, 0, 0))
		# for sprite in ww.group.sprites():
		# 	if isinstance(sprite, Tree):
		# 		hp_rect = pygame.Rect(sprite.rect.left, sprite.rect.bottom, sprite.rect.width, 8)
		# 		pygame.draw.rect(self.pg_screen, (0, 0, 0), hp_rect, 0, 5)
				
		# 		border = ww.HP_BAR_BORDER
		# 		hp_rect = pygame.Rect(sprite.rect.left + border, sprite.rect.bottom + border,
		# 							(sprite.rect.width - border * 2) * sprite.hp / sprite.mhp, 8 - border * 2)
		# 		pygame.draw.rect(self.pg_screen, (255, 0, 0), hp_rect, 0, 5)

		if ww.DEBUG:
			for body in ww.world.bodies:
				for fixture in body.fixtures:
					vertices = [body.transform * v * ww.PPM - self.rect.topleft for v in fixture.shape.vertices]
					pygame.draw.polygon(self.pg_screen, (192, 32, 32), vertices, 2)
				
		if ww.DEBUG:
			self.draw_debug_text()

		vertices_quad_2d = get_vertices_quad(pygame.rect.Rect((0, 0), ww.SCREEN_SIZE), self.pg_screen)
		self.vbo.write(vertices_quad_2d)
		self.pg_texture.use()
		self.pg_texture.write(self.pg_screen.get_view('1'))
		self.pg_texture.swizzle = 'BGRA'
		self.vao.render(moderngl.TRIANGLE_FAN)


		self.normal_layer_fbo.clear(0.5, 0.5, 1, 1)
		self.normal_layer_fbo.use()
		# for sprite in ww.group:
		# 	if sprite.normal:
		# 		vertices_quad_2d = get_vertices_quad(sprite.rect, self.pg_screen, 3.14 * 2 - sprite.image_rad)
		# 		self.vbo.write(vertices_quad_2d)
		# 		self.normals[sprite.normal].use()
		# 		self.vao.render(moderngl.TRIANGLE_FAN)


		# lightPos = []
		# for sprite in ww.group:
		# 	lightPos.append(get_gl_coord(sprite.rect.center, self.pg_screen))
		# 	lightPos[-1] = (lightPos[-1][0] / 2 + .5, lightPos[-1][1] / 2 + .5, 0)

		lightPos = [get_gl_coord(ww.player.pos, self.pg_screen)]
		lightPos[-1] = (lightPos[-1][0] / 2 + .5, lightPos[-1][1] / 2 + .5, 0.1)
		
		if len(lightPos) > 60:
			lightPos = lightPos[:60]
		else:
			lightPos.extend([(-2, -2, 0) for i in range(60 - len(lightPos))])
		self.program2['lightPos'].value = lightPos
		vertices_quad_2d = get_vertices_quad(pygame.rect.Rect((0, 0), ww.SCREEN_SIZE), self.pg_screen)
		self.vbo.write(vertices_quad_2d)
		self.ctx.screen.use()
		self.texture_layer.use(location=0)
		self.normal_layer.use(location=1)
		self.vao2.render(moderngl.TRIANGLE_FAN)
import pygame
import moderngl
import random
import sys
import numpy as np
from PIL import Image

class Plane(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__() 
		self.image = pygame.image.load('test\graphics\VEkp8.png').convert_alpha()
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

N = 1000

framebuffer_size = (500, 500)

# pygame init
screen = pygame.display.set_mode(framebuffer_size, pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()
group = pygame.sprite.LayeredUpdates([Plane(
	random.random() * screen.get_rect().width,
	random.random() * screen.get_rect().height)
	for _ in range(N)
])
##############

ctx = moderngl.create_context()
ctx.enable(moderngl.DEPTH_TEST)

textures = [
	ctx.texture(sprite.image.get_size(), 4, sprite.image.get_buffer())
	for sprite in group
]
# fbo = ctx.framebuffer(
#	 ctx.renderbuffer(framebuffer_size),
#	 ctx.depth_renderbuffer(framebuffer_size),
# )

program = ctx.program(
	vertex_shader="""
	#version 330

	in vec2 in_pos;
	in vec2 in_uv;
	out vec2 uv;

	void main() {
		gl_Position = vec4(in_pos, 0.0, 1.0);
		uv = in_uv;
	}
	""",
fragment_shader="""
	#version 330

	uniform sampler2D texture0;
	out vec4 fragColor;
	in vec2 uv;

	void main() {
		fragColor = texture(texture0, uv);
	}
	""",
)


def convert_vertex(pt, surface):
	return pt[0] / surface.get_width() * 2 - 1, 1 - pt[1] / surface.get_height() * 2 
buffers = [
	ctx.buffer(np.array(
	[
		# pos xy	uv
		*convert_vertex(sprite.rect.bottomleft, screen), 1.0, 0.0,
		*convert_vertex(sprite.rect.bottomright, screen), 0.0, 0.0,
		*convert_vertex(sprite.rect.topleft, screen), 1.0, 1.0,
		*convert_vertex(sprite.rect.topright, screen), 1.0, 0.0,
	], dtype=np.float32))
	for sprite in group
]

# vaos = [
#	 ctx.vertex_array(program, [(buffer, '2f 2f', 'in_pos', 'in_uv')])
#	 for buffer in buffers
# ]

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
	

	group.update(screen)
	ctx.clear()

	for i, sprite in enumerate(group):
		new_content = np.array(
		[
			# pos xy	uv
			*convert_vertex(sprite.rect.bottomleft, screen), 1.0, 0.0,
			*convert_vertex(sprite.rect.bottomright, screen), 0.0, 0.0,
			*convert_vertex(sprite.rect.topleft, screen), 1.0, 1.0,
			*convert_vertex(sprite.rect.topright, screen), 1.0, 0.0,
		], dtype=np.float32)
		buffers[i].write(new_content)

	vaos = [
		ctx.vertex_array(program, [(buffer, '2f 2f', 'in_pos', 'in_uv')])
		for buffer in buffers
	]

	for i in range(N):
		textures[i].use()
		vaos[i].render(mode=moderngl.TRIANGLE_STRIP)
	
	pygame.display.flip()
	clock.tick(300)
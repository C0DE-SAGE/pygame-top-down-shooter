import pygame
import moderngl
import random
import sys
import numpy as np

class Plane(pygame.sprite.Sprite):
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

screen = pygame.display.set_mode((500, 500), pygame.DOUBLEBUF | pygame.OPENGL)

image = pygame.image.load('test\graphics\VEkp8.png').convert_alpha()
# screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

group = pygame.sprite.LayeredUpdates([Plane(
    random.random() * screen.get_rect().width,
    random.random() * screen.get_rect().height)
    for _ in range(1000)
])

ctx = moderngl.create_context()
ctx.enable(moderngl.BLEND)
program = ctx.program(vertex_shader=vshader, fragment_shader=fshader)
vbo = ctx.buffer(None, reserve=6 * 5 * 4)
vao = ctx.vertex_array(program, [(vbo, "2f4 2f4", "in_position", "in_uv")])
textures = {}

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
    
    
    keys = pygame.key.get_pressed()

    group.update(screen)

    ctx.clear(0.2, 0.2, 0.2)

    for sprite in group:
        group.change_layer(sprite, sprite.rect.centery)

    for sprite in group:
        if not keys[pygame.K_LCTRL]:
            def convert_vertex(pt, surface):
                return pt[0] / surface.get_width() * 2 - 1, 1 - pt[1] / surface.get_height() * 2 
            corners = [
                convert_vertex(sprite.rect.bottomleft, screen),
                convert_vertex(sprite.rect.bottomright, screen),
                convert_vertex(sprite.rect.topright, screen),
                convert_vertex(sprite.rect.topleft, screen)
            ] 
            vertices_quad_2d = np.array([
                *corners[0], 0.0, 1.0, 
                *corners[1], 1.0, 1.0, 
                *corners[2], 1.0, 0.0,
                *corners[0], 0.0, 1.0, 
                *corners[2], 1.0, 0.0, 
                *corners[3], 0.0, 0.0
            ], dtype=np.float32)
        
        vbo.write(vertices_quad_2d)

        if sprite.image not in textures:
            texture = sprite.image
            texture = ctx.texture(texture.get_size(), 4, texture.get_buffer())
            texture.swizzle = 'BGRA'
            textures[sprite.image] = texture
        textures[sprite.image].use()
        vao.render()
    
    pygame.display.flip()
    clock.tick(120)
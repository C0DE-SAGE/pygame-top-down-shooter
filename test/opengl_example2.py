import moderngl
from array import array
from PIL import Image

ctx = moderngl.create_context(standalone=True)
framebuffer_size = (512, 512)

import pygame
pygame.init()
screen = pygame.display.set_mode(framebuffer_size, pygame.DOUBLEBUF | pygame.OPENGL)
image = pygame.image.load('test\graphics\\tree.png').convert_alpha()
# texture1 = ctx.texture((2, 2), 3, array('B', [200, 0, 0] * 4))
# texture2 = ctx.texture((2, 2), 3, array('B', [0, 200, 0] * 4))
texture1 = ctx.texture(image.get_size(), 4, image.get_buffer())
texture2 = ctx.texture(image.get_size(), 4, image.get_buffer())

fbo = ctx.framebuffer(
    ctx.renderbuffer(framebuffer_size),
    ctx.depth_renderbuffer(framebuffer_size),
)

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

buffer1 = ctx.buffer(array('f',
    [
        # pos xy    uv
        -0.75,  0.75, 1.0, 0.0,
        -0.75, -0.75, 0.0, 0.0,
         0.75,  0.75, 1.0, 1.0,
         0.75, -0.75, 1.0, 0.0,
    ]
))

buffer2 = ctx.buffer(array('f',
    [
        # pos xy    uv
        -0.5, -0.1, 1.0, 0.0,
        -0.5, -0.5, 0.0, 0.0,
        -0.1, -0.1, 1.0, 1.0,
        -0.1, -0.5, 1.0, 0.0,
    ]
))


vao1 = ctx.vertex_array(program, [(buffer1, '2f 2f', 'in_pos', 'in_uv')])
vao2 = ctx.vertex_array(program, [(buffer2, '2f 2f', 'in_pos', 'in_uv')])

# --- Render ---
# Make a loop here if you need to render multiple passes

fbo.use()
fbo.clear()

# draw quad with red texture
texture1.use()
# vao1.render(mode=moderngl.TRIANGLE_STRIP)

# draw quad with green texture
texture2.use()
vao2.render(mode=moderngl.TRIANGLE_STRIP)

ctx.finish()

img = Image.frombytes('RGB', fbo.size, fbo.read())
img.save('./test/output.png')
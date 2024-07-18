import pygame
from pygame.locals import *
import sys
import moderngl
import numpy as np
from camera import Camera

vertex_shader = """
#version 330

in vec2 in_vert;
void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
}
"""

pygame.init()
screen = pygame.display.set_mode((1920, 1080), DOUBLEBUF | OPENGL | FULLSCREEN)
clock = pygame.time.Clock()

ctx = moderngl.create_context()

prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=open("shaders/fragment.glsl", "r").read())

vertices = [-1, -1], [1, -1], [-1, 1], [1, 1]
vao = ctx.simple_vertex_array(prog, ctx.buffer(np.array(vertices, dtype=np.float32)), 'in_vert')

prog['u_resolution'] = (1920, 1080)

pygame.mouse.set_visible(False)

camera = Camera(pygame.Vector3(0, 0, -35))

while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
    ctx.clear(1.0, 1.0, 1.0)

    camera.update()

    prog['u_position'] = camera.position
    prog['u_mouse'] = camera.rotation.xy
    
    
    vao.render(moderngl.TRIANGLE_STRIP)
    pygame.display.flip()
    pygame.mouse.set_pos(400, 300)
    clock.tick(60)
    

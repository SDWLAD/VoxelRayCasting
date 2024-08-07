import pygame
from pygame.locals import *
import sys
import moderngl
import numpy as np
from camera import Camera

class Engine:
    def __init__(self, resolution = (1920, 1080)):
        pygame.init()
        self.screen = pygame.display.set_mode(resolution, DOUBLEBUF | OPENGL | FULLSCREEN)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)

        self.ctx = moderngl.create_context()

        self.prog = self.load_shaders('shaders/vertex.glsl', 'shaders/fragment.glsl')

        vertices = [-1, -1], [1, -1], [-1, 1], [1, 1]
        self.vao = self.ctx.simple_vertex_array(self.prog, self.ctx.buffer(np.array(vertices, dtype=np.float32)), 'in_vert')

        self.prog['u_resolution'] = resolution
        texture = self.ctx.texture((2560, 1280), 4, pygame.image.tobytes(pygame.image.load('imgs/1.png'), 'RGBA'))
        texture.use(0)

        self.prog['u_skybox'].value = 0

        voxel_data = np.load('a.npy')
        voxel_texture = self.ctx.texture3d((64, 64, 64), 1, voxel_data.tobytes())
        voxel_texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        voxel_texture.use(1)
        self.prog['u_voxel_data'] = 1

        self.camera = Camera(pygame.Vector3(0, 0, 0))

    def load_shaders(self, vertex_shader_name, fragment_shader_name):
        with open(vertex_shader_name, 'r') as f:
            vertex_shader = f.read()
        with open(fragment_shader_name, 'r') as f:
            fragment_shader = f.read()
        return self.ctx.program(vertex_shader, fragment_shader)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

    def render(self):
        self.ctx.clear(1.0, 1.0, 1.0)

        self.prog['u_position'] = self.camera.position
        self.prog['u_mouse'] = self.camera.rotation.xy
        
        self.vao.render(moderngl.TRIANGLE_STRIP)

    def update(self):
        self.camera.update()
        pygame.mouse.set_pos(400, 300)

    def run(self):
        while 1:
            self.check_events()
            self.update()
            self.render()

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    engine = Engine()
    engine.run()
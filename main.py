from shader_program import ShaderProgram
from pygame.locals import *
from camera import Camera
from scene import Scene
from settings import *
import numpy as np
import moderngl
import pygame


class Engine:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(WIN_RES, DOUBLEBUF | OPENGL)
        self.ctx = moderngl.create_context()

        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.time = 0

        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        self.is_running = True
        self.on_init()
    
    def on_init(self):
        self.camera = Camera(pygame.Vector3(0, 0, 0))
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)

        self.vao = self.ctx.simple_vertex_array(self.shader_program.prog, self.ctx.buffer(np.array([[-1, -1], [1, -1], [-1, 1], [1, 1]], dtype=np.float32)), 'in_vert')
        texture = self.ctx.texture((2560, 1280), 4, pygame.image.tobytes(pygame.image.load('imgs/1.png'), 'RGBA'))
        texture.use(0)

    def handle_events(self):
        for event  in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.is_running = False

    def render(self):
        self.ctx.clear(0, 0, 0)
        self.vao.render(moderngl.TRIANGLE_STRIP)
        pygame.display.flip()

    def update(self):
        self.camera.update()
        self.shader_program.update()

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        quit()

if __name__ == '__main__':
    engine = Engine()
    engine.run()
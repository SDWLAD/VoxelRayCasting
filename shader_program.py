from settings import *

class ShaderProgram:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.prog = self.get_program()
        self.set_uniforms_on_init()

    def set_uniforms_on_init(self):
        self.prog['u_resolution'] = WIN_RES
        self.prog['u_skybox']     = 0
        self.prog['u_voxel_data'] = 1

    def update(self):
        self.prog['u_position'] = self.app.camera.position
        self.prog['u_mouse'] = self.app.camera.rotation.xy

    def get_program(self):
        with open(f'shaders/vertex.glsl') as file:
            vertex_shader = file.read()

        with open(f'shaders/fragment.glsl') as file:
            fragment_shader = file.read()

        return self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
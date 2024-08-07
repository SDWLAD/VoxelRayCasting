class ShaderProgram:
    def __init__(self, app):
        self.program = app.ctx.program(
            self.load_shader("shaders/vertex.glsl"),
            self.load_shader("shaders/fragment.glsl"),
        )

    def load_shader(self, filename):
        with open(filename, "r") as f:
            return f.read()
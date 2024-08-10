from model import Model


class Scene:
    def __init__(self, app):
        self.app = app
        self.test_obj = Model(self.app, "models/model.npy")

    def update(self):
        self.test_obj.update()

    def render(self):
        self.test_obj.render()
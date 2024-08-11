import numpy as np


class Model:
    def __init__(self, app, path):
        self.app = app
        self.path = path
        self.voxel_data = self.get_voxel_data()
        self.voxel_texture = self.app.ctx.texture3d((64, 64, 64), 1, self.voxel_data.tobytes())

    def get_voxel_data(self):
        return np.load(self.path)
    
    def update(self):
        pass
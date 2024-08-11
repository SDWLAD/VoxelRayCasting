from model import Model
import moderngl
import numpy as np

class Scene:
    def __init__(self, app):
        self.app = app
        self.size = (64, 64, 64)
        
        self.voxel_data = np.zeros(self.size, dtype=np.uint8)
        
        self.objects = [
            Model(self.app, "models/model.npy"),
            Model(self.app, "models/model2.npy"),
        ]
        
        for i in self.objects:
            self.voxel_data = np.where(self.voxel_data == 0, i.voxel_data, self.voxel_data)

        self.voxel_texture = self.app.ctx.texture3d(self.size, 1, self.voxel_data.tobytes())
        self.voxel_texture.filter = (moderngl.NEAREST, moderngl.NEAREST)

        self.voxel_texture.use(1)

    def update(self):
        for i in self.objects:
            i.update()
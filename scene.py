from model import Model
import moderngl
import numpy as np

class Scene:
    def __init__(self, app):
        self.app = app
        self.size = (128, 128, 128)
        self.voxel_data = np.zeros(self.size, dtype=np.uint8)

        self.objects = [
            Model(self.app, "models/model.npy"),
            Model(self.app, "models/model2.npy")
        ]

        for obj in self.objects:
            scale_factors = tuple(s // os for s, os in zip(self.size, obj.voxel_data.shape))
            obj_data_resized = np.kron(obj.voxel_data, np.ones(scale_factors, dtype=np.uint8))
            self.voxel_data = np.where(self.voxel_data == 0, obj_data_resized, self.voxel_data)
        self.voxel_texture = self.app.ctx.texture3d(self.size, 1, self.voxel_data.tobytes())
        self.voxel_texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.voxel_texture.use(1)

    def update(self):
        for obj in self.objects:
            obj.update()

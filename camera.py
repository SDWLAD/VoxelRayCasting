import pygame as pg
import math

class Camera:
    def __init__(self, position):
        self.position = pg.Vector3(position)
        self.rotation = pg.Vector3(0, 0, 0)
        self.mouse_sensitivity = 0.002
        self.move_speed = 0.1

    def update(self):
        self.keyboard_control()
        self.mouse_control()

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        self.rotation.x += mouse_dx * self.mouse_sensitivity
        self.rotation.y += mouse_dy * self.mouse_sensitivity
        self.rotation.y = max(-math.pi/2, min(math.pi/2, self.rotation.y))

    def keyboard_control(self):
        key_state = pg.key.get_pressed()

        sin_y = math.sin(self.rotation.x)
        cos_y = math.cos(self.rotation.x)
        sin_p = math.sin(self.rotation.y)
        cos_p = math.cos(self.rotation.y)

        forward = pg.Vector3(cos_p * sin_y, -sin_p, cos_p * cos_y)
        right = pg.Vector3(cos_y, 0, -sin_y)
        up = pg.Vector3(0, 1, 0)

        if key_state[pg.K_w]: self.position += forward * self.move_speed
        if key_state[pg.K_s]: self.position -= forward * self.move_speed
        if key_state[pg.K_a]: self.position -= right * self.move_speed
        if key_state[pg.K_d]: self.position += right * self.move_speed
        if key_state[pg.K_SPACE]: self.position += up * self.move_speed
        if key_state[pg.K_LSHIFT]: self.position -= up * self.move_speed
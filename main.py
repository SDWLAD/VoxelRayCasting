import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

def create_shader_program():
    with open("shaders/fragment.glsl", "r") as f:
        fragment_shader = compileShader(f.read(), GL_FRAGMENT_SHADER)
    shader_program = compileProgram(fragment_shader)
    return shader_program

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

shader_program = create_shader_program()
glUseProgram(shader_program)

while True:
    [sys.exit() for event in pygame.event.get() if event.type == pygame.QUIT]
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glBegin(GL_QUADS)
    glVertex2f(-1, -1)
    glVertex2f(1, -1)
    glVertex2f(1, 1)
    glVertex2f(-1, 1)

    glEnd()

    pygame.display.flip()
    pygame.time.wait(10)


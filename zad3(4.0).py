#!/usr/bin/env python3
import sys
import random
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(time, seed):
    #set the same seed for every render, thus getting the same colors
    random.seed(seed)
    glClear(GL_COLOR_BUFFER_BIT)
    renderRectangle(0,0,50,50,2)



    glFlush()

def renderRectangle(x, y, a, b, d = 0):

    if(d != 0):
        a = a * d
        b = b * d
    glBegin(GL_TRIANGLE_STRIP)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x + 0.5 * a, y - 0.5 * b)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x + 0.5 * a, y + 0.5 * b)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x - 0.5 * a, y - 0.5 * b)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x - 0.5 * a, y + 0.5 * b)
    glEnd()

def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspectRatio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    # Randomize a seed once
    seed = random.random()
    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), seed)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()

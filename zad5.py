#!/usr/bin/env python3
import sys
import random
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import colorsys
import numpy
MAX_ITER = 80
REAL_START = -2
REAL_END = 2
IMAG_START = -2
IMAG_END = 2


def startup(width, height):
    update_viewport(None, width, height)
    glClearColor(0, 0, 0, 1.0)


def shutdown():
    pass

def rgb_conv(i):
    color = 255 * numpy.asarray(colorsys.hsv_to_rgb(i/255, 1.0, 0.5))
    return tuple(color.astype(int))

def render(time, width, height):

    glClear(GL_COLOR_BUFFER_BIT)

    for x in range(0, width):
        for y in range(0, height):
            c = complex(REAL_START + (x/width) *(REAL_END - REAL_START),
                        IMAG_START + (y/height) * (IMAG_END - IMAG_START))
            iterations = mandelbrot(c)
            if iterations == MAX_ITER:
                glBegin(GL_POINTS)
                glColor3ub(0,0, 0)
                glVertex2f(x / (width / 200) - 100, y / (height / 200) - 100)
                glEnd()
            else:
                color = rgb_conv(iterations)
                glBegin(GL_POINTS)
                glColor3ub(color[0], color[1], color[2])
                glVertex2f(x / (width / 200) - 100, y / (height / 200) - 100)
                glEnd()




def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z*z + c
        n += 1
    return n


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
    width = 800
    height = 800
    window = glfwCreateWindow(width, height, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)


    startup(width, height)
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), width, height)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()

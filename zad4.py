#!/usr/bin/env python3
# Prosze podac argument przy odpalaniu programu. Jest to stopien dywanu.
# Dostepne sa dwie implementacje, jedna robi wciecia, druga rysuje male kwadraty.
# Wybor algorytmu jest poprzez zakomentowanie, odkomentowanie jednej z funkcji
# w redner().
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


def render(time, seed, depth):
    # Set the same seed for every render, thus getting the same colors
    random.seed(seed)
    glClear(GL_COLOR_BUFFER_BIT)


    # Choose which version of sierpinski's carpet to render, indents works
    # much faster.
    renderCarpetSquares(0,0,150,150,depth)
    #rednerCarpetIndents(0, 0, 120, 120,depth)


    glFlush()


def renderFragment(x, y, a, b, d = 0):
    if(d != 0):
        a = a * d
        b = b * d
    renderRectangle(x-a, y+b, a, b)
    renderRectangle(x, y+b, a, b)
    renderRectangle(x+a, y+b, a, b)
    renderRectangle(x-a, y, a, b)
    renderEmptyRectangle(x, y, a, b)
    renderRectangle(x+a, y, a, b)
    renderRectangle(x-a, y-b, a, b)
    renderRectangle(x, y-b, a, b)
    renderRectangle(x+a, y-b, a, b)

def renderCarpetSquares(x, y, a, b, depth):
    if depth > 0:
        a = a / 3.0
        b = b / 3.0
        renderFragment(x, y, a, b)
        if depth > 1:
            for i  in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    renderCarpetSquares(x + (a * i), y + (b * j), a, b, depth - 1)

def rednerCarpetIndents(x, y, a, b, depth):
    renderFragment(0, 0, a/3, b/3)
    renderCarpetv2(0, 0, a, b, depth)

def renderCarpetv2(x, y, a, b, depth):
    if depth > 0:
        a = a / 3.0
        b = b / 3.0
        renderEmptyRectangle(x, y, a, b)
        if depth > 1:
            for i  in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    renderCarpetv2(x + (a * i), y + (b * j), a, b, depth - 1)

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

def renderEmptyRectangle(x, y, a, b, d = 0):
    if(d != 0):
        a = a * d
        b = b * d
    glBegin(GL_TRIANGLE_STRIP)
    glColor3f(0.5, 0.5, 0.5)
    glVertex2f(x + 0.5 * a, y - 0.5 * b)
    glColor3f(0.5, 0.5, 0.5)
    glVertex2f(x + 0.5 * a, y + 0.5 * b)
    glColor3f(0.5, 0.5, 0.5)
    glVertex2f(x - 0.5 * a, y - 0.5 * b)
    glColor3f(0.5, 0.5, 0.5)
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
        render(glfwGetTime(), seed, int(sys.argv[1]))
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()

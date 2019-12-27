from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np

import math
import sys

step_room = 32
step_sofa = 8


def _draw_arm(tex):
    h = 0.7

    glBindTexture(GL_TEXTURE_2D, tex)

    ss = [1, 0.0, 0.0]
    tt = [0.0, 1, 0.0]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    glPushMatrix()

    # Фронт
    draw_quads_xy(0, 0, 0.25, h, 0, step_sofa)
    # Зад
    draw_r_quads_xy(0, 0, 0.25, h, -1, step_sofa)

    ss = [1, 0.0, 0.0]
    tt = [0.0, 0.0, 1]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    # Верх
    draw_r_quads_xz(0, -1, 0.25, 0, h, step_sofa)
    # Низ
    draw_quads_xz(0, -1, 0.25, 0, 0, step_sofa)

    ss = [0.0, 0.0, 1]
    tt = [0.0, 1, 0.0]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    # Лево
    draw_r_quads_yz(0, -1, h, 0, 0, step_sofa)
    # Право
    draw_quads_yz(0, -1, h, 0, 0.25, step_sofa)

    glPopMatrix()


def _draw_main_sofa(tex):
    glPushMatrix()

    glBindTexture(GL_TEXTURE_2D, tex)

    ss = [1, 0.0, 0.0]
    tt = [0.0, 1, 0.0]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    # Фронт спинки
    draw_quads_xy(0, 0.5, 2, 1, -0.6, step_sofa)

    # Фронт сидушки
    draw_quads_xy(0, 0, 2, 0.5, 0, step_sofa)

    ss = [-1, 0.0, 0.0]
    tt = [0.0, 1, 0.0]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    # Спинка
    draw_r_quads_xy(0, 0, 2, 1, -1, step_sofa)

    ss = [1, 0.0, 0.0]
    tt = [0.0, 0.0, -1]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    # Верх спинки
    draw_r_quads_xz(0, -1, 2, -0.6, 1, step_sofa)
    # Верх сидушки
    draw_r_quads_xz(0, -0.6, 2, 0, 0.5, step_sofa)

    ss = [1, 0.0, 0.0]
    tt = [0.0, 0.0, 1]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    # Низ
    draw_quads_xz(0, -1, 2, 0, 0, step_sofa)

    ss = [0.0, 0.0, 1]
    tt = [0.0, 1, 0.0]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    # Бок спинки (Правая)
    draw_quads_yz(0, -1, 1, -0.6, 2, step_sofa)
    # Бок спинки (Левая)
    draw_r_quads_yz(0, -1, 1, -0.6, 0, step_sofa)

    glPopMatrix()


def draw_sofa(tex):
    glPushMatrix()

    _draw_arm(tex[1])
    glTranslatef(0.25, 0, 0)
    _draw_main_sofa(tex[0])
    glTranslate(2, 0, 0)
    _draw_arm(tex[1])

    glPopMatrix()


def draw_room(tex):
    global step_room

    glPushMatrix()

    glBindTexture(GL_TEXTURE_2D, tex[0])

    # Пол
    ss = [1, 0.0, 0.0]
    tt = [0.0, 0.0, 1]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    draw_r_quads_xz(0, -10, 10, 0, 0, step_room)

    glBindTexture(GL_TEXTURE_2D, tex[1])

    # Левая
    ss = [0.0, 0.0, 1.0]
    tt = [0.0, 1.0, 0.0]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    draw_quads_yz(0, -10, 5, 0, 0, step_room)

    # Правая
    draw_r_quads_yz(0, -10, 5, 0, 10, step_room)

    glPopMatrix()

    # Передняя
    ss = [1.0, 0.0, 0.0]
    tt = [0.0, 1.0, 0.0]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    draw_r_quads_xy(0, 0, 10, 5, 0, step_room)

    # Задняя
    draw_quads_xy(0, 0, 10, 5, -10, step_room)

    # Потолок
    glBindTexture(GL_TEXTURE_2D, tex[2])

    ss = [1.0, 0.0, 0.0]
    tt = [0.0, 0.0, -1.0]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    draw_quads_xz(0, -10, 10, 0, 5, step_room)


def draw_door(tex):
    glPushMatrix()

    glBindTexture(GL_TEXTURE_2D, tex)

    ss = [1.0, 0.0, 0.0]
    tt = [0.0, 0.5, 0.0]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    draw_quads_xy(0, 0, 1, 2, 0, step_sofa)

    glPopMatrix()


def draw_quads_xy(xmin, ymin, xmax, ymax, z, step):
    step_x = (xmax - xmin) / step
    step_y = (ymax - ymin) / step

    glBegin(GL_QUADS)
    glNormal3f(0.0, 0.0, 1.0);
    for x_coord in np.arange(xmin, xmax, step_x):
        for y_coord in np.arange(ymin, ymax, step_y):
            glVertex3f(x_coord, y_coord, z)
            glVertex3f(x_coord, y_coord + step_y, z)
            glVertex3f(x_coord + step_x, y_coord + step_y, z)
            glVertex3f(x_coord + step_x, y_coord, z)
    glEnd()


def draw_r_quads_xy(xmin, ymin, xmax, ymax, z, step):
    step_x = (xmax - xmin) / step
    step_y = (ymax - ymin) / step

    glBegin(GL_QUADS)
    glNormal3f(0.0, 0.0, -1.0);
    for x_coord in np.arange(xmin, xmax, step_x):
        for y_coord in np.arange(ymin, ymax, step_y):
            glVertex3f(x_coord, y_coord, z)
            glVertex3f(x_coord + step_x, y_coord, z)
            glVertex3f(x_coord + step_x, y_coord + step_y, z)
            glVertex3f(x_coord, y_coord + step_y, z)
    glEnd()


def draw_quads_xz(xmin, zmin, xmax, zmax, y, step):
    step_x = (xmax - xmin) / step
    step_z = (zmax - zmin) / step

    glBegin(GL_QUADS)
    glNormal3f(0.0, -1.0, 0.0)
    for x_coord in np.arange(xmin, xmax, step_x):
        for z_coord in np.arange(zmin, zmax, step_z):
            glVertex3f(x_coord, y, z_coord)
            glVertex3f(x_coord, y, z_coord + step_z)
            glVertex3f(x_coord + step_x, y, z_coord + step_z)
            glVertex3f(x_coord + step_x, y, z_coord)
    glEnd()


def draw_r_quads_xz(xmin, zmin, xmax, zmax, y, step):
    step_x = (xmax - xmin) / step
    step_z = (zmax - zmin) / step

    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)
    for x_coord in np.arange(xmin, xmax, step_x):
        for z_coord in np.arange(zmin, zmax, step_z):
            glVertex3f(x_coord, y, z_coord)
            glVertex3f(x_coord + step_x, y, z_coord)
            glVertex3f(x_coord + step_x, y, z_coord + step_z)
            glVertex3f(x_coord, y, z_coord + step_z)
    glEnd()


def draw_quads_yz(ymin, zmin, ymax, zmax, x, step):
    step_y = (ymax - ymin) / step
    step_z = (zmax - zmin) / step

    glBegin(GL_QUADS)
    glNormal3f(1.0, 0.0, 0.0)
    for y_coord in np.arange(ymin, ymax, step_y):
        for z_coord in np.arange(zmin, zmax, step_z):
            glVertex3f(x, y_coord, z_coord)
            glVertex3f(x, y_coord, z_coord + step_z)
            glVertex3f(x, y_coord + step_y, z_coord + step_z)
            glVertex3f(x, y_coord + step_y, z_coord)
    glEnd()


def draw_r_quads_yz(ymin, zmin, ymax, zmax, x, step):
    step_y = (ymax - ymin) / step
    step_z = (zmax - zmin) / step

    glBegin(GL_QUADS)
    glNormal3f(-1.0, 0.0, 0.0)
    for y_coord in np.arange(ymin, ymax, step_y):
        for z_coord in np.arange(zmin, zmax, step_z):
            glVertex3f(x, y_coord, z_coord)
            glVertex3f(x, y_coord + step_y, z_coord)
            glVertex3f(x, y_coord + step_y, z_coord + step_z)
            glVertex3f(x, y_coord, z_coord + step_z)
    glEnd()

# Импортируем все необходимые библиотеки:
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PIL import Image

import math
import sys


global view_width
global view_height
global size
global xrot
global yrot

global wood_texture
global texture2

view_width = 800
view_height = 800
size = 0.5

position = [0.0, 0.0]
startRot = 90
yrot = 90
delta = 0.5

light_offset = 0

light1_diffuse = [0.5, 0.5, 0.5, 1]
low_shinness = 100

text_coords = [
    [0, 0, 0],
    [0, 0, 1],
    [0, 1, 1],
    [1, 1, 1]
]


def draw_cube(xSize, ySize, zSize, color: list = [0.5, 0.5, 0.5]):
    glTranslatef(-xSize / 2, -ySize / 2, -zSize / 2)

    glBegin(GL_QUADS)
    # near
    glColor3fv(color)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, 0)

    # far
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, zSize)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, zSize)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, zSize)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, zSize)

    # left
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(0, ySize, zSize)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(0, 0, zSize)

    # right
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize, 0, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize, ySize, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, zSize)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, zSize)

    # bottom
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, 0, zSize)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, 0, zSize)

    # top
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, ySize, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, ySize, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, zSize)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, zSize)
    glEnd()


def draw_room():
    # near
    glPushMatrix()
    glTranslatef(0, 0, 0.5)
    draw_cube(22, 10, 1, [0.3, 0.3, 0.3])
    glPopMatrix()

    # far
    glPushMatrix()
    glTranslatef(0, 0, -40.5)
    draw_cube(22, 10, 1, [0.4, 0.3, 0.3])
    glPopMatrix()

    # left
    glPushMatrix()
    glTranslatef(-10.5, 0, -20)
    draw_cube(1, 10, 40, [0.4, 0.4, 0.3])
    glPopMatrix()

    # right
    glPushMatrix()
    glTranslatef(10.5, 0, -20)
    draw_cube(1, 10, 40, [0.4, 0.4, 0.4])
    glPopMatrix()

    # bottom
    glPushMatrix()
    glTranslatef(0, -5.5, -20)
    draw_cube(22, 1, 42, [0.5, 0.4, 0.5])
    glPopMatrix()

    # top
    glPushMatrix()
    glTranslatef(0, 5.5, -20)
    draw_cube(22, 1, 42, [0.5, 0.4, 0.5])
    glPopMatrix()

    glTranslate(0, 0, -20)


def draw_table(xSize, ySize, zSize):
    glPushMatrix()
    glTranslatef(-xSize / 2, ySize / 2, -zSize / 2)
    draw_cube(0.5, ySize, 0.5)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(xSize / 2, ySize / 2, -zSize / 2)
    draw_cube(0.5, ySize, 0.5)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-xSize / 2, ySize / 2, zSize / 2)
    draw_cube(0.5, ySize, 0.5)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(xSize / 2, ySize / 2, zSize / 2)
    draw_cube(0.5, ySize, 0.5)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, ySize + 0.25, 0)
    draw_cube(xSize + 0.5, 0.5, zSize + 0.5)
    glPopMatrix()


def draw_cupboard(xSize, ySize, zSize):
    # left
    glPushMatrix()
    glTranslatef(-xSize / 2, 0, 0)
    draw_cube(0.2, ySize, zSize)
    glPopMatrix()

    # right
    glPushMatrix()
    glTranslatef(xSize / 2, 0, 0)
    draw_cube(0.2, ySize, zSize)
    glPopMatrix()

    # top
    glPushMatrix()
    glTranslatef(0, ySize / 2 + 0.1, 0)
    draw_cube(xSize + 0.2, 0.2, zSize)
    glPopMatrix()

    # bottom
    glPushMatrix()
    glTranslatef(0, -(ySize / 2 + 0.1), 0)
    draw_cube(xSize + 0.2, 0.2, zSize)
    glPopMatrix()

    # far
    glPushMatrix()
    glTranslatef(0, 0, -zSize / 2 + 0.1)
    draw_cube(xSize - 0.2, ySize, 0.2)
    glPopMatrix()

    # door1
    glPushMatrix()
    glTranslatef(-xSize / 4, 0, zSize / 2 + 0.1)
    draw_cube(xSize / 2, ySize, 0.2)
    glPopMatrix()

    # door2
    glPushMatrix()
    glTranslatef(xSize / 4, 0, zSize / 2 + 0.1)
    draw_cube(xSize / 2, ySize, 0.2)
    glPopMatrix()

def load_texture(textureName):
    image = Image.open(textureName)
    imageData = image.tobytes("raw", "RGB", 0, -1)

    textureID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureID)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1],
                 0, GL_RGB, GL_UNSIGNED_BYTE, imageData)

    image.close()
    return textureID


def specialkeys(key, x, y):
    global position
    global yrot
    global light_offset

    if key == GLUT_KEY_UP:
        position[0] += delta * math.cos(math.radians(yrot))
        position[1] += delta * math.sin(math.radians(yrot))
    if key == GLUT_KEY_DOWN:
        position[0] -= delta * math.cos(math.radians(yrot))
        position[1] -= delta * math.sin(math.radians(yrot))
    if key == GLUT_KEY_LEFT:
        yrot -= 1.0
    if key == GLUT_KEY_RIGHT:
        yrot += 1.0

    if key == GLUT_KEY_PAGE_UP:
        light_offset += 1
    if key == GLUT_KEY_PAGE_DOWN:
        light_offset -= 1


    glutPostRedisplay()


def initialize():
    global wood_texture
    global texture2

    glClearColor(0, 0, 0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glFrustum(-5.0, 5.0, -5.0, 5.0, 20.0, 1000.0)  # Определяем границы рисования по горизонтали и вертикали
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

    glEnable(GL_LIGHTING)  # Включаем освещение

    glEnable(GL_LIGHT0)  # Включаем один источник света
    # glEnable(GL_LIGHT1)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_AUTO_NORMAL)

    # glEnable(GL_TEXTURE_2D)

    wood_texture = load_texture("wood.jpg")
    texture2 = load_texture("2.png")
    # glBindTexture(GL_TEXTURE_2D, texture)

    # glLightModelfv(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    # glLight(GL_LIGHT0, GL_POSITION, [0, 20, 0, 1])
    # glLight(GL_LIGHT0, GL_SPOT_DIRECTION, [0, -100, 0])
    # glLight(GL_LIGHT0, GL_SPOT_CUTOFF, 45)


def redraw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glPushMatrix()
    glTranslatef(0, 0, -50)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-5.0, 5.0, -5.0, 5.0, 10.0, 1000.0)
    glRotate(yrot, 0, 1, 0)
    glRotate(-90, 0, 1, 0)
    glTranslate(position[0], 0, position[1])
    glMatrixMode(GL_MODELVIEW)

    print(position, yrot, light_offset)

    glBindTexture(GL_TEXTURE_2D, wood_texture)
    glEnable(GL_TEXTURE_2D)
    draw_room()
    glDisable(GL_TEXTURE_2D)

    #table
    glBindTexture(GL_TEXTURE_2D, wood_texture)
    glEnable(GL_TEXTURE_2D)
    glPushMatrix()
    glTranslate(0, -5, 0)
    draw_table(4, 3, 4)
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)
    #

    #shkaff
    glBindTexture(GL_TEXTURE_2D, texture2)
    glEnable(GL_TEXTURE_2D)
    glPushMatrix()
    glTranslate(0, 0, -10)
    draw_cupboard(10, 8, 5)
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)
    #

    glPushMatrix()
    # glLight(GL_LIGHT0, GL_POSITION, [0, 0, 1, 0])
    # glLight(GL_LIGHT0, GL_AMBIENT, [0.9, 0.5, 0.5, 1.0])

    glTranslate(0, 0, light_offset)
    glLightfv(GL_LIGHT1, GL_POSITION, [0.0, 0.0, 0.0, 1])
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, [0, 0, -1])
    glLight(GL_LIGHT1, GL_SPOT_CUTOFF, 45)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [1, 1, 0.1, 1.0])
    glLight(GL_LIGHT1, GL_SPOT_EXPONENT, 15.0)
    glPopMatrix()

    glPopMatrix()

    glutSwapBuffers()


if __name__ == '__main__':
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(view_width, view_height)
    glutInitWindowPosition(350, 20)

    glutInit(sys.argv)

    glutCreateWindow(b'Light')
    glutDisplayFunc(redraw)
    glutSpecialFunc(specialkeys)

    initialize()

    glutMainLoop()

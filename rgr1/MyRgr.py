from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np
from imageio import imread

import math
import sys

xRot = 0
xPos = 0
zPos = 0

lightX = 0
lightZ = 0

global bark_texture
global tree_texture
global floor_texture
global wall1_texture
global wall2_texture
global wall3_texture
global wall4_texture

posDelta = 1


def specialKeys(key, x, y):
    global xRot
    global zPos
    global xPos

    # Обработчики для клавиш со стрелками
    if key == GLUT_KEY_UP:  # Клавиша вверх
        zPos += posDelta * math.cos(math.radians(xRot))
        xPos += posDelta * math.sin(math.radians(xRot))
    if key == GLUT_KEY_DOWN:  # Клавиша вниз
        zPos -= posDelta * math.cos(math.radians(xRot))
        xPos -= posDelta * math.sin(math.radians(xRot))
    if key == GLUT_KEY_LEFT:  # Клавиша влево
        xRot -= 5
    if key == GLUT_KEY_RIGHT:  # Клавиша вправо
        xRot += 5

    # if (key == GLUT_KEY_F1):
    print(key)

    print("x={}, z={}, angle={}".format(xPos, zPos, xRot))
    glutPostRedisplay()  # Вызываем процедуру перерисовки


def load_texture(file_name: str):
    image = Image.open(file_name)
    image.load()  # this is not a list, nor is it list()'able
    width, height = image.size
    textureData = np.asarray(image)
    textureData = textureData[::-1]
    image.close()

    texId = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texId)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    if "png" in file_name:
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    else:
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)

    return texId


def drawWalls(xSize, ySize, zSize):
    glPushMatrix()

    glTranslatef(-xSize / 2, -ySize / 2, -zSize / 2)
    glEnable(GL_TEXTURE_2D)

    # front
    glBindTexture(GL_TEXTURE_2D, wall1_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, 0)
    glEnd()

    # back
    glBindTexture(GL_TEXTURE_2D, wall2_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, zSize)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, zSize)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, zSize)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, zSize)
    glEnd()

    # right
    glBindTexture(GL_TEXTURE_2D, wall3_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize, 0, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize, ySize, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, zSize)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, zSize)
    glEnd()

    # left
    glBindTexture(GL_TEXTURE_2D, wall4_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(0, ySize, zSize)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(0, 0, zSize)
    glEnd()

    # bottom
    glBindTexture(GL_TEXTURE_2D, floor_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, 0, zSize)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, 0, zSize)
    glEnd()

    # top
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, ySize, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, ySize, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, zSize)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, zSize)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glPopMatrix()


def drawRoom():
    glPushMatrix()
    drawWalls(80, 40, 80)
    drawTree(20, 35)
    glPopMatrix()


def drawPlayerLight():
    global lightZ
    global lightX
    global xRot
    global xPos
    global zPos

    glPushMatrix()
    glLoadIdentity()

    glEnable(GL_LIGHT1)
    # glTranslate(lightX, 0, -lightZ - 1)
    # glRotate(-xRot, 0, 1, 0)
    # glutSolidSphere(1, 5, 5)
    glLight(GL_LIGHT1, GL_POSITION, (xPos, 0, -zPos, 1))
    # glLight(GL_LIGHT1, GL_AMBIENT, (0.5, 0.5, 0.5, 1))
    glLight(GL_LIGHT1, GL_DIFFUSE, (0.8, 0.8, 0.8, 1))
    direction = (0, 1, 0)
    print(direction)
    glLight(GL_LIGHT1, GL_SPOT_DIRECTION, direction)
    # glLight(GL_LIGHT1, GL_SPECULAR, (1, 1, 1, 1))
    # glLight(GL_LIGHT1, GL_)
    glPopMatrix()


def drawTree(xSize, ySize):
    glPushMatrix()

    glTranslatef(-xSize / 2, -ySize / 2, 0)
    glEnable(GL_TEXTURE_2D)
    # glEnable(GL_TEXTURE_GEN_S)
    # glEnable(GL_TEXTURE_GEN_T)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glBindTexture(GL_TEXTURE_2D, tree_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, 0)
    glEnd()

    glTranslatef(xSize / 2, 0, xSize / 2)
    glRotate(90, 0, 1, 0)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, 0)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)
    glDisable(GL_BLEND)
    glPopMatrix()


# Процедура перерисовки
def draw():
    global xRot
    global zPos
    global xPos

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # glPushMatrix()
    glMatrixMode(GL_MODELVIEW)
    drawPlayerLight()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-10.0, 10.0, -10.0, 10.0, 10.0, 100.0)
    # glRotate(-90, 0, 1, 0)
    glRotate(xRot, 0, 1, 0)
    glTranslate(-xPos, 0, zPos)
    glMatrixMode(GL_MODELVIEW)
    # glPopMatrix()

    drawRoom()
    glutSwapBuffers()  # Выводим все нарисованное в памяти на экран


# Процедура инициализации
def init():
    global bark_texture
    global tree_texture
    global floor_texture
    global wall1_texture
    global wall2_texture
    global wall3_texture
    global wall4_texture

    glClearColor(0, 0, 0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glOrtho(-5.0, 5.0, -10.0, 10.0, -5.0, 1000.0)  # Определяем границы рисования по горизонтали и вертикали

    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    # glEnable(GL_LIGHTING)  # Включаем освещение
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_AUTO_NORMAL)
    glAlphaFunc(GL_GREATER, 0.5)
    glEnable(GL_ALPHA_TEST)

    tree_texture = load_texture("tree.png")
    bark_texture = load_texture("bark.jpg")
    floor_texture = load_texture("floor.jpeg")
    wall1_texture = load_texture("wall1.jpeg")
    wall2_texture = load_texture("wall2.jpeg")
    wall3_texture = load_texture("wall3.jpeg")
    wall4_texture = load_texture("wall.jpeg")


def keyPressed(key, x, y):
    global lightX
    global lightZ
    global cutoff
    global exponent

    if key == b"w":
        lightZ += 1
    elif key == b"s":
        lightZ -= 1
    elif key == b"a":
        lightX -= 1
    elif key == b"d":
        lightX += 1

    print("Light: x={}, z={}".format(lightX, lightZ))
    glutPostRedisplay()


if __name__ == '__main__':
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(350, 20)

    glutInit(sys.argv)

    glutCreateWindow(b'Light')
    glutDisplayFunc(draw)
    glutSpecialFunc(specialKeys)
    glutKeyboardFunc(keyPressed)

    init()

    glutMainLoop()
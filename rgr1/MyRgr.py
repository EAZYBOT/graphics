from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
from threading import Thread
from time import sleep
import numpy as np
import colorsys

import math
import sys

xRot = 0
xPos = 0
zPos = 0
playerHeight = 0

isPlayerLightEnabled = True
isTreeLightEnabled = True
isFireplaceLightEnabled = True
isMoonLightEnabled = True

treeLightH = 0

global bark_texture
global tree_texture
global floor_texture
global wall1_texture
global wall2_texture
global wall3_texture
global wall4_texture

posDelta = 1


def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q

    return r, g, b


def togglePlayerLight():
    global isPlayerLightEnabled
    isPlayerLightEnabled = (isPlayerLightEnabled != True)

    if isPlayerLightEnabled:
        glEnable(GL_LIGHT1)
    else:
        glDisable(GL_LIGHT1)


def toggleFireplaceLight():
    global isFireplaceLightEnabled
    isFireplaceLightEnabled = (isFireplaceLightEnabled != True)

    if isFireplaceLightEnabled:
        glEnable(GL_LIGHT2)
    else:
        glDisable(GL_LIGHT2)


def toggleTreeLight():
    global isTreeLightEnabled
    isTreeLightEnabled = (isTreeLightEnabled != True)

    if isTreeLightEnabled:
        glEnable(GL_LIGHT3)
    else:
        glDisable(GL_LIGHT3)


def toggleMoonLight():
    global isMoonLightEnabled
    isMoonLightEnabled = (isMoonLightEnabled != True)

    if isMoonLightEnabled:
        glEnable(GL_LIGHT4)
    else:
        glDisable(GL_LIGHT4)


def specialKeys(key, x, y):
    global xRot
    global zPos
    global xPos
    global playerHeight

    # Обработчики для клавиш со стрелками
    if key == GLUT_KEY_UP:  # Клавиша вверх
        zPos += posDelta * math.cos(math.radians(xRot))
        xPos += posDelta * math.sin(math.radians(xRot))
        playerHeight += 15
        playerHeight %= 180
    if key == GLUT_KEY_DOWN:  # Клавиша вниз
        zPos -= posDelta * math.cos(math.radians(xRot))
        xPos -= posDelta * math.sin(math.radians(xRot))
        playerHeight -= 15
        playerHeight %= 180
    if key == GLUT_KEY_LEFT:  # Клавиша влево
        xRot -= 5
    if key == GLUT_KEY_RIGHT:  # Клавиша вправо
        xRot += 5
    if key == GLUT_KEY_F1:
        togglePlayerLight()
        print("Player light toggled")
    if key == GLUT_KEY_F2:
        toggleFireplaceLight()
        print("Fireplace light toggled")
    if key == GLUT_KEY_F3:
        toggleTreeLight()
        print("Tree light toggled")
    if key == GLUT_KEY_F4:
        toggleMoonLight()
        print("Moon light toggled")

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

    # glEnable(GL_CULL_FACE)
    # glCullFace(GL_BACK)
    # glFrontFace(GL_CW)

    glTranslatef(-xSize / 2, -ySize / 2, -zSize / 2)
    glEnable(GL_TEXTURE_2D)

    # front
    glBindTexture(GL_TEXTURE_2D, wall1_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, 0)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, 0)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, 0)
    glEnd()

    # back
    glBindTexture(GL_TEXTURE_2D, wall2_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, zSize)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, zSize)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, zSize)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, zSize)
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

    glTexCoord2f(1.0, 0.0)
    glVertex3f(0, 0, zSize)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(0, ySize, zSize)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, 0)
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

    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, zSize)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, zSize)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, ySize, 0)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glPopMatrix()


def drawRoom():
    glPushMatrix()
    drawWalls(80, 40, 80)

    glPushMatrix()
    glTranslate(-20, 0, -30)
    drawTree(20, 35)
    glPopMatrix()

    drawTreeLight()
    drawFireplaceLight()
    glPopMatrix()


def drawTree(xSize, ySize):
    glPushMatrix()

    glTranslatef(-xSize / 2, -ySize / 2, 0)
    glEnable(GL_TEXTURE_2D)

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
    glDisable(GL_BLEND)
    glPopMatrix()


def drawTreeLight():
    global lightZ
    global lightX
    global treeLightH

    if isTreeLightEnabled:
        glPushMatrix()
        glLoadIdentity()

        colors = list(hsv2rgb(treeLightH, 0.5, 0.5))
        colors.append(1)

        glEnable(GL_LIGHT3)
        glLight(GL_LIGHT3, GL_POSITION, (-15, 0, -25, 1))
        glLight(GL_LIGHT3, GL_DIFFUSE, colors)

        glPopMatrix()
    else:
        glDisable(GL_LIGHT3)


def drawPlayerLight():
    global xRot
    global xPos
    global zPos

    if isPlayerLightEnabled:
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glEnable(GL_LIGHT1)
        glLight(GL_LIGHT1, GL_POSITION, (xPos, 0, -zPos + 20, 1))
        glLight(GL_LIGHT1, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
        glLight(GL_LIGHT1, GL_DIFFUSE, (0.4, 0.4, 0.4, 1))
        glLight(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 0)
        glLight(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.0004)
        glPopMatrix()
    else:
        glDisable(GL_LIGHT1)


def drawMoonLight():
    glPushMatrix()
    glLoadIdentity()
    color = convertColors(0, 14, 60, 255)

    glLight(GL_LIGHT4, GL_POSITION, (1, 0, -1, 0))
    glLight(GL_LIGHT4, GL_DIFFUSE, color)
    glLight(GL_LIGHT4, GL_SPECULAR, color)
    glPopMatrix()


def convertColors(r, g, b, a):
    return r / 255, g / 255, b / 255, a / 255


def drawFireplaceLight():
    if isFireplaceLightEnabled:
        glPushMatrix()
        glLoadIdentity()

        glEnable(GL_LIGHT2)
        glLight(GL_LIGHT2, GL_POSITION, (0, 1, 75, 1))
        glLight(GL_LIGHT2, GL_DIFFUSE, convertColors(241, 128, 53, 255))
        glLight(GL_LIGHT2, GL_SPECULAR, convertColors(241, 128, 53, 255))

        glLight(GL_LIGHT2, GL_CONSTANT_ATTENUATION, 0)
        glLight(GL_LIGHT2, GL_QUADRATIC_ATTENUATION, 0.0008)
        glPopMatrix()
    else:
        glDisable(GL_LIGHT2)


def draw():
    global xRot
    global zPos
    global xPos

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    drawPlayerLight()
    drawMoonLight()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-10.0, 10.0, -10.0, 10.0, 10.0, 500.0)
    glRotate(xRot, 0, 1, 0)

    y = -math.sin(math.radians(playerHeight)) * 3
    glTranslate(-xPos, y, zPos)
    glMatrixMode(GL_MODELVIEW)
    drawRoom()
    glutSwapBuffers()


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
    glFrustum(-10.0, 10.0, -10.0, 10.0, 10.0, 500.0)
    
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glShadeModel(GL_SMOOTH)
    glAlphaFunc(GL_GREATER, 0.5)
    glEnable(GL_ALPHA_TEST)

    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHT3)
    glEnable(GL_LIGHT4)

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


def threadFunc(arg):
    global treeLightH

    while True:
        treeLightH += 1
        treeLightH %= 360
        sleep(0.015)
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
    thread = Thread(target=threadFunc, args=(1,))
    thread.start()
    # thread.join()
    glutMainLoop()

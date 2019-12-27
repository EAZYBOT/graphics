from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np

from models import *

import math
import sys

view_rot = 0
view_z_pos = 0
view_x_pos = 0

speed = 0.07

flash_cutoff = 30
flash_exp = 0

xrot = 0
yrot = 0

tex_sofa = []
tex_home = []
tex_door = 0

light_switch = [True, True, True, True]


def rgba(r, g, b, a=1):
    return r / 255, g / 255, b / 255, a / 255


def rgb(r, g, b):
    return r / 255, g / 255, b / 255


def load_texture(file_name: str):
    image = Image.open(file_name)
    image.load()
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

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)

    return texId


def init():
    global tex_door

    glClearColor(0.2, 0.2, 0.2, 1.0)

    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glEnable(GL_CULL_FACE)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHT3)

    glFrontFace(GL_CW)

    glTexGenf(GL_S, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
    glTexGenf(GL_T, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)

    tex_sofa.append(load_texture('sofa_main.jpg'))
    tex_sofa.append(load_texture('sofa_arm.jpg'))

    tex_home.append(load_texture('floor_home.jpg'))
    tex_home.append(load_texture('wallpaper.jpg'))
    tex_home.append(load_texture('ceiling.jpg'))

    tex_door = load_texture('door.jpg')


def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMaterial(GL_FRONT, GL_AMBIENT, (0.3, 0.3, 0.3, 1))

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()
    glFrustum(-0.1, 0.1, -0.1, 0.1, 0.1, 200)
    glRotate(view_rot, 0, 1, 0)
    glTranslate(-view_x_pos, 0, view_z_pos)
    glTranslatef(0, 0.7, 0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glRotatef(180, 0, 1, 0)
    glTranslatef(0, -2, -1.99)
    draw_door(tex_door)

    glLoadIdentity()

    moon_light()
    player_flashlight()
    room_light()
    projector()

    glTranslate(-2, -2, 2)
    draw_room(tex_home)

    glLoadIdentity()
    glTranslatef(1.5, -2, -7)
    draw_sofa(tex_sofa)

    glutSwapBuffers()


def specialKeys(key, x, y):
    global flash_exp
    global flash_cutoff

    if key == GLUT_KEY_UP:
        if flash_exp < 128:
            flash_exp += 1
    elif key == GLUT_KEY_DOWN:
        if flash_exp > 0:
            flash_exp -= 1
    elif key == GLUT_KEY_LEFT:
        if flash_cutoff == 180:
            flash_cutoff = 90
        elif flash_cutoff > 0:
            flash_cutoff -= 1
    elif key == GLUT_KEY_RIGHT:
        if flash_cutoff < 90:
            flash_cutoff += 1
        elif flash_cutoff == 90:
            flash_cutoff = 180
    elif key == GLUT_KEY_F1:
        light_switch[0] = light_switch[0] == False
        if light_switch[0]:
            glEnable(GL_LIGHT0)
        else:
            glDisable(GL_LIGHT0)
    elif key == GLUT_KEY_F2:
        light_switch[1] = light_switch[1] == False
        if light_switch[1]:
            glEnable(GL_LIGHT1)
        else:
            glDisable(GL_LIGHT1)
    elif key == GLUT_KEY_F3:
        light_switch[2] = light_switch[2] == False
        if light_switch[2]:
            glEnable(GL_LIGHT2)
        else:
            glDisable(GL_LIGHT2)
    elif key == GLUT_KEY_F4:
        light_switch[3] = light_switch[3] == False
        if light_switch[3]:
            glEnable(GL_LIGHT3)
        else:
            glDisable(GL_LIGHT3)

    glutPostRedisplay()  # Вызываем процедуру перерисовки


def keyPressed(key, x, y):
    global view_rot
    global view_z_pos
    global view_x_pos
    global speed

    if key == b'a':
        view_rot -= 2
    elif key == b'd':
        view_rot += 2
    elif key == b'w':
        view_z_pos += speed * math.cos(math.radians(view_rot))
        view_x_pos += speed * math.sin(math.radians(view_rot))
    elif key == b's':
        view_z_pos -= speed * math.cos(math.radians(view_rot))
        view_x_pos -= speed * math.sin(math.radians(view_rot))

    view_rot = view_rot % 360

    glutPostRedisplay()


def moon_light():
    glPushMatrix()
    glLoadIdentity()

    glLight(GL_LIGHT0, GL_POSITION, (0, -1, 0, 0))
    glLight(GL_LIGHT0, GL_DIFFUSE, rgba(10, 50, 255))
    glLight(GL_LIGHT0, GL_SPECULAR, rgba(10, 50, 255))
    glPopMatrix()


def player_flashlight():
    global view_rot
    global view_z_pos
    global view_x_pos

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glLight(GL_LIGHT1, GL_POSITION, (view_x_pos, 0, -view_z_pos, 1))
    glRotatef(-view_rot, 0, 1, 0)
    glLight(GL_LIGHT1, GL_DIFFUSE, (1, 1, 1, 1))
    glLight(GL_LIGHT1, GL_SPECULAR, (1, 1, 1, 1))
    glLight(GL_LIGHT1, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
    direction = (0, 0, -1)
    glLight(GL_LIGHT1, GL_SPOT_CUTOFF, flash_cutoff)
    glLight(GL_LIGHT1, GL_SPOT_EXPONENT, flash_exp)
    glLight(GL_LIGHT1, GL_SPOT_DIRECTION, direction)
    glLight(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 0)
    glLight(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.5)
    glPopMatrix()


def projector():
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(3, 2, 1.8)

    if light_switch[3]:
        glMaterialfv(GL_FRONT, GL_EMISSION, (1, 1, 0, 1))
    else:
        glMaterialfv(GL_FRONT, GL_EMISSION, (0, 0, 0, 1))

    glBindTexture(GL_TEXTURE_2D, 0)

    glutSolidCube(0.2)

    glMaterialfv(GL_FRONT, GL_EMISSION, (0, 0, 0, 1))

    glLight(GL_LIGHT3, GL_POSITION, (0, 0, 0, 1))
    glLight(GL_LIGHT3, GL_DIFFUSE, (0.8, 0.8, 0.2, 1))
    glLight(GL_LIGHT3, GL_SPECULAR, (0.8, 0.8, 0.2, 1))

    direction = (0, 0, -1)
    glLight(GL_LIGHT3, GL_SPOT_CUTOFF, 30)
    glLight(GL_LIGHT3, GL_SPOT_DIRECTION, direction)
    glLight(GL_LIGHT3, GL_CONSTANT_ATTENUATION, 0)
    glLight(GL_LIGHT3, GL_LINEAR_ATTENUATION, 0.5)
    glPopMatrix()


def room_light():
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(3, 2.95, -2)

    if light_switch[2]:
        glMaterialfv(GL_FRONT, GL_EMISSION, (1, 1, 0, 1))
    else:
        glMaterialfv(GL_FRONT, GL_EMISSION, (0, 0, 0, 1))

    glBindTexture(GL_TEXTURE_2D, 0)

    glutSolidCube(0.05)

    glMaterialfv(GL_FRONT, GL_EMISSION, (0, 0, 0, 1))

    glLight(GL_LIGHT2, GL_POSITION, (0, 0, 0, 1))
    glLight(GL_LIGHT2, GL_DIFFUSE, (0.8, 0.8, 0.8, 1))
    glLight(GL_LIGHT2, GL_SPECULAR, (0.8, 0.8, 0.8, 1))

    direction = (0, -1, 0)
    glLight(GL_LIGHT2, GL_SPOT_CUTOFF, 180)
    glLight(GL_LIGHT2, GL_SPOT_DIRECTION, direction)
    glLight(GL_LIGHT2, GL_CONSTANT_ATTENUATION, 0)
    glLight(GL_LIGHT2, GL_LINEAR_ATTENUATION, 0.5)
    glPopMatrix()


if __name__ == '__main__':
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(350, 20)

    glutInit(sys.argv)

    glutCreateWindow(b'Sofa?')
    glutDisplayFunc(draw)
    glutSpecialFunc(specialKeys)
    glutKeyboardFunc(keyPressed)

    init()
    glutMainLoop()

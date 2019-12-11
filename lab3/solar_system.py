# Импортируем все необходимые библиотеки:
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math

# Объявляем все глобальные переменные
angle = 1
speed = 0.5


def convert_colors(red, green, blue) -> tuple:
    return red / 255, green / 255, blue / 255


# Процедура инициализации
def init():
    glClearColor(0, 0, 0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glOrtho(-2.0, 2.0, -2.0, 2.0, -2.0, 2.0)  # Определяем границы рисования по горизонтали и вертикали
    glMatrixMode(GL_MODELVIEW)


#  glRotatef(-90, 1.0, 0.0, 0.0)                   # Сместимся по оси Х на 90 градусов


def restore_matrix():
    glPopMatrix()
    glPushMatrix()


def draw_circle():
    glPushMatrix()

    glBegin(GL_POLYGON)
    x = math.cos(359 * math.pi / 180)
    y = math.sin(359 * math.pi / 180)
    for i in range(360):
        glVertex2f(x, y)
        x = math.cos(i * math.pi / 180)
        y = math.sin(i * math.pi / 180)
        glVertex2f(x, y)

    glEnd()
    glPopMatrix()


def draw_sun():
    glPushMatrix()

    glColor(convert_colors(255, 255, 51))
    draw_circle()

    glPopMatrix()


def draw_earth():
    glPushMatrix()

    glScalef(0.5, 0.5, 0.5)
    glColor(convert_colors(26, 26, 255))
    draw_circle()

    draw_moon()

    glPopMatrix()


def draw_moon():
    glPushMatrix()

    glScalef(0.2, 0.2, 0.2)
    glColor(convert_colors(230, 230, 230))
    glRotatef(-angle * 4, 0, 0, 1)
    glTranslatef(8, 0, 0)
    draw_circle()

    glPopMatrix()


def draw_mercury():
    glPushMatrix()

    glScalef(0.2, 0.2, 0.2)
    glColor(convert_colors(237, 160, 70))
    draw_circle()

    glPopMatrix()


def draw_mars():
    glPushMatrix()

    glScalef(1.5, 1.5, 1.5)
    glColor(convert_colors(237, 160, 70))
    draw_circle()

    glPopMatrix()


# Процедура перерисовки
def draw():
    global angle

    while True:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glScalef(0.2, 0.2, 0.2)

        glPushMatrix()
        draw_sun()

        glRotatef(angle * 0.6, 0, 0, 1)
        glTranslatef(8, 0, 0)
        draw_earth()
        glPopMatrix()

        glPushMatrix()
        glRotatef(-angle * 3, 0, 0, 1)
        glTranslatef(3, 0, 0)
        draw_mercury()
        glPopMatrix()

        angle = (angle) % sys.maxsize + speed
        glutSwapBuffers()  # Выводим все нарисованное в памяти на экран


# Использовать двойную буферизацию и цвета в формате RGB (Красный, Зеленый, Синий)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutInitWindowPosition(50, 50)
glutInit(sys.argv)
glutCreateWindow(b"Solar system!")
glutDisplayFunc(draw)
# glutSpecialFunc(specialkeys)
init()
glutMainLoop()

# Импортируем все необходимые библиотеки:
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math as m
import numpy

# Объявляем все глобальные переменные
global xRot # Величина вращения по оси x
global zPos # Величина вращения по оси y
a=0.3

clientwidth = 200
clientheight = 200

# Процедура инициализации
def init():
    global xRot # Величина вращения по оси x
    global zPos # Величина вращения по оси y

    xrot = 0.0 # Величина вращения по оси x = 0
    yrot = 0.0 # Величина вращения по оси y = 0

    glClearColor(0, 0, 0, 1.0)

    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

# Процедура обработки специальных клавиш
def specialkeys(key, x, y):
    global xRot
    global zPos

    # Обработчики для клавиш со стрелками
    if key == GLUT_KEY_UP:      # Клавиша вверх
        xrot -= 2.0             # Уменьшаем угол вращения по оси Х
    if key == GLUT_KEY_DOWN:    # Клавиша вниз
        xrot += 2.0             # Увеличиваем угол вращения по оси Х
    if key == GLUT_KEY_LEFT:    # Клавиша влево
        yrot -= 2.0             # Уменьшаем угол вращения по оси Y
    if key == GLUT_KEY_RIGHT:   # Клавиша вправо
        yrot += 2.0             # Увеличиваем угол вращения по оси Y

    glutPostRedisplay()         # Вызываем процедуру перерисовки

def drawimagefront():
    glViewport(0, 400, clientwidth, clientheight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -2, 2)  # Определяем границы рисования по горизонтали и вертикали
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    drawfigura()

def drawimageleft():
    glViewport(300, 400, clientwidth, clientheight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -2, 2)  # Определяем границы рисования по горизонтали и вертикали
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(90, 0, 1, 0)
    drawfigura()

def drawimageup():
    glViewport(600, 400, clientwidth, clientheight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -2, 2)  # Определяем границы рисования по горизонтали и вертикали
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(90, 1, 0, 0)
    drawfigura()


def drawimageTrimetric():
    glViewport(0, 200, clientwidth, clientheight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -2, 2)  # Определяем границы рисования по горизонтали и вертикали
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(-45, 1, 0, 0)
    glRotatef(-20, 0, 1, 0)
    drawfigura()

def drawimageDimetric():
    fz = 5 / 9;
    glViewport(300, 200, clientwidth, clientheight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -2, 2)  # Определяем границы рисования по горизонтали и вертикали
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(m.degrees(-m.asin(fz / m.sqrt(2))), 1, 0, 0)
    glRotatef(m.degrees(m.asin(fz / m.sqrt(2 - m.pow(fz, 2)))), 0, 1, 0)
    drawfigura()

def drawimageIsometric():
    glViewport(600, 200, clientwidth, clientheight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -2, 2)  # Определяем границы рисования по горизонтали и вертикали
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(32.264, 1, 0, 0)
    glRotatef(-45, 0, 1, 0)
    drawfigura()

def drawimageCabinet():
    glViewport(900, 400, clientwidth, clientheight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -2, 2)  # Определяем границы рисования по горизонтали и вертикали
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    matr = numpy.array(glGetFloatv(GL_MODELVIEW_MATRIX))
    matr[2][0] = -m.cos(m.radians(45))
    matr[2][1] = -m.sin(m.radians(45))
    glLoadMatrixf(matr)
    drawfigura()

def drawimageCavalier():
    glViewport(900, 200, clientwidth, clientheight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -2, 2)  # Определяем границы рисования по горизонтали и вертикали
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    matr = numpy.array(glGetFloatv(GL_MODELVIEW_MATRIX))
    matr[2][0] = -m.cos(m.radians(45)) / 2
    matr[2][1] = -m.sin(m.radians(45)) / 2
    glLoadMatrixf(matr)
    drawfigura()

def drawimagePerOnePoint():
    glViewport(0, 0, clientwidth, clientheight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1.75, -0.25, -0.75, 0.75, 1, 3)
    glTranslatef(-1, 0, -1.75)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    drawfigura()


def drawimagePerTwoPoint():
    glViewport(300, 0, clientwidth, clientheight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-0.75, 0.75, -0.75, 0.75, 1, 3)
    glTranslatef(0, 0, -1.75)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(30, 1, 0, 0)
    drawfigura()


def drawimagePerThreePoint():
    glViewport(600, 0, clientwidth, clientheight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-0.75, 0.75, -0.75, 0.75, 1, 3)
    glTranslatef(0, 0, -1.75)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(-45, 0, 1, 0)
    glRotatef(30, 1, 0, 0)
    drawfigura()


def drawfigura():
    glBegin(GL_LINES)
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 1, 0)
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 1)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0.5)
    glVertex3f(0.5, 0, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0, -0.5, 0.5)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0, 0.5, 0.5)
    glVertex3f(0, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(0.6, 0.7, 0.9)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(0, 1, 0)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0, 0.5, -0.5)
    glVertex3f(0, 0.5, 0.5)
    glEnd()
    #
    glBegin(GL_POLYGON)
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0.5)
    glVertex3f(0, 0.5, 0.5)
    glVertex3f(0, 0.5, -0.5)
    glVertex3f(0, 0, -0.5)
    glEnd()
    #
    glBegin(GL_POLYGON)
    glColor3f(1, 1, 0)
    glVertex3f(0, 0, -0.5)
    glVertex3f(0, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0, -0.5)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(0, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0, -0.5, -0.5)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(1, 0, 1)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(0, 1, 1)
    glVertex3f(0.5, 0, 0.5)
    glVertex3f(0, 0, 0.5)
    glVertex3f(0, 0, -0.5)
    glVertex3f(0.5, 0, -0.5)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(1, 1, 1)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0, 0.5)
    glVertex3f(0.5, 0, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glEnd()

# Процедура перерисовки
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    drawimagefront()
    drawimageleft()
    drawimageup()
    drawimageTrimetric()
    drawimageDimetric()
    drawimageIsometric()
    drawimageCabinet()
    drawimageCavalier()

    drawimagePerOnePoint()
    drawimagePerTwoPoint()
    drawimagePerThreePoint()

    glutSwapBuffers()  # Выводим все нарисованное в памяти на экран

# Использовать двойную буферизацию и цвета в формате RGB (Красный, Зеленый, Синий)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(1200, 600)
glutInitWindowPosition(50, 50)
glutInit(sys.argv)
glutCreateWindow("Projections")
glutDisplayFunc(draw)
glutSpecialFunc(specialkeys)
init()
glutMainLoop()
# Импортируем все необходимые библиотеки:
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np
import math
import sys

# Объявляем все глобальные переменные
a = 0.5
xrot = 0
yrot = 0

array_texture = []


# Процедура обработки специальных клавиш
def specialkeys(key, x, y):
    global xrot
    global yrot
    # Обработчики для клавиш со стрелками
    if key == GLUT_KEY_UP:  # Клавиша вверх
        xrot -= 2.0  # Уменьшаем угол вращения по оси Х
    if key == GLUT_KEY_DOWN:  # Клавиша вниз
        xrot += 2.0  # Увеличиваем угол вращения по оси Х
    if key == GLUT_KEY_LEFT:  # Клавиша влево
        yrot -= 2.0  # Уменьшаем угол вращения по оси Y
    if key == GLUT_KEY_RIGHT:  # Клавиша вправо
        yrot += 2.0  # Увеличиваем угол вращения по оси Y

    print(key)

    glutPostRedisplay()  # Вызываем процедуру перерисовки


# Процедура инициализации
def init():
    glClearColor(a, 0.5, 0.5, 1.0)
    glMatrixMode(GL_PROJECTION)
    glOrtho(-5.0, 5.0, -5.0, 5.0, -5.0, 5.0)  # Определяем границы рисования по горизонтали и вертикали
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    glBindTexture(GL_TEXTURE_2D, 1)
    load_texture("1.bmp")
    glBindTexture(GL_TEXTURE_2D, 2)
    load_texture("2.bmp")
    glBindTexture(GL_TEXTURE_2D, 3)
    load_texture("3.bmp")
    glBindTexture(GL_TEXTURE_2D, 4)
    load_texture("4.bmp")
    glBindTexture(GL_TEXTURE_2D, 5)
    load_texture("5.bmp")
    glBindTexture(GL_TEXTURE_2D, 6)
    load_texture("6.bmp")


def load_texture(file_name: str):
    global array_texture
    image = Image.open(file_name)
    image.load()  # this is not a list, nor is it list()'able
    width, height = image.size

    array_texture = np.asarray(image, dtype='uint8')
    array_texture = array_texture[::-1]

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, array_texture)


# Процедура перерисовки
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glRotatef(xrot, 1, 0, 0)
    glRotatef(yrot, 0, 1, 0)
    glTranslate(-1, -1, 1)
    draw_cube()

    glutSwapBuffers()  # Выводим все нарисованное в памяти на экран


def draw_cube():
    glPushMatrix()

    ss = [0.5, 0.0, 0.0]
    tt = [0.0, 0.5, 0.0]
    glTexGenf(GL_S, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)

    glTexGenf(GL_T, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    glBindTexture(GL_TEXTURE_2D, 1)

    glBegin(GL_POLYGON)
    glVertex3f(0, 0, 0)
    glVertex3f(2, 0, 0)
    glVertex3f(2, 2, 0)
    glVertex3f(0, 2, 0)
    glEnd()

    ss = [0.0, 0.0, -0.5]
    tt = [0.0, 0.5, 0.0]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    glBindTexture(GL_TEXTURE_2D, 2)

    glBegin(GL_POLYGON)
    glVertex3f(2, 0, 0)
    glVertex3f(2, 2, 0)
    glVertex3f(2, 2, -2)
    glVertex3f(2, 0, -2)
    glEnd()

    ss = [-0.5, 0.0, 0.0]
    tt = [0.0, 0.5, 0.0]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    glBindTexture(GL_TEXTURE_2D, 6)

    glBegin(GL_POLYGON)
    glVertex3f(2, 0, -2)
    glVertex3f(2, 2, -2)
    glVertex3f(0, 2, -2)
    glVertex3f(0, 0, -2)
    glEnd()

    ss = [0.0, 0.0, 0.5]
    tt = [0.0, 0.5, 0.0]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    glBindTexture(GL_TEXTURE_2D, 5)

    glBegin(GL_POLYGON)
    glVertex3f(0, 0, -2)
    glVertex3f(0, 2, -2)
    glVertex3f(0, 2, 0)
    glVertex3f(0, 0, 0)
    glEnd()

    ss = [0.5, 0.0, 0.0]
    tt = [0.0, 0.0, -0.5]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    glBindTexture(GL_TEXTURE_2D, 3)

    glBegin(GL_POLYGON)
    glVertex3f(0, 2, 0)
    glVertex3f(0, 2, -2)
    glVertex3f(2, 2, -2)
    glVertex3f(2, 2, 0)
    glEnd()

    ss = [0.5, 0.0, 0.0]
    tt = [0.0, 0.0, 0.5]

    glTexGenfv(GL_S, GL_OBJECT_PLANE, ss)
    glTexGenfv(GL_T, GL_OBJECT_PLANE, tt)

    glBindTexture(GL_TEXTURE_2D, 4)

    glBegin(GL_POLYGON)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, -2)
    glVertex3f(2, 0, -2)
    glVertex3f(2, 0, 0)
    glEnd()

    glPopMatrix()


# Здесь начинается выполнение программы
# Использовать двойную буферизацию и цвета в формате RGB (Красный, Зеленый, Синий)

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
# Указываем начальный размер окна (ширина, высота)
glutInitWindowSize(500, 500)
# Указываем начальное положение окна относительно левого верхнего угла экрана
glutInitWindowPosition(50, 50)
# Инициализация OpenGl
glutInit(sys.argv)
# Создаем окно с заголовком "Happy New Year!"
glutCreateWindow("FEAR AND HATE IN LAS-VEGAS")
# Определяем процедуру, отвечающую за перерисовку
glutDisplayFunc(draw)
# Определяем процедуру, отвечающую за обработку клавиш
glutSpecialFunc(specialkeys)
# Вызываем нашу функцию инициализации
init()
# Запускаем основной цикл
glutMainLoop()

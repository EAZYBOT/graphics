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

zpos = 0

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


def keyPressed(key, x, y):
    global zpos

    if key == b"w":
        zpos += 1
    elif key == b"s":
        zpos -= 1

    glutPostRedisplay()


# Процедура инициализации
def init():
    glClearColor(a, 0.5, 0.5, 1.0)
    glMatrixMode(GL_PROJECTION)
    glFrustum(-5.0, 5.0, -5.0, 5.0, 5.0, 200.0)  # Определяем границы рисования по горизонтали и вертикали
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_AUTO_NORMAL)
    glEnable(GL_TEXTURE_2D)
    load_texture()


def load_texture():
    global array_texture

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)

    file_names = []
    for i in range(8):
        file_names.append("textures/{}.bmp".format(2 ** i))
    file_names.reverse()

    for i, file_name in enumerate(file_names):
        image = Image.open(file_names[i])
        image.load()  # this is not a list, nor is it list()'able
        width, height = image.size

        array_texture = image.tobytes("raw", "RGB", 0, -1)
        glTexImage2D(GL_TEXTURE_2D, i, GL_RGB, width, height,
                     0, GL_RGB, GL_UNSIGNED_BYTE, array_texture)


# Процедура перерисовки
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()

    glTranslate(0, 0, zpos)
    print(zpos)
    glRotatef(xrot, 1, 0, 0)
    glRotatef(yrot, 0, 1, 0)
    # glTranslate(-1, -1, 1)
    draw_edge(5, 5)

    glPopMatrix()
    glutSwapBuffers()  # Выводим все нарисованное в памяти на экран


def draw_edge(xSize, ySize):
    glTranslatef(-xSize / 2, -ySize / 2, 0)

    glBegin(GL_POLYGON)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, 0)
    glEnd()


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
glutKeyboardFunc(keyPressed)
# Вызываем нашу функцию инициализации
init()
# Запускаем основной цикл
glutMainLoop()

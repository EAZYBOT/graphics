# Импортируем все необходимые библиотеки:
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math

# Объявляем все глобальные переменные
global xrot  # Величина вращения по оси x
global yrot  # Величина вращения по оси y
a = 0.5


def convert_colors(red, green, blue) -> tuple:
    return red / 255, green / 255, blue / 255


# Процедура инициализации
def init():
    global xrot  # Величина вращения по оси x
    global yrot  # Величина вращения по оси y

    xrot = 0.0  # Величина вращения по оси x = 0
    yrot = 0.0  # Величина вращения по оси y = 0
    glClearColor(0, 0, 0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glOrtho(-2.0, 2.0, -2.0, 2.0, -2.0, 2.0)  # Определяем границы рисования по горизонтали и вертикали
    glMatrixMode(GL_MODELVIEW)


#  glRotatef(-90, 1.0, 0.0, 0.0)                   # Сместимся по оси Х на 90 градусов

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

    glutPostRedisplay()  # Вызываем процедуру перерисовки


def restore_matrix():
    glPopMatrix()
    glPushMatrix()


def get_triangle_height() -> float:
    hypo = math.sqrt(2 * a**2)
    return hypo / 2


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
    glRotatef(-xrot * 4, 0, 0, 1)
    glTranslatef(8, 0, 0)
    draw_circle()

    glPopMatrix()

# Процедура перерисовки
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glScalef(0.5, 0.5, 0.5)
    draw_sun()

    glRotatef(xrot, 0, 0, 1)
    glTranslatef(3, 0, 0)
    draw_earth()



    glutSwapBuffers()  # Выводим все нарисованное в памяти на экран


# Использовать двойную буферизацию и цвета в формате RGB (Красный, Зеленый, Синий)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutInitWindowPosition(50, 50)
glutInit(sys.argv)
glutCreateWindow(b"Solar system!")
glutDisplayFunc(draw)
glutSpecialFunc(specialkeys)
init()
glutMainLoop()

# Импортируем все необходимые библиотеки:
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math

# Объявляем все глобальные переменные
global xRot  # Величина вращения по оси x
global zPos  # Величина вращения по оси y
a = 0.5


# Процедура инициализации
def init():
    global xRot  # Величина вращения по оси x
    global zPos  # Величина вращения по оси y

    xrot = 0.0  # Величина вращения по оси x = 0
    yrot = 0.0  # Величина вращения по оси y = 0
    glClearColor(0, 0, 0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glOrtho(-2.0, 2.0, -2.0, 2.0, -2.0, 2.0)  # Определяем границы рисования по горизонтали и вертикали
    glMatrixMode(GL_MODELVIEW)


#  glRotatef(-90, 1.0, 0.0, 0.0)                   # Сместимся по оси Х на 90 градусов

# Процедура обработки специальных клавиш
def specialkeys(key, x, y):
    global xRot
    global zPos

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


def draw_house():
    glPushMatrix()

    glTranslatef(a, a, 0)
    glRotatef(180, 0, 0, 1)

    glBegin(GL_POLYGON)
    glVertex3f(0, 0, 0)
    glVertex3f(0, a, 0)
    glVertex3f(a, 0, 0)
    glEnd()

    restore_matrix()

    glBegin(GL_POLYGON)
    glVertex3f(0, 0, 0)
    glVertex3f(0, a, 0)
    glVertex3f(a, 0, 0)
    glEnd()

    restore_matrix()

    glTranslate(a/2, a + get_triangle_height(), 0)
    glRotatef(-135, 0, 0, 1)

    glBegin(GL_POLYGON)
    glVertex3f(0, 0, 0)
    glVertex3f(0, a, 0)
    glVertex3f(a, 0, 0)
    glEnd()

    glPopMatrix()


# Процедура перерисовки
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslate(1, 0, 0)
    glScalef(1.2, 1.2, 0)
    draw_house()

    glLoadIdentity()
    draw_house()

    glLoadIdentity()
    glTranslate(-1, 0, 0)
    glScalef(0.6, 0.6, 0)
    draw_house()

    glutSwapBuffers()  # Выводим все нарисованное в памяти на экран


# Использовать двойную буферизацию и цвета в формате RGB (Красный, Зеленый, Синий)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutInitWindowPosition(50, 50)
glutInit(sys.argv)
glutCreateWindow(b"Happy New Year!")
glutDisplayFunc(draw)
glutSpecialFunc(specialkeys)
init()
glutMainLoop()

# Импортируем все необходимые библиотеки:
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import sys

# Объявляем все глобальные переменные
a = 0.5
xrot = 0
yrot = 0


directionalAngleY = 0
directionalAngleX = 0

positionalY = 0
positionalX = 0

cutoff = 70
spot_exponent = 5

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
    glOrtho(-3.0, 3.0, -3.0, 3.0, -3.0, 3.0)  # Определяем границы рисования по горизонтали и вертикали
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)  # Включаем освещение
    glShadeModel(GL_SMOOTH)
    glEnable(GL_AUTO_NORMAL)  # Включаем один источник света

    glEnable(GL_LIGHT0)  # Включаем один источник света
    glEnable(GL_LIGHT1)


def draw_directional_light():
    glPushMatrix()
    glLoadIdentity()
    glRotate(directionalAngleY, 0, 1, 0)
    glRotate(directionalAngleX, 1, 0, 0)
    glLight(GL_LIGHT1, GL_POSITION, (0, 0, 1, 0))
    glLight(GL_LIGHT1, GL_DIFFUSE, (1, 1, 1, 1))
    glLight(GL_LIGHT1, GL_SPECULAR, (1, 1, 1, 1))
    glPopMatrix()


def draw_positional_light():
    glPushMatrix()
    glLoadIdentity()
    glLight(GL_LIGHT0, GL_POSITION, (positionalX, positionalY, 6, 1))
    glLight(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glLight(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
    glLight(GL_LIGHT0, GL_SPOT_CUTOFF, cutoff)
    glLight(GL_LIGHT0, GL_SPOT_EXPONENT, spot_exponent)
    glLight(GL_LIGHT0, GL_SPOT_DIRECTION, (0, 0, -1))
    glPopMatrix()


# Процедура перерисовки
def draw():
    #   glViewport(0,0,100,100)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glPushMatrix()

    glTranslatef(-2, 0, 0)
    glMaterial(GL_FRONT, GL_DIFFUSE, (0.2, 0.9, 0.2, 1))
    glMaterial(GL_FRONT, GL_SPECULAR, (0.4, 0.4, 0.4, 1))
    glMaterial(GL_FRONT, GL_SHININESS, 30)
    glutSolidSphere(0.5, 15, 15)
    glPopMatrix()

    glPushMatrix()
    glLoadIdentity()
    glMaterial(GL_FRONT, GL_DIFFUSE, (0.9, 0.2, 0.2, 1))
    glMaterial(GL_FRONT, GL_SPECULAR, (0.1, 0.1, 0.1, 1))
    glTranslatef(2, 0, 0)
    glutSolidSphere(0.5, 30, 30)
    glPopMatrix()

    glPushMatrix()  # Возвращаем сохраненное положение "камеры"
    glTranslatef(-0.8, 0, 0)
    glRotatef(xrot, 1, 0, 0)
    glRotatef(yrot, 0, 1, 0)
    glMaterial(GL_FRONT, GL_DIFFUSE, (0.2, 0.2, 0.9, 1))
    glMaterial(GL_FRONT, GL_SPECULAR, (0, 0, 0, 1))
    glutSolidCube(1)
    glPopMatrix()

    glTranslatef(0.8, 0, 0)
    glRotatef(xrot, 1, 0, 0)
    glRotatef(yrot, 0, 1, 0)
    glMaterial(GL_FRONT, GL_SHININESS, 0)
    glMaterial(GL_FRONT, GL_DIFFUSE, (0.9, 0.9, 0.2, 1))
    glutSolidCube(1)

    # draw_directional_light()
    draw_positional_light()

    glutSwapBuffers()  # Выводим все нарисованное в памяти на экран


def keyPressed(key, x, y):
    global directionalAngleY
    global directionalAngleX
    global positionalX
    global positionalY
    global spot_exponent
    global cutoff

    if key == b'a':
        directionalAngleY -= 5
    elif key == b'd':
        directionalAngleY += 5
    elif key == b'w':
        directionalAngleX -= 5
    elif key == b's':
        directionalAngleX += 5
    elif key == b'j':
        positionalX -= 0.1
    elif key == b'l':
        positionalX += 0.1
    elif key == b'i':
        positionalY += 0.1
    elif key == b'k':
        positionalY -= 0.1
    elif key == b'q':
        if spot_exponent >= 1:
            spot_exponent -= 1
            print('exponent:', spot_exponent)
    elif key == b'e':
        if spot_exponent <= 127:
            spot_exponent += 1
            print('exponent:', spot_exponent)
    elif key == b'u':
        if cutoff >= 1:
            cutoff -= 1
            print('cutoff:', cutoff)
    elif key == b'o':
        if cutoff <= 89:
            cutoff += 1
            print('cutoff:', cutoff)
    glutPostRedisplay()

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
glutCreateWindow("Happy New Year!")
# Определяем процедуру, отвечающую за перерисовку
glutDisplayFunc(draw)
# Определяем процедуру, отвечающую за обработку клавиш
glutSpecialFunc(specialkeys)
glutKeyboardFunc(keyPressed)
# Вызываем нашу функцию инициализации
init()
# Запускаем основной цикл
glutMainLoop()

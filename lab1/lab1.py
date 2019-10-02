from tkinter import *
import random

x, y, color, shape_type = 0, 0, "blue", "line"
shape = 1
should_draw = False
shapes = ('line', 'rect', 'circle')


def btn_press(event):
    global shape, x, y, should_draw

    should_draw = True
    x = event.x
    y = event.y
    shape = canvas.create_line(x, y, x, y, fill=color, smooth=1, width=2)


def btn_release(event):
    global shape, should_draw, x, y

    canvas.delete(shape)
    xx = event.x
    yy = event.y

    if shape_type == "line":
        shape = canvas.create_line(x, y, xx, yy, fill=color, smooth=1, width=2)
    elif shape_type == "rect":
        shape = canvas.create_rectangle(x, y, xx, yy, fill=color, stipple='gray25')
    elif shape_type == "circle":
        shape = canvas.create_oval(x, y, xx, yy, fill=color, stipple='gray12')

    should_draw = False


def move(event):
    global shape

    if should_draw:
        xx = event.x
        yy = event.y
        canvas.coords(shape, x, y, xx, yy)


def change_color():
    global color

    r = lambda: random.randint(0, 255)
    color = '#%02X%02X%02X' % (r(), r(), r())


def change_type():
    global shape_type

    r = lambda: random.randint(0, 2)
    shape_type = shapes[r()]


tk = Tk()
tk.title("lab1")
tk.geometry("500x500")
tk.bind('<ButtonPress-1>', btn_press)
tk.bind('<ButtonRelease-1>', btn_release)
tk.bind('<Motion>', move)

btnFrame = Frame(tk)
btnFrame.pack()

btnColor = Button(btnFrame)
btnColor["text"] = "Цвет"
btnColor.pack(side="left")
btnColor["command"] = change_color

btnType = Button(btnFrame)
btnType["text"] = "Тип фигуры"
btnType.pack(side="left")
btnType["command"] = change_type

canvas = Canvas(tk)
canvas["width"] = 500
canvas["height"] = 500
canvas["background"] = "#ffffff"
canvas.pack()

tk.mainloop()

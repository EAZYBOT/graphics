from tkinter import *
import random
from collections import deque

x, y, color, shape_type = 0, 0, "blue", "line"
shape = 1
shape_right = 1
should_draw = False
should_draw_right = False
shapes = ('line', 'rect', 'circle')

deq = deque()

models = []

test_model = {"x0": 0, "y0": 0, "x1": 1, "y1": 1, "type_shape": "line", "fill": "blue", "width": 1, "id": 0}
test_model2 = {"x0": 0.25, "y0": 0.25, "x1": 0.5, "y1": 0.5, "type_shape": "rect", "fill": "blue", "width": 1, "id": 0}
test_model3 = {"x0": 0.75, "y0": 0.75, "x1": 1, "y1": 1, "type_shape": "circle", "fill": "blue", "width": 1, "id": 0}

maxX = 500
maxY = 500

win = {"minX": 0, "minY": 0, "maxX": 1, "maxY": 1}
vp = {"minX": 0, "minY": 0, "maxX": maxX, "maxY": maxY}


def NDC_to_DC(coordX = 0, coordY = 0):
    newCoordX, newCoordY = coordX, coordY
    if win["maxX"] - win["minX"] > 0.00000005:
        newCoordX = vp["minX"] + ((vp["maxX"] - vp["minX"])/(win["maxX"] - win["minX"])) * (coordX - win["minX"])
    if win["maxY"] - win["minY"] > 0.00000005:
        newCoordY = vp["minY"] + ((vp["maxY"] - vp["minY"])/(win["maxY"] - win["minY"])) * (coordY - win["minY"])
    return newCoordX, newCoordY

def DC_to_NDC(coordX = 0, coordY = 0):
    newCoordX, newCoordY = coordX, coordY
    if vp["maxX"] - vp["minX"] > 0.00000005:
        newCoordX = win["minX"] + ((win["maxX"] - win["minX"]) / (vp["maxX"] - vp["minX"])) * (coordX - vp["minX"])
    if vp["maxY"] - vp["minY"] > 0.00000005:
        newCoordY = win["minY"] + ((win["maxY"] - win["minY"]) / (vp["maxY"] - vp["minY"])) * (coordY - vp["minY"])

    return newCoordX, newCoordY

def reDrawAll():
    global models

    for item in models:
        canvas.delete(item["id"])

        vpCoords0 = NDC_to_DC(item["x0"], item["y0"])
        vpCoords1 = NDC_to_DC(item["x1"], item["y1"])

        if item["type_shape"] == "line":
            item["id"] = canvas.create_line(vpCoords0[0], vpCoords0[1], vpCoords1[0], vpCoords1[1], fill=item["fill"],
                                            width=item["width"])
        elif item["type_shape"] == "rect":
            item["id"] = canvas.create_rectangle(vpCoords0[0], vpCoords0[1], vpCoords1[0], vpCoords1[1],
                                                 fill=item["fill"], width=item["width"])
        elif item["type_shape"] == "circle":
            item["id"] = canvas.create_oval(vpCoords0[0], vpCoords0[1], vpCoords1[0], vpCoords1[1], fill=item["fill"],
                                            width=item["width"])

def unzoom():
    global win

    if len(deq) != 0:
        win = deq.pop()

    reDrawAll()


def btn_press_zoom(event):
    global x, y, shape_right, should_draw_right

    x = event.x
    y = event.y
    should_draw_right = True
    shape_right = canvas.create_rectangle(x, y, x, y)

def btn_release_zoom(event):
    global x, y, shape_right, should_draw_right, win, deq

    canvas.delete(shape_right)
    should_draw_right = False
    xx = event.x
    yy = event.y

    dX = abs(xx - x)
    dY = abs(yy - y)
    dD = min(dX, dY)

    w, h = 1, 1
    if xx - x < 0:
        w = -1
    if yy - y < 0:
        h = -1

    newX, newY = DC_to_NDC(x, y)
    newXX, newYY = DC_to_NDC(x + dD*w, y + dD*h)

    if newX > newXX:
        tmp = newX
        newX = newXX
        newXX = tmp

    if newY > newYY:
        tmp = newY
        newY = newYY
        newYY = tmp

    deq.append(win)
    win = {"minX": newX, "minY": newY, "maxX": newXX, "maxY": newYY}

    reDrawAll()

def btn_press(event):
    global shape, x, y, should_draw

    should_draw = True
    x = event.x
    y = event.y
    shape = canvas.create_line(x, y, x, y, fill=color, smooth=1, width= 1)


def btn_release(event):
    global shape, should_draw, x, y

    canvas.delete(shape)
    xx = event.x
    yy = event.y

    newX, newY = DC_to_NDC(x, y)
    newXX, newYY = DC_to_NDC(xx, yy)

    primitiv = {"x0": newX, "y0": newY, "x1": newXX, "y1": newYY, "type_shape": shape_type, "fill": color, "width": 1,
             "id": 0}
    models.append(primitiv)
    reDrawAll()
    #
    # if shape_type == "line":
    #     shape = canvas.create_line(x, y, xx, yy, fill=color, smooth=1, width=2)
    # elif shape_type == "rect":
    #     shape = canvas.create_rectangle(x, y, xx, yy, fill=color, stipple='gray25')
    # elif shape_type == "circle":
    #     shape = canvas.create_oval(x, y, xx, yy, fill=color, stipple='gray12')

    should_draw = False


def move(event):
    global shape, shape_right

    xx = event.x
    yy = event.y

    if should_draw:
        canvas.coords(shape, x, y, xx, yy)
    if should_draw_right:
        dX = abs(xx - x)
        dY = abs(yy - y)
        w, h = 1, 1
        if xx - x < 0:
            w = -1
        if yy - y < 0:
            h = -1

        dD = min(dX, dY)
        canvas.coords(shape_right, x, y, x + dD*w, y + dD*h)



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
tk.geometry("600x600")

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

btnUnzoom = Button(btnFrame)
btnUnzoom["text"] = "Unzoom"
btnUnzoom.pack(side="left")
btnUnzoom["command"] = unzoom

canvas = Canvas(tk)
canvas["width"] = 500
canvas["height"] = 500
canvas["background"] = "#ffffff"

canvas.bind('<ButtonPress-1>', btn_press)
canvas.bind('<ButtonRelease-1>', btn_release)
canvas.bind('<ButtonPress-3>', btn_press_zoom)
canvas.bind('<ButtonRelease-3>', btn_release_zoom)
canvas.bind('<Motion>', move)

canvas.pack()

models.append(test_model)
models.append(test_model2)
models.append(test_model3)

deq.append(win)

reDrawAll()

tk.mainloop()

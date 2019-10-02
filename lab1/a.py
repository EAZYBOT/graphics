import tkinter
import math

xx = 0
yy = 0
go = 1
TypePrim = 'line'
rubber = 1


def bp(event):
    global xx
    global yy
    global go
    global rubber
    go = 1
    xx = event.x
    yy = event.y
    rubber = canvas.create_line(xx, yy, xx, yy, fill="black", smooth=1, width=10)


def br(event):
    global xx
    global yy
    global go
    global TypePrim
    canvas.delete(rubber)
    ex = event.x
    ey = event.y
    if TypePrim == "line":
        canvas.create_line(xx, yy, ex, ey, fill="blue", smooth=1)
    elif TypePrim == "Rect":
        canvas.create_rectangle(xx, yy, ex, ey, fill="blue")
    else:
        rad = math.sqrt((xx - ex) ** 2 + (yy - ey) ** 2)
        print(rad)
        print("coords:", xx - rad, yy - rad, xx + rad, yy + rad)
        canvas.create_oval(xx - rad, yy - rad, xx + rad, yy + rad, fill="blue")


def move(event):
    global xx
    global yy
    global ex
    global ey
    global go
    global rubber
    if go:
        ex = event.x
        ey = event.y
        canvas.coords(rubber, xx, yy, ex, ey)


def Primline():
    global TypePrim
    TypePrim = "line"


def PrimRect():
    global TypePrim
    TypePrim = "Rect"


def PrimOval():
    global TypePrim
    TypePrim = "Oval"


tk = tkinter.Tk()
tk.title("Sample")
tk.geometry("500x500+300+300")
TypePrim = "line"
tk.bind('<ButtonPress-1>', bp)
tk.bind('<ButtonRelease-1>', br)
tk.bind('<Motion>', move)

fr = tkinter.Frame(tk)
fr.pack()

button = tkinter.Button(fr)
button["text"] = "Line"
button["command"] = Primline
button.pack(side="left")
buttonr = tkinter.Button(fr)
buttonr["text"] = "Rect"
buttonr["command"] = PrimRect
buttonr.pack(side="left")
buttono = tkinter.Button(fr)
buttono["text"] = "Circle"
buttono["command"] = PrimOval
buttono.pack(side="left")

canvas = tkinter.Canvas(tk)
canvas["height"] = 500
canvas["width"] = 500
# canvas["background"] = "#eeeeff"
canvas.background = "#ffffff"
canvas["borderwidth"] = 2
canvas.pack()
# canvas.create_text(20,10,text="20,10")
# canvas.create_text(460,350,text="460,350")


tk.mainloop()

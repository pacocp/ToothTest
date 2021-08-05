import pandas as pd
from tkinter import Tk, Label


def read_file(file_name):
    extension = file_name.split('.')[-1]
    if extension == 'csv':
        data = pd.read_csv(file_name)
    elif extension == 'xlsx':
        data = pd.read_csv(file_name)
    else:
        data = ''

    return data


def RGBtoHEX(r, g, b):
    def clamp(x):
        return max(0, min(x, 255))

    return "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))


def error_popup(title, text):
    app = Tk()
    app.title(title)
    app.geometry("500x300+200+200")
    label = Label(app, text=text, height=100, width=100)
    label.pack()
    app.mainloop()

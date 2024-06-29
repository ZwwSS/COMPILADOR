import os
import codecs
from lexico import tokens, analizador
from sintactico import prueba, parser
from tkinter import *
from tkinter import filedialog as FileDialog
from tkinter import messagebox

# Ventana que muestra los resultados
def Ventana2(data, title):
    vt2 = Tk()
    vt2.title(title)
    vt2.geometry('400x400')
    canvas = Canvas(vt2)
    scroll_y = Scrollbar(vt2, orient="vertical", command=canvas.yview)
    frame = Frame(canvas)
    i = 0
    for item in data:
        e = Label(frame, text=item)
        e.grid(row=i, column=2)
        i += 1
    canvas.create_window(0, 0, anchor='nw', window=frame)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set)
    canvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')
    vt2.mainloop()

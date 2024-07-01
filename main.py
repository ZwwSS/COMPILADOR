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

def Ventana():
    def lexico():
        # Analizador léxico
        cadena = texto.get(1.0, 'end-1c')
        if len(cadena) > 0:
            lexico = analizador
            lexico.input(cadena)
            tok = lexico.token()
            a_tok = []
            while True:
                tok = lexico.token()
                if not tok: break
                a_tok.append(tok)
            Ventana2(a_tok, "Analizador Léxico")
        else:
            messagebox.showwarning(message="Debes escribir código !!", title="Error")

    def sintactico():
        # Analizador sintáctico
        cadena = texto.get(1.0, 'end-1c')
        if len(cadena) > 0:
            cad = []
            for i in prueba(cadena):
                if i != "[None]" and "Error sintactico" not in i:
                    cad.append(i)
            Ventana2(cad, "Analizador Sintáctico")
        else:
            messagebox.showwarning(message="Debes escribir código !!", title="Error")

    def nuevo():
        mensaje.set('Nuevo fichero')
        texto.delete(1.0, END)

    def abrir():
        global ruta
        mensaje.set('Abrir fichero')
        ruta = FileDialog.askopenfilename(
            initialdir='',
            filetypes=(("Ficheros de texto", "*.txt"),),
            title="Abrir un fichero."
        )
        if ruta:
            with open(ruta, 'r') as fichero:
                contenido = fichero.read()
                texto.delete(1.0, END)
                texto.insert(INSERT, contenido)
                vt.title(os.path.basename(ruta) + " - Mi editor")

    def guardar():
        global ruta
        if ruta:
            contenido = texto.get(1.0, 'end-1c')
            with open(ruta, 'w') as fichero:
                fichero.write(contenido)
            mensaje.set('Fichero guardado correctamente')
        else:
            guardar_como()

    def guardar_como():
        global ruta
        mensaje.set("Guardar fichero como")
        fichero = FileDialog.asksaveasfile(
            title="Guardar fichero", mode="w", defaultextension=".txt",
            filetypes=(("Ficheros de texto", "*.txt"),)
        )
        if fichero:
            ruta = fichero.name
            contenido = texto.get(1.0, 'end-1c')
            with open(ruta, 'w') as f:
                f.write(contenido)
            mensaje.set("Fichero guardado correctamente")
        else:
            mensaje.set("Guardado cancelado")
            ruta = ""

    ruta = ''

    # Main
    vt = Tk()
    vt.title("Mi editor")
    vt.geometry('800x600')

    # Menú superior
    menubar = Menu(vt)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Nuevo", command=nuevo)
    filemenu.add_command(label="Abrir", command=abrir)
    filemenu.add_command(label="Guardar", command=guardar)
    filemenu.add_command(label="Guardar como", command=guardar_como)
    filemenu.add_separator()
    filemenu.add_command(label="Salir", command=vt.quit)
    menubar.add_cascade(label="Archivo", menu=filemenu)

    ejecutar_menu = Menu(menubar, tearoff=0)
    ejecutar_menu.add_command(label="Ejecutar Analizador Léxico", command=lexico)
    ejecutar_menu.add_command(label="Ejecutar Analizador Sintáctico", command=sintactico)
    menubar.add_cascade(label="Ejecutar", menu=ejecutar_menu)

    vt.config(menu=menubar)

    # Caja de texto central
    texto = Text(vt, wrap='word')
    texto.pack(fill='both', expand=True)

    # Barra de estado
    mensaje = StringVar()
    mensaje.set('Bienvenido a tu editor')
    barra_estado = Label(vt, textvariable=mensaje, bd=1, relief=SUNKEN, anchor=W)
    barra_estado.pack(side=BOTTOM, fill=X)

    vt.mainloop()

if __name__ == "__main__":
    Ventana()
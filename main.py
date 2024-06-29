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

# Función para abrir el archivo
def abrir_archivo():
    ruta = FileDialog.askopenfilename(
        initialdir='.', 
        filetypes=(("Ficheros de texto", "*.txt"),),
        title="Abrir un archivo de texto"
    )
    if ruta:
        try:
            with codecs.open(ruta, 'r', 'utf-8') as f:
                contenido = f.read()
                txt_editor.delete(1.0, END)
                txt_editor.insert(INSERT, contenido)
        except Exception as e:
            messagebox.showerror("Error", f"No se puede abrir el archivo: {e}")

# Función para analizar el archivo
def analizar():
    contenido = txt_editor.get(1.0, END)
    try:
        resultado_lexico = analizador(contenido)
        resultado_sintactico = prueba(contenido)
        Ventana2(resultado_lexico, "Resultado Léxico")
        Ventana2(resultado_sintactico, "Resultado Sintáctico")
    except Exception as e:
        messagebox.showerror("Error", f"No se puede analizar el archivo: {e}")

# Ventana principal
root = Tk()
root.title("Analizador Léxico y Sintáctico")
root.geometry('600x400')

# Crear menú
menubar = Menu(root)
root.config(menu=menubar)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Abrir", command=abrir_archivo)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=root.quit)
menubar.add_cascade(label="Archivo", menu=filemenu)

# Crear editor de texto
txt_editor = Text(root, wrap='word')
txt_editor.pack(expand=YES, fill=BOTH)

# Crear botón para analizar
btn_analizar = Button(root, text="Analizar", command=analizar)
btn_analizar.pack(side=BOTTOM)

# Iniciar la aplicación
root.mainloop()

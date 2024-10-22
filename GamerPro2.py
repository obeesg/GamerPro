import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk  # Asegúrate de instalar Pillow con "pip install Pillow"
import mysql.connector

# Conexión a la base de datos MySQL
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="bibliouser2",
        password="Strategas.2024%$#",
        database="gestion_videojuegos"
    )

# Función para agregar un videojuego a la base de datos
def agregar_videojuego():
    titulo = entry_titulo.get()
    genero = entry_genero.get()
    clasificacion = entry_clasificacion.get()
    plataforma = entry_plataforma.get()

    if titulo and genero and clasificacion and plataforma:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO videojuegos (titulo, genero, clasificacion, plataforma) VALUES (%s, %s, %s, %s)", 
                       (titulo, genero, clasificacion, plataforma))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Videojuego agregado correctamente")
        limpiar_campos()
    else:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")

# Función para mostrar todos los videojuegos en una ventana nueva
def mostrar_videojuegos():
    ventana_lista = tk.Toplevel()
    ventana_lista.title("Lista de Videojuegos")
    ventana_lista.geometry("600x200")
    
    # Scrollbar
    frame = tk.Frame(ventana_lista)
    frame.pack(fill=tk.BOTH, expand=1)

    canvas_lista = tk.Canvas(frame)
    canvas_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas_lista.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas_lista.configure(yscrollcommand=scrollbar.set)
    canvas_lista.bind('<Configure>', lambda e: canvas_lista.configure(scrollregion=canvas_lista.bbox("all")))

    list_frame = tk.Frame(canvas_lista)
    canvas_lista.create_window((0, 0), window=list_frame, anchor="nw")

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videojuegos")
    videojuegos = cursor.fetchall()
    conn.close()

    for videojuego in videojuegos:
        frame_fila = tk.Frame(list_frame)
        frame_fila.pack(fill=tk.X, padx=10, pady=5)

        lbl_info = tk.Label(frame_fila, text=f"{videojuego[1]} ({videojuego[2]}, {videojuego[3]}, {videojuego[4]})")
        lbl_info.pack(side=tk.LEFT)

        # Botón para eliminar videojuego
        btn_eliminar = tk.Button(frame_fila, text="Eliminar", bg="red", command=lambda id=videojuego[0]: eliminar_videojuego(id))
        btn_eliminar.pack(side=tk.RIGHT, padx=5)

        # Botón para actualizar videojuego
        btn_actualizar = tk.Button(frame_fila, text="Actualizar Informacion", bg="blue", command=lambda id=videojuego[0]: abrir_ventana_actualizar(id))
        btn_actualizar.pack(side=tk.RIGHT)

# Función para eliminar un videojuego
def eliminar_videojuego(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM videojuegos WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Videojuego eliminado correctamente")
    mostrar_videojuegos()

# Función para abrir ventana de actualización de videojuego
def abrir_ventana_actualizar(id):
    ventana_actualizar = tk.Toplevel()
    ventana_actualizar.title("Actualizar Videojuego")
    ventana_actualizar.geometry("600x200")

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videojuegos WHERE id = %s", (id,))
    videojuego = cursor.fetchone()
    conn.close()

    if videojuego:
        lbl_titulo = tk.Label(ventana_actualizar, text="Título:")
        lbl_titulo.pack()
        entry_titulo = tk.Entry(ventana_actualizar)
        entry_titulo.pack()
        entry_titulo.insert(0, videojuego[1])

        lbl_genero = tk.Label(ventana_actualizar, text="Género:")
        lbl_genero.pack()
        entry_genero = tk.Entry(ventana_actualizar)
        entry_genero.pack()
        entry_genero.insert(0, videojuego[2])

        lbl_clasificacion = tk.Label(ventana_actualizar, text="Clasificación:")
        lbl_clasificacion.pack()
        entry_clasificacion = tk.Entry(ventana_actualizar)
        entry_clasificacion.pack()
        entry_clasificacion.insert(0, videojuego[3])

        lbl_plataforma = tk.Label(ventana_actualizar, text="Plataforma:")
        lbl_plataforma.pack()
        entry_plataforma = tk.Entry(ventana_actualizar)
        entry_plataforma.pack()
        entry_plataforma.insert(0, videojuego[4])

        btn_guardar = tk.Button(ventana_actualizar, text="Guardar Cambios", bg="green", command=lambda: actualizar_videojuego(id, entry_titulo, entry_genero, entry_clasificacion, entry_plataforma))
        btn_guardar.pack()

# Función para actualizar videojuego
def actualizar_videojuego(id, entry_titulo, entry_genero, entry_clasificacion, entry_plataforma):
    titulo = entry_titulo.get()
    genero = entry_genero.get()
    clasificacion = entry_clasificacion.get()
    plataforma = entry_plataforma.get()

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE videojuegos SET titulo = %s, genero = %s, clasificacion = %s, plataforma = %s WHERE id = %s
    """, (titulo, genero, clasificacion, plataforma, id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Videojuego actualizado correctamente")

# Función para limpiar campos de entrada
def limpiar_campos():
    entry_titulo.delete(0, tk.END)
    entry_genero.delete(0, tk.END)
    entry_clasificacion.delete(0, tk.END)
    entry_plataforma.delete(0, tk.END)

# Configuración de la ventana principal
root = tk.Tk()
root.title("GamerPro")

# Cargar la imagen de fondo
imagen_fondo = Image.open("C:/Users/marcos/OneDrive - KGHM CHILE SPA/Documentos/Programacion Avanzada 1/semana 8/GamerPro.png")
imagen_fondo = imagen_fondo.resize((400, 500))  # Ajusta el tamaño según sea necesario
imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

# Crear un widget Canvas para el fondo
canvas = tk.Canvas(root, width=400, height=500)
canvas.pack(fill="both", expand=True)

# Colocar la imagen en el canvas
canvas.create_image(0, 0, image=imagen_fondo, anchor="nw")

# Campos de entrada en el canvas
lbl_titulo = tk.Label(root, text="Título:", bg="white")
canvas.create_window(50, 20, window=lbl_titulo)
entry_titulo = tk.Entry(root)
canvas.create_window(200, 20, window=entry_titulo)

lbl_genero = tk.Label(root, text="Género:", bg="white")
canvas.create_window(50, 60, window=lbl_genero)
entry_genero = tk.Entry(root)
canvas.create_window(200, 60, window=entry_genero)

lbl_clasificacion = tk.Label(root, text="Clasificación:", bg="white")
canvas.create_window(50, 100, window=lbl_clasificacion)
entry_clasificacion = tk.Entry(root)
canvas.create_window(200, 100, window=entry_clasificacion)

lbl_plataforma = tk.Label(root, text="Plataforma:", bg="white")
canvas.create_window(50, 140, window=lbl_plataforma)
entry_plataforma = tk.Entry(root)
canvas.create_window(200, 140, window=entry_plataforma)

# Botones en el canvas
btn_agregar = tk.Button(root, text="Agregar Videojuego", bg="green", command=agregar_videojuego)
canvas.create_window(100, 180, window=btn_agregar)

btn_mostrar = tk.Button(root, text="Mostrar Videojuegos", bg="blue", command=mostrar_videojuegos)
canvas.create_window(300, 180, window=btn_mostrar)

root.geometry("400x500")
root.mainloop()

import tkinter as tk
from PIL import Image, ImageTk
import os


def IrA(frame, ventana):
    frame.pack_forget()
    MenuA(frame, ventana)


def Return(frame, frame_menu):
    frame.pack_forget()
    frame_menu.pack(fill="both", expand=True)


def Creditos(frame_menu, ventana):
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()

    frame_menu.pack_forget()
    frame_creditos = tk.Frame(ventana, width=ancho, height=alto)
    frame_creditos.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_creditos, width=ancho, height=alto, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Imagen de fondo
    fondo = Image.open(os.path.join(os.path.dirname(__file__), "Imagenes", "Fondo.png")).resize((ancho, alto))
    fondo_tk = ImageTk.PhotoImage(fondo)
    canvas.fondo = fondo_tk
    canvas.create_image(0, 0, image=fondo_tk, anchor="nw")

    # Imagen centrada
    try:
        imagen_centro = Image.open(os.path.join(os.path.dirname(__file__), "Imagenes", "Creditos.jpg"))
        imagen_centro = imagen_centro.resize((1050, 600))
        imagen_centro_tk = ImageTk.PhotoImage(imagen_centro)
        canvas.imagen_centro = imagen_centro_tk
        canvas.create_image(ancho // 2 - 230, alto // 2 - 100, image=imagen_centro_tk, anchor="center")
    except FileNotFoundError:
        print("No se pudo cargar la imagen central")
    except Exception as e:
        print(f"Error al cargar imagen: {e}")

    # Label con texto de créditos - CORRECCIÓN PRINCIPAL
    texto_creditos = """Este proyecto contable fue concluido por un grupo de estudiantes
de la carrera de ISIC de Instituto Tecnológico Superior de Apatzingán. 

En este los integrantes cumplieron con roles demasiado importantes:

1.- Nolberto y Zuleyma: Arte (El fondo e imágenes).
2.- Yulissa y Omar: Los explotados laboralmente por Telcel.
3.- Fernando: El que se mato haciendo el proyecto.
4.- Camila: La que si ayudo a Fernando.
5.- Brayan: El de relleno (no echo ni porras)

Mencion Honorifica A: Yulissa Ponce Javier por humillarse para conseguir una cuenta prestada con ChatGPT Premium"""

    # SOLUCIÓN: Crear el label como hijo del canvas, no del frame
    label_creditos = tk.Label(canvas, text=texto_creditos, font=("Minecraftia", 12, "bold"),
                              bg="white", fg="black", relief="solid", bd=2,
                              justify="left", wraplength=350, padx=10, pady=10)

    # Usar create_window para agregar el label al canvas
    canvas.create_window(ancho - 450, alto // 2, window=label_creditos, anchor="w")

    # Botón para volver
    from PaginaPrincipal import Return
    tk.Button(canvas, text="VOLVER AL MENU", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
              activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=40,
              command=lambda: Return(frame_creditos, frame_menu)).place(x=ancho // 2 - 280, y=alto - 90)
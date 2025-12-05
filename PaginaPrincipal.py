import tkinter as tk
from PIL import Image, ImageTk
import os


def Return(frame, frame_menu):
    frame.pack_forget()
    frame_menu.pack(fill="both", expand=True)

def IrA(frame_menu, frame, ventana):
    frame.destroy()
    frame_menu.pack(fill="both", expand=True)

def Menu(ventana):
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()

    frame_menu = tk.Frame(ventana, width=ancho, height=alto)
    frame_menu.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_menu, width=ancho, height=alto, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Imagen de fondo
    fondo = Image.open(os.path.join(os.path.dirname(__file__), "Imagenes", "Portada.png")).resize((ancho, alto))
    fondo_tk = ImageTk.PhotoImage(fondo)
    canvas.fondo = fondo_tk
    canvas.create_image(0, 0, image=fondo_tk, anchor="nw")

    from Ingresar import PaginaIng
    tk.Button(frame_menu, text="INGRESAR", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white", activebackground="#2f2f2f",
        activeforeground="white", relief="raised", bd=4, width=40,  # MÁS ANCHO (número de caracteres)
    command = lambda: PaginaIng(frame_menu, ventana)).place(x=ancho // 2 - 270, y=ancho // 2 - 400)

    from Catalogo import CatalogoC
    tk.Button(frame_menu, text="CATALOGO", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
        activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=40,  # MÁS ANCHO (número de caracteres)
    command = lambda: CatalogoC(frame_menu, ventana)).place(x=ancho // 2 - 270, y=ancho // 2 - 340)

    from LibroMayor import mostrar_libro_mayor
    tk.Button(frame_menu, text="LIBRO MAYOR", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
        activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=40, # MÁS ANCHO (número de caracteres)
    command = lambda: mostrar_libro_mayor(frame_menu, ventana)).place(x=ancho // 2 - 270, y=ancho // 2 - 280)

    from LibroDiario import mostrar_libro_diario
    tk.Button(frame_menu, text="LIBRO DIARIO", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
    activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=40, # MÁS ANCHO (número de caracteres)
    command = lambda: mostrar_libro_diario(frame_menu, ventana)).place(x=ancho // 2 - 270, y=ancho // 2 - 220)

    from Balanza import mostrar_balanza
    tk.Button(frame_menu, text="BALANZA", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
    activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=40, # MÁS ANCHO (número de caracteres# )
    command = lambda: mostrar_balanza(frame_menu, ventana) ).place(x=ancho // 2 - 270, y=ancho // 2 - 160)

    # Botón de Estado de Situación Financiera (Balance General)
    from EstadoSitFinanciera import mostrar_estado_situacion_financiera
    tk.Button(frame_menu, text="ESTADO DE SITUACION", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
    activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=19,
    command=lambda: mostrar_estado_situacion_financiera(frame_menu, ventana)).place(x=ancho // 2 + 3,y=ancho // 2 - 100)

    # En PaginaPrincipal.py, modifica los botones sin función:
    from EstadoResultado import mostrar_estado_resultado
    tk.Button(frame_menu, text="ESTADO DE RESULTADO", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
    activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=19,
    command=lambda: mostrar_estado_resultado(frame_menu, ventana)).place(x=ancho // 2 - 270, y=ancho // 2 - 100)

    from PaginaConA import IrA
    tk.Button(frame_menu, text="CON AJUSTES", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
    activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=20, # MÁS ANCHO (número de caracteres# )
    command = lambda: IrA(frame_menu, ventana)).place(x=ancho // 2 + 390, y=ancho // 2 - 220)

    from Creditos import Creditos
    tk.Button(frame_menu, text="CREDITOS :D", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
    activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=20,# MÁS ANCHO (número de caracteres# )
    command = lambda: Creditos(frame_menu, ventana)).place(x=ancho // 2 - 690, y=ancho // 2 - 220)

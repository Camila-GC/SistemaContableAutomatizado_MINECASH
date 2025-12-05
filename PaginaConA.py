import tkinter as tk
from PIL import Image, ImageTk
import os

def IrA(frame, ventana):
    frame.pack_forget()
    MenuA(frame, ventana)

def Return(frame, frame_menu):
    frame.pack_forget()
    frame_menu.pack(fill="both", expand=True)

def MenuA(frame, ventana):
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()

    frame_menuA = tk.Frame(ventana, width=ancho, height=alto)
    frame_menuA.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_menuA, width=ancho, height=alto, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Imagen de fondo
    fondo = Image.open(os.path.join(os.path.dirname(__file__), "Imagenes", "Portada.png")).resize((ancho, alto))
    fondo_tk = ImageTk.PhotoImage(fondo)
    canvas.fondo = fondo_tk
    canvas.create_image(0, 0, image=fondo_tk, anchor="nw")

    from IngresarAjustes import PaginaAj
    tk.Button(frame_menuA, text="INGRESAR AJUSTES", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
              activebackground="#2f2f2f",
              activeforeground="white", relief="raised", bd=4, width=40,  # MÁS ANCHO (número de caracteres)
              command=lambda: PaginaAj(frame_menuA, ventana)).place(x=ancho // 2 - 270, y=ancho // 2 - 400)

    from Catalogo import CatalogoC
    tk.Button(frame_menuA, text="CATALOGO", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
    activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=40, # MÁS ANCHO (número de caracteres)
    command=lambda: CatalogoC(frame_menu, ventana)).place(x=ancho // 2 - 270, y=ancho // 2 - 340)

    # Asegúrate que la importación sea así:
    from LibroMayorConA import mostrar_libro_mayor  # Nombre exacto de la función
    # Y que el botón la llame así:
    tk.Button(frame_menuA, text="LIBRO MAYOR CON AJUSTES", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
    activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=40,
    command=lambda: mostrar_libro_mayor(frame_menuA, ventana)).place(x=ancho // 2 - 270,y=ancho // 2 - 280)

    from LibroDiarioA import mostrar_libro_diario
    tk.Button(frame_menuA, text="LIBRO DIARIO CON AJUSTES", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
              activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=40,# MÁS ANCHO (número de caracteres)
    command = lambda: mostrar_libro_diario(frame_menuA, ventana) ).place(x=ancho // 2 - 270, y=ancho // 2 - 220)

    from BalanzaConA import mostrar_balanza_cierre
    tk.Button(frame_menuA, text="BALANZA CON AJUSTES", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
              activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=40,# MÁS ANCHO (número de caracteres# )
    command = lambda: mostrar_balanza_cierre(frame_menuA, ventana) ).place(x=ancho // 2 - 270, y=ancho // 2 - 160)

    from EstadoSitFinanciera import mostrar_estado_situacion_financiera
    tk.Button(frame_menuA, text="ESTADO DE SITUACION", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
              activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=19,# MÁS ANCHO (número de caracteres# )
    command=lambda: mostrar_estado_situacion_financiera(frame_menuA, ventana)).place(x=ancho // 2 + 3, y=ancho // 2 - 100)

    # En PaginaPrincipal.py, modifica los botones sin función:
    from EstadoResultado import mostrar_estado_resultado
    tk.Button(frame_menuA, text="ESTADO DE RESULTADO", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
              activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=19,
              command=lambda: mostrar_estado_resultado(frame_menuA, ventana)).place(x=ancho // 2 - 270, y=ancho // 2 - 100)

    from PaginaPrincipal import IrA
    tk.Button(frame_menuA, text="SIN AJUSTES", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
    activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=20, # MÁS ANCHO (número de caracteres# )
    command=lambda: IrA(frame, frame_menuA, ventana)).place(x=ancho // 2 + 390, y=ancho // 2 - 220)

    from Creditos import Creditos
    tk.Button(frame_menuA, text="CREDITOS :D", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
              activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=20,
              # MÁS ANCHO (número de caracteres# )
              command=lambda: Creditos(frame_menuA, ventana)).place(x=ancho // 2 - 690, y=ancho // 2 - 220)
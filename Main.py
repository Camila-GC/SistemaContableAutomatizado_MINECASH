import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Label
from PaginaPrincipal import Menu
import pygame  # <-- NUEVO
import sys  # Para detectar rutas al empaquetar con PyInstaller
import os  # Para obtener rutas absolutas de archivos

def rutas(relative_path):
    """Devuelve la ruta absoluta para los archivos empaquetados (compatible con PyInstaller)."""
    try:
        base_path = sys._MEIPASS  # Carpeta temporal donde PyInstaller guarda los archivos
    except Exception:
        base_path = os.path.abspath(".")  # Si no está empaquetado, usar ruta actual

    return os.path.join(base_path, relative_path)  # Ruta absoluta final

def reproducir_musica():
    pygame.mixer.init()
    pygame.mixer.music.load(rutas("Musica/Song.mp3"))  # Ruta a tu archivo de música
    pygame.mixer.music.set_volume(0.3)  # Volumen entre 0.0 y 1.0
    pygame.mixer.music.play(-1)  # -1 para que suene en bucle

def Ventana():
    pygame.init()  # <-- NUEVO
    ventana = tk.Tk()
    ventana.title("SISTEMA CONTABLE DE REGISTRO AUTOMATICO - MINECASH: IVA EDITION")
    ventana.config(bg="#dcdcdc")
    ventana.state('zoomed')
    ventana.resizable(False, False)

    reproducir_musica()  # <-- NUEVO

    Menu(ventana)
    ventana.mainloop()


Ventana()

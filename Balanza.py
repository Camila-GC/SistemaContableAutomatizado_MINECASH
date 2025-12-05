import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from LibroMayor import resumen_cuentas
import os
import sys

def Contorno(canvas, texto, x, y, fuente, color, contorno):
    for dx in [-3, -1.5, 0, 1.5, 3]:
        for dy in [-3, -1.5, 0, 1.5, 3]:
            if dx != 0 or dy != 0:
                canvas.create_text(x + dx, y + dy, text=texto, font=fuente, fill=contorno)
    canvas.create_text(x, y, text=texto, font=fuente, fill=color)

def rutas(relative_path):
    """Devuelve la ruta absoluta para los archivos empaquetados (compatible con PyInstaller)."""
    try:
        base_path = sys._MEIPASS  # Carpeta temporal donde PyInstaller guarda los archivos
    except Exception:
        base_path = os.path.abspath(".")  # Si no está empaquetado, usar ruta actual

    return os.path.join(base_path, relative_path)  # Ruta absoluta final

def mostrar_balanza(frame_menu, ventana):
    # Filtrar cuentas excluyendo inventario final
    cuentas_filtradas = [c for c in resumen_cuentas if "inventario final" not in c['cuenta'].lower()]

    if not cuentas_filtradas:
        messagebox.showwarning("Sin datos", "No hay datos contables disponibles para generar la balanza.")
        return

    frame_menu.pack_forget()
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()

    frame = tk.Frame(ventana, bg="white")
    frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Fondo
    fondo = Image.open(rutas("Imagenes/Fondo.png")).resize((ancho, alto))
    fondo_tk = ImageTk.PhotoImage(fondo)
    canvas.fondo = fondo_tk
    canvas.create_image(0, 0, image=fondo_tk, anchor="nw")

    # Título
    Contorno(canvas, "BALANZA DE COMPROBACIÓN", ancho // 2, 50,
             ("Minecraftia", 40, "bold"), "black", "white")

    # Marco para la tabla
    tabla_frame = tk.Frame(canvas, bg="white", bd=2, relief="sunken")
    tabla_frame.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.7)

    # Configurar tabla con 6 columnas
    columnas = ("Código", "Cuenta", "Debe", "Haber", "Deudor", "Acreedor")
    tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=20)

    # Configurar encabezados principales
    tabla.heading("Código", text="Código")
    tabla.heading("Cuenta", text="Cuenta")
    tabla.heading("Debe", text="Debe")
    tabla.heading("Haber", text="Haber")
    tabla.heading("Deudor", text="Deudor")
    tabla.heading("Acreedor", text="Acreedor")

    # Ajustar columnas
    tabla.column("Código", width=100, anchor="center")
    tabla.column("Cuenta", width=250, anchor="w")
    tabla.column("Debe", width=120, anchor="center")
    tabla.column("Haber", width=120, anchor="center")
    tabla.column("Deudor", width=120, anchor="center")
    tabla.column("Acreedor", width=120, anchor="center")

    # Crear encabezados combinados superiores (ahora dentro del mismo frame que el Treeview)
    movimientos_label = tk.Label(tabla_frame, text="MOVIMIENTOS", font=("Minecraftia", 10, "bold"),
                                 bg="#d0e0ff", relief="ridge", bd=2)
    movimientos_label.place(x=474, y=0, width=365, height=25)

    saldos_label = tk.Label(tabla_frame, text="SALDOS", font=("Minecraftia", 10, "bold"),
                            bg="#d0e0ff", relief="ridge", bd=2)
    saldos_label.place(x=839, y=0, width=365, height=25)

    # Estilo
    style = ttk.Style()
    style.configure("Treeview", font=("Minecraftia", 10), rowheight=28)
    style.configure("Treeview.Heading", font=("Minecraftia", 10, "bold"), background="#d0e0ff")
    style.map("Treeview", background=[("selected", "#3399FF")])

    # Alternar colores de filas
    tabla.tag_configure('oddrow', background='white')
    tabla.tag_configure('evenrow', background='#f0f0f0')
    tabla.tag_configure('totalrow', background='#3399FF', foreground='white', font=("Minecraftia", 10, "bold"))

    # Scrollbar
    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tabla.pack(fill="both", expand=True, pady=(25, 0))  # Altura del encabezado combinando

    # Insertar datos
    total_debe = 0
    total_haber = 0
    total_saldo_deudor = 0
    total_saldo_acreedor = 0

    for i, cuenta in enumerate(cuentas_filtradas):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'

        # Determinar si el saldo es deudor o acreedor
        saldo_deudor = f"{cuenta['saldo_final']:.2f}" if cuenta['total_debe'] > cuenta['total_haber'] else ""
        saldo_acreedor = f"{cuenta['saldo_final']:.2f}" if cuenta['total_haber'] > cuenta['total_debe'] else ""

        # Sumar a totales
        total_debe += cuenta['total_debe']
        total_haber += cuenta['total_haber']

        if saldo_deudor:
            total_saldo_deudor += cuenta['saldo_final']
        else:
            total_saldo_acreedor += cuenta['saldo_final']

        tabla.insert("", "end", values=(
            cuenta['codigo'],
            cuenta['cuenta'],
            f"{cuenta['total_debe']:.2f}",
            f"{cuenta['total_haber']:.2f}",
            saldo_deudor,
            saldo_acreedor
        ), tags=(tag,))

    # Agregar fila de totales
    tabla.insert("", "end", values=(
        "",
        "TOTALES",
        f"{total_debe:.2f}",
        f"{total_haber:.2f}",
        f"{total_saldo_deudor:.2f}",
        f"{total_saldo_acreedor:.2f}"
    ), tags=("totalrow",))

    # Botón para volver
    from PaginaPrincipal import Return
    tk.Button(canvas, text="VOLVER AL MENÚ", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
              activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=40,
              command=lambda: Return(frame, frame_menu)).place(x=ancho // 2 - 280, y=alto - 80)
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from PaginaPrincipal import Return
from Ingresar import movimientos
from Catalogo import datos as catalogo_datos
import os
import sys

def rutas(relative_path):
    """Devuelve la ruta absoluta para los archivos empaquetados (compatible con PyInstaller)."""
    try:
        base_path = sys._MEIPASS  # Carpeta temporal donde PyInstaller guarda los archivos
    except Exception:
        base_path = os.path.abspath(".")  # Si no está empaquetado, usar ruta actual

    return os.path.join(base_path, relative_path)  # Ruta absoluta final

def Contorno(canvas, texto, x, y, fuente, color, contorno):
    for dx in [-3, -1.5, 0, 1.5, 3]:
        for dy in [-3, -1.5, 0, 1.5, 3]:
            if dx != 0 or dy != 0:
                canvas.create_text(x + dx, y + dy, text=texto, font=fuente, fill=contorno)
    canvas.create_text(x, y, text=texto, font=fuente, fill=color)

def mostrar_libro_diario(frame_menu, ventana):
    if not movimientos:
        messagebox.showwarning("Sin movimientos",
                               "Primero debes ingresar movimientos antes de acceder al Libro Diario.")
        return

    frame_menu.pack_forget()
    ventana.state('zoomed')

    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()

    # Frame principal
    frame_principal = tk.Frame(ventana, bg="white")
    frame_principal.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_principal, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Cargar imagen de fondo
    try:
        fondo = Image.open(rutas("Imagenes/Fondo.png")).resize((ancho, alto))
        fondo_tk = ImageTk.PhotoImage(fondo)
        canvas.fondo = fondo_tk
        canvas.create_image(0, 0, image=fondo_tk, anchor="nw")
    except:
        canvas.configure(bg="#f0f8ff")

    # Título
    Contorno(canvas, "LIBRO DIARIO", ancho // 2, 50,
             ("Minecraftia", 40, "bold"), "black", "white")

    # Crear diccionario de códigos de cuenta para búsqueda rápida
    codigos_cuentas = {fila[1]: fila[0] for fila in catalogo_datos if len(fila[0]) == 3}

    # Frame para la tabla del libro diario
    tabla_frame = tk.Frame(canvas, bg="white", bd=2, relief="sunken")
    tabla_frame.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.75)

    # Configurar el Treeview para mostrar el libro diario
    columnas = ("No. Op", "Fecha", "Código", "Cuenta", "Debe", "Haber")
    tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings")

    # Configurar columnas
    for col in columnas:
        tabla.heading(col, text=col)
        if col == "Cuenta":
            tabla.column(col, width=200, anchor="w")
        elif col in ["Debe", "Haber"]:
            tabla.column(col, width=120, anchor="e")
        else:
            tabla.column(col, width=80, anchor="center")

    tabla.pack(fill="both", expand=True)

    # Scrollbar
    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Estilo de la tabla
    style = ttk.Style()
    style.configure("Treeview", font=("Minecraftia", 10), rowheight=25)
    style.configure("Treeview.Heading", font=("Minecraftia", 10, "bold"), background="#d0e0ff")
    style.map("Treeview", background=[("selected", "#3399FF")])
    tabla.tag_configure('oddrow', background='white')
    tabla.tag_configure('evenrow', background='#f0f0f0')
    tabla.tag_configure('debe', background='#ffdddd')
    tabla.tag_configure('haber', background='#ddffdd')
    tabla.tag_configure('total', background='#d0e0ff', font=('Minecraftia', 10, 'bold'))

    # Variables para sumatorias
    total_debe = 0.0
    total_haber = 0.0

    def mostrar_todos_los_movimientos():
        nonlocal total_debe, total_haber
        total_debe = 0.0
        total_haber = 0.0

        # Limpiar tabla
        for item in tabla.get_children():
            tabla.delete(item)

        # Mostrar todos los movimientos
        for op in movimientos:
            op_num = op["numero"]

            # Mostrar cada movimiento en una fila separada
            for cuenta, debe, haber in op["datos"]:
                # Excluir cuenta "Inventario Final"
                if "inventario final" in cuenta.lower():
                    continue

                # Obtener código de cuenta del catálogo
                codigo = codigos_cuentas.get(cuenta, "---")

                # Actualizar sumatorias
                total_debe += debe
                total_haber += haber

                # Determinar estilo de fila
                tag = 'evenrow' if len(tabla.get_children()) % 2 == 0 else 'oddrow'
                if debe > 0:
                    tag = ('debe', tag)
                elif haber > 0:
                    tag = ('haber', tag)

                tabla.insert("", "end", values=(
                    op_num,
                    "",  # Fecha (podría implementarse si se agrega)
                    codigo,
                    cuenta,
                    f"${debe:,.2f}" if debe > 0 else "",
                    f"${haber:,.2f}" if haber > 0 else ""
                ), tags=tag)

        # Agregar fila de totales al final
        tabla.insert("", "end", values=(
            "",
            "",
            "TOTAL:",
            "",
            f"${total_debe:,.2f}",
            f"${total_haber:,.2f}"
        ), tags=('total',))

    # Botón para volver al menú
    tk.Button(canvas, text="VOLVER AL MENU", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
              activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=40,
              command=lambda: Return(frame_principal, frame_menu)).place(x=ancho // 2 - 280, y=alto - 80)

    # Mostrar todos los movimientos
    mostrar_todos_los_movimientos()
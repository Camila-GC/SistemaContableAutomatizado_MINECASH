import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import os

# Datos extraídos del PDF
datos = [
        ("1", "Activos", "DEUDOR", "", ""),
        ("11", "Activo circulante", "DEUDOR", "AC", ""),
        ("111", "Caja-Efectivo", "DEUDOR", "AC", "ESF"),
        ("112", "Bancos", "DEUDOR", "AC", "ESF"),
        ("113", "Cuentas por cobrar", "DEUDOR", "AC", "ESF"),
        ("114", "Inventario", "DEUDOR", "AC", "ESF"),
        ("115", "Gastos pagados por adelantado", "DEUDOR", "AC", "ESF"),
        ("116", "Deudores diversos", "DEUDOR", "AC", "ESF"),
        ("117", "Clientes", "DEUDOR", "AC", "ESF"),
        ("118", "Documentos por cobrar", "DEUDOR", "AC", "ESF"),
        ("12", "Activo no circulante", "DEUDOR", "", "ESF"),
        ("121", "Terrenos", "DEUDOR", "ACN", "ESF"),
        ("122", "Edificios", "DEUDOR", "ACN", "ESF"),
        ("123", "Equipo de reparto", "DEUDOR", "ACN", "ESF"),
        ("124", "Equipo de computo", "DEUDOR", "ACN", "ESF"),
        ("125", "Mobiliario y equipo", "DEUDOR", "ACN", "ESF"),
        ("126", "Equipo de computo", "DEUDOR", "ACN", "ESF"),
        ("2", "Pasivos", "ACREDOR", "", "ESF"),
        ("21", "Pasivo a corto plazo", "ACREDOR", "", "ESF"),
        ("211", "Cuentas por pagar", "ACREDOR", "PCP", "ESF"),
        ("212", "Intereses por pagar", "ACREDOR", "PCP", "ESF"),
        ("213", "Proveedores", "ACREDOR", "PCP", "ESF"),
        ("214", "Sueldos por pagar", "ACREDOR", "PCP", "ESF"),
        ("215", "Documentos por pagar", "ACREDOR", "PCP", "ESF"),
        ("216", "Acreedores diversos", "ACREDOR", "PCP", "ESF"),
        ("22", "Pasivo a largo plazo", "ACREDOR", "", "ESF"),
        ("221", "Documentos por pagar", "ACREDOR", "PLP", "ESF"),
        ("222", "Hipoteca por pagar", "ACREDOR", "PLP", "ESF"),
        ("3", "Capital contable", "ACREDOR", "CC", "ESF"),
        ("311", "Capital social", "ACREDOR", "CC", "ESF"),
        ("312", "Utilidad neta del ejercicio", "ACREDOR", "CG", "ESF"),
        ("313", "Reserva legal", "ACREDOR", "CG", "ESF"),
        ("314", "Capital contable", "ACREDOR", "CC", "ESF"),
        ("315", "Perdidas y Ganancias", "DUAL", "CG", "ESF"),
        ("316", "Perdida neta del ejercicio", "DEUDOR", "CG", "ESF"),
        ("4", "Ingresos", "ACREDOR", "RA", "ER"),
        ("411", "Ventas", "ACREDOR", "RA", "ER"),
        ("412", "Rebajas sobre compras", "ACREDOR", "RA", "ER"),
        ("413", "Devolución sobre compras", "ACREDOR", "RA", "ER"),
        ("414", "Descuentos sobre compras", "ACREDOR", "RA", "ER"),
        ("415", "Otros ingresos", "ACREDOR", "RA", "ER"),
        ("5", "Costos", "DEUDOR", "RD", "ER"),
        ("51", "Costo de ventas", "DEUDOR", "RD", "ER"),
        ("511", "Compras", "DEUDOR", "RD", "ER"),
        ("512", "Devoluciones sobre ventas", "DEUDOR", "RD", "ER"),
        ("513", "Rebajas sobre ventas", "DEUDOR", "RD", "ER"),
        ("514", "Descuentos sobre ventas", "DEUDOR", "RD", "ER"),
        ("515", "Gastos de compra", "DEUDOR", "RD", "ER"),
        ("6", "Gastos", "DEUDOR", "RD", "ER"),
        ("61", "Gastos de ventas", "DEUDOR", "RD", "ER"),
        ("611", "Sueldos ventas", "DEUDOR", "RD", "ER"),
        ("612", "Publicidad", "DEUDOR", "RD", "ER"),
        ("613", "Comisiones", "DEUDOR", "RD", "ER"),
        ("62", "Gastos administrativos", "DEUDOR", "RD", "ER"),
        ("621", "Sueldos Admon", "DEUDOR", "RD", "ER"),
        ("622", "Renta", "DEUDOR", "RD", "ER"),
        ("623", "Servicios", "DEUDOR", "RD", "ER"),
        ("63", "Otros Gastos", "DEUDOR", "RD", "ER"),
        ("631", "Intereses", "DEUDOR", "RD", "ER"),
]

def Contorno(canvas, texto, x, y, fuente, color, contorno):
    for dx in [-3, -1.5, 0, 1.5, 3]:
        for dy in [-3, -1.5, 0, 1.5, 3]:
            if dx != 0 or dy != 0:
                canvas.create_text(x + dx, y + dy, text=texto, font=fuente, fill=contorno)
    canvas.create_text(x, y, text=texto, font=fuente, fill=color)  # Texto principal

def rutas(relative_path):
    """Devuelve la ruta absoluta para los archivos empaquetados (compatible con PyInstaller)."""
    try:
        base_path = sys._MEIPASS  # Carpeta temporal donde PyInstaller guarda los archivos
    except Exception:
        base_path = os.path.abspath(".")  # Si no está empaquetado, usar ruta actual

    return os.path.join(base_path, relative_path)  # Ruta absoluta final

def CatalogoC(frame_menu, ventana):
    frame_menu.pack_forget()

    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()

    frame_cata = tk.Frame(ventana, width=ancho, height=alto)
    frame_cata.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_cata, width=ancho, height=alto, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Imagen de fondo
    fondo = Image.open(rutas("Imagenes/Fondo.png")).resize((ancho, alto))
    fondo_tk = ImageTk.PhotoImage(fondo)
    canvas.fondo = fondo_tk
    canvas.create_image(0, 0, image=fondo_tk, anchor="nw")

    Contorno(canvas, texto="CATALOGO DE CUENTAS", x=ancho//2, y=50, fuente=("Minecraftia", 50, "bold"),
    color="black", contorno="white")

    # Crear Frame para la tabla sobre el canvas
    tabla_frame = tk.Frame(canvas, bg="white", bd=2, relief="sunken")  # Borde opcional
    tabla_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

    # Crear tabla Treeview
    columnas = ("CODIGO", "DESCRIPCION", "SALDO", "SIGLA", "TIPO")
    tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings")

    # Configurar columnas
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center")

    tabla.pack(fill="both", expand=True)

    # Añadir scrollbar vertical
    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Estilos para Treeview
    style = ttk.Style()
    style.configure("Treeview", rowheight=25, font=('Minecraftia', 10))
    style.map("Treeview", background=[('selected', '#3399FF')])
    style.configure("Treeview.Heading", font=('Minecraftia', 10, 'bold'))

    # Colores por tipo de código
    tabla.tag_configure('oddrow', background='white')
    tabla.tag_configure('evenrow', background='#f0f0f0')
    tabla.tag_configure('unicodigo', background='#003366', foreground='white')  # Azul rey
    tabla.tag_configure('dosdigitos', background='#87CEEB', foreground='black')  # Azul cielo

    # Insertar filas con estilos según longitud del código
    for i, fila in enumerate(datos):
        codigo = fila[0]
        if len(codigo) == 1:
            tag = 'unicodigo'
        elif len(codigo) == 2:
            tag = 'dosdigitos'
        else:
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tabla.insert("", "end", values=fila, tags=(tag,))

    from PaginaPrincipal import Return
    tk.Button(canvas, text="VOLVER AL MENU", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
    activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=40,  # MÁS ANCHO (número de caracteres)
    command= lambda: Return(frame_cata,frame_menu)).place(x=ancho // 2 - 280, y=alto - 70)
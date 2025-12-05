import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from EstadoResultado import IMPUESTO_CALCULADO, UTILIDAD_NETA, PERDIDA_NETA
from LibroMayor import resumen_cuentas
import os
import sys

def rutas(relative_path):
    """Devuelve la ruta absoluta para los archivos empaquetados (compatible con PyInstaller)."""
    try:
        base_path = sys._MEIPASS  # Carpeta temporal donde PyInstaller guarda los archivos
    except Exception:
        base_path = os.path.abspath(".")  # Si no está empaquetado, usar ruta actual

    return os.path.join(base_path, relative_path)  # Ruta absoluta final

def mostrar_balanza_cierre(frame_menu, ventana):
    cuentas_excluidas = [
        "inventario", "ventas", "compras",
        "rebajas sobre ventas", "devoluciones sobre ventas", "descuentos sobre ventas",
        "rebajas sobre compras", "devoluciones sobre compras", "descuentos sobre compras",
        "gastos de compra", "gastos de venta", "gastos de administración", "gastos de ventas",
        "otros gastos", "otros ingresos"
    ]

    cuentas_filtradas = []

    for cuenta in resumen_cuentas:
        nombre = cuenta['cuenta'].lower()
        if nombre not in cuentas_excluidas:
            cuenta_copia = cuenta.copy()

            if nombre == "capital contable":
                ajuste = UTILIDAD_NETA - PERDIDA_NETA
                cuenta_copia['saldo_final'] = cuenta['saldo_final'] + ajuste
                cuenta_copia['total_haber'] = cuenta['total_haber'] + ajuste
                cuenta_copia['saldo_original'] = cuenta['saldo_final']
                cuenta_copia['haber_original'] = cuenta['total_haber']

            cuentas_filtradas.append(cuenta_copia)

    frame_menu.pack_forget()
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()

    frame = tk.Frame(ventana, bg="white")
    frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    fondo = Image.open(rutas("Imagenes/Fondo.png")).resize((ancho, alto))
    fondo_tk = ImageTk.PhotoImage(fondo)
    canvas.fondo = fondo_tk
    canvas.create_image(0, 0, image=fondo_tk, anchor="nw")

    from Balanza import Contorno
    Contorno(canvas, "BALANZA CON AJUSTES", ancho // 2, 50, ("Minecraftia", 40, "bold"), "black", "white")

    tabla_frame = tk.Frame(canvas, bg="white", bd=2, relief="sunken")
    tabla_frame.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.7)

    columnas = ("Codigo", "Cuenta", "Debe", "Haber", "Deudor", "Acreedor")
    tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=20)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center")

    tabla.column("Cuenta", anchor="w", width=250)
    tabla.column("Codigo", width=100)

    tabla.tag_configure('oddrow', background='white')
    tabla.tag_configure('evenrow', background='#f0f0f0')
    tabla.tag_configure('totalrow', background='#3399FF', foreground='white')

    total_debe = total_haber = total_deudor = total_acreedor = 0

    for i, cuenta in enumerate(cuentas_filtradas):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        nombre = cuenta['cuenta'].lower()

        if nombre == "inventario final":
            debe = cuenta['total_haber']
            haber = 0
            cuenta['total_debe'] = debe
            cuenta['total_haber'] = 0
            saldo_deudor = f"{debe:.2f}" if debe > 0 else ""
            saldo_acreedor = ""
            if debe > 0:
                total_deudor += debe
        elif nombre == "capital contable":
            debe = cuenta['total_debe']
            haber = cuenta['total_haber']
            if haber > debe:
                saldo_deudor = ""
                saldo_acreedor = f"{(haber - debe):.2f}"
                total_acreedor += (haber - debe)
            elif debe > haber:
                saldo_deudor = f"{(debe - haber):.2f}"
                saldo_acreedor = ""
                total_deudor += (debe - haber)
            else:
                saldo_deudor = saldo_acreedor = ""
        else:
            debe = cuenta['total_debe']
            haber = cuenta['total_haber']
            if haber > debe:
                saldo_deudor = ""
                saldo_acreedor = f"{(haber - debe):.2f}"
                total_acreedor += (haber - debe)
            elif debe > haber:
                saldo_deudor = f"{(debe - haber):.2f}"
                saldo_acreedor = ""
                total_deudor += (debe - haber)
            else:
                saldo_deudor = saldo_acreedor = ""

        total_debe += debe
        total_haber += haber

        tabla.insert("", "end", values=(
            cuenta['codigo'], cuenta['cuenta'], f"{debe:.2f}", f"{haber:.2f}", saldo_deudor, saldo_acreedor
        ), tags=(tag,))

    i = len(cuentas_filtradas)
    tag = 'evenrow' if i % 2 == 0 else 'oddrow'
    debe_imp = 0.0
    haber_imp = IMPUESTO_CALCULADO
    saldo_deudor_imp = ""
    saldo_acreedor_imp = f"{IMPUESTO_CALCULADO:.2f}"

    total_debe += debe_imp
    total_haber += haber_imp
    total_acreedor += IMPUESTO_CALCULADO

    tabla.insert("", "end", values=(
        "N/A", "Impuestos", f"{debe_imp:.2f}", f"{haber_imp:.2f}",
        saldo_deudor_imp, saldo_acreedor_imp
    ), tags=(tag,))

    tabla.insert("", "end", values=("", "TOTALES", f"{total_debe:.2f}", f"{total_haber:.2f}",
                                    f"{total_deudor:.2f}", f"{total_acreedor:.2f}"), tags=('totalrow',))

    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tabla.pack(fill="both", expand=True, pady=(25, 0))

    from PaginaPrincipal import Return

    def actualizar_valores():
        global UTILIDAD_NETA, PERDIDA_NETA, IMPUESTO_CALCULADO
        from EstadoResultado import IMPUESTO_CALCULADO, UTILIDAD_NETA, PERDIDA_NETA

        for item in tabla.get_children():
            tabla.delete(item)

        total_debe = total_haber = total_deudor = total_acreedor = 0

        for i, cuenta in enumerate(cuentas_filtradas):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            nombre = cuenta['cuenta'].lower()

            if nombre == "capital contable":
                ajuste = UTILIDAD_NETA - PERDIDA_NETA
                haber = cuenta['haber_original'] + ajuste
                debe = cuenta['total_debe']
                if haber > debe:
                    saldo_deudor = ""
                    saldo_acreedor = f"{(haber - debe):.2f}"
                    total_acreedor += (haber - debe)
                elif debe > haber:
                    saldo_deudor = f"{(debe - haber):.2f}"
                    saldo_acreedor = ""
                    total_deudor += (debe - haber)
                else:
                    saldo_deudor = saldo_acreedor = ""
            elif nombre == "inventario final":
                # Buscar el valor original de inventario final en resumen_cuentas
                valor_original = 0
                for cuenta_original in resumen_cuentas:
                    if cuenta_original['cuenta'].lower() == "inventario final":
                        valor_original = cuenta_original['total_haber']
                        break

                debe = valor_original
                haber = 0
                saldo_deudor = f"{debe:.2f}" if debe > 0 else ""
                saldo_acreedor = ""
                if debe > 0:
                    total_deudor += debe
            else:
                debe = cuenta['total_debe']
                haber = cuenta['total_haber']
                if haber > debe:
                    saldo_deudor = ""
                    saldo_acreedor = f"{(haber - debe):.2f}"
                    total_acreedor += (haber - debe)
                elif debe > haber:
                    saldo_deudor = f"{(debe - haber):.2f}"
                    saldo_acreedor = ""
                    total_deudor += (debe - haber)
                else:
                    saldo_deudor = saldo_acreedor = ""

            total_debe += debe
            total_haber += haber

            tabla.insert("", "end", values=(
                cuenta['codigo'], cuenta['cuenta'], f"{debe:.2f}", f"{haber:.2f}", saldo_deudor, saldo_acreedor
            ), tags=(tag,))

        i = len(cuentas_filtradas)
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        debe_imp = 0.0
        haber_imp = IMPUESTO_CALCULADO
        saldo_deudor_imp = ""
        saldo_acreedor_imp = f"{IMPUESTO_CALCULADO:.2f}"

        total_debe += debe_imp
        total_haber += haber_imp
        total_acreedor += IMPUESTO_CALCULADO

        tabla.insert("", "end", values=(
            "N/A", "Impuestos", f"{debe_imp:.2f}", f"{haber_imp:.2f}",
            saldo_deudor_imp, saldo_acreedor_imp
        ), tags=(tag,))

        tabla.insert("", "end", values=("", "TOTALES", f"{total_debe:.2f}", f"{total_haber:.2f}",
                                        f"{total_deudor:.2f}", f"{total_acreedor:.2f}"), tags=('totalrow',))

    tk.Button(canvas, text="ACTUALIZAR", font=("Minecraftia", 12, "bold"),
              bg="#4CAF50", fg="white", relief="raised", bd=4, width=10,
              command=actualizar_valores).place(x=ancho // 2 + 500, y=alto - 80)

    tk.Button(canvas, text="VOLVER AL MENÚ", font=("Minecraftia", 12, "bold"),
              bg="#888888", fg="white", relief="raised", bd=4, width=40,
              command=lambda: Return(frame, frame_menu)).place(x=ancho // 2 - 280, y=alto - 80)
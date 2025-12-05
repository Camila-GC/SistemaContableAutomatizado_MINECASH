import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from Ingresar import movimientos
from Catalogo import datos as catalogo_datos
import os  # Añade esto al inicio del archivo con los otros imports
import sys

# Cambiar esta parte en LibroMayor.py (al inicio del archivo)
resumen_cuentas = []  # Mantener esta línea
cuentas_procesadas = set()  # Añadir esta línea para controlar cuentas ya procesadas

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


def mostrar_libro_mayor(frame_menu, ventana):
    if not movimientos:
        messagebox.showwarning("Sin movimientos", "Primero debes ingresar movimientos antes de acceder al Libro Mayor.")
        return

    frame_menu.pack_forget()
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()

    index = [0]
    cuentas = list(set(
        cuenta
        for m in movimientos
        for cuenta, debe, haber in m['datos']
    ))

    # Variable para almacenar las referencias de los textos de cuenta
    texto_cuenta_refs = []

    frame = tk.Frame(ventana, bg="white")
    frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Luego modifica la línea del fondo así:
    fondo = Image.open(rutas("Imagenes/Fondo.png")).resize((ventana.winfo_width(), ventana.winfo_height()))
    fondo_tk = ImageTk.PhotoImage(fondo)
    canvas.fondo = fondo_tk
    canvas.create_image(0, 0, image=fondo_tk, anchor="nw")

    # Título
    Contorno(canvas, texto="LIBRO MAYOR", x=ancho // 2, y=ancho - (ancho-50), fuente=("Minecraftia", 50, "bold"),
             color="black", contorno="white")


    tabla_frame = tk.Frame(canvas, bg="white", bd=2, relief="sunken")
    tabla_frame.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.65)

    columnas = ("No.", "Descripción", "Debe", "Haber", "Saldo")
    tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        if col == "Descripción":
            tabla.column(col, anchor="center", width=300)
        else:
            tabla.column(col, anchor="center", width=150)

    tabla.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    style = ttk.Style()
    style.configure("Treeview", font=("Minecraftia", 10), rowheight=28)
    style.configure("Treeview.Heading", font=("Minecraftia", 10, "bold"), background="#d0e0ff")
    style.map("Treeview", background=[("selected", "#3399FF")])

    tabla.tag_configure('oddrow', background='white')
    tabla.tag_configure('evenrow', background='#f0f0f0')
    tabla.tag_configure('totalrow', background='#3399FF', foreground='white', font=("Minecraftia", 10, "bold"))

    def borrar_texto_cuenta():
        """Borra todos los textos de cuenta anteriores"""
        for ref in texto_cuenta_refs:
            canvas.delete(ref)
        texto_cuenta_refs.clear()

    def crear_texto_cuenta_con_contorno(texto, x, y, fuente, color, contorno):
        """Crea texto con contorno y guarda las referencias"""
        # Crear contorno
        for dx in [-3, -1.5, 0, 1.5, 3]:
            for dy in [-3, -1.5, 0, 1.5, 3]:
                if dx != 0 or dy != 0:
                    ref = canvas.create_text(x + dx, y + dy, text=texto, font=fuente, fill=contorno)
                    texto_cuenta_refs.append(ref)

        # Crear texto principal
        ref = canvas.create_text(x, y, text=texto, font=fuente, fill=color)
        texto_cuenta_refs.append(ref)

    # Luego modificar la función mostrar_cuenta() así:
    def mostrar_cuenta(i):
        cuenta = cuentas[i]

        # Borrar texto de cuenta anterior
        borrar_texto_cuenta()

        # Mostrar nuevo letrero con Contorno
        crear_texto_cuenta_con_contorno(f"Cuenta: {cuenta}", ancho // 2, ancho - (ancho-100),
                                        ("Minecraftia", 22, "bold"), "black", "white")

        for item in tabla.get_children():
            tabla.delete(item)

        saldo = 0.0
        fila_par = True
        total_debe = 0
        total_haber = 0

        for mov in movimientos:
            for cta, debe, haber in mov['datos']:
                if cta == cuenta:
                    if debe:
                        saldo += debe
                        total_debe += debe
                        saldo_mostrar = abs(saldo) if saldo < 0 else saldo
                        tag = 'evenrow' if fila_par else 'oddrow'
                        tabla.insert("", "end", values=(
                            mov['numero'], mov['descripcion'], f"{debe:.2f}", "", f"{saldo_mostrar:.2f}"
                        ), tags=(tag,))
                        fila_par = not fila_par
                    elif haber:
                        saldo -= haber
                        total_haber += haber
                        saldo_mostrar = abs(saldo) if saldo < 0 else saldo
                        tag = 'evenrow' if fila_par else 'oddrow'
                        tabla.insert("", "end", values=(
                            mov['numero'], mov['descripcion'], "", f"{haber:.2f}", f"{saldo_mostrar:.2f}"
                        ), tags=(tag,))
                        fila_par = not fila_par

        saldo_final = abs(saldo) if saldo < 0 else saldo
        tabla.insert("", "end", values=("", "TOTALES", f"{total_debe:.2f}", f"{total_haber:.2f}", f"{saldo_final:.2f}"),
                     tags=("totalrow",))

        # === Modificación clave: Solo agregar si no ha sido procesada antes ===
        if cuenta not in cuentas_procesadas:
            codigo_cuenta = "N/A"
            nombre_cuenta = cuenta

            for cod, nombre, *_ in catalogo_datos:
                if nombre.lower() == cuenta.lower():
                    codigo_cuenta = cod
                    nombre_cuenta = nombre
                    break
            else:
                for cod, nombre, *_ in catalogo_datos:
                    if cuenta.lower() in nombre.lower():
                        codigo_cuenta = cod
                        nombre_cuenta = nombre
                        break

            resumen_cuentas.append({
                'codigo': codigo_cuenta,
                'cuenta': nombre_cuenta,
                'total_debe': total_debe,
                'total_haber': total_haber,
                'saldo_final': saldo_final
            })
            cuentas_procesadas.add(cuenta)  # Marcar como procesada

    def anterior():
        if index[0] > 0:
            index[0] -= 1
            mostrar_cuenta(index[0])

    def siguiente():
        if index[0] < len(cuentas) - 1:
            index[0] += 1
            mostrar_cuenta(index[0])

    tk.Button(canvas, text="Anterior", font=("Minecraftia", 12, "bold"), bg="#444", fg="white", bd=3,
              command=anterior).place(x=ancho // 2 - 120, y=alto - 150)
    tk.Button(canvas, text="Siguiente", font=("Minecraftia", 12, "bold"), bg="#444", fg="white", bd=3,
              command=siguiente).place(x=ancho // 2 + 5, y=alto - 150)

    # Cuadro de información en esquina inferior izquierda
    info_frame = tk.Frame(canvas, bg="#f0f0f0", bd=2, relief="raised")
    info_frame.place(x=20, y=alto - 120, width=200, height=80)

    # Calcular estadísticas
    num_operaciones = len(movimientos)
    num_libros_mayor = len(cuentas)

    tk.Label(info_frame, text="ESTADÍSTICAS", font=("Minecraftia", 10, "bold"),
             bg="#f0f0f0", fg="#333").pack(pady=2)
    tk.Label(info_frame, text=f"Operaciones: {num_operaciones}", font=("Minecraftia", 8),
             bg="#f0f0f0", fg="#555").pack()
    tk.Label(info_frame, text=f"Libros Mayor: {num_libros_mayor}", font=("Minecraftia", 8),
             bg="#f0f0f0", fg="#555").pack()

    from PaginaPrincipal import Return
    tk.Button(canvas, text="VOLVER AL MENU", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
              activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=40,
              command=lambda: Return(frame, frame_menu)).place(x=ancho // 2 - 280, y=alto - 90)

    mostrar_cuenta(index[0])
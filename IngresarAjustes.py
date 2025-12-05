import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys

# Diccionario de grupos y cuentas
catalogo = {
    "Activo circulante": [
        "Inventario", "Inventario Final"
    ],
    "Capital contable": [
        "Capital social", "Utilidad neta del ejercicio", "Reserva legal",
        "Capital contable", "Perdidas y Ganancias", "Perdida neta del ejercicio"
    ],
    "Ingresos": [
        "Ventas", "Rebajas sobre compras", "Devoluciones sobre compras","Descuentos sobre compras", "Otros ingresos"
    ],
    "Costos": [
        "Compras", "Devoluciones sobre ventas", "Rebajas sobre ventas","Descuentos sobre ventas", "Gastos de compra"
    ],
    "Gastos de ventas": ["Gastos de venta"],
    "Gastos administrativos": ["Gastos de administración"],
    "Otros Gastos": ["Otros Gastos"]
}

# Lista para guardar registros
ajustes = []

# Contador de operaciones
contador_operacion = [1]

def rutas(relative_path):
    """Devuelve la ruta absoluta para los archivos empaquetados (compatible con PyInstaller)."""
    try:
        base_path = sys._MEIPASS  # Carpeta temporal donde PyInstaller guarda los archivos
    except Exception:
        base_path = os.path.abspath(".")  # Si no está empaquetado, usar ruta actual

    return os.path.join(base_path, relative_path)  # Ruta absoluta final

def PaginaAj(frame_menu, ventana):
    frame_menu.pack_forget()
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()

    frame_ing = tk.Frame(ventana, width=ancho, height=alto)
    frame_ing.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_ing, width=ancho, height=alto, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Imagen de fondo
    fondo = Image.open(rutas("Imagenes/Fondo.png")).resize((ancho, alto))
    fondo_tk = ImageTk.PhotoImage(fondo)
    canvas.fondo = fondo_tk
    canvas.create_image(0, 0, image=fondo_tk, anchor="nw")

    # Agregar imagen decorativa de Bob en la esquina superior derecha
    try:
        bob = Image.open(rutas("Imagenes/Bob.png")).resize((450, 600))
        bob_tk = ImageTk.PhotoImage(bob)
        canvas.bob = bob_tk
        canvas.create_image(ancho - 150, 325, image=bob_tk, anchor="center")
    except Exception as e:
        print("No se pudo cargar la imagen de Bob:", e)

    def crear_label(canvas, texto, x, y, w=0.15, h=0.05):
        fondo_label = tk.Frame(canvas, bg="#d0e0ff", highlightbackground="#003366", highlightthickness=1)
        fondo_label.place(relx=x, rely=y, relwidth=w, relheight=h)
        tk.Label(fondo_label, text=texto, bg="#d0e0ff", fg="#003366", font=("Minecraftia", 10, "bold")) \
            .pack(expand=True, fill="both")

    def actualizar_cuentas(combo_grupo, combo_cuenta):
        grupo = combo_grupo.get()
        combo_cuenta['values'] = catalogo.get(grupo, [])
        if catalogo.get(grupo):
            combo_cuenta.set(catalogo[grupo][0])

    # Variables para almacenar los frames de movimientos
    movimientos_debe = []
    movimientos_haber = []

    # Frames contenedores para los movimientos
    frame_debe_container = None
    frame_haber_container = None

    def crear_movimiento_debe():
        if len(movimientos_debe) >= 10:  # Límite de 10 movimientos
            messagebox.showwarning("Límite alcanzado", "Máximo 10 movimientos de DEBE por operación.")
            return

        idx = len(movimientos_debe)

        # Determinar la columna (0 o 1) y fila
        columna = idx % 2
        fila_container = idx // 2

        # Si es la primera columna de una nueva fila, crear un frame contenedor
        if columna == 0:
            frame_fila = tk.Frame(frame_debe_container, bg="white")
            frame_fila.pack(fill="x", padx=5, pady=2)
            # Guardar referencia al frame de fila
            if not hasattr(crear_movimiento_debe, 'filas_debe'):
                crear_movimiento_debe.filas_debe = []
            crear_movimiento_debe.filas_debe.append(frame_fila)
        else:
            # Usar el frame de fila existente - VERIFICAR QUE EXISTE
            if (hasattr(crear_movimiento_debe, 'filas_debe') and
                    fila_container < len(crear_movimiento_debe.filas_debe)):
                frame_fila = crear_movimiento_debe.filas_debe[fila_container]
            else:
                # Si no existe, crear uno nuevo (caso de error)
                frame_fila = tk.Frame(frame_debe_container, bg="white")
                frame_fila.pack(fill="x", padx=5, pady=2)
                if not hasattr(crear_movimiento_debe, 'filas_debe'):
                    crear_movimiento_debe.filas_debe = []
                crear_movimiento_debe.filas_debe.append(frame_fila)

        frame_mov = tk.Frame(frame_fila, bg="white", relief="groove", bd=1, width=350)
        frame_mov.pack(side="left", fill="both", expand=True, padx=2)
        frame_mov.pack_propagate(False)

        # Etiquetas de cabecera (solo en los primeros dos movimientos)
        if idx < 2:
            tk.Label(frame_mov, text="", font=("Minecraftia", 7), bg="white", width=6).grid(row=0, column=0, padx=1)
            tk.Label(frame_mov, text="GRUPO", font=("Minecraftia", 7, "bold"), bg="white", fg="#003366").grid(row=0,
                                                                                                              column=1,
                                                                                                              padx=1)
            tk.Label(frame_mov, text="CUENTA", font=("Minecraftia", 7, "bold"), bg="white", fg="#003366").grid(row=0,
                                                                                                               column=2,
                                                                                                               padx=1)
            tk.Label(frame_mov, text="MONTO", font=("Minecraftia", 7, "bold"), bg="white", fg="#003366").grid(row=0,
                                                                                                              column=3,
                                                                                                              padx=1)
            tk.Label(frame_mov, text="", font=("Minecraftia", 7), bg="white", width=2).grid(row=0, column=4, padx=1)

        fila = 1 if idx < 2 else 0

        tk.Label(frame_mov, text=f"DEBE #{idx + 1}:", font=("Minecraftia", 8, "bold"), bg="white").grid(row=fila,
                                                                                                        column=0,
                                                                                                        sticky="w",
                                                                                                        padx=2)

        grupo_var = ttk.Combobox(frame_mov, values=list(catalogo.keys()), state="readonly", width=15, font=("Arial", 8))
        grupo_var.grid(row=fila, column=1, padx=1)

        cuenta_var = ttk.Combobox(frame_mov, state="readonly", width=15, font=("Arial", 8))
        cuenta_var.grid(row=fila, column=2, padx=1)

        monto_var = tk.Entry(frame_mov, width=12, font=("Arial", 8))
        monto_var.grid(row=fila, column=3, padx=1)

        btn_eliminar = tk.Button(frame_mov, text="X", bg="red", fg="white", font=("Arial", 7, "bold"),
                                 command=lambda: eliminar_movimiento_debe(idx))
        btn_eliminar.grid(row=fila, column=4, padx=1)

        grupo_var.bind("<<ComboboxSelected>>", lambda e: actualizar_cuentas(grupo_var, cuenta_var))

        movimientos_debe.append({
            'frame': frame_mov,
            'frame_fila': frame_fila,
            'grupo': grupo_var,
            'cuenta': cuenta_var,
            'monto': monto_var,
            'original_idx': idx  # Guardar el índice original
        })

    def crear_movimiento_haber():
        if len(movimientos_haber) >= 10:  # Límite de 10 movimientos
            messagebox.showwarning("Límite alcanzado", "Máximo 10 movimientos de HABER por operación.")
            return

        idx = len(movimientos_haber)

        # Determinar la columna (0 o 1) y fila
        columna = idx % 2
        fila_container = idx // 2

        # Si es la primera columna de una nueva fila, crear un frame contenedor
        if columna == 0:
            frame_fila = tk.Frame(frame_haber_container, bg="white")
            frame_fila.pack(fill="x", padx=5, pady=2)
            # Guardar referencia al frame de fila
            if not hasattr(crear_movimiento_haber, 'filas_haber'):
                crear_movimiento_haber.filas_haber = []
            crear_movimiento_haber.filas_haber.append(frame_fila)
        else:
            # Usar el frame de fila existente - VERIFICAR QUE EXISTE
            if (hasattr(crear_movimiento_haber, 'filas_haber') and
                    fila_container < len(crear_movimiento_haber.filas_haber)):
                frame_fila = crear_movimiento_haber.filas_haber[fila_container]
            else:
                # Si no existe, crear uno nuevo (caso de error)
                frame_fila = tk.Frame(frame_haber_container, bg="white")
                frame_fila.pack(fill="x", padx=5, pady=2)
                if not hasattr(crear_movimiento_haber, 'filas_haber'):
                    crear_movimiento_haber.filas_haber = []
                crear_movimiento_haber.filas_haber.append(frame_fila)

        frame_mov = tk.Frame(frame_fila, bg="white", relief="groove", bd=1, width=350)
        frame_mov.pack(side="left", fill="both", expand=True, padx=2)
        frame_mov.pack_propagate(False)

        # Etiquetas de cabecera (solo en los primeros dos movimientos)
        if idx < 2:
            tk.Label(frame_mov, text="", font=("Minecraftia", 7), bg="white", width=6).grid(row=0, column=0, padx=1)
            tk.Label(frame_mov, text="GRUPO", font=("Minecraftia", 7, "bold"), bg="white", fg="#003366").grid(row=0,
                                                                                                              column=1,
                                                                                                              padx=1)
            tk.Label(frame_mov, text="CUENTA", font=("Minecraftia", 7, "bold"), bg="white", fg="#003366").grid(row=0,
                                                                                                               column=2,
                                                                                                               padx=1)
            tk.Label(frame_mov, text="MONTO", font=("Minecraftia", 7, "bold"), bg="white", fg="#003366").grid(row=0,
                                                                                                              column=3,
                                                                                                              padx=1)
            tk.Label(frame_mov, text="", font=("Minecraftia", 7), bg="white", width=2).grid(row=0, column=4, padx=1)

        fila = 1 if idx < 2 else 0

        tk.Label(frame_mov, text=f"HABER #{idx + 1}:", font=("Minecraftia", 8, "bold"), bg="white").grid(row=fila,
                                                                                                         column=0,
                                                                                                         sticky="w",
                                                                                                         padx=2)

        grupo_var = ttk.Combobox(frame_mov, values=list(catalogo.keys()), state="readonly", width=15, font=("Arial", 8))
        grupo_var.grid(row=fila, column=1, padx=1)

        cuenta_var = ttk.Combobox(frame_mov, state="readonly", width=15, font=("Arial", 8))
        cuenta_var.grid(row=fila, column=2, padx=1)

        monto_var = tk.Entry(frame_mov, width=12, font=("Arial", 8))
        monto_var.grid(row=fila, column=3, padx=1)

        btn_eliminar = tk.Button(frame_mov, text="X", bg="red", fg="white", font=("Arial", 7, "bold"),
                                 command=lambda: eliminar_movimiento_haber(idx))
        btn_eliminar.grid(row=fila, column=4, padx=1)

        grupo_var.bind("<<ComboboxSelected>>", lambda e: actualizar_cuentas(grupo_var, cuenta_var))

        movimientos_haber.append({
            'frame': frame_mov,
            'frame_fila': frame_fila,
            'grupo': grupo_var,
            'cuenta': cuenta_var,
            'monto': monto_var,
            'original_idx': idx  # Guardar el índice original
        })

    def eliminar_movimiento_debe(idx):
        if idx < len(movimientos_debe):
            mov_a_eliminar = None
            # Buscar el movimiento por su índice original
            for i, mov in enumerate(movimientos_debe):
                if mov.get('original_idx', i) == idx:
                    mov_a_eliminar = mov
                    break

            if mov_a_eliminar:
                frame_mov = mov_a_eliminar['frame']
                frame_fila = mov_a_eliminar['frame_fila']

                frame_mov.destroy()
                movimientos_debe.remove(mov_a_eliminar)

                # Si el frame de fila está vacío, eliminarlo también
                if len(frame_fila.winfo_children()) == 0:
                    frame_fila.destroy()
                    if hasattr(crear_movimiento_debe, 'filas_debe'):
                        try:
                            crear_movimiento_debe.filas_debe.remove(frame_fila)
                        except ValueError:
                            pass  # Ya fue removido

                # Renumerar y reorganizar los movimientos restantes
                reorganizar_movimientos_debe()

    def eliminar_movimiento_haber(idx):
        if idx < len(movimientos_haber):
            mov_a_eliminar = None
            # Buscar el movimiento por su índice original
            for i, mov in enumerate(movimientos_haber):
                if mov.get('original_idx', i) == idx:
                    mov_a_eliminar = mov
                    break

            if mov_a_eliminar:
                frame_mov = mov_a_eliminar['frame']
                frame_fila = mov_a_eliminar['frame_fila']

                frame_mov.destroy()
                movimientos_haber.remove(mov_a_eliminar)

                # Si el frame de fila está vacío, eliminarlo también
                if len(frame_fila.winfo_children()) == 0:
                    frame_fila.destroy()
                    if hasattr(crear_movimiento_haber, 'filas_haber'):
                        try:
                            crear_movimiento_haber.filas_haber.remove(frame_fila)
                        except ValueError:
                            pass  # Ya fue removido

                # Renumerar y reorganizar los movimientos restantes
                reorganizar_movimientos_haber()

    def reorganizar_movimientos_debe():
        # Guardar los datos actuales ANTES de destruir los widgets
        datos_temp = []
        for mov in movimientos_debe:
            try:
                # Verificar que los widgets aún existan antes de acceder a ellos
                if mov['grupo'].winfo_exists() and mov['cuenta'].winfo_exists() and mov['monto'].winfo_exists():
                    datos_temp.append({
                        'grupo': mov['grupo'].get(),
                        'cuenta': mov['cuenta'].get(),
                        'monto': mov['monto'].get()
                    })
                else:
                    # Si el widget no existe, agregar datos vacíos
                    datos_temp.append({
                        'grupo': '',
                        'cuenta': '',
                        'monto': ''
                    })
            except tk.TclError:
                # Widget destruido, agregar datos vacíos
                datos_temp.append({
                    'grupo': '',
                    'cuenta': '',
                    'monto': ''
                })

        # Limpiar y recrear la estructura
        if hasattr(crear_movimiento_debe, 'filas_debe'):
            for frame_fila in crear_movimiento_debe.filas_debe[:]:  # Crear copia de la lista
                try:
                    if frame_fila.winfo_exists():
                        frame_fila.destroy()
                except tk.TclError:
                    pass  # Frame ya destruido
            crear_movimiento_debe.filas_debe.clear()

        # Limpiar movimientos
        movimientos_debe.clear()

        # Recrear movimientos con los datos guardados
        for i, datos in enumerate(datos_temp):
            crear_movimiento_debe()
            if datos['grupo']:
                movimientos_debe[i]['grupo'].set(datos['grupo'])
                actualizar_cuentas(movimientos_debe[i]['grupo'], movimientos_debe[i]['cuenta'])
                if datos['cuenta']:
                    movimientos_debe[i]['cuenta'].set(datos['cuenta'])
                if datos['monto']:
                    movimientos_debe[i]['monto'].insert(0, datos['monto'])

    def reorganizar_movimientos_haber():
        # Guardar los datos actuales ANTES de destruir los widgets
        datos_temp = []
        for mov in movimientos_haber:
            try:
                # Verificar que los widgets aún existan antes de acceder a ellos
                if mov['grupo'].winfo_exists() and mov['cuenta'].winfo_exists() and mov['monto'].winfo_exists():
                    datos_temp.append({
                        'grupo': mov['grupo'].get(),
                        'cuenta': mov['cuenta'].get(),
                        'monto': mov['monto'].get()
                    })
                else:
                    # Si el widget no existe, agregar datos vacíos
                    datos_temp.append({
                        'grupo': '',
                        'cuenta': '',
                        'monto': ''
                    })
            except tk.TclError:
                # Widget destruido, agregar datos vacíos
                datos_temp.append({
                    'grupo': '',
                    'cuenta': '',
                    'monto': ''
                })

        # Limpiar y recrear la estructura
        if hasattr(crear_movimiento_haber, 'filas_haber'):
            for frame_fila in crear_movimiento_haber.filas_haber[:]:  # Crear copia de la lista
                try:
                    if frame_fila.winfo_exists():
                        frame_fila.destroy()
                except tk.TclError:
                    pass  # Frame ya destruido
            crear_movimiento_haber.filas_haber.clear()

        # Limpiar movimientos
        movimientos_haber.clear()

        # Recrear movimientos con los datos guardados
        for i, datos in enumerate(datos_temp):
            crear_movimiento_haber()
            if datos['grupo']:
                movimientos_haber[i]['grupo'].set(datos['grupo'])
                actualizar_cuentas(movimientos_haber[i]['grupo'], movimientos_haber[i]['cuenta'])
                if datos['cuenta']:
                    movimientos_haber[i]['cuenta'].set(datos['cuenta'])
                if datos['monto']:
                    movimientos_haber[i]['monto'].insert(0, datos['monto'])

    def limpiar_campos():
        entry_desc.delete(0, tk.END)

        # Limpiar todos los movimientos DEBE
        for mov in movimientos_debe[:]:
            try:
                mov['frame'].destroy()
            except tk.TclError:
                pass
        movimientos_debe.clear()

        # Limpiar todos los movimientos HABER
        for mov in movimientos_haber[:]:
            try:
                mov['frame'].destroy()
            except tk.TclError:
                pass
        movimientos_haber.clear()

        # Limpiar y destruir TODOS los frames de fila DEBE
        if hasattr(crear_movimiento_debe, 'filas_debe'):
            for frame_fila in crear_movimiento_debe.filas_debe[:]:
                try:
                    frame_fila.destroy()
                except tk.TclError:
                    pass
            crear_movimiento_debe.filas_debe.clear()

        # Limpiar y destruir TODOS los frames de fila HABER
        if hasattr(crear_movimiento_haber, 'filas_haber'):
            for frame_fila in crear_movimiento_haber.filas_haber[:]:
                try:
                    frame_fila.destroy()
                except tk.TclError:
                    pass
            crear_movimiento_haber.filas_haber.clear()

        # Limpiar completamente los contenedores
        for widget in frame_debe_container.winfo_children():
            widget.destroy()
        for widget in frame_haber_container.winfo_children():
            widget.destroy()

    def validar_balance():
        total_debe = 0
        total_haber = 0

        for mov in movimientos_debe:
            try:
                monto = float(mov['monto'].get())
                total_debe += monto
            except (ValueError, tk.TclError):
                continue

        for mov in movimientos_haber:
            try:
                monto = float(mov['monto'].get())
                total_haber += monto
            except (ValueError, tk.TclError):
                continue

        return abs(total_debe - total_haber) < 0.01  # Tolerancia para errores de punto flotante

    def guardar():
        desc = entry_desc.get().strip()

        if not desc:
            messagebox.showwarning("Campo incompleto", "Por favor ingresa una descripción.")
            return

        # CAMBIO: Permitir solo DEBE o solo HABER
        if not movimientos_debe and not movimientos_haber:
            messagebox.showwarning("Movimientos incompletos",
                                   "Debe haber al menos un movimiento (DEBE o HABER).")
            return

        # Validar que todos los campos estén completos
        datos_movimiento = []

        for mov in movimientos_debe:
            try:
                grupo = mov['grupo'].get()
                cuenta = mov['cuenta'].get()
                monto_str = mov['monto'].get().strip()
            except tk.TclError:
                continue  # Widget destruido, saltar

            if not all([grupo, cuenta, monto_str]):
                messagebox.showwarning("Campos incompletos", "Todos los movimientos deben tener grupo, cuenta y monto.")
                return

            try:
                monto = float(monto_str)
                if monto <= 0:
                    messagebox.showerror("Error de monto", "Los montos deben ser números positivos.")
                    return
                datos_movimiento.append((cuenta, monto, 0.0))  # (cuenta, debe, haber)
            except ValueError:
                messagebox.showerror("Error de monto", "Los montos deben ser números válidos.")
                return

        for mov in movimientos_haber:
            try:
                grupo = mov['grupo'].get()
                cuenta = mov['cuenta'].get()
                monto_str = mov['monto'].get().strip()
            except tk.TclError:
                continue  # Widget destruido, saltar

            if not all([grupo, cuenta, monto_str]):
                messagebox.showwarning("Campos incompletos", "Todos los movimientos deben tener grupo, cuenta y monto.")
                return

            try:
                monto = float(monto_str)
                if monto <= 0:
                    messagebox.showerror("Error de monto", "Los montos deben ser números positivos.")
                    return
                datos_movimiento.append((cuenta, 0.0, monto))  # (cuenta, debe, haber)
            except ValueError:
                messagebox.showerror("Error de monto", "Los montos deben ser números válidos.")
                return

        # CAMBIO: Solo validar balance si hay movimientos de ambos tipos
        if movimientos_debe and movimientos_haber:
            if not validar_balance():
                messagebox.showerror("Error de balance", "El total de DEBE debe ser igual al total de HABER.")
                return

        # Guardar el movimiento (ahora en 'ajustes' en lugar de 'movimientos')
        movimiento = {
            "numero": contador_operacion[0],
            "descripcion": desc,
            "datos": datos_movimiento
        }

        ajustes.append(movimiento)

        messagebox.showinfo("Guardado", f"Operación #{contador_operacion[0]} guardada correctamente.")

        contador_operacion[0] += 1
        operacion_num_label.config(text=f"#{contador_operacion[0]}")
        limpiar_campos()

    # Estiliza el número de operación
    op_frame = tk.Frame(canvas, bg="#d0e0ff", highlightbackground="#003366", highlightthickness=2)
    op_frame.place(relx=0.02, rely=0.02, relwidth=0.17, relheight=0.07)
    tk.Label(op_frame, text="AJUSTE", bg="#d0e0ff", fg="#003366", font=("Minecraftia", 10, "bold")).pack(side="left",
                                                                                                            padx=5)
    operacion_num_label = tk.Label(op_frame, text=f"#{contador_operacion[0]}", bg="#d0e0ff", fg="#003366",
                                   font=("Minecraftia", 11, "bold"))
    operacion_num_label.pack(side="left")

    # Descripción
    crear_label(canvas, "DESCRIPCIÓN:", 0.02, 0.12)
    entry_desc = tk.Entry(canvas, width=80, bg="#DDDDDD", bd=2, font=("Minecraftia", 11))
    entry_desc.place(relx=0.18, rely=0.12)

    # Frame principal para los movimientos
    main_frame = tk.Frame(canvas, bg="white")
    main_frame.place(relx=0.02, rely=0.20, relwidth=0.75, relheight=0.55)

    # Frame para movimientos DEBE
    debe_frame = tk.LabelFrame(main_frame, text="MOVIMIENTOS DEBE", font=("Minecraftia", 12, "bold"),
                               bg="white", fg="#003366")
    debe_frame.pack(fill="both", expand=True, padx=5, pady=5)

    frame_debe_container = tk.Frame(debe_frame, bg="white")
    frame_debe_container.pack(fill="both", expand=True, padx=5, pady=5)

    btn_add_debe = tk.Button(debe_frame, text="+ Agregar DEBE", font=("Minecraftia", 10, "bold"),
                             bg="#4CAF50", fg="white", command=crear_movimiento_debe)
    btn_add_debe.pack(pady=5)

    # Frame para movimientos HABER
    haber_frame = tk.LabelFrame(main_frame, text="MOVIMIENTOS HABER", font=("Minecraftia", 12, "bold"),
                                bg="white", fg="#003366")
    haber_frame.pack(fill="both", expand=True, padx=5, pady=5)

    frame_haber_container = tk.Frame(haber_frame, bg="white")
    frame_haber_container.pack(fill="both", expand=True, padx=5, pady=5)

    btn_add_haber = tk.Button(haber_frame, text="+ Agregar HABER", font=("Minecraftia", 10, "bold"),
                              bg="#2196F3", fg="white", command=crear_movimiento_haber)
    btn_add_haber.pack(pady=5)

    # Botones principales
    tk.Button(canvas, text="GUARDAR OPERACIÓN", font=("Minecraftia", 12, "bold"), bg="#444", fg="white",
              command=guardar, bd=3).place(relx=0.35, rely=0.78)

    from PaginaConA import Return
    tk.Button(canvas, text="VOLVER AL MENU", font=("Minecraftia", 12, "bold"), bg="#888888", fg="white",
              activebackground="#2f2f2f", activeforeground="white", relief="raised", bd=4, width=40,
              command=lambda: Return(frame_ing, frame_menu)).place(x=ancho // 2 - 280, y=alto - 100)

    # Crear al menos un movimiento de cada tipo al inicio
    crear_movimiento_debe()
    crear_movimiento_haber()
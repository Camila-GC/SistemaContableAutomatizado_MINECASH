import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
from PaginaPrincipal import Return
from LibroMayor import resumen_cuentas, cuentas_procesadas
from Catalogo import datos as catalogo_datos
import os
import sys


def rutas(relative_path):
    """Devuelve la ruta absoluta para los archivos empaquetados (compatible con PyInstaller)."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def Contorno(canvas, texto, x, y, fuente, color, contorno):
    for dx in [-3, -1.5, 0, 1.5, 3]:
        for dy in [-3, -1.5, 0, 1.5, 3]:
            if dx != 0 or dy != 0:
                canvas.create_text(x + dx, y + dy, text=texto, font=fuente, fill=contorno)
    canvas.create_text(x, y, text=texto, font=fuente, fill=color)


def calcular_valores_estado_resultado():
    """Calcula los valores del estado de resultado necesarios para el balance"""
    # Obtener datos del libro mayor
    datos = obtener_datos_estado_resultado()

    # Calcular ventas netas
    ventas_netas = datos['ventas_totales'] - datos['devoluciones_ventas'] - datos['rebajas_ventas']

    # Calcular costo de ventas
    compras_totales = datos['compras'] + datos['gastos_compras']
    compras_netas = compras_totales - datos['devoluciones_compras'] - datos['rebajas_compras']
    mercancia_disponible = compras_netas + datos['inventario_inicial']
    costo_ventas = mercancia_disponible - datos['inventario_final']

    # Calcular gastos de operación
    gastos_operacion = datos['gastos_administracion'] + datos['gastos_venta']

    # Calcular utilidad/pérdida bruta
    if ventas_netas > costo_ventas:
        utilidad_bruta = ventas_netas - costo_ventas
        es_utilidad_bruta = True
    else:
        perdida_bruta = costo_ventas - ventas_netas
        es_utilidad_bruta = False

    # Calcular utilidad/pérdida en operación
    if es_utilidad_bruta:
        if utilidad_bruta > gastos_operacion:
            utilidad_operacion = utilidad_bruta - gastos_operacion
            es_utilidad_operacion = True
        else:
            perdida_operacion = gastos_operacion - utilidad_bruta
            es_utilidad_operacion = False
    else:
        perdida_operacion = perdida_bruta + gastos_operacion
        es_utilidad_operacion = False

    # Calcular resultado final
    impuesto_calculado = 0.0
    utilidad_neta = 0.0
    perdida_neta = 0.0

    if not es_utilidad_operacion:
        # Pérdida neta del ejercicio
        perdida_neta = perdida_operacion + datos['otros_gastos'] - datos['otros_ingresos']
    else:
        # Utilidad antes de impuestos
        utilidad_antes_impuestos = utilidad_operacion + datos['otros_ingresos'] - datos['otros_gastos']

        if utilidad_antes_impuestos > 0:
            # Calcular impuestos del 25%
            impuesto_calculado = utilidad_antes_impuestos * 0.25
            utilidad_neta = utilidad_antes_impuestos - impuesto_calculado
        else:
            utilidad_neta = utilidad_antes_impuestos

    return impuesto_calculado, utilidad_neta, perdida_neta


def obtener_datos_estado_resultado():
    """Extrae los datos necesarios del libro mayor para el estado de resultado"""
    global resumen_cuentas, cuentas_procesadas

    # Regenerar datos si es necesario
    if not resumen_cuentas:
        regenerar_libro_mayor()

    datos = {
        'ventas_totales': 0,
        'devoluciones_ventas': 0,
        'rebajas_ventas': 0,
        'compras': 0,
        'gastos_compras': 0,
        'devoluciones_compras': 0,
        'rebajas_compras': 0,
        'inventario_inicial': 0,
        'inventario_final': 0,
        'gastos_administracion': 0,
        'gastos_venta': 0,
        'otros_ingresos': 0,
        'otros_gastos': 0
    }

    # Mapeo de cuentas
    mapeo_cuentas = {
        'ventas': 'ventas_totales',
        'ventas totales': 'ventas_totales',
        'ingresos por ventas': 'ventas_totales',
        'devolución sobre ventas': 'devoluciones_ventas',
        'devoluciones sobre ventas': 'devoluciones_ventas',
        'devolucion sobre ventas': 'devoluciones_ventas',
        'rebajas sobre ventas': 'rebajas_ventas',
        'descuentos sobre ventas': 'rebajas_ventas',
        'compras': 'compras',
        'compra': 'compras',
        'compra de mercancia': 'compras',
        'compra de mercancía': 'compras',
        'gastos de compra': 'gastos_compras',
        'gasto de compra': 'gastos_compras',
        'gastos sobre compras': 'gastos_compras',
        'fletes sobre compras': 'gastos_compras',
        'devolución sobre compras': 'devoluciones_compras',
        'devoluciones sobre compras': 'devoluciones_compras',
        'devolucion sobre compras': 'devoluciones_compras',
        'rebajas sobre compras': 'rebajas_compras',
        'descuentos sobre compras': 'rebajas_compras',
        'inventario': 'inventario_inicial',
        'inventario inicial': 'inventario_inicial',
        'inventario final': 'inventario_final',
        'inv final': 'inventario_final',
        'inv inicial': 'inventario_inicial',
        'gastos de administracion': 'gastos_administracion',
        'gastos de administración': 'gastos_administracion',
        'gastos administrativos': 'gastos_administracion',
        'gasto de administracion': 'gastos_administracion',
        'gastos de venta': 'gastos_venta',
        'gasto de venta': 'gastos_venta',
        'gastos de ventas': 'gastos_venta',
        'gastos comerciales': 'gastos_venta',
        'otros ingresos': 'otros_ingresos',
        'ingresos diversos': 'otros_ingresos',
        'ingresos varios': 'otros_ingresos',
        'intereses': 'otros_gastos',
        'otros gastos': 'otros_gastos',
        'gastos diversos': 'otros_gastos',
        'gastos varios': 'otros_gastos',
        'intereses pagados': 'otros_gastos',
        'gastos financieros': 'otros_gastos'
    }

    for cuenta in resumen_cuentas:
        if isinstance(cuenta, dict):
            cuenta_nombre = cuenta.get('cuenta', '')
            saldo_final = float(cuenta.get('saldo_final', 0))
        elif isinstance(cuenta, (list, tuple)) and len(cuenta) >= 2:
            cuenta_nombre = str(cuenta[0])
            saldo_final = float(cuenta[1])
        else:
            continue

        cuenta_normalizada = cuenta_nombre.strip().lower()

        # Buscar coincidencia exacta
        if cuenta_normalizada in mapeo_cuentas:
            clave = mapeo_cuentas[cuenta_normalizada]
            datos[clave] += saldo_final
        else:
            # Buscar coincidencia parcial
            for nombre_mapeo, clave in mapeo_cuentas.items():
                if nombre_mapeo in cuenta_normalizada or cuenta_normalizada in nombre_mapeo:
                    datos[clave] += saldo_final
                    break

    return datos


def obtener_datos_libro_mayor():
    """Extrae y organiza los datos necesarios del libro mayor para el balance general"""
    global resumen_cuentas, cuentas_procesadas

    resumen_cuentas.clear()
    cuentas_procesadas.clear()
    regenerar_libro_mayor()

    datos = {
        'activo_circulante': {},
        'activo_no_circulante': {},
        'pasivo_corto_plazo': {},
        'pasivo_largo_plazo': {},
        'capital_contable': {}
    }

    # Obtener datos del estado de resultado para el inventario final
    estado_resultado_datos = obtener_datos_estado_resultado()

    for cuenta in resumen_cuentas:
        codigo = cuenta['codigo']
        nombre = cuenta['cuenta']
        saldo = cuenta['saldo_final']

        if codigo.startswith('11'):
            # CORRECCIÓN 1: Cambiar inventario por inventario final en activo circulante
            if 'inventario' in nombre.lower() and 'final' not in nombre.lower():
                # Usar el inventario final del estado de resultado
                datos['activo_circulante']['Inventario Final'] = estado_resultado_datos['inventario_final']
            else:
                datos['activo_circulante'][nombre] = saldo
        elif codigo.startswith('12'):
            datos['activo_no_circulante'][nombre] = saldo
        elif codigo.startswith('21'):
            datos['pasivo_corto_plazo'][nombre] = saldo
        elif codigo.startswith('22'):
            datos['pasivo_largo_plazo'][nombre] = saldo
        elif codigo.startswith('3'):
            datos['capital_contable'][nombre] = saldo

    return datos


def regenerar_libro_mayor():
    """Regenera los datos del libro mayor"""
    from Ingresar import movimientos

    if not movimientos:
        return

    cuentas = list(set(
        cuenta for m in movimientos for cuenta, debe, haber in m['datos']
    ))

    for cuenta in cuentas:
        if cuenta not in cuentas_procesadas:
            saldo = 0.0
            total_debe = 0
            total_haber = 0

            for mov in movimientos:
                for cta, debe, haber in mov['datos']:
                    if cta == cuenta:
                        if debe:
                            saldo += debe
                            total_debe += debe
                        elif haber:
                            saldo -= haber
                            total_haber += haber

            saldo_final = abs(saldo) if saldo < 0 else saldo
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
            cuentas_procesadas.add(cuenta)


def mostrar_estado_situacion_financiera(frame_menu, ventana):
    from Ingresar import movimientos

    if not movimientos:
        messagebox.showwarning("Sin movimientos",
                               "Primero debes ingresar movimientos antes de acceder al Estado de Situación Financiera.")
        return

    frame_menu.pack_forget()
    ventana.state('zoomed')
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()

    frame_principal = tk.Frame(ventana, bg="white")
    frame_principal.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_principal, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    try:
        fondo = Image.open(rutas("Imagenes/Fondo.png")).resize((ancho, alto))
        fondo_tk = ImageTk.PhotoImage(fondo)
        canvas.fondo = fondo_tk
        canvas.create_image(0, 0, image=fondo_tk, anchor="nw")
    except:
        canvas.configure(bg="#f0f8ff")

    Contorno(canvas, "ESTADO DE SITUACIÓN FINANCIERA", ancho // 2, 50,
             ("Minecraftia", 30, "bold"), "black", "white")

    # Obtener datos del balance
    datos = obtener_datos_libro_mayor()

    # Calcular valores del estado de resultado
    impuesto_calculado, utilidad_neta, perdida_neta = calcular_valores_estado_resultado()

    tabla_frame = tk.Frame(canvas, bg="white", bd=2, relief="sunken")
    tabla_frame.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.75)

    columnas = ("Col1", "Col2", "Col3", "Col4", "Col5", "Col6")
    tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings")

    # Configurar columnas con anchos fijos desde el inicio
    tabla.column("Col1", width=150, anchor="w")
    tabla.column("Col2", width=150, anchor="w")
    tabla.column("Col3", width=150, anchor="w")
    tabla.column("Col4", width=150, anchor="w")
    tabla.column("Col5", width=150, anchor="w")
    tabla.column("Col6", width=150, anchor="w")

    for col in columnas:
        tabla.heading(col, text="")

    tabla.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    style = ttk.Style()
    style.configure("Treeview", font=("Minecraftia", 9), rowheight=25, fieldbackground="white")
    style.configure("Treeview.Heading", font=("Minecraftia", 10, "bold"), background="#d0e0ff")

    # Configurar bordes para la tabla
    style.configure("Treeview",
                    font=("Minecraftia", 9),
                    rowheight=25,
                    fieldbackground="white",
                    borderwidth=1,
                    relief="solid")

    # Configurar los estilos de las celdas con bordes
    style.configure("Treeview.Item",
                    borderwidth=1,
                    relief="solid")

    tabla.tag_configure('empresa', background='#4472C4', foreground='white', font=('Minecraftia', 10, 'bold'))
    tabla.tag_configure('fecha', background='#4472C4', foreground='white', font=('Minecraftia', 9, 'bold'))
    tabla.tag_configure('encabezado', background='#D9E1F2', foreground='black', font=('Minecraftia', 9, 'bold'))
    tabla.tag_configure('subgrupo', background='#E7E6E6', foreground='black', font=('Minecraftia', 9, 'bold'))
    tabla.tag_configure('cuenta', background='white', foreground='black')
    tabla.tag_configure('total', background='#C5D9F1', foreground='black', font=('Minecraftia', 9, 'bold'))
    tabla.tag_configure('total_final', background='#4472C4', foreground='white', font=('Minecraftia', 10, 'bold'))

    def formato_moneda(valor):
        return f"${valor:,.2f}" if valor else ""

    def agregar_fila(valores, tag='cuenta'):
        tabla.insert("", "end", values=valores, tags=(tag,))

    def llenar_tabla():
        # Limpiar tabla sin recrear estructura
        for item in tabla.get_children():
            tabla.delete(item)

        # Recalcular valores del estado de resultado
        nonlocal impuesto_calculado, utilidad_neta, perdida_neta
        impuesto_calculado, utilidad_neta, perdida_neta = calcular_valores_estado_resultado()

        # Crear texto centrado manualmente usando espacios
        empresa_texto = "EMPRESA TECNM S.A. DE C.V.".center(90)
        fecha = datetime.now().strftime('%d/%m/%Y')
        fecha_texto = f"Estado de Situación Financiera al {fecha}".center(90)

        # Fila 1: Nombre de empresa (usando la primera columna con texto centrado)
        agregar_fila((empresa_texto, "", "", "", "", ""), 'empresa')

        # Fila 2: Título del estado (usando la primera columna con texto centrado)
        agregar_fila((fecha_texto, "", "", "", "", ""), 'fecha')

        # Fila 3: Encabezados de grupos principales
        agregar_fila(("ACTIVOS", "1", "2", "PASIVOS", "1", "2"), 'encabezado')

        # Calcular totales
        total_activo_circulante = sum(datos['activo_circulante'].values())
        total_activo_no_circulante = sum(datos['activo_no_circulante'].values())
        total_pasivo_corto = sum(datos['pasivo_corto_plazo'].values())
        total_pasivo_largo = sum(datos['pasivo_largo_plazo'].values())

        capital_social = sum(datos['capital_contable'].values())

        # CORRECCIÓN 2: Incluir impuestos en el total del capital
        total_capital = capital_social + impuesto_calculado

        if utilidad_neta > 0:
            total_capital += utilidad_neta
        else:
            total_capital -= abs(perdida_neta)

        # Fila 4: Subgrupos (Circulante y A corto plazo)
        if datos['activo_circulante'] or datos['pasivo_corto_plazo']:
            col1 = "Circulante" if datos['activo_circulante'] else ""
            col4 = "A corto plazo" if datos['pasivo_corto_plazo'] else ""
            agregar_fila((col1, "", "", col4, "", ""), 'subgrupo')

        # Procesar activo circulante y pasivo corto plazo en paralelo
        cuentas_ac = list(datos['activo_circulante'].items())
        cuentas_pc = list(datos['pasivo_corto_plazo'].items())

        max_filas = max(len(cuentas_ac), len(cuentas_pc))

        for i in range(max_filas):
            col1 = col2 = col3 = col4 = col5 = col6 = ""

            # Procesar activo circulante
            if i < len(cuentas_ac):
                cuenta_ac, saldo_ac = cuentas_ac[i]
                col1 = cuenta_ac
                col2 = formato_moneda(saldo_ac)
                # En la última cuenta del activo circulante, colocar el total en col3
                if i == len(cuentas_ac) - 1:
                    col3 = formato_moneda(total_activo_circulante)

            # Procesar pasivo corto plazo
            if i < len(cuentas_pc):
                cuenta_pc, saldo_pc = cuentas_pc[i]
                col4 = cuenta_pc
                col5 = formato_moneda(saldo_pc)
                # En la última cuenta del pasivo corto plazo, colocar el total en col6
                if i == len(cuentas_pc) - 1:
                    col6 = formato_moneda(total_pasivo_corto)

            agregar_fila((col1, col2, col3, col4, col5, col6))

        # Activo No Circulante
        if datos['activo_no_circulante']:
            agregar_fila(("No circulante", "", "", "", "", ""), 'subgrupo')

            cuentas_anc = list(datos['activo_no_circulante'].items())
            for i, (cuenta, saldo) in enumerate(cuentas_anc):
                # En la última cuenta, colocar el total en col3
                col3 = formato_moneda(total_activo_no_circulante) if i == len(cuentas_anc) - 1 else ""
                agregar_fila((cuenta, formato_moneda(saldo), col3, "", "", ""))

        # CORRECCIÓN 3: Pasivo a Largo Plazo independiente del activo no circulante
        if datos['pasivo_largo_plazo']:
            agregar_fila(("", "", "", "A largo plazo", "", ""), 'subgrupo')

            cuentas_plp = list(datos['pasivo_largo_plazo'].items())
            for i, (cuenta, saldo) in enumerate(cuentas_plp):
                # En la última cuenta, colocar el total en col6
                col6 = formato_moneda(total_pasivo_largo) if i == len(cuentas_plp) - 1 else ""
                agregar_fila(("", "", "", cuenta, formato_moneda(saldo), col6))

        # Capital Contable
        agregar_fila(("", "", "", "Capital Contable", "", ""), 'subgrupo')

        # Cuentas de capital
        for cuenta, saldo in datos['capital_contable'].items():
            agregar_fila(("", "", "", cuenta, formato_moneda(saldo), ""))

        # Escenario 1: Utilidad Neta
        if utilidad_neta > 0:
            agregar_fila(("", "", "", "Utilidad Neta del Ejercicio", formato_moneda(utilidad_neta), ""))
            # En la fila de impuestos, colocar el total del capital en col6
            agregar_fila(("", "", "", "Impuestos", formato_moneda(impuesto_calculado), formato_moneda(total_capital)),
                         'total')

        # Escenario 2: Pérdida Neta
        else:
            # Capital menos pérdida se coloca en col6 en la misma fila de la pérdida
            resultado_capital = capital_social - abs(perdida_neta)
            agregar_fila(("", "", "", "Pérdida Neta del Ejercicio", formato_moneda(abs(perdida_neta)),
                          formato_moneda(resultado_capital)), 'total')

        # Fila final de totales
        total_activos = total_activo_circulante + total_activo_no_circulante
        total_pasivo_capital = total_pasivo_corto + total_pasivo_largo + total_capital

        agregar_fila(("Total Activo", "", formato_moneda(total_activos),
                      "Pasivo + Capital", "", formato_moneda(total_pasivo_capital)), 'total_final')

    # Botones
    tk.Button(canvas, text="VOLVER AL MENU", font=("Minecraftia", 12, "bold"),
              bg="#888888", fg="white", activebackground="#2f2f2f", activeforeground="white",
              relief="raised", bd=4, width=40,
              command=lambda: Return(frame_principal, frame_menu)).place(x=ancho // 2 - 280, y=alto - 80)

    tk.Button(canvas, text="ACTUALIZAR", font=("Minecraftia", 12, "bold"),
              bg="#4472C4", fg="white", activebackground="#2f4f8f", activeforeground="white",
              relief="raised", bd=4, width=20,
              command=lambda: [obtener_datos_libro_mayor(), llenar_tabla()]).place(x=ancho // 2 + 300, y=alto - 80)

    llenar_tabla()
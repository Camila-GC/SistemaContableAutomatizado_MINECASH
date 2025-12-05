import tkinter as tk
from tkinter import ttk, font
from datetime import datetime
from LibroMayor import resumen_cuentas, cuentas_procesadas
from Ingresar import catalogo

IMPUESTO_CALCULADO = 0.0
UTILIDAD_NETA = 0.0
PERDIDA_NETA = 0.0


class EstadoResultado:
    def __init__(self, frame_menu, ventana):
        self.frame_menu = frame_menu
        self.ventana = ventana
        self.datos = self.obtener_datos_libro_mayor()
        self.crear_interfaz()

    def obtener_datos_libro_mayor(self):
        """Extrae y organiza los datos necesarios del libro mayor"""
        # LIMPIAR Y REGENERAR los datos cada vez que se abre el estado de resultado
        global resumen_cuentas, cuentas_procesadas
        resumen_cuentas.clear()
        cuentas_procesadas.clear()

        # Forzar regeneración del libro mayor
        self.regenerar_libro_mayor()

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

        # Mapeo mejorado de cuentas - nombres exactos y variaciones comunes
        mapeo_cuentas = {
            # Ventas
            'ventas': 'ventas_totales',
            'ventas totales': 'ventas_totales',
            'ingresos por ventas': 'ventas_totales',

            # Devoluciones y rebajas sobre ventas
            'devolución sobre ventas': 'devoluciones_ventas',
            'devoluciones sobre ventas': 'devoluciones_ventas',
            'devolucion sobre ventas': 'devoluciones_ventas',
            'rebajas sobre ventas': 'rebajas_ventas',
            'descuentos sobre ventas': 'rebajas_ventas',

            # Compras
            'compras': 'compras',
            'compra': 'compras',
            'compra de mercancia': 'compras',
            'compra de mercancía': 'compras',

            # Gastos de compra
            'gastos de compra': 'gastos_compras',
            'gasto de compra': 'gastos_compras',
            'gastos sobre compras': 'gastos_compras',
            'fletes sobre compras': 'gastos_compras',

            # Devoluciones y rebajas sobre compras
            'devolución sobre compras': 'devoluciones_compras',
            'devoluciones sobre compras': 'devoluciones_compras',
            'devolucion sobre compras': 'devoluciones_compras',
            'rebajas sobre compras': 'rebajas_compras',
            'descuentos sobre compras': 'rebajas_compras',

            # Inventarios - CORRECCIÓN: inventario inicial es la misma que inventario
            'inventario': 'inventario_inicial',
            'inventario inicial': 'inventario_inicial',
            'inventario final': 'inventario_final',
            'inv final': 'inventario_final',
            'inv inicial': 'inventario_inicial',

            # Gastos operativos
            'gastos de administracion': 'gastos_administracion',
            'gastos de administración': 'gastos_administracion',
            'gastos administrativos': 'gastos_administracion',
            'gasto de administracion': 'gastos_administracion',
            'gastos de venta': 'gastos_venta',
            'gasto de venta': 'gastos_venta',
            'gastos de ventas': 'gastos_venta',
            'gastos comerciales': 'gastos_venta',

            # Otros ingresos y gastos
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

        print("=== DEBUG: Contenido de resumen_cuentas ===")
        print(f"Número de cuentas en resumen: {len(resumen_cuentas)}")

        for i, cuenta in enumerate(resumen_cuentas):
            print(f"Cuenta {i + 1}: {cuenta}")

            # Extraer datos según la estructura
            if isinstance(cuenta, dict):
                cuenta_nombre = cuenta.get('cuenta', '')
                saldo_final = float(cuenta.get('saldo_final', 0))
                print(f"  -> Nombre: '{cuenta_nombre}', Saldo final: {saldo_final}")
            elif isinstance(cuenta, (list, tuple)) and len(cuenta) >= 2:
                cuenta_nombre = str(cuenta[0])
                saldo_final = float(cuenta[1])
                print(f"  -> Nombre: '{cuenta_nombre}', Saldo: {saldo_final}")
            else:
                print(f"  -> Estructura no reconocida: {type(cuenta)}")
                continue

            # Buscar coincidencia exacta primero
            cuenta_normalizada = cuenta_nombre.strip().lower()
            print(f"  -> Cuenta normalizada: '{cuenta_normalizada}'")

            encontrada = False

            # Buscar coincidencia exacta
            if cuenta_normalizada in mapeo_cuentas:
                clave = mapeo_cuentas[cuenta_normalizada]
                datos[clave] += saldo_final
                print(f"  -> ¡COINCIDENCIA EXACTA! Asignado a '{clave}': {saldo_final}")
                encontrada = True
            else:
                # Buscar coincidencia parcial
                for nombre_mapeo, clave in mapeo_cuentas.items():
                    if nombre_mapeo in cuenta_normalizada or cuenta_normalizada in nombre_mapeo:
                        datos[clave] += saldo_final
                        print(f"  -> COINCIDENCIA PARCIAL con '{nombre_mapeo}' -> '{clave}': {saldo_final}")
                        encontrada = True
                        break

            if not encontrada:
                print(f"  -> NO SE ENCONTRÓ COINCIDENCIA para '{cuenta_normalizada}'")

        print("\n=== Datos finales extraídos ===")
        for clave, valor in datos.items():
            if valor != 0:
                print(f"{clave}: {valor}")

        print("=========================================\n")
        return datos

    def regenerar_libro_mayor(self):
        """Regenera los datos del libro mayor para obtener información actualizada"""
        from Ingresar import movimientos
        from Catalogo import datos as catalogo_datos

        if not movimientos:
            return

        # Obtener todas las cuentas únicas
        cuentas = list(set(
            cuenta
            for m in movimientos
            for cuenta, debe, haber in m['datos']
        ))

        # Procesar cada cuenta
        for cuenta in cuentas:
            if cuenta not in cuentas_procesadas:
                saldo = 0.0
                total_debe = 0
                total_haber = 0

                # Calcular saldos para esta cuenta
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

                # Buscar código de cuenta en el catálogo
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

                # Agregar al resumen
                resumen_cuentas.append({
                    'codigo': codigo_cuenta,
                    'cuenta': nombre_cuenta,
                    'total_debe': total_debe,
                    'total_haber': total_haber,
                    'saldo_final': saldo_final
                })
                cuentas_procesadas.add(cuenta)

    def crear_interfaz(self):
        """Crea la interfaz gráfica mejorada del estado de resultado"""
        self.frame_menu.pack_forget()

        # Configuración de estilos
        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')

        # Colores
        self.color_fondo = "#f5f5f5"
        self.color_encabezado = "#3a7cff"
        self.color_texto_encabezado = "white"
        self.color_total = "#2e7d32"
        self.color_perdida = "#c62828"
        self.color_separador = "#e0e0e0"

        # Frame principal con mejor apariencia
        self.frame_principal = tk.Frame(self.ventana, bg=self.color_fondo)
        self.frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # Barra superior con botón de regreso
        frame_superior = tk.Frame(self.frame_principal, bg=self.color_encabezado)
        frame_superior.pack(fill="x", padx=0, pady=0)

        tk.Button(frame_superior, text="← Volver", command=self.regresar_menu,
                  font=("Minecraftia", 10, "bold"), bg=self.color_encabezado, fg="white",
                  bd=0, activebackground="#1e56d1", activeforeground="white").pack(side="left", padx=10, pady=5)

        tk.Label(frame_superior, text="ESTADO DE RESULTADOS",
                 font=("Minecraftia", 12, "bold"), bg=self.color_encabezado,
                 fg=self.color_texto_encabezado).pack(side="left", padx=10, pady=5)

        # Botón de actualizar
        tk.Button(frame_superior, text="🔄 Actualizar", command=self.actualizar_estado,
                  font=("Minecraftia", 10, "bold"), bg="#4caf50", fg="white",
                  bd=0, activebackground="#45a049", activeforeground="white").pack(side="right", padx=10, pady=5)

        # Frame para el contenido con scroll
        frame_contenedor = tk.Frame(self.frame_principal, bg=self.color_fondo)
        frame_contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(frame_contenedor, bg=self.color_fondo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=self.color_fondo)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Configurar fuente para negritas
        self.fuente_normal = font.Font(family="Minecraftia", size=10)
        self.fuente_negrita = font.Font(family="Minecraftia", size=10, weight="bold")
        self.fuente_titulo = font.Font(family="Minecraftia", size=12, weight="bold")

        # Generar el estado de resultado
        self.generar_estado()

        # Configurar evento de rueda del ratón para el scroll
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    def actualizar_estado(self):
        """Actualiza el estado de resultado con los datos más recientes"""
        # Limpiar el frame scrollable
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Obtener datos actualizados
        self.datos = self.obtener_datos_libro_mayor()

        # Regenerar el estado
        self.generar_estado()

    def crear_seccion(self, titulo):
        """Crea una sección con título"""
        frame_seccion = tk.Frame(self.scrollable_frame, bg=self.color_fondo)
        frame_seccion.pack(fill="x", padx=5, pady=5)

        tk.Label(frame_seccion, text=titulo, font=self.fuente_negrita,
                 bg=self.color_fondo, fg=self.color_encabezado).pack(anchor="w")

        return frame_seccion

    def crear_fila(self, contenedor, descripcion, monto="", calculo="", total="",
                   es_total=False, es_subtotal=False, es_perdida=False):
        """Crea una fila de datos estilizada"""
        bg_color = self.color_fondo
        fg_color = "black"

        if es_total:
            bg_color = "#e8f5e9"  # Verde claro para totales
            fg_color = self.color_total
        elif es_subtotal:
            bg_color = "#e3f2fd"  # Azul claro para subtotales
        elif es_perdida:
            fg_color = self.color_perdida

        frame_fila = tk.Frame(contenedor, bg=bg_color)
        frame_fila.pack(fill="x", padx=0, pady=1)

        # Descripción
        lbl_desc = tk.Label(frame_fila, text=descripcion, anchor="w",
                            font=self.fuente_negrita if es_total or es_subtotal else self.fuente_normal,
                            bg=bg_color, fg=fg_color)
        lbl_desc.pack(side="left", fill="x", expand=True, padx=10)

        # Monto
        lbl_monto = tk.Label(frame_fila, text=monto, anchor="e",
                             font=self.fuente_negrita if es_total else self.fuente_normal,
                             bg=bg_color, fg=fg_color)
        lbl_monto.pack(side="left", padx=10, ipadx=20)

        # Cálculo
        lbl_calculo = tk.Label(frame_fila, text=calculo, anchor="e",
                               font=self.fuente_normal, bg=bg_color, fg="gray")
        lbl_calculo.pack(side="left", padx=10, ipadx=20)

        # Total
        lbl_total = tk.Label(frame_fila, text=total, anchor="e",
                             font=self.fuente_negrita if es_total else self.fuente_normal,
                             bg=bg_color, fg=fg_color)
        lbl_total.pack(side="left", padx=10, ipadx=20)

        return frame_fila

    def generar_estado(self):
        """Genera el contenido del estado de resultado con mejor formato y lógica corregida"""
        datos = self.datos

        # Formateador de moneda
        def formato_moneda(valor):
            return f"${abs(valor):,.2f}" if valor >= 0 else f"(${abs(valor):,.2f})"

        # Encabezado
        frame_encabezado = tk.Frame(self.scrollable_frame, bg=self.color_fondo)
        frame_encabezado.pack(fill="x", pady=(0, 10))

        tk.Label(frame_encabezado, text="EMPRESA TECNM S.A. DE C.V.",
                 font=self.fuente_titulo, bg=self.color_fondo).pack()

        tk.Label(frame_encabezado, text=f"Estado de Resultados al {datetime.now().strftime('%d/%m/%Y')}",
                 font=self.fuente_negrita, bg=self.color_fondo).pack()

        # Sección de Ventas
        frame_ventas = self.crear_seccion("VENTAS")

        self.crear_fila(frame_ventas, "Ventas totales", formato_moneda(datos['ventas_totales']))
        self.crear_fila(frame_ventas, "(-) Devoluciones sobre ventas", formato_moneda(-datos['devoluciones_ventas']))
        self.crear_fila(frame_ventas, "(-) Rebajas sobre ventas", formato_moneda(-datos['rebajas_ventas']))

        ventas_netas = datos['ventas_totales'] - datos['devoluciones_ventas'] - datos['rebajas_ventas']
        self.crear_fila(frame_ventas, "Ventas netas", "",
                        f"{formato_moneda(datos['ventas_totales'])} - {formato_moneda(datos['devoluciones_ventas'])} - {formato_moneda(datos['rebajas_ventas'])}",
                        formato_moneda(ventas_netas), es_total=True)

        # Separador
        tk.Frame(self.scrollable_frame, height=2, bg=self.color_separador).pack(fill="x", pady=5)

        # Sección de Costo de Ventas
        frame_costo_ventas = self.crear_seccion("COSTO DE VENTAS")

        self.crear_fila(frame_costo_ventas, "Compras", formato_moneda(datos['compras']))
        self.crear_fila(frame_costo_ventas, "(+) Gastos de compra", formato_moneda(datos['gastos_compras']))

        compras_totales = datos['compras'] + datos['gastos_compras']
        self.crear_fila(frame_costo_ventas, "Compras totales", "",
                        f"{formato_moneda(datos['compras'])} + {formato_moneda(datos['gastos_compras'])}",
                        formato_moneda(compras_totales), es_subtotal=True)

        self.crear_fila(frame_costo_ventas, "(-) Devoluciones sobre compras",
                        formato_moneda(-datos['devoluciones_compras']))
        self.crear_fila(frame_costo_ventas, "(-) Rebajas sobre compras", formato_moneda(-datos['rebajas_compras']))

        compras_netas = compras_totales - datos['devoluciones_compras'] - datos['rebajas_compras']
        self.crear_fila(frame_costo_ventas, "Compras netas", "",
                        f"{formato_moneda(compras_totales)} - {formato_moneda(datos['devoluciones_compras'])} - {formato_moneda(datos['rebajas_compras'])}",
                        formato_moneda(compras_netas), es_subtotal=True)

        self.crear_fila(frame_costo_ventas, "(+) Inventario inicial", formato_moneda(datos['inventario_inicial']))

        mercancia_disponible = compras_netas + datos['inventario_inicial']
        self.crear_fila(frame_costo_ventas, "Mercancía disponible", "",
                        f"{formato_moneda(compras_netas)} + {formato_moneda(datos['inventario_inicial'])}",
                        formato_moneda(mercancia_disponible), es_subtotal=True)

        self.crear_fila(frame_costo_ventas, "(-) Inventario final", formato_moneda(-datos['inventario_final']))

        costo_ventas = mercancia_disponible - datos['inventario_final']
        self.crear_fila(frame_costo_ventas, "Costo de ventas", "",
                        f"{formato_moneda(mercancia_disponible)} - {formato_moneda(datos['inventario_final'])}",
                        formato_moneda(costo_ventas), es_total=True)

        # Separador
        tk.Frame(self.scrollable_frame, height=2, bg=self.color_separador).pack(fill="x", pady=5)

        # Utilidad/Pérdida bruta - CORREGIDO según las reglas
        frame_utilidad_bruta = self.crear_seccion("RESULTADO BRUTO")

        # Si ventas netas > costo de ventas: UTILIDAD BRUTA
        if ventas_netas > costo_ventas:
            utilidad_bruta = ventas_netas - costo_ventas
            self.crear_fila(frame_utilidad_bruta, "Utilidad bruta", "", "",
                            formato_moneda(utilidad_bruta), es_total=True)
            es_utilidad_bruta = True
        else:
            # Si costo de ventas > ventas netas: PÉRDIDA BRUTA
            perdida_bruta = costo_ventas - ventas_netas
            self.crear_fila(frame_utilidad_bruta, "Pérdida bruta", "", "",
                            formato_moneda(perdida_bruta), es_total=True, es_perdida=True)
            es_utilidad_bruta = False

        # Separador
        tk.Frame(self.scrollable_frame, height=2, bg=self.color_separador).pack(fill="x", pady=5)

        # Gastos de operación
        frame_gastos = self.crear_seccion("GASTOS DE OPERACIÓN")

        # Gastos de administración en tercera columna
        self.crear_fila(frame_gastos, "Gastos de administración", "",
                        formato_moneda(datos['gastos_administracion']))

        # Gastos de venta en tercera columna
        self.crear_fila(frame_gastos, "Gastos de venta", "",
                        formato_moneda(datos['gastos_venta']))

        # Total gastos de operación en cuarta columna
        gastos_operacion = datos['gastos_administracion'] + datos['gastos_venta']
        self.crear_fila(frame_gastos, "Gastos de operación", "", "",
                        formato_moneda(gastos_operacion), es_subtotal=True)

        # Separador
        tk.Frame(self.scrollable_frame, height=2, bg=self.color_separador).pack(fill="x", pady=5)

        # Utilidad/Pérdida en operación - CORREGIDO según las reglas
        frame_operacion = self.crear_seccion("RESULTADO EN OPERACIÓN")

        if es_utilidad_bruta:
            # Teníamos utilidad bruta
            if utilidad_bruta > gastos_operacion:
                # Utilidad bruta > gastos de operación: UTILIDAD EN OPERACIÓN
                utilidad_operacion = utilidad_bruta - gastos_operacion
                self.crear_fila(frame_operacion, "Utilidad en operación", "", "",
                                formato_moneda(utilidad_operacion), es_total=True)
                es_utilidad_operacion = True
            else:
                # Utilidad bruta < gastos de operación: PÉRDIDA EN OPERACIÓN
                perdida_operacion = gastos_operacion - utilidad_bruta
                self.crear_fila(frame_operacion, "Pérdida en operación", "", "",
                                formato_moneda(perdida_operacion), es_total=True, es_perdida=True)
                es_utilidad_operacion = False
        else:
            # Teníamos pérdida bruta: PÉRDIDA EN OPERACIÓN
            perdida_operacion = perdida_bruta + gastos_operacion
            self.crear_fila(frame_operacion, "Pérdida en operación", "", "",
                            formato_moneda(perdida_operacion), es_total=True, es_perdida=True)
            es_utilidad_operacion = False

        # Separador
        tk.Frame(self.scrollable_frame, height=2, bg=self.color_separador).pack(fill="x", pady=5)

        # Otros ingresos y gastos
        frame_otros = self.crear_seccion("OTROS INGRESOS Y GASTOS")

        # Otros ingresos en cuarta columna
        self.crear_fila(frame_otros, "Otros ingresos", "", "",
                        formato_moneda(datos['otros_ingresos']))

        # Otros gastos en cuarta columna
        self.crear_fila(frame_otros, "Otros gastos", "", "",
                        formato_moneda(datos['otros_gastos']))

        # Separador
        tk.Frame(self.scrollable_frame, height=2, bg=self.color_separador).pack(fill="x", pady=5)

        # Resultado final - CORREGIDO según las reglas
        frame_final = self.crear_seccion("RESULTADO FINAL")

        global IMPUESTO_CALCULADO, UTILIDAD_NETA, PERDIDA_NETA

        if not es_utilidad_operacion:
            # Teníamos pérdida en operación: PÉRDIDA NETA DEL EJERCICIO
            perdida_neta_ejercicio = perdida_operacion + datos['otros_gastos'] - datos['otros_ingresos']
            self.crear_fila(frame_final, "Pérdida neta del ejercicio", "", "",
                            formato_moneda(perdida_neta_ejercicio), es_total=True, es_perdida=True)

            IMPUESTO_CALCULADO = 0.0
            UTILIDAD_NETA = 0.0
            PERDIDA_NETA = perdida_neta_ejercicio
        else:
            # Teníamos utilidad en operación: UTILIDAD ANTES DE IMPUESTOS
            utilidad_antes_impuestos = utilidad_operacion + datos['otros_ingresos'] - datos['otros_gastos']
            self.crear_fila(frame_final, "Utilidad antes de impuestos", "", "",
                            formato_moneda(utilidad_antes_impuestos), es_total=True)

            if utilidad_antes_impuestos > 0:
                # Calcular impuestos del 25%
                impuestos = utilidad_antes_impuestos * 0.25
                self.crear_fila(frame_final, "Impuestos 25%", "", "",
                                formato_moneda(impuestos), es_subtotal=True)

                # Calcular utilidad neta del ejercicio
                utilidad_neta_ejercicio = utilidad_antes_impuestos - impuestos
                self.crear_fila(frame_final, "Utilidad neta del ejercicio", "", "",
                                formato_moneda(utilidad_neta_ejercicio), es_total=True)

                IMPUESTO_CALCULADO = impuestos
                UTILIDAD_NETA = utilidad_neta_ejercicio
                PERDIDA_NETA = 0.0
            else:
                # Si utilidad antes de impuestos es negativa o cero, no hay impuestos
                IMPUESTO_CALCULADO = 0.0
                UTILIDAD_NETA = utilidad_antes_impuestos
                PERDIDA_NETA = 0.0

    def regresar_menu(self):
        """Regresa al menú principal"""
        self.frame_principal.pack_forget()
        self.frame_menu.pack(fill="both", expand=True)


def mostrar_estado_resultado(frame_menu, ventana):
    """Función para llamar desde el menú principal"""
    app = EstadoResultado(frame_menu, ventana)
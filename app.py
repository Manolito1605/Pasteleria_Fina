import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

st.set_page_config(page_title="Pastelería Control", page_icon="🍰", layout="wide")

# =============================================================================
# --- INYECTAR CSS GLOBAL PARA ACHICAR ELEMENTOS Y FIX DE BOTONES (¡SÚPER COMPACTO! 🚀)
# =============================================================================
st.markdown("""
    <style>
        /* Le devolvemos el espacio superior al contenedor principal para que el título no se corte */
        .block-container {
            padding-top: 2.5rem !important;  
            padding-bottom: 0.5rem !important;
            margin-top: 0px !important; 
        }

        /* 🛒 NUEVO: Controlar y achicar las letras de st.title */
        h1 {
            font-size: 1.8rem !important; 
            margin-top: 5px !important;
            margin-bottom: 12px !important;
            line-height: 1.2 !important;
        }

        /* Reduce la separación vertical interna entre componentes */
        [data-testid="stVerticalBlock"] {
            gap: 0.4rem !important; 
        }
        
        /* Elimina el margen inferior por defecto de los textos */
        .stMarkdown div p {
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
        }

        /* FIX PARA TÍTULOS CORTADOS (H2) */
        h2, [data-testid="stMetricLabel"] { 
            font-size: 1.1rem !important; 
            line-height: 1.4 !important;   
            overflow: visible !important;  
            margin-top: 2px !important; 
            margin-bottom: 2px !important; 
        }
        
        /* Achicar el número o valor interno de las métricas */
        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
            font-weight: bold !important;
            margin-top: -5px !important;
        }
        
        /* FIX PARA TÍTULOS CORTADOS (H3) */
        h3 { 
            font-size: 1.1rem !important; 
            line-height: 1.4 !important;   
            overflow: visible !important;  
            margin-top: 5px !important; 
            margin-bottom: 5px !important; 
        }
        
        /* Reducir el espacio o contenedor de las tarjetas métricas */
        [data-testid="stMetric"] {
            padding: 0px !important;
            margin-bottom: -15px !important;
        }
        
        /* Reduce el espaciado interno en columnas */
        div[data-testid="column"] {
            padding: 2px 5px !important;
        }

        /* 🔵 Forzar a que los botones comunes sean AZULES */
        div.stButton > button {
            background-color: #1E3A8A !important;
            color: white !important;
            border: 1px solid #172554 !important;
            transition: background-color 0.2s ease;
        }
        div.stButton > button:hover {
            background-color: #1D4ED8 !important;
            border-color: #1D4ED8 !important;
        }
        
        /* 🟩 Forzar a que todos los botones de descarga sean VERDE EXCEL */
        div.stDownloadButton > button, 
        .stDownloadButton button, 
        button[data-testid="stBaseButton-secondary"] {
            background-color: #217346 !important;
            color: white !important;
            border: 1px solid #1e663e !important;
            transition: background-color 0.2s ease !important;
        }
        div.stDownloadButton > button:hover, 
        .stDownloadButton button:hover {
            background-color: #164f30 !important;
            border-color: #164f30 !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Función para conectar a la BD
def conectar_bd():
    return sqlite3.connect("pasteleria.db")

# --- BARRA LATERAL DE NAVEGACIÓN ---
st.sidebar.title("🍰 Menú de Control")
opcion = st.sidebar.radio("Ir a:", [
    "📋 Ver Inventario Total", 
    "🛒 Gestionar Ingredientes", 
    "🎂 Catálogo de Productos",
    "👩‍🍳 Registrar Producción",
    "💰 Registrar Ventas",
    "🛒 Registrar Compras Insumos",
    "📖 Configurar Recetas"  # 🌟 ¡Añadimos esta línea!
])

# ==========================================
# OPCIÓN 1: VISTA GENERAL DEL INVENTARIO (DISEÑO CORPORATIVO COMPACTO 🚀)
# ==========================================
if opcion == "📋 Ver Inventario Total":
    # Reemplazamos st.title por un texto H2 estilizado y compacto
    #st.markdown('## 📊 Panel de Control y Monitoreo')
    #st.markdown('<hr style="margin-top:2px; margin-bottom:10px;" />', unsafe_allow_html=True)

    # Añadimos un pequeño margen de espacio arriba del título en HTML
    st.markdown('<div style="margin-top:10px;"></div>', unsafe_allow_html=True)
    st.markdown('## 📊 Panel de Control y Monitoreo')
    st.markdown('<hr style="margin-top:2px; margin-bottom:10px;" />', unsafe_allow_html=True)
    
    conn = conectar_bd()
    
    # Calcular cuántos ingredientes están en alerta crítica
    df_alertas = pd.read_sql_query("SELECT COUNT(*) as conteo FROM ingredientes WHERE stock_actual <= stock_minimo", conn)
    conteo_alertas = int(df_alertas['conteo'].iloc[0]) # 👈 Corregido de forma segura
    
    # Renderizar métricas compactas en solo 2 columnas
    kpi1, kpi2 = st.columns(2)
    with kpi1:
        if conteo_alertas > 0:
            st.metric(label="🚨 INSUMOS EN ALERTA", value=f"{conteo_alertas} por comprar", delta="-¡Urgente!", delta_color="inverse")
        else:
            st.metric(label="🌾 ESTADO DE INSUMOS", value="✅ Todo Correcto", delta="Almacén lleno")
            
    with kpi2:
        # Contar total de productos listos en vitrina de forma segura
        df_vitrina = pd.read_sql_query("SELECT SUM(stock_actual) as total FROM productos", conn)
        valor_vitrina = df_vitrina['total'].iloc[0] # 👈 Corregido de forma segura
        total_vitrina = int(valor_vitrina) if pd.notnull(valor_vitrina) else 0
        
        st.metric(label="🧁 VITRINA DE VENTAS", value=f"✨ {total_vitrina} unidades", delta="Listo para despacho")
        
    st.markdown("---")

    # 🚨 NOTIFICACIONES EN TIEMPO REAL
    df_lista_alertas = pd.read_sql_query("SELECT nombre, stock_actual, unidad_medida, stock_minimo FROM ingredientes WHERE stock_actual <= stock_minimo", conn)
    if not df_lista_alertas.empty:
        st.error("### 🔴 ALERTA DE COMPRAS: Los siguientes insumos se están agotando:")
        for _, fila in df_lista_alertas.iterrows():
            st.warning(f"👉 **{fila['nombre']}**: Te queda solo `{fila['stock_actual']} {fila['unidad_medida']}` (Tu mínimo configurado es {fila['stock_minimo']})")
        st.markdown("---")

    # 📊 GRÁFICOS VISUALES INTERACTIVOS E ÍCONOS EN TABLAS
    st.subheader("📈 Análisis Comercial al Momento")
    col_grafico, col_tablas = st.columns(2)
    
    with col_grafico:
        st.markdown("#### **🔥 Top 5 - Más Vendidos**")
        query_top_ventas = """
            SELECT p.nombre AS Producto, SUM(sv.cantidad) AS Unidades_Vendidas
            FROM salidas_ventas sv
            JOIN productos p ON sv.producto_id = p.id
            WHERE sv.tipo_salida = 'Venta'
            GROUP BY p.nombre
            ORDER BY Unidades_Vendidas DESC
            LIMIT 5
        """
        df_top = pd.read_sql_query(query_top_ventas, conn)
        
        if not df_top.empty:
            st.bar_chart(data=df_top, x="Producto", y="Unidades_Vendidas", color="#ff4b4b", use_container_width=True)
        else:
            st.info("Aún no hay datos de ventas suficientes para proyectar el gráfico.")

    with col_tablas:
        st.markdown("#### **🍰 Stock de Vitrina Disponible**")
        
        # Agregamos íconos dinámicos en los nombres de la tabla usando SQL
        query_vitrina_iconos = """
            SELECT 
                '✨ ' || nombre AS "🧁 Producto en Exhibición", 
                stock_actual || ' unds' AS "📦 Stock Real" 
            FROM productos 
            ORDER BY stock_actual DESC
        """
        df_prod_rapido = pd.read_sql_query(query_vitrina_iconos, conn)
        
        if not df_prod_rapido.empty:
            st.dataframe(df_prod_rapido, use_container_width=True, hide_index=True)
        else:
            st.info("No hay productos en catálogo.")
            
    conn.close()

# ==========================================
# OPCIÓN 2: GESTIONAR INGREDIENTES
# ==========================================
elif opcion == "🛒 Gestionar Ingredientes":
    st.title("🛒 Gestión de Insumos y Materia Prima")
    
    # Creamos los dos tabs aquí arriba
    tab_registro, tab_catalogo = st.tabs(["➕ Registrar Insumo", "📂 Catálogo Guardado"])
    
    # --- PESTAÑA 1: REGISTRO ---
    with tab_registro:
        st.subheader("Registro de Insumos / Materia Prima")
        with st.form("form_ingrediente", clear_on_submit=True):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                nombre_insumo = st.text_input("Nombre del ingrediente", placeholder="Ej. Harina sin preparar")
            with col2:
                unidad = st.selectbox("Unidad de Medida", ["kg", "gr", "unidades", "litros"])
            with col3:
                stock_inicial = st.number_input("Stock Inicial", min_value=0.0, step=0.1)
            with col4:
                stock_min = st.number_input("Alerta Stock Mínimo", min_value=0.0, step=0.1)
                
            guardar_ing = st.form_submit_button("Guardar Ingrediente", type="primary")

        if guardar_ing:
            if nombre_insumo:
                conn = conectar_bd()
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        INSERT INTO ingredientes (nombre, unidad_medida, stock_actual, stock_minimo)
                        VALUES (?, ?, ?, ?)
                    """, (nombre_insumo, unidad, stock_inicial, stock_min))
                    conn.commit()
                    st.success(f"¡{nombre_insumo} guardado correctamente!")
                    # Forzamos el refresco para que el catálogo se actualice de inmediato al guardar
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al guardar: {e}")
                finally:
                    conn.close()
            else:
                st.warning("Por favor, escribe el nombre del ingrediente.")

    # --- PESTAÑA 2: CATÁLOGO ---
    with tab_catalogo:
        st.subheader("📋 Catálogo de Insumos en el Sistema")
        
        try:
            # Conectamos a la BD para leer los ingredientes ingresados
            conn = conectar_bd()
            
            # Usamos Pandas para leer la consulta SQL de forma limpia y directa
            df_ingredientes = pd.read_sql_query("""
                SELECT nombre AS [Nombre del Ingrediente], 
                       unidad_medida AS [Unidad de Medida], 
                       stock_actual AS [Stock Actual], 
                       stock_minimo AS [Alerta Mínima] 
                FROM ingredientes
            """, conn)
            
            conn.close()
            
            if not df_ingredientes.empty:
                # Mostramos la lista completa en un componente interactivo de Streamlit
                st.dataframe(
                    df_ingredientes,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Pequeño contador estético al final del catálogo
                st.metric("Total de insumos registrados", len(df_ingredientes))
            else:
                st.info("Aún no tienes ingredientes registrados. Usa la pestaña 'Registrar Insumo' para empezar.")
                
        except Exception as e:
            st.error(f"Error al cargar el catálogo: {e}")

# ==========================================
# OPCIÓN 3: CATÁLOGO DE PRODUCTOS
# ==========================================
elif opcion == "🎂 Catálogo de Productos":
    st.title("🎂 Gestión de Catálogo de Productos")
    
    tab_registro, tab_catalogo = st.tabs(["🆕 Registrar Nuevo Producto", "📋 Catálogo Guardado"])

    with tab_registro:
        st.subheader("Añade un producto final al menú")
        with st.form("form_producto", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                nombre_producto = st.text_input("Nombre del Producto", placeholder="Ej. Torta de Chocolate Familiar")
                precio_venta = st.number_input("Precio de Venta ($ / S/.)", min_value=0.0, step=0.5)
            with col2:
                descripcion = st.text_area("Descripción o detalles del producto", placeholder="Ej. Bizcocho húmedo con fudge artesanal")
                stock_inicial_prod = st.number_input("Stock Inicial Disponible (Pasteles ya listos)", min_value=0, step=1)
                
            guardar_prod = st.form_submit_button("Añadir al Catálogo", type="primary")

        if guardar_prod:
            if nombre_producto:
                conn = conectar_bd()
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        INSERT INTO productos (nombre, descripcion, precio_venta, stock_actual)
                        VALUES (?, ?, ?, ?)
                    """, (nombre_producto, descripcion, precio_venta, stock_inicial_prod))
                    conn.commit()
                    st.success(f"¡{nombre_producto} ha sido añadido con éxito al catálogo!")
                except Exception as e:
                    st.error(f"Error al guardar producto: {e}")
                finally:
                    conn.close()
            else:
                st.warning("Por favor, introduce el nombre del producto.")

    with tab_catalogo:
        st.subheader("Productos registrados actualmente")
        conn = conectar_bd()
        df_productos = pd.read_sql_query("SELECT id, nombre, descripcion, precio_venta, stock_actual FROM productos", conn)
        conn.close()

        if not df_productos.empty:
            st.dataframe(df_productos, use_container_width=True)
        else:
            st.info("Aún no tienes productos registrados en tu catálogo.")

# ==========================================
# OPCIÓN 4: REGISTRAR PRODUCCIÓN (¡AHORA CON TABS!)
# ==========================================
elif opcion == "👩‍🍳 Registrar Producción":
    st.title("👩‍🍳 Orden de Producción / Horneado")

    tab_nuevo_horneado, tab_historial_horneado = st.tabs(["⚡ Registrar Nuevo Horneado", "📜 Historial de Producción"])

    conn = conectar_bd()
    df_prod_existentes = pd.read_sql_query("SELECT id, nombre FROM productos", conn)
    conn.close()

    with tab_nuevo_horneado:
        if df_prod_existentes.empty:
            st.warning("⚠️ Primero debes agregar productos en el 'Catálogo de Productos' para poder producir algo.")
        else:
            dict_productos = dict(zip(df_prod_existentes['nombre'], df_prod_existentes['id']))
            
            with st.form("form_produccion", clear_on_submit=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    producto_seleccionado = st.selectbox("¿Qué producto cocinaste?", list(dict_productos.keys()))
                with col2:
                    cantidad_cocinada = st.number_input("¿Cuántas unidades preparaste?", min_value=1, step=1)
                with col3:
                    fecha_produccion = st.date_input("Fecha de preparación", date.today())
                    
                enviar_produccion = st.form_submit_button("Finalizar Horneado (Sumar al Stock)", type="primary")

        if enviar_produccion:
            id_producto = dict_productos[producto_seleccionado]
            
            conn = conectar_bd()
            cursor = conn.cursor()
            try:
                # 1. Buscar si este producto tiene ingredientes registrados en su receta
                receta_insumos = cursor.execute("""
                    SELECT ingrediente_id, cantidad_necesaria 
                    FROM recetas WHERE producto_id = ?
                """, (id_producto,)).fetchall()
                
                # 2. VALIDACIÓN: Verificar si nos alcanza la materia prima antes de cocinar
                alcanza_materia_prima = True
                insumos_insuficientes = []
                
                for ing_id, cant_base in receta_insumos:
                    cant_total_requerida = cant_base * cantidad_cocinada
                    # Consultamos el stock actual del ingrediente
                    stock_actual_ing = cursor.execute("SELECT stock_actual, nombre FROM ingredientes WHERE id = ?", (ing_id,)).fetchone()
                    
                    if stock_actual_ing[0] < cant_total_requerida:
                        alcanza_materia_prima = False
                        insumos_insuficientes.append(stock_actual_ing[1])
                
                if not alcanza_materia_prima:
                    st.error(f"❌ ¡No puedes hornear! Falta stock en el almacén de: {', '.join(insumos_insuficientes)}")
                else:
                    # 3. SI ALCANZA: Descontamos los insumos de la alacena automáticamente 🔮
                    for ing_id, cant_base in receta_insumos:
                        cant_total_requerida = cant_base * cantidad_cocinada
                        cursor.execute("""
                            UPDATE ingredientes 
                            SET stock_actual = stock_actual - ? 
                            WHERE id = ?
                        """, (cant_total_requerida, ing_id))
                    
                    # 4. Insertamos el registro en el historial de producción
                    cursor.execute("""
                        INSERT INTO produccion (producto_id, cantidad_producida, fecha, estado)
                        VALUES (?, ?, ?, 'Terminado')
                    """, (id_producto, cantidad_cocinada, fecha_produccion))
                    
                    # 5. Sumamos las unidades al catálogo de productos listos
                    cursor.execute("UPDATE productos SET stock_actual = stock_actual + ? WHERE id = ?", (cantidad_cocinada, id_producto))
                    
                    conn.commit()
                    st.success(f"👩‍🍳 ¡Horneado exitoso! Se sumaron {cantidad_cocinada} unidades a '{producto_seleccionado}' y se redujeron los ingredientes correspondientes del almacén.")
            except Exception as e:
                st.error(f"Error en el proceso de producción: {e}")
            finally:
                conn.close()

    with tab_historial_horneado:
        st.subheader("Horneados registrados anteriormente")
        conn = conectar_bd()
        query_historial = """
            SELECT pr.id, p.nombre AS Producto, pr.cantidad_producida AS Cantidad, pr.fecha AS Fecha, pr.estado AS Estado
            FROM produccion pr
            JOIN productos p ON pr.producto_id = p.id
            ORDER BY pr.id DESC
        """
        df_historial = pd.read_sql_query(query_historial, conn)
        conn.close()

        if not df_historial.empty:
            st.dataframe(df_historial, use_container_width=True)
        else:
            st.info("Aún no hay registros de horneados anteriores.")

# ==========================================
# OPCIÓN 5: REGISTRAR VENTAS (¡NUEVO MÓDULO!)
# ==========================================
elif opcion == "💰 Registrar Ventas":
    st.title("💰 Punto de Venta y Salidas")
    
    tab_vender, tab_historial_ventas = st.tabs(["💵 Registrar Nueva Venta", "📈 Historial de Ventas e Ingresos"])
    
    conn = conectar_bd()
    # Traemos productos y también su stock e información de precio para validar en la venta
    df_prod_ventas = pd.read_sql_query("SELECT id, nombre, precio_venta, stock_actual FROM productos", conn)
    conn.close()
    
    with tab_vender:
        if df_prod_ventas.empty:
            st.warning("⚠️ No tienes productos en el catálogo para vender.")
        else:
            # Diccionarios útiles para saber precios y stocks al instante
            dict_prod_id = dict(zip(df_prod_ventas['nombre'], df_prod_ventas['id']))
            dict_prod_precio = dict(zip(df_prod_ventas['nombre'], df_prod_ventas['precio_venta']))
            dict_prod_stock = dict(zip(df_prod_ventas['nombre'], df_prod_ventas['stock_actual']))
            
            with st.form("form_ventas", clear_on_submit=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    prod_vender = st.selectbox("Selecciona el producto vendido", list(dict_prod_id.keys()))
                with col2:
                    # Ponemos un indicador dinámico de cuánto stock queda disponible
                    stock_disp = dict_prod_stock[prod_vender]
                    st.write(f"📦 *Stock disponible actual: {stock_disp} unidades*")
                    cantidad_vender = st.number_input("Cantidad", min_value=1, step=1)
                with col3:
                    tipo_salida = st.selectbox("Tipo de Movimiento", ["Venta", "Merma/Desperdicio"])
            
                enviar_venta = st.form_submit_button("Registrar Transacción", type="primary")
                
            if enviar_venta:
                id_prod = dict_prod_id[prod_vender]
                precio_u = dict_prod_precio[prod_vender]
                stock_actual_real = dict_prod_stock[prod_vender]
                
                # Calculamos el ingreso (si es merma, el ingreso es 0)
                total_calculado = (precio_u * cantidad_vender) if tipo_salida == "Venta" else 0.0
                
                if cantidad_vender > stock_actual_real:
                    st.error(f"❌ ¡No puedes vender más de lo que tienes! Solo te quedan {stock_actual_real} unidades de '{prod_vender}'.")
                else:
                    conn = conectar_bd()
                    cursor = conn.cursor()
                    try:
                        # 1. Insertar la salida
                        cursor.execute("""
                            INSERT INTO salidas_ventas (producto_id, cantidad, tipo_salida, total_ingreso)
                            VALUES (?, ?, ?, ?)
                        """, (id_prod, cantidad_vender, tipo_salida, total_calculado))
                        
                        # 2. Restar del stock del producto
                        cursor.execute("""
                            UPDATE productos 
                            SET stock_actual = stock_actual - ? 
                            WHERE id = ?
                        """, (cantidad_vender, id_prod))
                        
                        conn.commit()
                        if tipo_salida == "Venta":
                            st.success(f"💰 ¡Venta registrada! {cantidad_vender}x '{prod_vender}' por un total de {total_calculado:.2f}")
                        else:
                            st.warning(f"⚠️ Se registraron {cantidad_vender} unidades como merma/desperdicio de '{prod_vender}'.")
                    except Exception as e:
                        st.error(f"Error al procesar la venta: {e}")
                    finally:
                        conn.close()
                        
    with tab_historial_ventas:
        st.subheader("Registro histórico de ingresos")
        conn = conectar_bd()
        query_ventas = """
            SELECT sv.id, p.nombre AS Producto, sv.cantidad AS Cantidad, sv.tipo_salida AS Tipo, sv.total_ingreso AS 'Total Ingreso', sv.fecha AS Fecha
            FROM salidas_ventas sv
            JOIN productos p ON sv.producto_id = p.id
            ORDER BY sv.id DESC
        """
        df_ventas = pd.read_sql_query(query_ventas, conn)
        
        if not df_ventas.empty:
            # Calculamos rápido el dinero total ganado
            total_ganado = df_ventas['Total Ingreso'].sum()
            st.metric(label="💰 Total de Ingresos Acumulados", value=f"${total_ganado:.2f}")
            
            st.dataframe(df_ventas, use_container_width=True)
        else:
            st.info("Aún no se han registrado ventas.")

# ==========================================
# OPCIÓN 6: REGISTRAR COMPRAS DE INSUMOS (¡NUEVO MÓDULO!)
# ==========================================
elif opcion == "🛒 Registrar Compras Insumos":
    st.title("🛒 Abastecimiento de Materia Prima")
    st.subheader("Registra tus compras del mercado para aumentar el inventario de insumos")

    tab_comprar, tab_historial_compras = st.tabs(["📦 Registrar Nueva Compra", "📜 Historial de Gastos en Insumos"])

    # Jalamos los ingredientes existentes para el buscador desplegable
    conn = conectar_bd()
    df_ing_existentes = pd.read_sql_query("SELECT id, nombre, unidad_medida FROM ingredientes", conn)
    conn.close()

    with tab_comprar:
        if df_ing_existentes.empty:
            st.warning("⚠️ Primero debes registrar los nombres de tus ingredientes en '🛒 Gestionar Ingredientes'.")
        else:
            # Diccionarios para enlazar nombres con IDs y Unidades de medida
            dict_ing_id = dict(zip(df_ing_existentes['nombre'], df_ing_existentes['id']))
            dict_ing_unidad = dict(zip(df_ing_existentes['nombre'], df_ing_existentes['unidad_medida']))
            
            with st.form("form_compras_insumos", clear_on_submit=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    ingrediente_elegido = st.selectbox("¿Qué insumo compraste?", list(dict_ing_id.keys()))
                with col2:
                    unidad_medida_actual = dict_ing_unidad[ingrediente_elegido]
                    cantidad_comprada = st.number_input(f"Cantidad comprada ({unidad_medida_actual})", min_value=0.1, step=0.1)
                with col3:
                    costo_total_compra = st.number_input("Costo Total de esta compra ($ / S/.)", min_value=0.0, step=0.5)
                    
                enviar_compra_insumo = st.form_submit_button("Registrar Compra (Sumar al Inventario)", type="primary")

            if enviar_compra_insumo:
                id_ingrediente = dict_ing_id[ingrediente_elegido]
                
                conn = conectar_bd()
                cursor = conn.cursor()
                try:
                    # 1. Insertamos el registro en la tabla de entradas_insumos
                    cursor.execute("""
                        INSERT INTO entradas_insumos (ingrediente_id, cantidad, costo_total)
                        VALUES (?, ?, ?)
                    """, (id_ingrediente, cantidad_comprada, costo_total_compra))
                    
                    # 2. ACTUALIZAMOS EL STOCK sumando lo nuevo al ingrediente correspondiente
                    cursor.execute("""
                        UPDATE ingredientes 
                        SET stock_actual = stock_actual + ? 
                        WHERE id = ?
                    """, (cantidad_comprada, id_ingrediente))
                    
                    conn.commit()
                    st.success(f"📦 ¡Inventario actualizado! Se sumaron {cantidad_comprada} {unidad_medida_actual} a '{ingrediente_elegido}'.")
                except Exception as e:
                    st.error(f"Error al registrar la compra: {e}")
                finally:
                    conn.close()

    with tab_historial_compras:
        st.subheader("Historial de dinero invertido en materia prima")
        conn = conectar_bd()
        # Hacemos un JOIN para ver los nombres de los ingredientes en vez de IDs numéricos
        query_entradas = """
            SELECT ei.id, i.nombre AS Insumo, ei.cantidad AS Cantidad, i.unidad_medida AS Unidad, ei.costo_total AS 'Costo Total', ei.fecha AS Fecha
            FROM entradas_insumos ei
            JOIN ingredientes i ON ei.ingrediente_id = i.id
            ORDER BY ei.id DESC
        """
        df_entradas = pd.read_sql_query(query_entradas, conn)
        
        if not df_entradas.empty:
            # Mostramos de forma discreta (dentro de esta pestaña protegida) el total gastado en insumos
            total_gastado_insumos = df_entradas['Costo Total'].sum()
            st.metric(label="📉 Total Invertido en Materia Prima", value=f"${total_gastado_insumos:,.2f}")
            
            st.dataframe(df_entradas, use_container_width=True, hide_index=True)
        else:
            st.info("Aún no has registrado ninguna compra de insumos.")
        conn.close()
# ==========================================
# OPCIÓN 7: CONFIGURAR RECETAS (¡NUEVO!)
# ==========================================
elif opcion == "📖 Configurar Recetas":
    st.markdown('## 📖 Configuración de Recetas de Producción')
    st.markdown('<hr style="margin-top:2px; margin-bottom:10px;" />', unsafe_allow_html=True)
    
    tab_crear_receta, tab_ver_recetas = st.tabs(["✨ Enlazar Ingrediente", "📋 Ver Fichas Técnicas"])
    
    conn = conectar_bd()
    df_prod = pd.read_sql_query("SELECT id, nombre FROM productos", conn)
    df_ing = pd.read_sql_query("SELECT id, nombre, unidad_medida FROM ingredientes", conn)
    conn.close()
    
    with tab_crear_receta:
        if df_prod.empty or df_ing.empty:
            st.warning("⚠️ Necesitas tener al menos un producto en tu catálogo y un ingrediente registrado para armar recetas.")
        else:
            dict_prod = dict(zip(df_prod['nombre'], df_prod['id']))
            dict_ing_id = dict(zip(df_ing['nombre'], df_ing['id']))
            dict_ing_uni = dict(zip(df_ing['nombre'], df_ing['unidad_medida']))
            
            with st.form("form_armar_receta", clear_on_submit=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    prod_sel = st.selectbox("Para el producto:", list(dict_prod.keys()))
                with col2:
                    ing_sel = st.selectbox("Usa el ingrediente:", list(dict_ing_id.keys()))
                with col3:
                    uni_actual = dict_ing_uni[ing_sel]
                    cant_nec = st.number_input(f"Cantidad para UN solo pastel ({uni_actual})", min_value=0.001, step=0.01, format="%.3f")
                    
                guardar_enlace = st.form_submit_button("Vincular Insumo a la Receta", type="primary")
                
            if guardar_enlace:
                conn = conectar_bd()
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        INSERT INTO recetas (producto_id, ingrediente_id, cantidad_necesaria)
                        VALUES (?, ?, ?)
                    """, (dict_prod[prod_sel], dict_ing_id[ing_sel], cant_nec))
                    conn.commit()
                    st.success(f"👍 ¡Añadido! Ahora 1 unidad de '{prod_sel}' descontará {cant_nec} {uni_actual} de '{ing_sel}'.")
                except Exception as e:
                    st.error(f"Error al guardar receta: {e}")
                finally:
                    conn.close()
                    
    with tab_ver_recetas:
        conn = conectar_bd()
        query_recetas = """
            SELECT p.nombre AS "🎂 Producto", i.nombre AS "🌾 Insumo Necesario", r.cantidad_necesaria || ' ' || i.unidad_medida AS "📦 Cantidad x Unidad"
            FROM recetas r
            JOIN productos p ON r.producto_id = p.id
            JOIN ingredientes i ON r.ingrediente_id = i.id
            ORDER BY p.nombre
        """
        df_recetas_completas = pd.read_sql_query(query_recetas, conn)
        conn.close()
        
        if not df_recetas_completas.empty:
            st.dataframe(df_recetas_completas, use_container_width=True, hide_index=True)
        else:
            st.info("Aún no has enlazado ingredientes a ningún producto.")

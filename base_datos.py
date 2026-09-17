import sqlite3

def inicializar_bd():
    conexion = sqlite3.connect("pasteleria.db")
    cursor = conexion.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # (Las tablas 1, 2, 3, 4 y 5 se quedan exactamente igual...)
    cursor.execute("CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, descripcion TEXT, precio_venta REAL NOT NULL, stock_actual INTEGER DEFAULT 0);")
    cursor.execute("CREATE TABLE IF NOT EXISTS ingredientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, unidad_medida TEXT NOT NULL, stock_actual REAL DEFAULT 0.0, stock_minimo REAL DEFAULT 0.0);")
    cursor.execute("CREATE TABLE IF NOT EXISTS entradas_insumos (id INTEGER PRIMARY KEY AUTOINCREMENT, ingrediente_id INTEGER, cantidad REAL NOT NULL, costo_total REAL NOT NULL, fecha DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id));")
    cursor.execute("CREATE TABLE IF NOT EXISTS produccion (id INTEGER PRIMARY KEY AUTOINCREMENT, producto_id INTEGER, cantidad_producida INTEGER NOT NULL, fecha DATE DEFAULT CURRENT_DATE, estado TEXT DEFAULT 'Terminado', FOREIGN KEY (producto_id) REFERENCES productos(id));")
    cursor.execute("CREATE TABLE IF NOT EXISTS salidas_ventas (id INTEGER PRIMARY KEY AUTOINCREMENT, producto_id INTEGER, cantidad INTEGER NOT NULL, tipo_salida TEXT NOT NULL, total_ingreso REAL DEFAULT 0.0, fecha DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (producto_id) REFERENCES productos(id));")

    # 🌟 NUEVA TABLA: RECENTAS (Conecta Producto con Ingrediente)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recetas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER,
        ingrediente_id INTEGER,
        cantidad_necesaria REAL NOT NULL, -- Cuánto usa para 1 Sola Unidad del producto
        FOREIGN KEY (producto_id) REFERENCES productos(id),
        FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id)
    );
    """)

    conexion.commit()
    conexion.close()
    print("¡Base de datos actualizada con la tabla de recetas!")

if __name__ == "__main__":
    inicializar_bd()
    

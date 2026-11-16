"""Tablas adicionales. Ejecutar después de crear_tablas()."""
from conexion import obtener_conexion


def crear_tablas_extra():
    with obtener_conexion() as conexion:
        conexion.executescript("""
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT NOT NULL DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS proveedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT NOT NULL DEFAULT '',
                email TEXT NOT NULL DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS producto_categoria (
                producto_id INTEGER NOT NULL,
                categoria_id INTEGER NOT NULL,
                PRIMARY KEY (producto_id, categoria_id),
                FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS producto_proveedor (
                producto_id INTEGER NOT NULL,
                proveedor_id INTEGER NOT NULL,
                PRIMARY KEY (producto_id, proveedor_id),
                FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
                FOREIGN KEY (proveedor_id) REFERENCES proveedores(id) ON DELETE CASCADE
            );
        """)

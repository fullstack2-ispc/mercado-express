from conexion import obtener_conexion
from modelos.producto import Producto


class ProductoDAO:
    def agregar(self, producto: Producto) -> int:
        with obtener_conexion() as conexion:
            cursor = conexion.execute(
                "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                (producto.nombre, producto.precio, producto.stock),
            )
            return cursor.lastrowid

    def listar(self) -> list[Producto]:
        with obtener_conexion() as conexion:
            filas = conexion.execute(
                "SELECT id, nombre, precio, stock FROM productos ORDER BY id"
            ).fetchall()
        return [Producto(f["nombre"], f["precio"], f["stock"], f["id"]) for f in filas]

    def buscar_por_id(self, producto_id: int) -> Producto | None:
        with obtener_conexion() as conexion:
            fila = conexion.execute(
                "SELECT id, nombre, precio, stock FROM productos WHERE id = ?",
                (producto_id,),
            ).fetchone()
        if fila is None:
            return None
        return Producto(fila["nombre"], fila["precio"], fila["stock"], fila["id"])

    def actualizar_precio(self, producto_id: int, nuevo_precio: float) -> bool:
        with obtener_conexion() as conexion:
            cursor = conexion.execute(
                "UPDATE productos SET precio = ? WHERE id = ?",
                (nuevo_precio, producto_id),
            )
            return cursor.rowcount > 0

    def eliminar(self, producto_id: int) -> bool:
        with obtener_conexion() as conexion:
            cursor = conexion.execute(
                "DELETE FROM productos WHERE id = ?", (producto_id,)
            )
            return cursor.rowcount > 0

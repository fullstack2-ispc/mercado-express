from conexion import obtener_conexion


class VentaDAO:
    def registrar(self, producto_id: int, cantidad: int) -> float:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")

        with obtener_conexion() as conexion:
            fila = conexion.execute(
                "SELECT precio, stock FROM productos WHERE id = ?", (producto_id,)
            ).fetchone()
            if fila is None:
                raise ValueError("El producto no existe")
            if fila["stock"] < cantidad:
                raise ValueError("Stock insuficiente")

            total = round(fila["precio"] * cantidad, 2)
            conexion.execute(
                "UPDATE productos SET stock = stock - ? WHERE id = ?",
                (cantidad, producto_id),
            )
            conexion.execute(
                "INSERT INTO ventas (producto_id, cantidad, total) VALUES (?, ?, ?)",
                (producto_id, cantidad, total),
            )
            return total

    def listar(self):
        with obtener_conexion() as conexion:
            return conexion.execute("""
                SELECT v.id, p.nombre AS producto, v.cantidad, v.total, v.fecha
                FROM ventas AS v
                INNER JOIN productos AS p ON p.id = v.producto_id
                ORDER BY v.id DESC
            """).fetchall()

from conexion import obtener_conexion


class ReporteDAO:
    def ventas_por_producto(self):
        with obtener_conexion() as conexion:
            return conexion.execute("""
                SELECT p.nombre AS producto,
                       COUNT(v.id) AS operaciones,
                       SUM(v.cantidad) AS unidades,
                       ROUND(SUM(v.total), 2) AS facturacion
                FROM productos AS p
                INNER JOIN ventas AS v ON v.producto_id = p.id
                GROUP BY p.id, p.nombre
                HAVING SUM(v.cantidad) > 0
                ORDER BY facturacion DESC
            """).fetchall()

    def productos_sobre_promedio(self):
        with obtener_conexion() as conexion:
            return conexion.execute("""
                SELECT p.id, p.nombre, p.precio
                FROM productos AS p
                WHERE p.precio > (
                    SELECT AVG(p2.precio) FROM productos AS p2
                )
                ORDER BY p.precio DESC
            """).fetchall()

    def productos_nunca_vendidos(self):
        with obtener_conexion() as conexion:
            return conexion.execute("""
                SELECT p.id, p.nombre, p.stock
                FROM productos AS p
                WHERE NOT EXISTS (
                    SELECT 1 FROM ventas AS v
                    WHERE v.producto_id = p.id
                )
                ORDER BY p.nombre
            """).fetchall()

    def ventas_superiores_al_promedio(self):
        with obtener_conexion() as conexion:
            return conexion.execute("""
                SELECT v.id AS venta_id, p.nombre AS producto,
                       v.total AS importe, v.fecha
                FROM ventas AS v
                INNER JOIN productos AS p ON p.id = v.producto_id
                WHERE v.total > (SELECT AVG(total) FROM ventas)
                ORDER BY importe DESC
            """).fetchall()

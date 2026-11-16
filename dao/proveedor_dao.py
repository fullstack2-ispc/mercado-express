from conexion import obtener_conexion
from modelos.proveedor import Proveedor


class ProveedorDAO:
    def agregar(self, proveedor: Proveedor) -> int:
        with obtener_conexion() as conexion:
            cursor = conexion.execute("""
                INSERT INTO proveedores (nombre, telefono, email)
                VALUES (?, ?, ?)
            """, (proveedor.nombre, proveedor.telefono, proveedor.email))
            return cursor.lastrowid

    def listar(self) -> list[Proveedor]:
        with obtener_conexion() as conexion:
            filas = conexion.execute("""
                SELECT id, nombre, telefono, email
                FROM proveedores ORDER BY nombre
            """).fetchall()
        return [Proveedor(f["nombre"], f["telefono"], f["email"], f["id"]) for f in filas]

    def asignar_producto(self, proveedor_id: int, producto_id: int) -> None:
        with obtener_conexion() as conexion:
            conexion.execute("""
                INSERT INTO producto_proveedor (producto_id, proveedor_id)
                VALUES (?, ?)
            """, (producto_id, proveedor_id))

    def catalogo_por_proveedor(self):
        """INNER JOIN a través de una tabla intermedia."""
        with obtener_conexion() as conexion:
            return conexion.execute("""
                SELECT pr.nombre AS proveedor, p.nombre AS producto, p.stock
                FROM proveedores AS pr
                INNER JOIN producto_proveedor AS pp ON pp.proveedor_id = pr.id
                INNER JOIN productos AS p ON p.id = pp.producto_id
                ORDER BY pr.nombre, p.nombre
            """).fetchall()

    def proveedores_con_mas_productos_que_promedio(self):
        """Subconsulta derivada con AVG, COUNT, GROUP BY y HAVING."""
        with obtener_conexion() as conexion:
            return conexion.execute("""
                SELECT pr.nombre AS proveedor, COUNT(pp.producto_id) AS cantidad
                FROM proveedores AS pr
                LEFT JOIN producto_proveedor AS pp ON pp.proveedor_id = pr.id
                GROUP BY pr.id, pr.nombre
                HAVING COUNT(pp.producto_id) > (
                    SELECT AVG(conteo.cantidad)
                    FROM (
                        SELECT COUNT(pp2.producto_id) AS cantidad
                        FROM proveedores AS pr2
                        LEFT JOIN producto_proveedor AS pp2
                            ON pp2.proveedor_id = pr2.id
                        GROUP BY pr2.id
                    ) AS conteo
                )
                ORDER BY cantidad DESC
            """).fetchall()

    def proveedores_sin_productos(self):
        """NOT EXISTS con subconsulta correlacionada."""
        with obtener_conexion() as conexion:
            return conexion.execute("""
                SELECT pr.id, pr.nombre
                FROM proveedores AS pr
                WHERE NOT EXISTS (
                    SELECT 1 FROM producto_proveedor AS pp
                    WHERE pp.proveedor_id = pr.id
                )
            """).fetchall()

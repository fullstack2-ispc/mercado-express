from conexion import obtener_conexion
from modelos.categoria import Categoria


class CategoriaDAO:
    def agregar(self, categoria: Categoria) -> int:
        with obtener_conexion() as conexion:
            cursor = conexion.execute(
                "INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)",
                (categoria.nombre, categoria.descripcion),
            )
            return cursor.lastrowid

    def listar(self) -> list[Categoria]:
        with obtener_conexion() as conexion:
            filas = conexion.execute("""
                SELECT id, nombre, descripcion
                FROM categorias ORDER BY nombre
            """).fetchall()
        return [Categoria(f["nombre"], f["descripcion"], f["id"]) for f in filas]

    def asignar_producto(self, categoria_id: int, producto_id: int) -> None:
        with obtener_conexion() as conexion:
            conexion.execute("""
                INSERT INTO producto_categoria (producto_id, categoria_id)
                VALUES (?, ?)
            """, (producto_id, categoria_id))

    def productos_por_categoria(self):
        """INNER JOIN, alias y agrupamiento."""
        with obtener_conexion() as conexion:
            return conexion.execute("""
                SELECT c.nombre AS categoria, p.nombre AS producto, p.precio
                FROM categorias AS c
                INNER JOIN producto_categoria AS pc ON pc.categoria_id = c.id
                INNER JOIN productos AS p ON p.id = pc.producto_id
                ORDER BY c.nombre, p.nombre
            """).fetchall()

    def categorias_con_varios_productos(self, minimo: int = 2):
        """GROUP BY, HAVING, COUNT y LEFT JOIN."""
        with obtener_conexion() as conexion:
            return conexion.execute("""
                SELECT c.nombre AS categoria, COUNT(pc.producto_id) AS cantidad
                FROM categorias AS c
                LEFT JOIN producto_categoria AS pc ON pc.categoria_id = c.id
                GROUP BY c.id, c.nombre
                HAVING COUNT(pc.producto_id) >= ?
                ORDER BY cantidad DESC
            """, (minimo,)).fetchall()

    def categorias_sin_productos(self):
        """Subconsulta correlacionada con NOT EXISTS."""
        with obtener_conexion() as conexion:
            return conexion.execute("""
                SELECT c.id, c.nombre
                FROM categorias AS c
                WHERE NOT EXISTS (
                    SELECT 1 FROM producto_categoria AS pc
                    WHERE pc.categoria_id = c.id
                )
            """).fetchall()

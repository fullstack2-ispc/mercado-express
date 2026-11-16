# Mercado Express — Proyecto integrador

Aplicación de escritorio con **Python 3.10+**, **SQLite3**, **Tkinter**, **CustomTkinter** y patrón **DAO**.

## Instalación y ejecución

1. Abrir una terminal en la carpeta `mercado_express`.
2. (Opcional) Crear un entorno virtual: `python -m venv .venv` y activarlo.
3. Instalar dependencia: `python -m pip install -r requirements.txt`.
4. Ejecutar: `python main.py`.

Tkinter y sqlite3 forman parte de la biblioteca estándar de Python (en instalaciones que incluyen Tcl/Tk). `customtkinter` se instala con pip. Se requiere un entorno gráfico para abrir la ventana.

La base `mercado_express.db` se crea automáticamente en la carpeta del proyecto. No se incluye en el ZIP.

## Arquitectura

- `main.py`: inicia la aplicación.
- `conexion.py`: conexión SQLite, activación de claves foráneas y DDL `CREATE TABLE`.
- `modelos/producto.py`: clase `Producto` con `@dataclass`.
- `dao/producto_dao.py`: `INSERT`, `SELECT`, `UPDATE`, `DELETE`.
- `dao/venta_dao.py`: venta transaccional, descuento de stock y `INNER JOIN` con alias.
- `dao/reporte_dao.py`: `INNER JOIN`, alias, `COUNT`, `SUM`, `GROUP BY`, `HAVING`, `AVG`, subconsultas y `NOT EXISTS`.
- `gui/app.py`: formularios y pestañas con CustomTkinter; tablas `ttk.Treeview` y cuadros `messagebox` de Tkinter.

## Flujo de prueba

1. Agregar tres productos con precios y stocks distintos.
2. Registrar dos ventas de productos diferentes.
3. Abrir **Reportes SQL** y ejecutar cada consulta.
4. Intentar vender más unidades que las disponibles y verificar que no se registra la venta.
5. Intentar eliminar un producto que tenga ventas: SQLite lo impide por integridad referencial.

## Preguntas para examen

### Bases de Datos

1. ¿Qué diferencia hay entre DDL y DML? Identificar ejemplos en el proyecto.
2. ¿Qué hacen `PRIMARY KEY`, `FOREIGN KEY` y `CHECK`?
3. ¿Qué condición une `ventas` y `productos` en el `INNER JOIN`?
4. ¿Para qué sirven los alias `p`, `v` y `AS facturacion`?
5. ¿Por qué `HAVING` filtra grupos y `WHERE` filtra filas?
6. ¿Qué devuelve la subconsulta `SELECT AVG(...)`?
7. ¿Qué significa `NOT EXISTS` y por qué la subconsulta es correlacionada?
8. ¿Por qué se utilizan `?` y parámetros en lugar de concatenar cadenas SQL?
9. ¿Qué pasa si falla el `INSERT` de una venta luego del `UPDATE` de stock?
10. ¿Por qué se habilita `PRAGMA foreign_keys = ON` por conexión?

### Programación I

1. ¿Cuál es el punto de entrada de la aplicación y qué hace `if __name__ == "__main__"`?
2. ¿Qué es una clase? Identificar atributos y métodos en `Producto` y `ProductoDAO`.
3. ¿Qué hace `@dataclass`?
4. ¿Cómo se conectan los eventos de botones con funciones mediante `command`?
5. ¿Qué diferencia hay entre `int`, `float` y `str`? ¿Dónde se convierten?
6. ¿Cómo se manejan las excepciones? ¿Qué errores captura la interfaz?
7. ¿Qué hace la comprensión de listas en `ProductoDAO.listar()`?
8. ¿Por qué se separa la interfaz gráfica de la capa de persistencia?

## Alcance didáctico

Proyecto sencillo, no sistema de facturación de producción. Se utilizan `REAL` para precios por simplicidad; para dinero real se recomienda guardar centavos como enteros o usar una estrategia decimal consistente. La eliminación de productos con ventas está restringida por la clave foránea. Cada registro de venta corresponde a un solo producto.

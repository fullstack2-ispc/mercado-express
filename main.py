"""Punto de entrada: inicia SQLite y la interfaz gráfica."""
from conexion import crear_tablas
from conexion import crear_tablas
from gui.app import MercadoExpressApp
from dao.esquema_extra import crear_tablas_extra


def main():
    crear_tablas()
    crear_tablas_extra()
    app = MercadoExpressApp()
    app.mainloop()


if __name__ == "__main__":
    main()

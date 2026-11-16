"""Punto de entrada: inicia SQLite y la interfaz gráfica."""
from conexion import crear_tablas
from gui.app import MercadoExpressApp


def main():
    crear_tablas()
    app = MercadoExpressApp()
    app.mainloop()


if __name__ == "__main__":
    main()

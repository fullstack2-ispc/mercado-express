import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk

from dao.producto_dao import ProductoDAO
from dao.venta_dao import VentaDAO
from dao.reporte_dao import ReporteDAO
from dao.categoria_dao import CategoriaDAO
from dao.proveedor_dao import ProveedorDAO
from modelos.categoria import Categoria
from modelos.proveedor import Proveedor
from modelos.producto import Producto


ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class MercadoExpressApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mercado Express | Gestión de almacén")
        self.geometry("1040x680")
        self.minsize(840, 580)
        self.productos = ProductoDAO()
        self.ventas = VentaDAO()
        self.reportes = ReporteDAO()
        self.categorias = CategoriaDAO()
        self.proveedores = ProveedorDAO()

        ctk.CTkLabel(self, text="MERCADO EXPRESS", font=("Arial", 25, "bold")).pack(pady=(18, 6))
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=18, pady=10)
        self.tab_productos = self.tabs.add("Productos")
        self.tab_ventas = self.tabs.add("Ventas")
        self.tab_reportes = self.tabs.add("Reportes SQL")
        self.tab_categorias = self.tabs.add("Categorías")
        self.tab_proveedores = self.tabs.add("Proveedores")
        self.crear_productos()
        self.crear_ventas()
        self.crear_reportes()
        self.crear_categorias()
        self.crear_proveedores()
        self.refrescar()

    def tabla(self, padre, columnas):
        contenedor = ctk.CTkFrame(padre)
        contenedor.pack(fill="both", expand=True, padx=12, pady=12)
        tabla = ttk.Treeview(contenedor, columns=columnas, show="headings", height=12)
        for columna in columnas:
            tabla.heading(columna, text=columna.replace("_", " ").title())
            tabla.column(columna, width=135, anchor="center")
        barra = ttk.Scrollbar(contenedor, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=barra.set)
        tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return tabla

    def cargar_tabla(self, tabla, filas):
        for item in tabla.get_children():
            tabla.delete(item)
        for fila in filas:
            tabla.insert("", "end", values=tuple(fila))

    def campo(self, padre, etiqueta, ancho=155):
        grupo = ctk.CTkFrame(padre, fg_color="transparent")
        grupo.pack(side="left", padx=5, pady=6)
        ctk.CTkLabel(grupo, text=etiqueta).pack(anchor="w")
        entrada = ctk.CTkEntry(grupo, width=ancho)
        entrada.pack()
        return entrada

    def crear_productos(self):
        formulario = ctk.CTkFrame(self.tab_productos)
        formulario.pack(fill="x", padx=12, pady=8)
        self.nombre = self.campo(formulario, "Nombre")
        self.precio = self.campo(formulario, "Precio")
        self.stock = self.campo(formulario, "Stock")
        ctk.CTkButton(formulario, text="Agregar", width=90, command=self.agregar_producto).pack(side="left", padx=6)
        self.tabla_productos = self.tabla(self.tab_productos, ("id", "nombre", "precio", "stock"))
        acciones = ctk.CTkFrame(self.tab_productos)
        acciones.pack(fill="x", padx=12, pady=5)
        self.nuevo_precio = self.campo(acciones, "Nuevo precio")
        ctk.CTkButton(acciones, text="Actualizar precio seleccionado", command=self.actualizar_precio).pack(side="left", padx=5)
        ctk.CTkButton(acciones, text="Eliminar seleccionado", fg_color="#a53c3c", hover_color="#802d2d", command=self.eliminar_producto).pack(side="left", padx=5)

    def crear_ventas(self):
        formulario = ctk.CTkFrame(self.tab_ventas)
        formulario.pack(fill="x", padx=12, pady=8)
        self.id_venta = self.campo(formulario, "ID producto")
        self.cantidad_venta = self.campo(formulario, "Cantidad")
        ctk.CTkButton(formulario, text="Registrar venta", command=self.registrar_venta).pack(side="left", padx=8)
        self.tabla_ventas = self.tabla(self.tab_ventas, ("id", "producto", "cantidad", "total", "fecha"))

    def crear_reportes(self):
        superior = ctk.CTkFrame(self.tab_reportes)
        superior.pack(fill="x", padx=12, pady=8)
        opciones = [
            "Ventas por producto (JOIN + GROUP BY + HAVING)",
            "Productos con precio superior al promedio (subconsulta)",
            "Productos nunca vendidos (NOT EXISTS)",
            "Ventas superiores al promedio (JOIN + subconsulta)",
        ]
        self.selector_reporte = ctk.CTkOptionMenu(superior, values=opciones, width=530)
        self.selector_reporte.pack(side="left", padx=8, pady=8)
        ctk.CTkButton(superior, text="Ejecutar consulta", command=self.ejecutar_reporte).pack(side="left", padx=8)
        self.marco_reporte = ctk.CTkFrame(self.tab_reportes)
        self.marco_reporte.pack(fill="both", expand=True, padx=12, pady=12)
        self.tabla_reporte = None
        ctk.CTkLabel(self.marco_reporte, text="Seleccioná un reporte para consultar los datos.").pack(pady=12)

    def seleccionado(self):
        seleccion = self.tabla_productos.selection()
        if not seleccion:
            raise ValueError("Seleccioná un producto de la tabla")
        return int(self.tabla_productos.item(seleccion[0], "values")[0])

    def ejecutar_seguro(self, operacion):
        try:
            operacion()
        except (ValueError, sqlite3.Error) as error:
            messagebox.showerror("Operación no realizada", str(error))

    def agregar_producto(self):
        def operacion():
            nombre = self.nombre.get().strip()
            precio = float(self.precio.get())
            stock = int(self.stock.get())
            if not nombre or precio <= 0 or stock < 0:
                raise ValueError("Ingresá un nombre, precio positivo y stock no negativo")
            self.productos.agregar(Producto(nombre, precio, stock))
            for entrada in (self.nombre, self.precio, self.stock):
                entrada.delete(0, tk.END)
            self.refrescar()
            messagebox.showinfo("Producto", "Producto agregado")
        self.ejecutar_seguro(operacion)

    def actualizar_precio(self):
        def operacion():
            producto_id = self.seleccionado()
            precio = float(self.nuevo_precio.get())
            if precio <= 0:
                raise ValueError("El precio debe ser positivo")
            self.productos.actualizar_precio(producto_id, precio)
            self.refrescar()
            messagebox.showinfo("Producto", "Precio actualizado")
        self.ejecutar_seguro(operacion)

    def eliminar_producto(self):
        def operacion():
            producto_id = self.seleccionado()
            if messagebox.askyesno("Confirmar", "¿Eliminar el producto seleccionado?"):
                self.productos.eliminar(producto_id)
                self.refrescar()
        self.ejecutar_seguro(operacion)

    def registrar_venta(self):
        def operacion():
            total = self.ventas.registrar(int(self.id_venta.get()), int(self.cantidad_venta.get()))
            self.refrescar()
            messagebox.showinfo("Venta registrada", f"Total: ${total:.2f}")
        self.ejecutar_seguro(operacion)

    def refrescar(self):
        productos = self.productos.listar()
        self.cargar_tabla(self.tabla_productos, [(p.id, p.nombre, f"{p.precio:.2f}", p.stock) for p in productos])
        self.cargar_tabla(self.tabla_categorias, [(c.id, c.nombre, c.descripcion) for c in self.categorias.listar()])
        self.cargar_tabla(self.tabla_proveedores, [(p.id, p.nombre, p.telefono, p.email) for p in self.proveedores.listar()])
        ventas = self.ventas.listar()
        self.cargar_tabla(self.tabla_ventas, [(v["id"], v["producto"], v["cantidad"], f'{v["total"]:.2f}', v["fecha"]) for v in ventas])

    def ejecutar_reporte(self):
        def operacion():
            opcion = self.selector_reporte.get()
            if opcion.startswith("Ventas por producto"):
                filas = self.reportes.ventas_por_producto()
                columnas = ("producto", "operaciones", "unidades", "facturacion")
            elif opcion.startswith("Productos con precio"):
                filas = self.reportes.productos_sobre_promedio()
                columnas = ("id", "nombre", "precio")
            elif opcion.startswith("Productos nunca"):
                filas = self.reportes.productos_nunca_vendidos()
                columnas = ("id", "nombre", "stock")
            else:
                filas = self.reportes.ventas_superiores_al_promedio()
                columnas = ("venta_id", "producto", "importe", "fecha")
            for widget in self.marco_reporte.winfo_children():
                widget.destroy()
            self.tabla_reporte = self.tabla(self.marco_reporte, columnas)
            self.cargar_tabla(self.tabla_reporte, filas)
        self.ejecutar_seguro(operacion)

    def crear_categorias(self):
        formulario = ctk.CTkFrame(self.tab_categorias)
        formulario.pack(fill="x", padx=12, pady=8)
        self.cat_nombre = self.campo(formulario, "Nombre", 160)
        self.cat_descripcion = self.campo(formulario, "Descripción", 220)
        ctk.CTkButton(formulario, text="Crear categoría", command=self.agregar_categoria).pack(side="left", padx=6)
        self.tabla_categorias = self.tabla(self.tab_categorias, ("id", "nombre", "descripcion"))
        asociacion = ctk.CTkFrame(self.tab_categorias)
        asociacion.pack(fill="x", padx=12, pady=6)
        self.cat_producto_id = self.campo(asociacion, "ID producto", 120)
        ctk.CTkButton(asociacion, text="Asociar a categoría seleccionada", command=self.asociar_categoria).pack(side="left", padx=6)
        ctk.CTkButton(asociacion, text="Ver productos por categoría", command=lambda: self.mostrar_consulta(self.categorias.productos_por_categoria, ("categoria", "producto", "precio"))).pack(side="left", padx=6)
        ctk.CTkButton(asociacion, text="Sin productos", command=lambda: self.mostrar_consulta(self.categorias.categorias_sin_productos, ("id", "nombre"))).pack(side="left", padx=6)
        ctk.CTkButton(self.tab_categorias, text="Categorías con 2 o más productos", command=lambda: self.mostrar_consulta(lambda: self.categorias.categorias_con_varios_productos(2), ("categoria", "cantidad"))).pack(pady=4)

    def crear_proveedores(self):
        formulario = ctk.CTkFrame(self.tab_proveedores)
        formulario.pack(fill="x", padx=12, pady=8)
        self.prov_nombre = self.campo(formulario, "Nombre", 160)
        self.prov_telefono = self.campo(formulario, "Teléfono", 150)
        self.prov_email = self.campo(formulario, "Email", 210)
        ctk.CTkButton(formulario, text="Crear proveedor", command=self.agregar_proveedor).pack(side="left", padx=6)
        self.tabla_proveedores = self.tabla(self.tab_proveedores, ("id", "nombre", "telefono", "email"))
        asociacion = ctk.CTkFrame(self.tab_proveedores)
        asociacion.pack(fill="x", padx=12, pady=6)
        self.prov_producto_id = self.campo(asociacion, "ID producto", 120)
        ctk.CTkButton(asociacion, text="Asociar a proveedor seleccionado", command=self.asociar_proveedor).pack(side="left", padx=6)
        ctk.CTkButton(asociacion, text="Ver catálogo", command=lambda: self.mostrar_consulta(self.proveedores.catalogo_por_proveedor, ("proveedor", "producto", "stock"))).pack(side="left", padx=6)
        ctk.CTkButton(asociacion, text="Sin productos", command=lambda: self.mostrar_consulta(self.proveedores.proveedores_sin_productos, ("id", "nombre"))).pack(side="left", padx=6)
        ctk.CTkButton(self.tab_proveedores, text="Proveedores sobre el promedio", command=lambda: self.mostrar_consulta(self.proveedores.proveedores_con_mas_productos_que_promedio, ("proveedor", "cantidad"))).pack(pady=4)

    def id_seleccionado(self, tabla, entidad):
        seleccion = tabla.selection()
        if not seleccion:
            raise ValueError(f"Seleccioná un registro de {entidad}")
        return int(tabla.item(seleccion[0], "values")[0])

    def agregar_categoria(self):
        def operacion():
            nombre = self.cat_nombre.get().strip()
            if not nombre:
                raise ValueError("Ingresá el nombre de la categoría")
            self.categorias.agregar(Categoria(nombre, self.cat_descripcion.get().strip()))
            self.cat_nombre.delete(0, tk.END)
            self.cat_descripcion.delete(0, tk.END)
            self.refrescar()
        self.ejecutar_seguro(operacion)

    def agregar_proveedor(self):
        def operacion():
            nombre = self.prov_nombre.get().strip()
            if not nombre:
                raise ValueError("Ingresá el nombre del proveedor")
            self.proveedores.agregar(Proveedor(nombre, self.prov_telefono.get().strip(), self.prov_email.get().strip()))
            for entrada in (self.prov_nombre, self.prov_telefono, self.prov_email):
                entrada.delete(0, tk.END)
            self.refrescar()
        self.ejecutar_seguro(operacion)

    def asociar_categoria(self):
        def operacion():
            categoria_id = self.id_seleccionado(self.tabla_categorias, "categorías")
            producto_id = int(self.cat_producto_id.get())
            if producto_id <= 0:
                raise ValueError("El ID del producto debe ser positivo")
            self.categorias.asignar_producto(categoria_id, producto_id)
            messagebox.showinfo("Categorías", "Producto asociado correctamente")
        self.ejecutar_seguro(operacion)

    def asociar_proveedor(self):
        def operacion():
            proveedor_id = self.id_seleccionado(self.tabla_proveedores, "proveedores")
            producto_id = int(self.prov_producto_id.get())
            if producto_id <= 0:
                raise ValueError("El ID del producto debe ser positivo")
            self.proveedores.asignar_producto(proveedor_id, producto_id)
            messagebox.showinfo("Proveedores", "Producto asociado correctamente")
        self.ejecutar_seguro(operacion)

    def mostrar_consulta(self, consulta, columnas):
        def operacion():
            filas = consulta()
            ventana = ctk.CTkToplevel(self)
            ventana.title("Mercado Express | Consulta SQL")
            ventana.geometry("760x440")
            tabla = self.tabla(ventana, columnas)
            self.cargar_tabla(tabla, filas)
            ventana.lift()
        self.ejecutar_seguro(operacion)

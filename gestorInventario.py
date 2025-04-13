import mysql.connector
from mysql.connector import Error
from base_datos import baseDatos
from enum import Enum

class GestorProductos:
    def __init__(self, db):
        self.db = db
        self.tabla = "productos"
        self.Categorias = Enum("categorias", self.CategoriasBase())

    hola = "algo"
    def agregar_producto(self):
        nombre = input("Ingrese el nombre del producto: ")
        descripcion = input("Ingrese la descripción del producto: ")
        precio = input("Ingrese el precio del producto: ")
        stock = input("Ingrese el stock del producto: ")
        print("elija una categoria")
        for i in self.Categorias:
            print(f"{i.value}. {i.name}")
        eleccion = input()
        categoria = self.Categorias(int(eleccion)).name
        valores = [nombre, descripcion, precio, stock, categoria]
        columnas = ["nombre", "descripcion", "precio", "cantidad_stock", "categoria"]
        if self.db.insertar(self.tabla, valores, columnas):
            print("Producto agregado exitosamente.")
        else:
            print("Error al agregar el producto.")

    def buscar_producto(self):

        opciones = {
            "0" : "\nOpciones de búsqueda:",
            "1" : "1. Buscar por ID",
            "2" : "2. buscar por precio",
            "3" : "3. buscar por stock",
            "4" : "4. buscar por categoria",
            "5" : "5. Buscar por Nombre"
        }

        columnas = {
            "1" : "id_producto",
            "2" : "precio",
            "3" : "cantidad_stock",
            "4" : "categoria",
            "5" : "Nombre"
        }

        condiciones = {}

        while True:
            for i in opciones:
                print(opciones[i])
           
            opcion = input("Seleccione una opción: ")
            
            match opcion:
                case "1":
                    id = input("ingrese el id")
                    condiciones[columnas[opcion]] = id
                case "2":
                    precio = input("ingrese el precio: ")
                    condiciones[columnas[opcion]] = precio
                case "3":
                    cantidad = input("ingrese la cantidad: ")
                    condiciones[columnas[opcion]] = cantidad
                case "4":
                    print("elija una categoria")
                    for i in self.Categorias:
                        print(f"{i.value}. {i.name}")
                    eleccion = input()
                    condiciones[columnas[opcion]] = self.Categorias(int(eleccion)).name
                case "5":
                    nombre = input("ingrese el nombre: ")
                    condiciones[columnas[opcion]] = nombre
                    

            agregar = input("quiere agregar una condicion mas?(s/n)\n")
            if "s" == agregar.lower():
               del opciones[opcion]
               continue
            else:
                break             

        resultados = self.db.buscar(self.tabla, condiciones=condiciones)
        if resultados:
            print("\nResultados de la búsqueda:")
            for producto in resultados:
                print(f"ID: {producto[0]}, Nombre: {producto[5]}, Descripción: {producto[1]}, Precio: {producto[2]}, Stock: {producto[3]}, categoria: {producto[4]}")
        else:
            print("No se encontraron productos con los criterios especificados.")

    def listar_productos(self):
        productos = self.db.buscar(self.tabla)
        if productos:
            print("\nLista de productos:")
            for producto in productos:
                print(f"ID: {producto[0]}, Nombre: {producto[5]}, Descripción: {producto[1]}, Precio: {producto[2]}, Stock: {producto[3]}, categoria: {producto[4]}")
        else:
            print("No hay productos registrados.")

    def actualizar_producto(self):
        try:
            id_producto = int(input("Ingrese el ID del producto que desea actualizar: "))
            condiciones = {"id_producto": id_producto}
            producto_existente = self.db.buscar(self.tabla, condiciones=condiciones)
            if not producto_existente:
                print("No se encontró un producto con ese ID.")
                return

            print("\nIngrese los nuevos datos del producto (deje en blanco para no modificar):")
            nombre = input(f"Nuevo nombre ({producto_existente[0][5]}): ")
            descripcion = input(f"Nueva descripción ({producto_existente[0][1]}): ")
            precio = input(f"Nuevo precio ({producto_existente[0][2]}): ")
            stock = input(f"Nuevo stock ({producto_existente[0][3]}): ")
            categoria = input(f"nueva categoria ({producto_existente[0][4]})")
            

            actualizaciones = {}
            if descripcion:
                actualizaciones["descripcion"] = descripcion
            if precio:
                actualizaciones["precio"] = precio
            if stock:
                actualizaciones["cantidad_stock"] = stock
            if categoria:
                actualizaciones["categoria"] = categoria
            if nombre:
                actualizaciones["nombre"] = nombre
            
            if actualizaciones:
                if self.db.actualizar(self.tabla, condiciones, actualizaciones):
                    print("Producto actualizado exitosamente.")
                else:
                    print("Error al actualizar el producto.")
            else:
                print("No se ingresaron datos para actualizar.")

        except ValueError:
            print("ID inválido.")

    def eliminar_producto(self):
        try:
            id_producto = int(input("Ingrese el ID del producto que desea eliminar: "))
            condiciones = {"id_producto": id_producto}
            producto_existente = self.db.buscar(self.tabla, condiciones=condiciones)
            if not producto_existente:
                print("No se encontró un producto con ese ID.")
                return

            confirmacion = input(f"¿Está seguro de que desea eliminar el producto con ID {id_producto}? (s/n): ")
            if confirmacion.lower() == 's':
                if self.db.eliminar(self.tabla, condiciones):
                    print("Producto eliminado exitosamente.")
                else:
                    print("Error al eliminar el producto.")
            else:
                print("Operación de eliminación cancelada.")
        except ValueError:
            print("ID inválido.")

    def menu(self):
        while True:
            print("\n--- Gestor de Productos ---")
            print("1. Agregar Producto")
            print("2. Buscar Producto")
            print("3. Listar Productos")
            print("4. Actualizar Producto")
            print("5. Eliminar Producto")
            print("6. Salir")

            opcion = input("Seleccione una opción: ")

            match opcion:
                case "1":
                    self.agregar_producto()
                case "2":
                    self.buscar_producto()
                case "3":
                    self.listar_productos()
                case "4":
                    self.actualizar_producto()
                case "5":
                    self.eliminar_producto()
                case "6":
                    print("Saliendo del gestor de productos.")
                    break
                case _:
                    print("Opción inválida. Por favor, intente de nuevo.")

    def CategoriasBase(self):
        categoria = self.db.buscar("productos", "categoria")
        elementos = []
        for i in categoria:
            elementos += list(i)
        elementos = list(set(elementos))
        return elementos

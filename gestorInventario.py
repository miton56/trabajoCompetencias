import mysql.connector
from mysql.connector import Error

class GestorProductos:
    def __init__(self, db):
        self.db = db
        self.tabla = "productos"

    def agregar_producto(self):
        nombre = input("Ingrese el nombre del producto: ")
        descripcion = input("Ingrese la descripción del producto: ")
        precio = input("Ingrese el precio del producto: ")
        stock = input("Ingrese el stock del producto: ")
        valores = [descripcion, precio, stock, nombre, ]
        columnas = ["nombre", "descripcion", "precio", "stock"]
        if self.db.insertar(self.tabla, valores, columnas):
            print("Producto agregado exitosamente.")
        else:
            print("Error al agregar el producto.")

    def buscar_producto(self):

        opciones = {
            "0" : "\nOpciones de búsqueda:",
            "1" : "1. Buscar por ID",
            "2" : "2. Buscar por Nombre",
            "3" : "3. buscar por precio",
            "4" : "4. buscar por stock"
        }

        columnas = {
            "1" : "id_producto"
            "2" : 
        }

        while True:
            for i in opciones:
                print(opciones[i])
           
            opcion = input("Seleccione una opción: ")
            
            agregar = input("quiere agregar una condicion mas?(s/n)\n")
            if "s" == agregar.lower():
               del opciones[opcion]
               continue
            else:
                break             
            print

        condiciones = {}
        match opcion:
            case "1":
                id = input("ingrese el id")
                condiciones

        resultados = self.db.buscar(self.tabla, condiciones=condiciones)
        if resultados:
            print("\nResultados de la búsqueda:")
            for producto in resultados:
                print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Precio: {producto[3]}, Stock: {producto[4]}")
        else:
            print("No se encontraron productos con los criterios especificados.")

    def listar_productos(self):
        productos = self.db.buscar(self.tabla)
        if productos:
            print("\nLista de productos:")
            for producto in productos:
                print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Precio: {producto[3]}, Stock: {producto[4]}")
        else:
            print("No hay productos registrados.")

    def actualizar_producto(self):
        try:
            id_producto = int(input("Ingrese el ID del producto que desea actualizar: "))
            condiciones = {"id_producto": id_producto}
            producto_existente = self.db.buscar(self.tabla, condiciones=condiciones)
            if not producto_existente:
                print("❌ No se encontró un producto con ese ID.")
                return

            print("\nIngrese los nuevos datos del producto (deje en blanco para no modificar):")
            nombre = input(f"Nuevo nombre ({producto_existente[0][1]}): ")
            descripcion = input(f"Nueva descripción ({producto_existente[0][2]}): ")
            precio = input(f"Nuevo precio ({producto_existente[0][3]}): ")
            stock = input(f"Nuevo stock ({producto_existente[0][4]}): ")

            actualizaciones = {}
            if nombre:
                actualizaciones["nombre"] = nombre
            if descripcion:
                actualizaciones["descripcion"] = descripcion
            if precio:
                actualizaciones["precio"] = precio
            if stock:
                actualizaciones["stock"] = stock

            if actualizaciones:
                if self.db.actualizar(self.tabla, condiciones, actualizaciones):
                    print("✅ Producto actualizado exitosamente.")
                else:
                    print("❌ Error al actualizar el producto.")
            else:
                print("No se ingresaron datos para actualizar.")

        except ValueError:
            print("❌ ID inválido.")

    def eliminar_producto(self):
        try:
            id_producto = int(input("Ingrese el ID del producto que desea eliminar: "))
            condiciones = {"id_producto": id_producto}
            producto_existente = self.db.buscar(self.tabla, condiciones=condiciones)
            if not producto_existente:
                print("❌ No se encontró un producto con ese ID.")
                return

            confirmacion = input(f"¿Está seguro de que desea eliminar el producto con ID {id_producto}? (s/n): ")
            if confirmacion.lower() == 's':
                if self.db.eliminar(self.tabla, condiciones):
                    print("✅ Producto eliminado exitosamente.")
                else:
                    print("❌ Error al eliminar el producto.")
            else:
                print("Operación de eliminación cancelada.")
        except ValueError:
            print("❌ ID inválido.")

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

            if opcion == '1':
                self.agregar_producto()
            elif opcion == '2':
                self.buscar_producto()
            elif opcion == '3':
                self.listar_productos()
            elif opcion == '4':
                self.actualizar_producto()
            elif opcion == '5':
                self.eliminar_producto()
            elif opcion == '6':
                print("Saliendo del gestor de productos.")
                break
            else:
                print("Opción inválida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    db_manager = baseDatos()
    if db_manager.conexion.is_connected():
        gestor = GestorProductos(db_manager)
        gestor.menu()
        db_manager.conexion.close()
        print("🔌 Conexión a la base de datos cerrada.")
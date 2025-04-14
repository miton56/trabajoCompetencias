import mysql.connector
from mysql.connector import Error

class GestorProveedor:
    def __init__(self, db):
        self.db = db
        self.tabla = "proveedores"

    def agregar_proveedor(self):
        nombre = input("Ingrese el nombre del proveedor: ")
        telefono = input("Ingrese el teléfono del proveedor: ")
        rut = input("Ingrese el rut del proveedor: ")
        correo = input("Ingrese el email del proveedor: ")
        direccion = input("Ingrese la dirección del proveedor: ")
        valores = [rut, nombre, correo, telefono, direccion]
        columnas = ["rut", "nombre", "correo", "telefono", "direccion"]
        if self.db.insertar(self.tabla, valores, columnas):
            print("Proveedor agregado exitosamente.")
        else:
            print("Error al agregar el proveedor.")

    def buscar_proveedor(self):
        condiciones = {}
    
        opciones = {
            "0" : "\nOpciones de búsqueda:",
            "1" : "1. Buscar por ID",
            "2" : "2. Buscar por rut",
            "3" : "3. Buscar por Nombre",
            "4" : "4. Buscar por correo",
            "5" : "5. Buscar por telefono",
            "6" : "6. Buscar por direccion"
        }

        columnas = {
            "1" : "id_proveedor",
            "2" : "rut",
            "3" : "Nombre",
            "4" : "correo",
            "5" : "telefono",
            "6" : "direccion"
        }

        while True:

            for i in opciones:
                print(opciones[i])
            opcion = input("Seleccione una opción: ")

            match opcion:
                case '1':
                    id_cliente = int(input("Ingrese el ID del proeveedor: "))
                    condiciones[columnas[opcion]] = id_cliente
                case '2':
                    rut = input("Ingrese el rut del proveedor: ")
                    condiciones[columnas[opcion]] = rut
                case '3':
                    nombre = input("Ingrese el nombre del proveedor: ")
                    condiciones[columnas[opcion]] = nombre
                case "4":
                    correo = input("ingrese el correo del proveedor: ")
                    condiciones[columnas[opcion]] = correo
                case "5":
                    telefono = input("ingrese el telefono del proveedor")
                    condiciones[columnas[opcion]] = telefono
                case "6":
                    direccion = input("ingrese la direccion del proveedor")
                    condiciones[columnas[opcion]] = direccion
                case _:
                    print("Opción inválida.")
                    continue
                
            agregar = input("quiere agregar una condicion mas?(s/n)\n")
            if "s" == agregar.lower():
                del opciones[opcion]
                continue
            else:
                break 

        resultados = self.db.buscar(self.tabla, condiciones=condiciones)
        if resultados:
                print("\nResultados de la búsqueda:")
                for proveedor in resultados:
                    print(f"ID: {proveedor[0]}, rut: {proveedor[1]}, Nombre: {proveedor[2]}, correo: {proveedor[3]}, telefono: {proveedor[4]}, Dirección: {proveedor[5]}")
        else:
            print("No se encontraron proveedores con los criterios especificados.")

    def listar_proveedores(self, imprimir=True):
        if imprimir:
            proveedores = self.db.buscar(self.tabla)
            if proveedores:
                print("\nLista de proveedores:")
                for proveedor in proveedores:
                    print(f"ID: {proveedor[0]}, rut: {proveedor[1]}, Nombre: {proveedor[2]}, correo: {proveedor[3]}, telefono: {proveedor[4]}, Dirección: {proveedor[5]}")
            else:
                print("No hay proveedores registrados.")
        else:
            proveedores = self.db.buscar(self.tabla)
            if proveedores:
                return proveedores
            else:
                print("No hay proveedores registrados.")


    def actualizar_proveedor(self):
        try:
            id_proveedor = int(input("Ingrese el ID del proveedor que desea actualizar: "))
            condiciones = {"id_proveedor": id_proveedor}
            proveedor_existente = self.db.buscar(self.tabla, condiciones=condiciones)
            if not proveedor_existente:
                print("No se encontró un proveedor con ese ID.")
                return

            print("\nIngrese los nuevos datos del proveedor (deje en blanco para no modificar):")
            rut = input(f"Nuevo rut ({proveedor_existente[0][1]}): ")
            nombre = input(f"Nuevo nombre ({proveedor_existente[0][2]}): ")
            correo = input(f"Nuevo correo ({proveedor_existente[0][3]}): ")
            telefono = input(f"Nuevo telefono ({proveedor_existente[0][4]}): ")
            direccion = input(f"Nueva dirección ({proveedor_existente[0][5]}): ")

            actualizaciones = {}
            if rut:
                actualizaciones["nombre"] = nombre
            if nombre:
                actualizaciones["contacto"] = nombre
            if correo:
                actualizaciones["telefono"] = telefono
            if telefono:
                actualizaciones["email"] = telefono
            if direccion:
                actualizaciones["direccion"] = direccion

            if actualizaciones:
                if self.db.actualizar(self.tabla, condiciones, actualizaciones):
                    print("Proveedor actualizado exitosamente.")
                else:
                    print("Error al actualizar el proveedor.")
            else:
                print("No se ingresaron datos para actualizar.")

        except ValueError:
            print("ID inválido.")

    def eliminar_proveedor(self):
        try:
            id_proveedor = int(input("Ingrese el ID del proveedor que desea eliminar: "))
            condiciones = {"id_proveedor": id_proveedor}
            proveedor_existente = self.db.buscar(self.tabla, condiciones=condiciones)
            if not proveedor_existente:
                print("No se encontró un proveedor con ese ID.")
                return

            confirmacion = input(f"¿Está seguro de que desea eliminar al proveedor con ID {id_proveedor}? (s/n): ")
            if confirmacion.lower() == 's':
                if self.db.eliminar(self.tabla, condiciones):
                    print("Proveedor eliminado exitosamente.")
                else:
                    print("Error al eliminar el proveedor.")
            else:
                print("Operación de eliminación cancelada.")
        except ValueError:
            print(" ID inválido.")

    def menu(self):
        while True:
            print("\n--- Gestor de Proveedores ---")
            print("1. Agregar Proveedor")
            print("2. Buscar Proveedor")
            print("3. Listar Proveedores")
            print("4. Actualizar Proveedor")
            print("5. Eliminar Proveedor")
            print("6. Salir")

            opcion = input("Seleccione una opción: ")

            match opcion:
                case "1":
                    self.agregar_proveedor()
                case "2":
                    self.buscar_proveedor()
                case "3":
                    self.listar_proveedores()
                case "4":
                    self.actualizar_proveedor()
                case "5":
                    self.eliminar_proveedor()
                case "6":
                    print("Saliendo del gestor de proveedores.")
                    break
                case _:
                     print("Opción inválida. Por favor, intente de nuevo.")

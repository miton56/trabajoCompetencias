import mysql.connector
from mysql.connector import Error

class GestorClientes:
    def __init__(self, db):
        self.db = db
        self.tabla = "clientes"




    def agregar_cliente(self):
        nombre = input("Ingrese el nombre del cliente: ")
        email = input("Ingrese el email del cliente: ")
        telefono = input("Ingrese el teléfono del cliente: ")
        direccion = input("Ingrese la dirección del cliente: ")
        rut = input("Ingrese el rut del cliente: ")
        valores = [rut, nombre, direccion, telefono, email]
        columnas = ["rut", "nombre", "direccion", "telefono", "correo"]
        if self.db.insertar(self.tabla, valores, columnas):
            print("Cliente agregado exitosamente.")
        else:
            print("Error al agregar el cliente.")

    def buscar_cliente(self):

        condiciones = {}
    
        opciones = {
            "0" : "\nOpciones de búsqueda:",
            "1" : "1. Buscar por ID",
            "2" : "2. Buscar por rut",
            "3" : "3. Buscar por Nombre",
            "4" : "4. Buscar por direccion",
            "5" : "5. Buscar por telefono",
            "6" : "6. Buscar por correo"
        }

        columnas = {
            "1" : "id_cliente",
            "2" : "rut",
            "3" : "Nombre",
            "4" : "direccion",
            "5" : "telefono",
            "6" : "correo"
        }

        while True:

            for i in opciones:
                print(opciones[i])
            opcion = input("Seleccione una opción: ")

            match opcion:
                case '1':
                    id_cliente = int(input("Ingrese el ID del cliente: "))
                    condiciones[columnas[opcion]] = id_cliente
                case '2':
                    rut = input("Ingrese el rut del cliente: ")
                    condiciones[columnas[opcion]] = rut
                case '3':
                    nombre = input("Ingrese el nombre del cliente: ")
                    condiciones[columnas[opcion]] = nombre
                case "4":
                    direccion = input("ingrese la direccion del cliente: ")
                    condiciones[columnas[opcion]] = direccion
                case "5":
                    telefono = input("ingrese el telefono del cliente")
                    condiciones[columnas[opcion]] = telefono
                case "6":
                    correo = input("ingrese el correo del cliente")
                    condiciones[columnas[opcion]] = correo
                case _:
                    print("Opción inválida.")
                    return
                
            agregar = input("quiere agregar una condicion mas?(s/n)\n")
            if "s" == agregar.lower():
                del opciones[opcion]
                continue
            else:
                break 

        resultados = self.db.buscar(self.tabla, condiciones=condiciones)
        if resultados:
            print("\nResultados de la búsqueda:")
            for cliente in resultados:
                print(f"ID: {cliente[0]}, Rut: {cliente[1]}, Nombre: {cliente[2]}, Direccion: {cliente[3]}, telefono: {cliente[4]}, correo: {cliente[5]}")
        else:
            print("No se encontraron clientes con los criterios especificados.")

    def listar_clientes(self):
        clientes = self.db.buscar(self.tabla)
        if clientes:
            print("\nLista de clientes:")
            for cliente in clientes:
                print(f"ID: {cliente[0]}, Rut: {cliente[1]}, Nombre: {cliente[2]}, Direccion: {cliente[3]}, telefono: {cliente[4]}, correo: {cliente[5]}")
        else:
            print("No hay clientes registrados.")

    def actualizar_cliente(self):
        try:
            id_cliente = int(input("Ingrese el ID del cliente que desea actualizar: "))
            condiciones = {"id_cliente": id_cliente}
            cliente_existente = self.db.buscar(self.tabla, condiciones=condiciones)
            if not cliente_existente:
                print("No se encontró un cliente con ese ID.")
                return

            print("\nIngrese los nuevos datos del cliente (deje en blanco para no modificar):")
            rut = input(f"Nuevo rut ({cliente_existente[0][1]}): ")
            nombre = input(f"Nuevo nombre ({cliente_existente[0][2]}): ")
            direccion = input(f"Nueva direccion ({cliente_existente[0][3]}): ")
            telefono = input(f"Nueva telefono ({cliente_existente[0][4]}): ")
            email = input(f"Nuevo email({cliente_existente[0][5]}): ")

            actualizaciones = {}
            if nombre:
                actualizaciones["nombre"] = nombre
            if email:
                actualizaciones["correo"] = email
            if telefono:
                actualizaciones["telefono"] = telefono
            if direccion:
                actualizaciones["direccion"] = direccion
            if rut:
                actualizaciones["rut"] = rut

            if actualizaciones:
                if self.db.actualizar(self.tabla, condiciones, actualizaciones):
                    print(" Cliente actualizado exitosamente.")
                else:
                    print("Error al actualizar el cliente.")
            else:
                print("No se ingresaron datos para actualizar.")

        except ValueError:
            print("ID inválido.")

    def eliminar_cliente(self):
        try:
            #bloque de codigo a cambiar mas adelante
            id_cliente = int(input("Ingrese el ID del cliente que desea eliminar: "))
            condiciones = {"id_cliente": id_cliente}
            cliente_existente = self.db.buscar(self.tabla, condiciones=condiciones)
            if not cliente_existente:
                print(" No se encontró un cliente con ese ID.")
                return

            confirmacion = input(f"¿Está seguro de que desea eliminar al cliente con ID {id_cliente}? (s/n): ")
            if confirmacion.lower() == 's':
                #bloque de codigo a usar si o si inicio
                if self.db.eliminar(self.tabla, condiciones):
                    print(" Cliente eliminado exitosamente.")
                else:
                    print(" Error al eliminar el cliente.")
            else:
                print("Operación de eliminación cancelada.")
                #bloque de codigo a usar si o si fin
        except ValueError:
            print(" ID inválido.")

    def menu(self):
        while True:
            print("\n--- Gestor de Clientes ---")
            print("1. Agregar Cliente")
            print("2. Buscar Cliente")
            print("3. Listar Clientes")
            print("4. Actualizar Cliente")
            print("5. Eliminar Cliente")
            print("6. Salir")

            opcion = input("Seleccione una opción: ")

            match opcion:
                case "1":
                    self.agregar_cliente()
                case '2':
                    self.buscar_cliente()
                case '3':
                    self.listar_clientes()
                case '4':
                    self.actualizar_cliente()
                case '5':
                    self.eliminar_cliente()
                case '6':
                    print("Saliendo del gestor de clientes.")
                    break
                case _:
                    print("Opción inválida. Por favor, intente de nuevo.")

    
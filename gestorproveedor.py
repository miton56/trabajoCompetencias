import mysql.connector
from mysql.connector import Error

class GestorProveedor:
    def __init__(self, db):
        self.db = db
        self.tabla = "proveedores"

    def agregar_proveedor(self):
        nombre = input("Ingrese el nombre del proveedor: ")
        contacto = input("Ingrese el nombre del contacto del proveedor: ")
        telefono = input("Ingrese el teléfono del proveedor: ")
        rut = input("Ingrese el rut del proveedor: ")
        email = input("Ingrese el email del proveedor: ")
        direccion = input("Ingrese la dirección del proveedor: ")
        valores = [rut, contacto, telefono, email, direccion]
        columnas = ["nombre", "contacto", "telefono", "email", "direccion"]
        if self.db.insertar(self.tabla, valores, columnas):
            print("Proveedor agregado exitosamente.")
        else:
            print("Error al agregar el proveedor.")

    def buscar_proveedor(self):
        print("\nOpciones de búsqueda:")
        print("1. Buscar por ID")
        print("2. Buscar por Nombre")
        print("3. Buscar por Contacto")
        print("4. Buscar por Email")
        opcion = input("Seleccione una opción: ")

        condiciones = {}
        if opcion == '1':
            try:
                id_proveedor = int(input("Ingrese el ID del proveedor: "))
                condiciones["id_proveedor"] = id_proveedor
            except ValueError:
                print("❌ ID inválido.")
                return
        elif opcion == '2':
            nombre = input("Ingrese el nombre del proveedor: ")
            condiciones["nombre"] = nombre
        elif opcion == '3':
            contacto = input("Ingrese el nombre del contacto: ")
            condiciones["contacto"] = contacto
        elif opcion == '4':
            email = input("Ingrese el email del proveedor: ")
            condiciones["email"] = email
        else:
            print("❌ Opción inválida.")
            return

        resultados = self.db.buscar(self.tabla, condiciones=condiciones)
        if resultados:
            print("\nResultados de la búsqueda:")
            for proveedor in resultados:
                print(f"ID: {proveedor[0]}, Nombre: {proveedor[1]}, Contacto: {proveedor[2]}, Teléfono: {proveedor[3]}, Email: {proveedor[4]}, Dirección: {proveedor[5]}")
        else:
            print("No se encontraron proveedores con los criterios especificados.")

    def listar_proveedores(self):
        proveedores = self.db.buscar(self.tabla)
        if proveedores:
            print("\nLista de proveedores:")
            for proveedor in proveedores:
                print(f"ID: {proveedor[0]}, Nombre: {proveedor[1]}, Contacto: {proveedor[2]}, Teléfono: {proveedor[3]}, Email: {proveedor[4]}, Dirección: {proveedor[5]}")
        else:
            print("No hay proveedores registrados.")

    def actualizar_proveedor(self):
        try:
            id_proveedor = int(input("Ingrese el ID del proveedor que desea actualizar: "))
            condiciones = {"id_proveedor": id_proveedor}
            proveedor_existente = self.db.buscar(self.tabla, condiciones=condiciones)
            if not proveedor_existente:
                print("❌ No se encontró un proveedor con ese ID.")
                return

            print("\nIngrese los nuevos datos del proveedor (deje en blanco para no modificar):")
            nombre = input(f"Nuevo nombre ({proveedor_existente[0][1]}): ")
            contacto = input(f"Nuevo contacto ({proveedor_existente[0][2]}): ")
            telefono = input(f"Nuevo teléfono ({proveedor_existente[0][3]}): ")
            email = input(f"Nuevo email ({proveedor_existente[0][4]}): ")
            direccion = input(f"Nueva dirección ({proveedor_existente[0][5]}): ")

            actualizaciones = {}
            if nombre:
                actualizaciones["nombre"] = nombre
            if contacto:
                actualizaciones["contacto"] = contacto
            if telefono:
                actualizaciones["telefono"] = telefono
            if email:
                actualizaciones["email"] = email
            if direccion:
                actualizaciones["direccion"] = direccion

            if actualizaciones:
                if self.db.actualizar(self.tabla, condiciones, actualizaciones):
                    print("✅ Proveedor actualizado exitosamente.")
                else:
                    print("❌ Error al actualizar el proveedor.")
            else:
                print("No se ingresaron datos para actualizar.")

        except ValueError:
            print("❌ ID inválido.")

    def eliminar_proveedor(self):
        try:
            id_proveedor = int(input("Ingrese el ID del proveedor que desea eliminar: "))
            condiciones = {"id_proveedor": id_proveedor}
            proveedor_existente = self.db.buscar(self.tabla, condiciones=condiciones)
            if not proveedor_existente:
                print("❌ No se encontró un proveedor con ese ID.")
                return

            confirmacion = input(f"¿Está seguro de que desea eliminar al proveedor con ID {id_proveedor}? (s/n): ")
            if confirmacion.lower() == 's':
                if self.db.eliminar(self.tabla, condiciones):
                    print("✅ Proveedor eliminado exitosamente.")
                else:
                    print("❌ Error al eliminar el proveedor.")
            else:
                print("Operación de eliminación cancelada.")
        except ValueError:
            print("❌ ID inválido.")

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

            if opcion == '1':
                self.agregar_proveedor()
            elif opcion == '2':
                self.buscar_proveedor()
            elif opcion == '3':
                self.listar_proveedores()
            elif opcion == '4':
                self.actualizar_proveedor()
            elif opcion == '5':
                self.eliminar_proveedor()
            elif opcion == '6':
                print("Saliendo del gestor de proveedores.")
                break
            else:
                print("Opción inválida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    db_manager = baseDatos()
    if db_manager.conexion.is_connected():
        gestor = GestorProveedores(db_manager)
        gestor.menu()
        db_manager.conexion.close()
        print("🔌 Conexión a la base de datos cerrada.")
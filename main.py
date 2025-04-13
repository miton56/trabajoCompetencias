from gestorcliente import GestorClientes
from base_datos import baseDatos
from gestorInventario import GestorProductos

print("""bienvenido al sistema de ventas""")

base = baseDatos()

while True:
    print("""

    elija una opcion
      
    1.gestionar clientes
    2.gestionar productos
    3.gestionar proveedores
    4.gestionar ventas
    5.salir
    """)
    eleccion = input(": ")

    match eleccion:

        case "1":
            gestorCliente = GestorClientes(base)
            gestorCliente.menu()
        case "2":
            gestorProductos = GestorProductos(base)
            gestorProductos.menu()
        case "5":
            break
        case _:
            print("opcion no valida")
            
            
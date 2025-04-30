from gestorInventario import GestorProductos
from gestorcliente import GestorClientes
from base_datos import baseDatos
from tabulate import tabulate
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

class GestorVenta():

    def __init__(self, base):
        self.base = base
        self.gestorCliente = GestorClientes(self.base)
        self.gestorProductos = GestorProductos(self.base)

    def realizarVenta(self):
        ids_productos = []
        productos = []
        while True:
            print("seleccione el id de un cliente")
            self.gestorCliente.listar_clientes()
            id_cliente = input(": ")
            bucle = True
            while bucle:
                print("seleccione el id de un producto")
                self.gestorProductos.listar_productos()
                id_producto = input(": ")
                ids_productos.append(id_producto)
                while True:
                    print("quiere agregar otro producto? (s/n)")
                    eleccion = input(": ")
                    if eleccion.lower() == "s":
                        break
                    elif eleccion.lower() == "n":
                        bucle = False
                        break
                    else:
                        print("seleccione una opcion valida")

            cliente = self.base.buscar("clientes", condiciones={"id_cliente" : id_cliente})

            for id in ids_productos:
                product = self.base.buscar("productos", condiciones={"id_producto" : id})
                productos.append(product[0])
            cantidades = []
            for producto in productos:
                cantidad = input(f"cuanto va a llevar de {producto[5]}?: ")
                cantidades.append(cantidad)
            
            print("lo que lleva es: ")
            
            titulos_columnas = ["Producto", "Precio", "Cantidad", "subtotal"]

            filas = []

            total = 0



            for producto, cantidad in zip(productos, cantidades):
                subtotal = int(cantidad) * int(producto[2])
                filas.append([producto[5], producto[2], cantidad, subtotal])
                total += subtotal 
            
                
            print(tabulate(filas, headers=titulos_columnas, tablefmt="grid"))

            print("total: " + str(total))
            
            eleccion = input("desea continuar? (s/n) : ")

            if eleccion.lower() != "s":
                break
            
            metodos_pago = []
            siclo = 0
            
            while True:

                siclo += 1

                print("elija un metodo de pago")

                metodos = self.base.buscar("metodo_de_pago")

                for metodo in metodos:
                    print(f"{metodo[0]}.-    {metodo[1]}")
                
                eleccion = input(": ")

                metodo_elegido = self.base.buscar("metodo_de_pago", condiciones={"id_metodo_pago" : int(eleccion)})

                metodos_pago.append(metodo_elegido[0])

                if siclo == 2:
                    break
    

                seguir = input("quiere agregar otro metodo de pago? (maximo 2) (s/n) : ")

                if seguir.lower() == "n":
                    break
                elif seguir.lower() == "s":
                    continue
                else:
                    print("ingrese una opcion valida")
            
            porcentajes = {}

            for metodo in metodos_pago:
                porcentajes[metodo[1]] = int(input(f"que porcentaje del total quiere pagar con {metodo[1]}? : ")) /100
            
            for por in porcentajes:
                print(f"tiene que pagar {total*porcentajes[por]} con {por}")
            
            print("desea realizar el pago? (s/n)")

            eleccion = input(": ")

            if eleccion.lower() == "s":

                print("pago realizado")

                cliente1 = {
                   "nombre" : cliente[0][2],
                   "rut" : cliente[0][1],
                   "email" : cliente[0][5],
                   "telefono" : cliente[0][4]  
                }

                productos_final = []

                self.base.insertar("ventas", [cliente[0][0], total, "pagado"], ["id_cliente", "monto_total", "estado"])

                id_venta = self.base.buscar("ventas", columnas = "id_venta")

                lista_ordenada = [item[0] for item in id_venta]
    
                # Ordenar la lista de mayor a menor
                lista_ordenada.sort()

                print(lista_ordenada)

                input("")

                id_venta_final = lista_ordenada[-1]

                for metodo in metodos_pago:

                    self.base.insertar("detalle_metodo_pago", [metodo[0], id_venta_final, (porcentajes[metodo[1]] * total)], ["id_metodo_pago", "id_venta", "monto_pagado"])
                
                for prod, cant in zip(productos, cantidades):

                    self.base.insertar("detalle_ventas", [prod[0], id_venta_final, cant, prod[2], (int(cant) * int(prod[2]))], ["id_producto", "id_venta", "cantidad", "precio_unitario", "subtotal"])

                for prod, cant in zip(productos, cantidades):
                    productos_final.append({"nombre": prod[5], "cantidad": cant, "precio": prod[2]})
                metodos_final = []

                for metod, por in zip(metodos_pago, porcentajes):
                    metodos_final.append( {"metodo": metod[1], "monto": (total * porcentajes[por]), "descuento": (int(metod[2])/100)})

                self.generar_recibo(cliente1, productos_final, metodos_final)

                eleccion = input("quiere realizar otra compra? (s/n) : ")

                if eleccion.lower() == "s":
                    continue
                else:
                    break
            
                



    def generar_recibo(self, cliente, productos, pagos):
        # Crear carpeta "recibos" si no existe
        carpeta = "recibos"
        os.makedirs(carpeta, exist_ok=True)

        # Obtener fecha y hora actuales
        ahora = datetime.now()
        fecha_str = ahora.strftime("%Y-%m-%d_%H-%M-%S")
        fecha_mostrada = ahora.strftime("%d/%m/%Y %H:%M:%S")

        # Crear nombre del archivo con fecha
        nombre_archivo = os.path.join(carpeta, f"recibo_{fecha_str}.pdf")

        c = canvas.Canvas(nombre_archivo, pagesize=A4)
        width, height = A4

        # Encabezado
        c.setFont("Helvetica-Bold", 14)
        c.drawString(2 * cm, height - 2 * cm, "RECIBO DE VENTA")

        # Fecha de emisión
        c.setFont("Helvetica", 10)
        c.drawString(14 * cm, height - 2 * cm, f"Fecha: {fecha_mostrada}")

        # Datos del cliente (incluyendo RUT)
        c.drawString(2 * cm, height - 3 * cm, f"Cliente: {cliente['nombre']}")
        c.drawString(2 * cm, height - 3.5 * cm, f"RUT: {cliente['rut']}")
        c.drawString(2 * cm, height - 4 * cm, f"Email: {cliente['email']}")
        c.drawString(2 * cm, height - 4.5 * cm, f"Teléfono: {cliente['telefono']}")

        # Tabla de productos
        c.setFont("Helvetica-Bold", 10)
        y = height - 5.5 * cm
        c.drawString(2 * cm, y, "Producto")
        c.drawString(8 * cm, y, "Cantidad")
        c.drawString(11 * cm, y, "Precio Unit.")
        c.drawString(15 * cm, y, "Subtotal")

        c.setFont("Helvetica", 10)
        total = 0
        y -= 0.5 * cm
        for prod in productos:
            subtotal = int(prod['cantidad']) * int(prod['precio'])
            total += subtotal

            c.drawString(2 * cm, y, prod['nombre'])
            c.drawString(8 * cm, y, str(prod['cantidad']))
            c.drawString(11 * cm, y, f"${prod['precio']:.2f}")
            c.drawString(15 * cm, y, f"${subtotal:.2f}")
            y -= 0.5 * cm

        # Métodos de pago y descuentos
        c.setFont("Helvetica-Bold", 10)
        y -= 1 * cm
        c.drawString(2 * cm, y, "Métodos de Pago y Descuentos:")

        c.setFont("Helvetica", 10)
        descuento_total = 0
        for pago in pagos:
            metodo = pago['metodo']
            monto = pago['monto']
            descuento = pago.get('descuento', 0.0)
            desc_aplicado = monto * descuento
            descuento_total += desc_aplicado
            y -= 0.5 * cm
            c.drawString(2.5 * cm, y,
                        f"{metodo}: ${monto:.2f}  (Descuento: {descuento*100:.0f}% = ${desc_aplicado:.2f})")

        # Total final
        y -= 1 * cm
        c.setFont("Helvetica-Bold", 11)
        c.drawString(2 * cm, y, f"TOTAL BRUTO: ${total:.2f}")
        y -= 0.5 * cm
        c.drawString(2 * cm, y, f"DESCUENTO TOTAL: -${descuento_total:.2f}")
        y -= 0.5 * cm
        c.drawString(2 * cm, y, f"TOTAL NETO A PAGAR: ${total - descuento_total:.2f}")

        c.save()
        print(f"Recibo generado: {nombre_archivo}")

    def menu(self):
        while True:

            print("elija una opcion")
            print("1.- realizar venta")
            print("6.- salir")

            opcion = input(": ")

            match opcion:
                case "1":
                    self.realizarVenta()
                case "6":
                    print("saliendo")
                    break

                










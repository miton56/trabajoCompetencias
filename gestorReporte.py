from gestorInventario import GestorProductos
from base_datos import baseDatos
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os
from decimal import Decimal


class gestorReporte:

    def __init__(self, db):
        self.db = db

    def reportePDF(self):
        
        carpeta_destino = "./reportes" 
        if not os.path.exists(carpeta_destino): 
            os.makedirs(carpeta_destino)
        pdf_Nombre = os.path.join(carpeta_destino, "reporte_inventario.pdf")
        doc = SimpleDocTemplate(pdf_Nombre, pagesize=letter)
        informacion = self.db.buscar("ventas_por_producto")
        datos = [['Producto', 'precio unitario', 'unidades vendidas', 'cantidad de ventas', 'total vendido', 'stock en dinero']]


        for filas in informacion:
            lista_base = []
            for i in filas:
                if type(i) is Decimal:

                    formateado = f"{float(i):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    lista_base.append((formateado))
                elif type(i) is int:
                    formateado = f"{i:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    lista_base.append((formateado))
                else:
                    lista_base.append((i))
            datos.append(lista_base)
        
        table = Table(datos)
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), 
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'), 
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  
            ('SIZE', (0, 0), (-1, -1), 10)  
        ]))

        elements = [table]
        doc.build(elements)

        print(f"reporte '{pdf_Nombre}' creado correctamente en la carpeta '{carpeta_destino}'.")
    
    def menu(self):
        while True:

            print("elija una opcion")
            print("1.- generar reporte inventario en pdf")
            print("6.- salir")

            opcion = input(": ")

            match opcion:
                case "1":
                    self.reportePDF()
                case "6":
                    print("saliendo")
                    break










gestor = gestorReporte(baseDatos())

gestor.reportePDF()
import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gestorReporte import gestorReporte

class TestGestorReporte(unittest.TestCase):
    
    def setUp(self):
        # Creamos un mock para la base de datos
        self.db_mock = MagicMock()
        
        # Creamos una instancia del gestor de reportes
        self.gestor = gestorReporte(self.db_mock)
        
        # Datos de prueba para información de ventas
        self.mock_informacion_ventas = [
            ('Producto 1', 10000, 5, 3, 50000, 20000),
            ('Producto 2', 20000, 10, 7, 200000, 60000)
        ]

    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('gestorReporte.datetime')
    @patch('gestorReporte.SimpleDocTemplate')
    @patch('gestorReporte.Table')
    @patch('gestorReporte.TableStyle')
    def test_generarReportePDf(self, mock_tablestyle, mock_table, mock_simpledoc, 
                               mock_datetime, mock_makedirs, mock_path_exists):
        # Configuramos los mocks
        mock_path_exists.return_value = False
        mock_datetime.now.return_value.strftime.return_value = "2025-04-22_10-30-00"
        
        # Mock para el objeto SimpleDocTemplate
        mock_doc = MagicMock()
        mock_simpledoc.return_value = mock_doc
        
        # Mock para el objeto Table
        mock_table_obj = MagicMock()
        mock_table.return_value = mock_table_obj
        
        # Nombre y columnas de ejemplo
        nombre_reporte = "reporte_test"
        columnas = ['Col1', 'Col2', 'Col3']
        informacion = [
            ('Dato1', 100, 200),
            ('Dato2', 300, 400)
        ]
        
        # Ejecutamos el método bajo prueba
        with patch('builtins.print') as mock_print:
            self.gestor.generarReportePDf(columnas, informacion, nombre_reporte)
        
        # Verificamos que se creó el directorio si no existía
        mock_makedirs.assert_called_once_with("./reportes")
        
        # Verificamos que se creó el objeto SimpleDocTemplate con la ruta correcta
        mock_simpledoc.assert_called_once()
        
        # Verificamos que se creó la tabla con los datos correctos
        mock_table.assert_called_once()
        
        # Verificamos que se aplicó el estilo a la tabla
        mock_table_obj.setStyle.assert_called_once()
        
        # Verificamos que se construyó el documento
        mock_doc.build.assert_called_once()
        
        # Verificamos que se mostró el mensaje de éxito
        mock_print.assert_called_with(f"reporte '{nombre_reporte}' creado correctamente en la carpeta './reportes'.")

    @patch('gestorReporte.gestorReporte.generarReportePDf')
    def test_reporte_ventas(self, mock_generar_pdf):
        # Configuramos el mock para que buscar devuelva información de ventas
        self.db_mock.buscar.return_value = self.mock_informacion_ventas
        
        # Ejecutamos el método bajo prueba
        self.gestor.reporte_ventas()
        
        # Verificamos que se llamó a buscar con la tabla correcta
        self.db_mock.buscar.assert_called_once_with("ventas_por_producto")
        
        # Verificamos que se llamó a generarReportePDf con los argumentos correctos
        columnas_esperadas = ['Producto', 'precio unitario', 'unidades vendidas', 'cantidad de ventas', 'total vendido', 'stock en dinero']
        mock_generar_pdf.assert_called_once_with(columnas=columnas_esperadas, informacion=self.mock_informacion_ventas, nombre_reporte="reporte_inventario")

    @patch('builtins.input')
    def test_menu_generar_reporte(self, mock_input):
        # Configuramos las entradas para generar un reporte y luego salir
        mock_input.side_effect = ["1", "6"]
        
        # Mock para reporte_ventas
        with patch.object(self.gestor, 'reporte_ventas') as mock_reporte_ventas:
            # Ejecutamos el método bajo prueba
            self.gestor.menu()
            
            # Verificamos que se llamó a reporte_ventas
            mock_reporte_ventas.assert_called_once()

    @patch('builtins.input')
    def test_menu_salir(self, mock_input):
        # Configuramos la entrada para salir directamente
        mock_input.return_value = "6"
        
        # Ejecutamos el método bajo prueba
        with patch('builtins.print') as mock_print:
            self.gestor.menu()
        
        # Verificamos que se mostró el mensaje de salida
        mock_print.assert_called_with("saliendo")

if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gestorReporte import gestorReporte
from gestorVenta import GestorVenta
from datetime import datetime

class TestGestorVenta(unittest.TestCase):
    
    def setUp(self):
        # Creamos un mock para la base de datos
        self.db_mock = MagicMock()
        
        # Mocks para los gestores que usa GestorVenta
        self.gestorCliente_mock = MagicMock()
        self.gestorProductos_mock = MagicMock()
        
        # Creamos una instancia del gestor de ventas con los mocks
        self.gestor = GestorVenta(self.db_mock)
        self.gestor.gestorCliente = self.gestorCliente_mock
        self.gestor.gestorProductos = self.gestorProductos_mock
        
        # Datos de prueba
        self.cliente_data = [(1, '20123456-7', 'Cliente Test', 'Dirección Test', 987654321, 'cliente@test.com')]
        self.producto_data = [("1", 'Descripción Test', "10000", "50", 'Electrónica', 'Producto Test', "1")]
        self.metodo_pago_data = [(1, 'Efectivo', 10)]
        
        # Mock para la lista ordenada de id_venta
        self.id_venta_list = [(1,), (2,), (3,)]

    @patch('builtins.input')
    @patch('os.makedirs')
    @patch('gestorVenta.canvas.Canvas')
    def test_generar_recibo(self, mock_canvas, mock_makedirs, mock_input):
        # Configuramos los datos para generar el recibo
        cliente = {
            'nombre': 'Cliente Test',
            'rut': '20123456-7',
            'email': 'cliente@test.com',
            'telefono': '987654321'
        }
        productos = [
            {'nombre': 'Producto Test', 'cantidad': '2', 'precio': 10000}
        ]
        pagos = [
            {'metodo': 'Efectivo', 'monto': 20000, 'descuento': 0.1}
        ]
        
        # Mock para el objeto Canvas
        mock_canvas_obj = MagicMock()
        mock_canvas.return_value = mock_canvas_obj
        
        # Mock para datetime
        with patch('gestorVenta.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 4, 22, 10, 30, 0)
            mock_datetime.strftime = datetime.strftime
            
            # Ejecutamos el método bajo prueba
            self.gestor.generar_recibo(cliente, productos, pagos)
        
        # Verificamos que se creó el directorio recibos
        mock_makedirs.assert_called_once_with('recibos', exist_ok=True)
        
        # Verificamos que se creó el objeto Canvas
        mock_canvas.assert_called_once()
        
        # Verificamos que se guardó el recibo
        mock_canvas_obj.save.assert_called_once()

    @patch('builtins.input')
    @patch('gestorVenta.tabulate')
    def test_realizarVenta_exitosa(self, mock_tabulate, mock_input):
        # Configuramos las entradas para simular una venta exitosa
        mock_input.side_effect = lambda *args: next(iter([
            "1",              # ID cliente
            "1",              # ID producto
            "n",              # No agregar más productos
            "2",              # Cantidad de producto
            "s",              # Continuar con la venta
            "1",
            "n",              # Método de pago
            "100",            # 100% con ese método
            "s",              # Realizar el pago
        ] + ["n"]))            # No realizar otra compra
        
        # Configuramos los mocks para las consultas a la base de datos
        self.db_mock.buscar.side_effect = [
            self.cliente_data,          # Cliente
            self.producto_data,         # Producto
            self.metodo_pago_data,      # Métodos de pago
            self.id_venta_list,         # ID ventas
        ]
        
        # Mock para tabulate
        mock_tabulate.return_value = "Tabla formateada"
        
        # Patcheamos el método generar_recibo para evitar la generación real
        with patch.object(self.gestor, 'generar_recibo') as mock_generar_recibo:
            # Ejecutamos el método bajo prueba
            self.gestor.realizarVenta()
            
            # Verificamos que se llamó a generar_recibo
            mock_generar_recibo.assert_called_once()
            
        # Verificamos que se hicieron las inserciones en la base de datos
        # Debería haberse insertado en ventas, detalle_metodo_pago y detalle_ventas
        self.assertEqual(self.db_mock.insertar.call_count, 3)

    @patch('builtins.input')
    def test_realizarVenta_cancelada(self, mock_input):
        # Configuramos las entradas para simular una venta cancelada
        mock_input.side_effect = [
            "1",              # ID cliente
            "1",              # ID producto
            "n",              # No agregar más productos
            "2",              # Cantidad de producto
            "n",              # No continuar con la venta
        ]
        
        # Configuramos los mocks para las consultas a la base de datos
        self.db_mock.buscar.side_effect = [
            self.cliente_data,          # Cliente
            self.producto_data,         # Producto
        ]
        
        # Ejecutamos el método bajo prueba
        self.gestor.realizarVenta()
        
        # Verificamos que no se hicieron inserciones en la base de datos
        self.db_mock.insertar.assert_not_called()

    @patch('builtins.input')
    def test_menu_realizar_venta(self, mock_input):
        # Configuramos las entradas para realizar una venta y luego salir
        mock_input.side_effect = ["1", "6"]
        
        # Mock para realizarVenta
        with patch.object(self.gestor, 'realizarVenta') as mock_realizar_venta:
            # Ejecutamos el método bajo prueba
            self.gestor.menu()
            
            # Verificamos que se llamó a realizarVenta
            mock_realizar_venta.assert_called_once()

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
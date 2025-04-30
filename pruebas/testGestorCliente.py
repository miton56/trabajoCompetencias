import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch, MagicMock
from gestorcliente import GestorClientes

class TestGestorClientes(unittest.TestCase):
    # Configuración común para todas las pruebas
    TEST_MODE = "BÁSICO"  # Cambiar a "COMPLETO" para pruebas más exhaustivas
    
    def setUp(self):
        # Mock de la base de datos
        self.db_mock = MagicMock()
        self.gestor = GestorClientes(self.db_mock)
    
    @patch('builtins.input')
    def test_agregar_cliente(self, input_mock):
        # Configurar respuestas para los inputs
        if self.TEST_MODE == "BÁSICO":
            input_mock.side_effect = ['Juan Pérez', 'juan@email.com', '912345678', 'Calle 123', '12345678-9']
        else:
            input_mock.side_effect = ['Maria González', 'maria@email.com', '987654321', 'Av Principal 456', '98765432-1']
        
        # Configurar que el método insertar devuelva True (éxito)
        self.db_mock.insertar.return_value = True
        
        # Llamar al método que estamos probando
        self.gestor.agregar_cliente()
        
        # Verificar que el método insertar de la base de datos fue llamado con los argumentos correctos
        self.db_mock.insertar.assert_called_once()
        
        # Obtener los argumentos con los que se llamó el método
        args, kwargs = self.db_mock.insertar.call_args
        
        # Verificar que se pasó la tabla correcta y los datos correctos
        self.assertEqual(args[0], "clientes")  # Primera posición: nombre de la tabla
        
        # Verificar que los datos del cliente son correctos
        if self.TEST_MODE == "BÁSICO":
            self.assertEqual(args[1], ['12345678-9', 'Juan Pérez', 'Calle 123', '912345678', 'juan@email.com'])
        else:
            self.assertEqual(args[1], ['98765432-1', 'Maria González', 'Av Principal 456', '987654321', 'maria@email.com'])

    @patch('builtins.input')
    @patch('builtins.print')
    def test_buscar_cliente(self, print_mock, input_mock):
        # Configurar respuestas para los inputs en la búsqueda
        if self.TEST_MODE == "BÁSICO":
            input_mock.side_effect = ['3', 'Juan Pérez', 'n']  # Buscar por nombre
        else:
            input_mock.side_effect = ['2', '12345678-9', 'n']  # Buscar por RUT
        
        # Configurar resultado de búsqueda
        cliente_ejemplo = [(1, '12345678-9', 'Juan Pérez', 'Calle 123', 912345678, 'juan@email.com')]
        self.db_mock.buscar.return_value = cliente_ejemplo
        
        # Ejecutar la búsqueda
        self.gestor.buscar_cliente()
        
        # Verificar que el método buscar de la base de datos fue llamado
        self.db_mock.buscar.assert_called_once()
        
        # Verificar los parámetros de la búsqueda
        args, kwargs = self.db_mock.buscar.call_args
        self.assertEqual(args[0], "clientes")
        
        # Verificar condiciones de búsqueda según el modo de prueba
        if self.TEST_MODE == "BÁSICO":
            self.assertEqual(kwargs['condiciones'], {"Nombre": "Juan Pérez"})
        else:
            self.assertEqual(kwargs['condiciones'], {"rut": "12345678-9"})

    @patch('builtins.print')
    def test_listar_clientes(self, print_mock):
        # Configurar datos de prueba
        clientes = [
            (1, '12345678-9', 'Juan Pérez', 'Calle 123', 912345678, 'juan@email.com'),
            (2, '98765432-1', 'Maria González', 'Av Principal 456', 987654321, 'maria@email.com')
        ]
        
        # Configurar el mock para que devuelva los clientes
        self.db_mock.buscar.return_value = clientes
        
        # Ejecutar el método a probar
        self.gestor.listar_clientes()
        
        # Verificar que el método buscar fue llamado con los parámetros correctos
        self.db_mock.buscar.assert_called_once_with("clientes")

    @patch('builtins.input')
    def test_actualizar_cliente(self, input_mock):
        # ID del cliente a actualizar
        id_cliente = 1
        
        # Cliente existente en la base de datos
        cliente_existente = [(1, '12345678-9', 'Juan Pérez', 'Calle 123', 912345678, 'juan@email.com')]
        
        # Configurar entradas del usuario
        if self.TEST_MODE == "BÁSICO":
            # Solo actualizar el email
            input_mock.side_effect = [str(id_cliente), '', '', '', '', 'nuevo@email.com']
            actualizaciones_esperadas = {"correo": "nuevo@email.com"}
        else:
            # Actualizar varios campos
            input_mock.side_effect = [str(id_cliente), '98765432-1', 'Juan Actualizado', 'Nueva Dirección', '999999999', 'nuevo@email.com']
            actualizaciones_esperadas = {
                "rut": "98765432-1", 
                "nombre": "Juan Actualizado", 
                "direccion": "Nueva Dirección", 
                "telefono": "999999999", 
                "correo": "nuevo@email.com"
            }
        
        # Configurar mock para la búsqueda y actualización
        self.db_mock.buscar.return_value = cliente_existente
        self.db_mock.actualizar.return_value = True
        
        # Ejecutar el método a probar
        self.gestor.actualizar_cliente()
        
        # Verificar que el método buscar fue llamado con los parámetros correctos
        self.db_mock.buscar.assert_called_once()
        buscar_args, buscar_kwargs = self.db_mock.buscar.call_args
        self.assertEqual(buscar_kwargs['condiciones'], {"id_cliente": id_cliente})
        
        # Verificar que el método actualizar fue llamado con los parámetros correctos
        self.db_mock.actualizar.assert_called_once()
        actualizar_args, actualizar_kwargs = self.db_mock.actualizar.call_args
        
        # Verificar tabla y condiciones
        self.assertEqual(actualizar_args[0], "clientes")
        self.assertEqual(actualizar_args[1], {"id_cliente": id_cliente})
        
        # Verificar actualizaciones según el modo de prueba
        for key, value in actualizaciones_esperadas.items():
            self.assertEqual(actualizar_args[2][key], value)

    @patch('builtins.input')
    def test_eliminar_cliente(self, input_mock):
        # ID del cliente a eliminar
        id_cliente = 1
        
        # Cliente existente en la base de datos
        cliente_existente = [(1, '12345678-9', 'Juan Pérez', 'Calle 123', 912345678, 'juan@email.com')]
        
        # Configurar entradas del usuario: ID y confirmación
        input_mock.side_effect = [str(id_cliente), 's']
        
        # Configurar mock para la búsqueda y eliminación
        self.db_mock.buscar.return_value = cliente_existente
        self.db_mock.eliminar.return_value = True
        
        # Ejecutar el método a probar
        self.gestor.eliminar_cliente()
        
        # Verificar que el método buscar fue llamado con los parámetros correctos
        self.db_mock.buscar.assert_called_once()
        buscar_args, buscar_kwargs = self.db_mock.buscar.call_args
        self.assertEqual(buscar_kwargs['condiciones'], {"id_cliente": id_cliente})
        
        # Verificar que el método eliminar fue llamado con los parámetros correctos
        self.db_mock.eliminar.assert_called_once()
        eliminar_args, eliminar_kwargs = self.db_mock.eliminar.call_args
        self.assertEqual(eliminar_args[0], "clientes")
        self.assertEqual(eliminar_args[1], {"id_cliente": id_cliente})

    @patch('builtins.input')
    @patch('builtins.print')
    def test_menu(self, print_mock, input_mock):
        # Probar el menú con la opción de salir directamente
        input_mock.side_effect = ['6']
        
        # Ejecutar el menú
        self.gestor.menu()
        
        # No necesitamos verificar llamadas a la base de datos aquí
        # ya que solo estamos probando la navegación del menú

if __name__ == '__main__':
    unittest.main()
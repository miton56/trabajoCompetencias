import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch, MagicMock
from gestorInventario import GestorProductos
from enum import Enum

class TestGestorProductos(unittest.TestCase):
    # Configuración común para todas las pruebas
    TEST_MODE = "BÁSICO"  # Cambiar a "COMPLETO" para pruebas más exhaustivas
    
    def setUp(self):
        # Mock de la base de datos
        self.db_mock = MagicMock()
        
        # Mock para las categorías base
        if self.TEST_MODE == "BÁSICO":
            self.db_mock.buscar.return_value = [("Tecnología",), ("Computación",)]
        else:
            self.db_mock.buscar.return_value = [("Tecnología",), ("Computación",), ("Calzado",), ("Electrodomésticos",)]
        
        # Crear el gestor de productos
        self.gestor = GestorProductos(self.db_mock)
        
        # Redefinir el mock de búsqueda después de inicializar el gestor
        # para evitar que el constructor afecte nuestras pruebas
        self.db_mock.buscar.reset_mock()
    
    @patch('builtins.input')
    @patch('gestorInventario.GestorProveedor')
    def test_agregar_producto(self, gestor_proveedor_mock, input_mock):
        # Mock para el GestorProveedor
        gestor_proveedor_instance = MagicMock()
        gestor_proveedor_mock.return_value = gestor_proveedor_instance
        
        # Configurar el mock para listar_proveedores
        gestor_proveedor_instance.listar_proveedores.return_value = [("1", '76451234-5', 'Distribuidora El Sol')]
        
        # Configurar respuestas para los inputs
        if self.TEST_MODE == "BÁSICO":
            input_mock.side_effect = [
                'Smartphone XYZ',              # nombre
                'Smartphone de última gen',    # descripción
                '200000',                      # precio
                '10',                          # stock
                '1',                           # id_proveedor
                '1'                            # categoría (1: Tecnología)
            ]
        else:
            input_mock.side_effect = [
                'Notebook ABC',                # nombre
                'Notebook potente',            # descripción
                '500000',                      # precio
                '5',                           # stock
                '1',                           # id_proveedor
                '2'                            # categoría (2: Computación)
            ]
        
        # Configurar que el método insertar devuelva True (éxito)
        self.db_mock.insertar.return_value = True
        
        # Llamar al método que estamos probando
        self.gestor.agregar_producto()
        
        # Verificar que el método insertar de la base de datos fue llamado
        self.db_mock.insertar.assert_called_once()
        
        # Obtener los argumentos con los que se llamó el método
        args, kwargs = self.db_mock.insertar.call_args
        
        # Verificar que se pasó la tabla correcta
        self.assertEqual(args[0], "productos")  # Primera posición: nombre de la tabla
        
        # Verificar columnas
        expected_columns = ["nombre", "descripcion", "precio", "cantidad_stock", "categoria", "id_proveedor"]
        self.assertEqual(args[2], expected_columns)
        
        # Verificar valores según el modo de prueba
        if self.TEST_MODE == "BÁSICO":
            expected_values = ['Smartphone XYZ', 'Smartphone de última gen', '200000', '10', 'Tecnología', '1']
        else:
            expected_values = ['Notebook ABC', 'Notebook potente', '500000', '5', 'Computación', '1']
        
        self.assertEqual(args[1], expected_values)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_buscar_producto(self, print_mock, input_mock):
        # Configurar respuestas para los inputs en la búsqueda
        if self.TEST_MODE == "BÁSICO":
            input_mock.side_effect = ['5', 'Smartphone XYZ', 'n']  # Buscar por nombre
        else:
            input_mock.side_effect = ['1', '1', 'n']  # Buscar por ID
        
        # Configurar resultado de búsqueda
        producto_ejemplo = [("1", 'Smartphone de última gen', "200000", "10", 'Tecnología', 'Smartphone XYZ', "1")]
        self.db_mock.buscar.return_value = producto_ejemplo
        
        # Ejecutar la búsqueda
        self.gestor.buscar_producto()
        
        # Verificar que el método buscar de la base de datos fue llamado
        self.assertTrue(self.db_mock.buscar.called)
        
        # Obtener la última llamada al método buscar
        args, kwargs = self.db_mock.buscar.call_args_list[-1]
        self.assertEqual(args[0], "productos")
        
        # Verificar condiciones de búsqueda según el modo de prueba
        if self.TEST_MODE == "BÁSICO":
            self.assertEqual(kwargs['condiciones'], {"Nombre": "Smartphone XYZ"})
        else:
            self.assertEqual(kwargs['condiciones'], {"id_producto": "1"})

    @patch('builtins.print')
    def test_listar_productos(self, print_mock):
        # Configurar datos de prueba
        productos = [
            (1, 'Smartphone de última gen', "200000", "10", 'Tecnología', 'Smartphone XYZ', "1"),
            (2, 'Notebook potente', "500000", "5", 'Computación', 'Notebook ABC', "2")
        ]
        
        # Configurar el mock para que devuelva los productos
        self.db_mock.buscar.return_value = productos
        
        # Ejecutar el método a probar
        self.gestor.listar_productos()
        
        # Verificar que el método buscar fue llamado con los parámetros correctos
        self.db_mock.buscar.assert_called_with("productos")

    @patch('builtins.input')
    def test_actualizar_producto(self, input_mock):
        # ID del producto a actualizar
        id_producto = 1
        
        # Producto existente en la base de datos
        producto_existente = [(1, 'Smartphone de última gen', "200000", "10", 'Tecnología', 'Smartphone XYZ', "1")]
        
        # Configurar entradas del usuario
        if self.TEST_MODE == "BÁSICO":
            # Solo actualizar el precio
            input_mock.side_effect = [str(id_producto), '', '', '220000', '', '']
            actualizaciones_esperadas = {"precio": "220000"}
        else:
            # Actualizar varios campos
            input_mock.side_effect = [str(id_producto), 'Smartphone XYZ Pro', 'Versión mejorada', '250000', '8', 'Tecnología Premium']
            actualizaciones_esperadas = {
                "nombre": "Smartphone XYZ Pro",
                "descripcion": "Versión mejorada",
                "precio": "250000",
                "cantidad_stock": "8",
                "categoria": "Tecnología Premium"
            }
        
        # Configurar mock para la búsqueda y actualización
        self.db_mock.buscar.return_value = producto_existente
        self.db_mock.actualizar.return_value = True
        
        # Ejecutar el método a probar
        self.gestor.actualizar_producto()
        
        # Verificar que el método buscar fue llamado con los parámetros correctos
        buscar_args_list = self.db_mock.buscar.call_args_list
        self.assertEqual(buscar_args_list[0][1]['condiciones'], {"id_producto": id_producto})
        
        # Verificar que el método actualizar fue llamado con los parámetros correctos
        self.db_mock.actualizar.assert_called_once()
        actualizar_args, actualizar_kwargs = self.db_mock.actualizar.call_args
        
        # Verificar tabla y condiciones
        self.assertEqual(actualizar_args[0], "productos")
        self.assertEqual(actualizar_args[1], {"id_producto": id_producto})
        
        # Verificar actualizaciones según el modo de prueba
        for key, value in actualizaciones_esperadas.items():
            self.assertEqual(actualizar_args[2][key], value)

    @patch('builtins.input')
    def test_eliminar_producto(self, input_mock):
        # ID del producto a eliminar
        id_producto = 1
        
        # Producto existente en la base de datos
        producto_existente = [(1, 'Smartphone de última gen', "200000", "10", 'Tecnología', 'Smartphone XYZ', "1")]
        
        # Configurar entradas del usuario: ID y confirmación
        input_mock.side_effect = [str(id_producto), 's']
        
        # Configurar mock para la búsqueda y eliminación
        self.db_mock.buscar.return_value = producto_existente
        self.db_mock.eliminar.return_value = True
        
        # Ejecutar el método a probar
        self.gestor.eliminar_producto()
        
        # Verificar que el método buscar fue llamado con los parámetros correctos
        buscar_args_list = self.db_mock.buscar.call_args_list
        self.assertEqual(buscar_args_list[0][1]['condiciones'], {"id_producto": id_producto})
        
        # Verificar que el método eliminar fue llamado con los parámetros correctos
        self.db_mock.eliminar.assert_called_once()
        eliminar_args, eliminar_kwargs = self.db_mock.eliminar.call_args
        self.assertEqual(eliminar_args[0], "productos")
        self.assertEqual(eliminar_args[1], {"id_producto": id_producto})

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
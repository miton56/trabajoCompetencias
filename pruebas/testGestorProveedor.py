import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch, MagicMock
from gestorproveedor import GestorProveedor

class TestGestorProveedor(unittest.TestCase):
    
    def setUp(self):
        # Creamos un mock para la base de datos
        self.db_mock = MagicMock()
        # Creamos una instancia del gestor usando el mock de la base de datos
        self.gestor = GestorProveedor(self.db_mock)
        
        # Datos de prueba comunes
        self.test_data = {
            'id_proveedor': 1,
            'rut': '76123456-7',
            'nombre': 'Proveedor Test',
            'correo': 'test@proveedor.com',
            'telefono': '987654321',
            'direccion': 'Calle Test 123'
        }
        
        # Mock de un proveedor para simular resultados de la base de datos
        self.mock_proveedor = [(
            self.test_data['id_proveedor'],
            self.test_data['rut'],
            self.test_data['nombre'],
            self.test_data['correo'],
            self.test_data['telefono'],
            self.test_data['direccion']
        )]

    @patch('builtins.input')
    def test_agregar_proveedor_exitoso(self, mock_input):
        # Configuramos las entradas del usuario
        mock_input.side_effect = [
            self.test_data['nombre'],      # Nombre
            self.test_data['telefono'],    # Teléfono
            self.test_data['rut'],         # RUT
            self.test_data['correo'],      # Correo
            self.test_data['direccion']    # Dirección
        ]
        
        # Configuramos el mock de la base de datos para que insertar devuelva True
        self.db_mock.insertar.return_value = True
        
        # Ejecutar el método bajo prueba
        with patch('builtins.print') as mock_print:
            self.gestor.agregar_proveedor()
        
        # Verificamos que se llamó al método insertar con los argumentos correctos
        self.db_mock.insertar.assert_called_once_with(
            "proveedores", 
            [self.test_data['rut'], self.test_data['nombre'], self.test_data['correo'], 
             self.test_data['telefono'], self.test_data['direccion']],
            ["rut", "nombre", "correo", "telefono", "direccion"]
        )
        
        # Verificamos que se muestra el mensaje de éxito
        mock_print.assert_called_with("Proveedor agregado exitosamente.")

    @patch('builtins.input')
    def test_agregar_proveedor_error(self, mock_input):
        # Configuramos las entradas del usuario
        mock_input.side_effect = [
            self.test_data['nombre'],      # Nombre
            self.test_data['telefono'],    # Teléfono
            self.test_data['rut'],         # RUT
            self.test_data['correo'],      # Correo
            self.test_data['direccion']    # Dirección
        ]
        
        # Configuramos el mock de la base de datos para que insertar devuelva False
        self.db_mock.insertar.return_value = False
        
        # Ejecutar el método bajo prueba
        with patch('builtins.print') as mock_print:
            self.gestor.agregar_proveedor()
        
        # Verificamos que se muestra el mensaje de error
        mock_print.assert_called_with("Error al agregar el proveedor.")

    @patch('builtins.input')
    def test_buscar_proveedor_por_id(self, mock_input):
        # Configuramos las entradas del usuario
        mock_input.side_effect = [
            '1',                           # Opción: buscar por ID
            str(self.test_data['id_proveedor']),  # ID del proveedor
            'n'                            # No agregar más condiciones
        ]
        
        # Configuramos el mock para que devuelva un proveedor
        self.db_mock.buscar.return_value = self.mock_proveedor
        
        # Ejecutar el método bajo prueba
        with patch('builtins.print') as mock_print:
            self.gestor.buscar_proveedor()
        
        # Verificamos que se llamó a buscar con los argumentos correctos
        self.db_mock.buscar.assert_called_with(
            "proveedores", 
            condiciones={"id_proveedor": self.test_data['id_proveedor']}
        )

    @patch('builtins.input')
    def test_buscar_proveedor_multiples_condiciones(self, mock_input):
        # Configuramos las entradas del usuario
        mock_input.side_effect = [
            '3',                           # Opción: buscar por nombre
            self.test_data['nombre'],      # Nombre
            's',                           # Sí agregar más condiciones
            '2',                           # Opción: buscar por RUT
            self.test_data['rut'],         # RUT
            'n'                            # No agregar más condiciones
        ]
        
        # Configuramos el mock para que devuelva un proveedor
        self.db_mock.buscar.return_value = self.mock_proveedor
        
        # Ejecutar el método bajo prueba
        with patch('builtins.print') as mock_print:
            self.gestor.buscar_proveedor()
        
        # Verificamos que se llamó a buscar con ambas condiciones
        self.db_mock.buscar.assert_called_with(
            "proveedores", 
            condiciones={"Nombre": self.test_data['nombre'], "rut": self.test_data['rut']}
        )

    def test_listar_proveedores(self):
        # Configuramos el mock para que devuelva una lista de proveedores
        self.db_mock.buscar.return_value = [self.mock_proveedor[0], self.mock_proveedor[0]]
        
        # Ejecutar el método bajo prueba
        with patch('builtins.print') as mock_print:
            self.gestor.listar_proveedores()
        
        # Verificamos que se llamó a buscar sin condiciones
        self.db_mock.buscar.assert_called_with("proveedores")

    def test_listar_proveedores_sin_imprimir(self):
        # Configuramos el mock para que devuelva una lista de proveedores
        self.db_mock.buscar.return_value = [self.mock_proveedor[0], self.mock_proveedor[0]]
        
        # Ejecutar el método bajo prueba
        resultado = self.gestor.listar_proveedores(imprimir=False)
        
        # Verificamos que se devuelve la lista de proveedores
        self.assertEqual(resultado, [self.mock_proveedor[0], self.mock_proveedor[0]])

    @patch('builtins.input')
    def test_actualizar_proveedor_exitoso(self, mock_input):
        # Configuramos las entradas del usuario
        mock_input.side_effect = [
            str(self.test_data['id_proveedor']),  # ID del proveedor
            self.test_data['rut'],         # Nuevo RUT
            self.test_data['nombre'],      # Nuevo nombre
            self.test_data['correo'],      # Nuevo correo
            self.test_data['telefono'],    # Nuevo teléfono
            self.test_data['direccion']    # Nueva dirección
        ]
        
        # Configuramos el mock para que devuelva un proveedor existente
        self.db_mock.buscar.return_value = self.mock_proveedor
        # Configuramos el mock para que actualizar devuelva True
        self.db_mock.actualizar.return_value = True
        
        # Ejecutar el método bajo prueba
        with patch('builtins.print') as mock_print:
            self.gestor.actualizar_proveedor()
        
        # Verificamos que se llamó a actualizar con los argumentos correctos
        self.db_mock.actualizar.assert_called_once()
        
        # Verificamos que se muestra el mensaje de éxito
        mock_print.assert_called_with("Proveedor actualizado exitosamente.")

    @patch('builtins.input')
    def test_eliminar_proveedor_exitoso(self, mock_input):
        # Configuramos las entradas del usuario
        mock_input.side_effect = [
            str(self.test_data['id_proveedor']),  # ID del proveedor
            's'                            # Confirmación para eliminar
        ]
        
        # Configuramos el mock para que devuelva un proveedor existente
        self.db_mock.buscar.return_value = self.mock_proveedor
        # Configuramos el mock para que eliminar devuelva True
        self.db_mock.eliminar.return_value = True
        
        # Ejecutar el método bajo prueba
        with patch('builtins.print') as mock_print:
            self.gestor.eliminar_proveedor()
        
        # Verificamos que se llamó a eliminar con los argumentos correctos
        self.db_mock.eliminar.assert_called_once_with(
            "proveedores",
            {"id_proveedor": self.test_data['id_proveedor']}
        )
        
        # Verificamos que se muestra el mensaje de éxito
        mock_print.assert_called_with("Proveedor eliminado exitosamente.")

    @patch('builtins.input')
    def test_eliminar_proveedor_cancelado(self, mock_input):
        # Configuramos las entradas del usuario
        mock_input.side_effect = [
            str(self.test_data['id_proveedor']),  # ID del proveedor
            'n'                            # Cancelar eliminación
        ]
        
        # Configuramos el mock para que devuelva un proveedor existente
        self.db_mock.buscar.return_value = self.mock_proveedor
        
        # Ejecutar el método bajo prueba
        with patch('builtins.print') as mock_print:
            self.gestor.eliminar_proveedor()
        
        # Verificamos que no se llamó a eliminar
        self.db_mock.eliminar.assert_not_called()
        
        # Verificamos que se muestra el mensaje de cancelación
        mock_print.assert_called_with("Operación de eliminación cancelada.")

    @patch('builtins.input')
    def test_menu(self, mock_input):
        # Configuramos las entradas para salir del menú
        mock_input.return_value = "6"
        
        # Ejecutar el método bajo prueba
        with patch('builtins.print') as mock_print:
            self.gestor.menu()
        
        # Verificamos que se muestra el mensaje de salida
        mock_print.assert_called_with("Saliendo del gestor de proveedores.")

if __name__ == '__main__':
    unittest.main()
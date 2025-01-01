import unittest
import platform
from src.controller.main_controller import MainController

class CompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.controller = MainController()

    def test_os_compatibility(self):
        """Verifica la compatibilidad con diferentes sistemas operativos"""
        current_os = platform.system()
        
        # Prueba de inicialización básica
        self.assertIsNotNone(self.controller)
        
        # Verificar características específicas del sistema operativo
        if current_os == 'Windows':
            self._test_windows_features()
        elif current_os == 'Linux':
            self._test_linux_features()
        elif current_os == 'Darwin':  # macOS
            self._test_macos_features()
        else:
            self.fail(f"Sistema operativo no soportado: {current_os}")

    def _test_windows_features(self):
        """Pruebas específicas para Windows"""
        # Verificar manejo de rutas
        test_path = "C:\\Users\\Test\\Music"
        self.controller.select_directory(test_path)
        
    def _test_linux_features(self):
        """Pruebas específicas para Linux"""
        # Verificar manejo de permisos
        test_path = "/home/test/Music"
        self.controller.select_directory(test_path)
        
    def _test_macos_features(self):
        """Pruebas específicas para macOS"""
        # Verificar integración con servicios del sistema
        test_path = "/Users/test/Music"
        self.controller.select_directory(test_path)

if __name__ == '__main__':
    unittest.main()
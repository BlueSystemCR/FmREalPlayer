import unittest
from pathlib import Path
from src.controller.main_controller import MainController

class UsabilityTests(unittest.TestCase):
    def setUp(self):
        self.controller = MainController()
        self.test_dir = Path('tests/usability_data')
        self.test_dir.mkdir(exist_ok=True)
        
        # Crear archivos de prueba
        self.test_files = [
            self.test_dir / 'test1.mp3',
            self.test_dir / 'test2.mp3',
            self.test_dir / 'test3.mp3'
        ]
        for file in self.test_files:
            file.touch()

    def test_main_workflow(self):
        """Prueba el flujo principal de uso"""
        # 1. Abrir directorio
        self.controller.select_directory(str(self.test_dir))
        self.assertTrue(len(self.controller.file_manager.scan_directory(str(self.test_dir))) > 0)
        
        # 2. Reproducir música
        self.controller.play_track({'path': str(self.test_files[0])})
        self.assertEqual(self.controller.state_manager.current_status.state, PlayerState.PLAYING)
        
        # 3. Seleccionar tracks
        selected_files = [str(self.test_files[0]), str(self.test_files[1])]
        self.controller.file_manager.move_selected_files(selected_files, str(self.test_dir / 'moved'))
        self.assertTrue((self.test_dir / 'moved').exists())
        self.assertTrue(len(list((self.test_dir / 'moved').iterdir())) == 2)

    def test_error_handling(self):
        """Prueba el manejo de errores"""
        # Archivo inválido
        with self.assertRaises(Exception):
            self.controller.play_track({'path': 'invalid_file.mp3'})
        
        # Permisos denegados
        with self.assertRaises(Exception):
            self.controller.select_directory('/root')

    def tearDown(self):
        # Limpiar archivos de prueba
        for p in self.test_dir.rglob('*'):
            if p.is_file():
                p.unlink()
        for p in self.test_dir.rglob('*'):
            if p.is_dir():
                p.rmdir()
        self.test_dir.rmdir()

if __name__ == '__main__':
    unittest.main()
import unittest
import os
import time
from pathlib import Path
from src.controller.main_controller import MainController
from src.core.player_state import PlayerState

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.controller = MainController()
        self.test_dir = Path('tests/integration_data')
        self.test_dir.mkdir(exist_ok=True)
        
        # Crear archivos de prueba
        self.test_files = [
            self.test_dir / 'test1.mp3',
            self.test_dir / 'test2.mp3',
            self.test_dir / 'test3.mp3'
        ]
        for file in self.test_files:
            file.touch()

    def test_full_workflow(self):
        """Prueba el flujo completo de la aplicación"""
        # 1. Cargar directorio
        self.controller.select_directory(str(self.test_dir))
        self.assertTrue(len(self.controller.file_manager.scan_directory(str(self.test_dir))) > 0)
        
        # 2. Seleccionar y reproducir track
        self.controller.play_track({'path': str(self.test_files[0])})
        self.assertEqual(self.controller.state_manager.current_status.state, PlayerState.PLAYING)
        
        # 3. Pausar reproducción
        self.controller.playPause()
        self.assertEqual(self.controller.state_manager.current_status.state, PlayerState.PAUSED)
        
        # 4. Mover archivos seleccionados
        selected_files = [str(self.test_files[0]), str(self.test_files[1])]
        self.controller.file_manager.move_selected_files(selected_files, str(self.test_dir / 'moved'))
        self.assertTrue((self.test_dir / 'moved').exists())
        self.assertTrue(len(list((self.test_dir / 'moved').iterdir())) == 2)

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
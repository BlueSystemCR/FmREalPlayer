import unittest
import os
import time
from pathlib import Path
from src.controller.main_controller import MainController
from src.core.player_state import PlayerState
from src.utils.file_manager import FileManager

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        self.controller = MainController()
        self.test_dir = Path('tests/test_data')
        self.test_dir.mkdir(exist_ok=True)
        
        # Crear archivos de prueba
        self.test_files = [
            self.test_dir / 'test1.mp3',
            self.test_dir / 'test2.mp3',
            self.test_dir / 'test3.mp3'
        ]
        for file in self.test_files:
            file.touch()

    def test_directory_loading(self):
        """Prueba la carga de un directorio"""
        # Prueba de carga exitosa
        self.controller.select_directory(str(self.test_dir))
        self.assertTrue(len(self.controller.file_manager.scan_directory(str(self.test_dir))) > 0)
        
        # Prueba de directorio inválido
        with self.assertRaises(Exception):
            self.controller.select_directory('invalid_path')

    def test_playback_controls(self):
        """Prueba los controles de reproducción"""
        # Cargar archivo
        self.controller.play_track({'path': str(self.test_files[0])})
        
        # Prueba play/pause
        self.controller.playPause()
        self.assertEqual(self.controller.state_manager.current_status.state, PlayerState.PLAYING)
        
        self.controller.playPause()
        self.assertEqual(self.controller.state_manager.current_status.state, PlayerState.PAUSED)
        
        # Prueba seek
        self.controller.player.seek(10)
        self.assertAlmostEqual(self.controller.player.get_position(), 10, delta=0.5)
        
        # Prueba volumen
        self.controller.player.set_volume(50)
        self.assertEqual(self.controller.player.volume, 50)

    def test_file_operations(self):
        """Prueba las operaciones con archivos"""
        # Prueba selección de archivos
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
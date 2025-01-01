import unittest
import os
import time
import psutil
from pathlib import Path
from src.controller.main_controller import MainController

class PerformanceTests(unittest.TestCase):
    def setUp(self):
        self.controller = MainController()
        self.test_dir = Path('tests/performance_data')
        self.test_dir.mkdir(exist_ok=True)
        
        # Crear archivos de prueba
        self.test_files = [self.test_dir / f'test{i}.mp3' for i in range(1000)]
        for file in self.test_files:
            file.touch()

    def test_directory_loading_time(self):
        """Mide el tiempo de carga de directorios de diferentes tamaños"""
        # 100 archivos
        start_time = time.time()
        self.controller.select_directory(str(self.test_dir))
        load_time_100 = time.time() - start_time
        print(f"\nTiempo de carga (1000 archivos): {load_time_100:.2f}s")

    def test_memory_usage(self):
        """Mide el uso de memoria en diferentes operaciones"""
        process = psutil.Process(os.getpid())
        
        # Memoria base
        base_memory = process.memory_info().rss / 1024 / 1024
        
        # Memoria durante carga
        self.controller.select_directory(str(self.test_dir))
        load_memory = process.memory_info().rss / 1024 / 1024
        print(f"\nUso de memoria (carga): {load_memory - base_memory:.2f} MB")
        
        # Memoria durante reproducción
        self.controller.play_track({'path': str(self.test_files[0])})
        play_memory = process.memory_info().rss / 1024 / 1024
        print(f"Uso de memoria (reproducción): {play_memory - base_memory:.2f} MB")

    def test_ui_responsiveness(self):
        """Mide la respuesta de la interfaz"""
        # Tiempo de respuesta para selección múltiple
        start_time = time.time()
        self.controller.file_manager.move_selected_files(
            [str(self.test_files[0]), str(self.test_files[1])],
            str(self.test_dir / 'moved')
        )
        operation_time = time.time() - start_time
        print(f"\nTiempo de operación (mover archivos): {operation_time:.2f}s")

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
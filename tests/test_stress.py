import unittest
import os
import time
import psutil
from pathlib import Path
from src.controller.main_controller import MainController

class StressTests(unittest.TestCase):
    def setUp(self):
        self.controller = MainController()
        self.test_dir = Path('tests/stress_data')
        self.test_dir.mkdir(exist_ok=True)
        
        # Crear 5000 archivos de prueba
        self.test_files = [self.test_dir / f'test{i}.mp3' for i in range(5000)]
        for file in self.test_files:
            file.touch()

    def test_large_directory_load(self):
        """Prueba la carga de un directorio muy grande"""
        start_time = time.time()
        self.controller.select_directory(str(self.test_dir))
        load_time = time.time() - start_time
        print(f"\nTiempo de carga (5000 archivos): {load_time:.2f}s")
        self.assertTrue(load_time < 5)  # Objetivo: menos de 5 segundos

    def test_memory_usage_during_playback(self):
        """Mide el uso de memoria durante reproducción prolongada"""
        process = psutil.Process(os.getpid())
        
        # Memoria base
        base_memory = process.memory_info().rss / 1024 / 1024
        
        # Reproducir durante 5 minutos
        self.controller.play_track({'path': str(self.test_files[0])})
        time.sleep(300)  # 5 minutos
        playback_memory = process.memory_info().rss / 1024 / 1024
        print(f"\nUso de memoria (reproducción prolongada): {playback_memory - base_memory:.2f} MB")
        self.assertTrue(playback_memory - base_memory < 50)  # Objetivo: menos de 50 MB

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
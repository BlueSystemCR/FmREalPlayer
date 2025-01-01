import unittest
import os
from pathlib import Path
from src.model.track_model import Track
from src.utils.metadata_reader import MetadataReader
from src.utils.file_manager import FileManager

class TestTrackModel(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path('tests/test_data')
        self.test_dir.mkdir(exist_ok=True)
        
        # Crear archivo de prueba
        self.test_file = self.test_dir / 'test.mp3'
        self.test_file.touch()
        
        self.track = Track()
        self.metadata_reader = MetadataReader()
        self.file_manager = FileManager()

    def test_track_creation(self):
        self.track.file_path = str(self.test_file)
        self.track.title = "Test Track"
        self.assertTrue(self.track.validate())
        
    def test_metadata_reading(self):
        metadata = self.metadata_reader.read_metadata(str(self.test_file))
        self.assertIsNotNone(metadata)
        
    def test_file_operations(self):
        files = self.file_manager.scan_directory(str(self.test_dir))
        self.assertIn(str(self.test_file), files)
        
        new_dir = self.test_dir / 'new_dir'
        self.assertTrue(self.file_manager.move_selected_files(
            [str(self.test_file)], str(new_dir)
        ))
        
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
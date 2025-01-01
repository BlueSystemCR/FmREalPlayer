import unittest
import os
from pathlib import Path
from src.model.track_model import Track
from src.utils.metadata_reader import MetadataReader
from src.utils.file_manager import FileManager

class TestTrackModel(unittest.TestCase):
    def setUp(self):
        # Use environment variable for audio test path
        self.audio_path = Path(os.environ.get('AUDIO_TEST_PATH', 'tests/test_data'))
        self.audio_path.mkdir(exist_ok=True)
        
        # Use first available audio file for testing
        audio_files = list(self.audio_path.glob('*.mp3'))
        if audio_files:
            self.test_file = audio_files[0]
        else:
            # Fallback to test file if no audio files found
            self.test_file = self.audio_path / 'test.mp3'
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
        # Accept either valid metadata or None, but no exceptions
        if metadata is not None:
            self.assertIsInstance(metadata, dict)
        
    def test_file_operations(self):
        files = self.file_manager.scan_directory(str(self.audio_path))
        self.assertIn(str(self.test_file), files)
        
        new_dir = self.audio_path / 'new_dir'
        self.assertTrue(self.file_manager.move_selected_files(
            [str(self.test_file)], str(new_dir)
        ))
        
    def tearDown(self):
        # Limpiar archivos de prueba
        for p in self.audio_path.rglob('*'):
            if p.is_file():
                p.unlink()
        for p in self.audio_path.rglob('*'):
            if p.is_dir():
                p.rmdir()
        self.audio_path.rmdir()

if __name__ == '__main__':
    unittest.main()
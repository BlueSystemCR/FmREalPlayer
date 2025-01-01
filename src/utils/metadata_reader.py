import logging
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from pathlib import Path

class MetadataReader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def read_metadata(self, file_path):
        """Lee los metadatos de un archivo de audio"""
        try:
            if not Path(file_path).exists():
                self.logger.error(f"Archivo no encontrado: {file_path}")
                return None
                
            audio = File(file_path, easy=True)
            
            if audio is None:
                self.logger.error(f"Formato no soportado: {file_path}")
                return None
                
            track = {
                'title': audio.get('title', [''])[0],
                'artist': audio.get('artist', [''])[0],
                'album': audio.get('album', [''])[0],
                'year': audio.get('date', [''])[0],
                'duration': audio.info.length if hasattr(audio, 'info') else 0
            }
            
            self.logger.info(f"Metadatos leídos: {file_path}")
            return track
            
        except Exception as e:
            self.logger.error(f"Error leyendo metadatos: {str(e)}")
            return None
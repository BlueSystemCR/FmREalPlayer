import sys
from PySide6.QtWidgets import QApplication
import vlc
from utils.logger import setup_logger
from src.model.track_model import Track
from src.utils.metadata_reader import MetadataReader
from src.utils.file_manager import FileManager

class MusicManagerApp:
    def __init__(self):
        self.logger = setup_logger()
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()
        self.metadata_reader = MetadataReader()
        self.file_manager = FileManager()
        
        self.logger.info("Music Manager iniciado")

    def play(self, file_path):
        try:
            media = self.vlc_instance.media_new(file_path)
            self.player.set_media(media)
            self.player.play()
            
            # Leer metadatos
            track = Track()
            track.file_path = file_path
            metadata = self.metadata_reader.read_metadata(file_path)
            if metadata:
                track.title = metadata.get('title', '')
                track.artist = metadata.get('artist', '')
                track.album = metadata.get('album', '')
                track.duration = metadata.get('duration', 0)
                
            self.logger.info(f"Reproduciendo: {track}")
            
        except Exception as e:
            self.logger.error(f"Error al reproducir: {str(e)}")

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        music_app = MusicManagerApp()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error crítico: {str(e)}")
        sys.exit(1)
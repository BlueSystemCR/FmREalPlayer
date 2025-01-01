import logging

class Track:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.file_path = ""
        self.title = ""
        self.artist = ""
        self.album = ""
        self.year = ""
        self.comments = ""
        self.duration = 0
        self.selected = False
        
    def __str__(self):
        return f"{self.artist} - {self.title} ({self.album})"
        
    def validate(self):
        """Valida los datos básicos del track"""
        if not self.file_path:
            self.logger.error("Track sin ruta de archivo")
            return False
        if not self.title:
            self.logger.warning("Track sin título")
        return True
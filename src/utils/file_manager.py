import logging
import os
from pathlib import Path
from typing import List

class FileManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def scan_directory(self, path: str = None) -> List[str]:
        """Escanea un directorio en busca de archivos de audio.
        Si no se proporciona un path, usa AUDIO_TEST_PATH del entorno."""
        try:
            scan_path = Path(path) if path else Path(os.environ.get('AUDIO_TEST_PATH', '.'))
            
            if not scan_path.exists():
                self.logger.error(f"Directorio no encontrado: {scan_path}")
                return []
                
            supported_formats = ['.mp3', '.flac', '.ogg', '.wav']
            audio_files = [
                str(p) for p in Path(path).rglob('*') 
                if p.suffix.lower() in supported_formats
            ]
            
            self.logger.info(f"Encontrados {len(audio_files)} archivos en {path}")
            return audio_files
            
        except Exception as e:
            self.logger.error(f"Error escaneando directorio: {str(e)}")
            return []
            
    def move_selected_files(self, files: List[str], destination: str) -> bool:
        """Mueve archivos seleccionados a un directorio destino"""
        try:
            dest_path = Path(destination)
            if not dest_path.exists():
                self.logger.info(f"Creando directorio: {destination}")
                dest_path.mkdir(parents=True)
                
            for file_path in files:
                src = Path(file_path)
                if src.exists():
                    dest = dest_path / src.name
                    src.rename(dest)
                    self.logger.info(f"Movido {src} -> {dest}")
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Error moviendo archivos: {str(e)}")
            return False
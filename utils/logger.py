import logging
import sys
from pathlib import Path

def setup_logger():
    """Configura el logger centralizado de la aplicación"""
    logger = logging.getLogger('music_manager')
    logger.setLevel(logging.DEBUG)
    
    # Formato del log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    file_handler = logging.FileHandler(logs_dir / 'music_manager.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
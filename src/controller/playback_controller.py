from core.player import AudioPlayer
from core.state_manager import StateManager
from core.player_state import PlayerState
from utils.logger import setup_logger

class PlaybackController:
    def __init__(self):
        self.player = AudioPlayer()
        self.state_manager = StateManager()
        self.logger = setup_logger()
        self.state_manager.add_observer(self.on_state_changed)
        self.logger.info("Controlador de reproducción inicializado")

    def handle_playback(self, command, **kwargs):
        """Maneja los comandos de reproducción"""
        try:
            if command == "play":
                if 'file_path' in kwargs:
                    self.state_manager.update_state(PlayerState.LOADING)
                    if not self.player.load_file(kwargs['file_path']):
                        return False
                self.state_manager.update_state(PlayerState.PLAYING)
                return self.player.play()
                
            elif command == "pause":
                self.state_manager.update_state(PlayerState.PAUSED)
                self.player.pause()
                return True
                
            elif command == "stop":
                self.state_manager.update_state(PlayerState.STOPPED)
                self.player.stop()
                return True
                
            elif command == "volume":
                if 'value' in kwargs:
                    self.player.set_volume(kwargs['value'])
                    self.state_manager.update_state(
                        self.state_manager.current_status.state,
                        volume=kwargs['value']
                    )
                    return True
                return False
                
            elif command == "seek":
                if 'position' in kwargs:
                    self.player.seek(kwargs['position'])
                    self.state_manager.update_state(
                        self.state_manager.current_status.state,
                        position=kwargs['position']
                    )
                    return True
                return False
                
            else:
                self.logger.warning(f"Comando no reconocido: {command}")
                return False
                
        except Exception as e:
            self.state_manager.update_state(
                PlayerState.ERROR,
                error_message=str(e)
            )
            self.logger.error(f"Error en comando {command}: {str(e)}")
            return False

    def on_state_changed(self, new_status):
        """Maneja los cambios de estado"""
        self.logger.info(f"Nuevo estado: {new_status}")
        # Aquí se pueden agregar acciones adicionales en respuesta a cambios de estado

    def get_playback_info(self):
        """Obtiene información del estado de reproducción"""
        return self.state_manager.current_status
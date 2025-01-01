from PySide6.QtCore import QObject, Signal, Slot
from src.core.player import AudioPlayer
from src.core.state_manager import StateManager
from src.utils.file_manager import FileManager
from utils.logger import setup_logger

class MainController(QObject):
    # Señales para QML
    trackChanged = Signal(dict)
    playbackStateChanged = Signal(bool)
    error = Signal(str)
    positionChanged = Signal(float)
    durationChanged = Signal(float)
    volumeChanged = Signal(int)

    def __init__(self):
        super().__init__()
        self.logger = setup_logger()
        self.player = AudioPlayer()
        self.state_manager = StateManager()
        self.file_manager = FileManager()
        
        # Conexiones internas
        self.state_manager.add_observer(self.on_state_changed)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        self.player.volumeChanged.connect(self.volumeChanged)
        self.player.error.connect(self.on_player_error)
        
        self.logger.info("Controlador principal inicializado")

    @Slot(str)
    def select_directory(self, path):
        """Maneja la selección de directorio desde QML"""
        try:
            tracks = self.file_manager.scan_directory(path)
            self.update_track_list(tracks)
        except Exception as e:
            self.error.emit(str(e))

    @Slot(dict)
    def play_track(self, track):
        """Maneja la reproducción de un track desde QML"""
        try:
            self.player.load_and_play(track['path'])
            self.trackChanged.emit(track)
        except Exception as e:
            self.error.emit(str(e))

    @Slot()
    def playPause(self):
        """Maneja la acción de play/pause desde QML"""
        try:
            if self.state_manager.current_status.state == PlayerState.PLAYING:
                self.player.pause()
            else:
                self.player.play()
        except Exception as e:
            self.error.emit(str(e))

    def on_state_changed(self, status):
        """Maneja cambios de estado internos"""
        self.playbackStateChanged.emit(status.state == PlayerState.PLAYING)

    def on_player_error(self, message):
        """Maneja errores del reproductor"""
        self.error.emit(message)

    @property
    def currentPosition(self):
        return self.player.get_position()

    @property
    def currentDuration(self):
        return self.player.get_duration()

    @property
    def currentVolume(self):
        return self.player.volume
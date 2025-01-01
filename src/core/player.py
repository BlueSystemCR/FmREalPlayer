import vlc
import logging

class AudioPlayer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.current_media = None
        self._volume = 100
        self._state = "STOPPED"
        self.logger.info("Reproductor VLC inicializado")

    def load_file(self, file_path):
        """Carga un archivo de audio para reproducción"""
        try:
            self.current_media = self.instance.media_new(file_path)
            self.player.set_media(self.current_media)
            self._state = "LOADED"
            self.logger.info(f"Archivo cargado: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error cargando archivo: {str(e)}")
            return False

    def play(self):
        """Inicia o reanuda la reproducción"""
        if self.player.play() == -1:
            self.logger.error("Error al iniciar reproducción")
            return False
        self._state = "PLAYING"
        self.logger.info("Reproducción iniciada")
        return True

    def pause(self):
        """Pausa la reproducción"""
        self.player.pause()
        self._state = "PAUSED"
        self.logger.info("Reproducción pausada")

    def stop(self):
        """Detiene la reproducción"""
        self.player.stop()
        self._state = "STOPPED"
        self.logger.info("Reproducción detenida")

    def set_volume(self, volume):
        """Ajusta el volumen (0-100)"""
        try:
            volume = max(0, min(100, volume))
            self.player.audio_set_volume(volume)
            self._volume = volume
            self.logger.info(f"Volumen ajustado a: {volume}")
        except Exception as e:
            self.logger.error(f"Error ajustando volumen: {str(e)}")

    def seek(self, position):
        """Mueve la posición de reproducción (en segundos)"""
        try:
            self.player.set_time(int(position * 1000))
            self.logger.info(f"Posición movida a: {position}s")
        except Exception as e:
            self.logger.error(f"Error moviendo posición: {str(e)}")

    def get_position(self):
        """Obtiene la posición actual en segundos"""
        return self.player.get_time() / 1000

    def get_duration(self):
        """Obtiene la duración total en segundos"""
        return self.player.get_length() / 1000

    @property
    def state(self):
        return self._state

    @property
    def volume(self):
        return self._volume
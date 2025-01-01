import logging
from typing import Callable
from src.core.player_state import PlayerState, PlayerStatus

class StateManager:
    def __init__(self):
        self._status = PlayerStatus(state=PlayerState.STOPPED)
        self._observers = []
        self.logger = logging.getLogger(__name__)
        self.logger.info("State Manager inicializado")

    def update_state(self, new_state: PlayerState, **kwargs):
        """Actualiza el estado del reproductor"""
        try:
            previous_state = self._status.state
            self._status.state = new_state
            
            # Actualizar propiedades adicionales
            for key, value in kwargs.items():
                if hasattr(self._status, key):
                    setattr(self._status, key, value)
                    
            self.logger.info(
                f"Cambio de estado: {previous_state.value} -> {new_state.value}"
            )
            self.notify_observers()
            
        except Exception as e:
            self._status.state = PlayerState.ERROR
            self._status.error_message = str(e)
            self.logger.error(f"Error actualizando estado: {str(e)}")
            self.notify_observers()

    def add_observer(self, observer: Callable[[PlayerStatus], None]):
        """Agrega un observador para cambios de estado"""
        if observer not in self._observers:
            self._observers.append(observer)
            self.logger.info("Nuevo observador agregado")

    def remove_observer(self, observer: Callable[[PlayerStatus], None]):
        """Elimina un observador"""
        if observer in self._observers:
            self._observers.remove(observer)
            self.logger.info("Observador eliminado")

    def notify_observers(self):
        """Notifica a todos los observadores del cambio de estado"""
        for observer in self._observers:
            try:
                observer(self._status)
            except Exception as e:
                self.logger.error(f"Error notificando observador: {str(e)}")

    @property
    def current_status(self):
        return self._status
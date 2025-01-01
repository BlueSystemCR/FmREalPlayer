from enum import Enum
from dataclasses import dataclass
from typing import Optional

class PlayerState(Enum):
    STOPPED = "STOPPED"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    LOADING = "LOADING"
    ERROR = "ERROR"

@dataclass
class PlayerStatus:
    state: PlayerState
    current_track: Optional[object] = None
    position: float = 0.0
    duration: float = 0.0
    volume: int = 100
    error_message: Optional[str] = None

    def __str__(self):
        return (f"Estado: {self.state.value}, "
                f"Posición: {self.position:.1f}/{self.duration:.1f}s, "
                f"Volumen: {self.volume}%")
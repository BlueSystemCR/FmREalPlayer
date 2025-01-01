import logging
from typing import Dict, Any
from PySide6.QtCore import Signal, QObject

class ErrorHandler(QObject):
    error_occurred = Signal(str, str)  # message, details
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
    def handle_error(self, error: Exception, context: Dict[str, Any] = None):
        """Maneja errores y emite señales para la UI"""
        error_message = self._get_user_friendly_message(error)
        error_details = self._get_error_details(error, context)
        
        # Loggear el error
        self.logger.error(f"{error_message}\nDetails: {error_details}")
        
        # Emitir señal para la UI
        self.error_occurred.emit(error_message, error_details)
        
    def _get_user_friendly_message(self, error: Exception) -> str:
        """Genera un mensaje amigable para el usuario"""
        error_type = type(error).__name__
        
        messages = {
            'FileNotFoundError': "El archivo no fue encontrado",
            'PermissionError': "Permiso denegado",
            'RuntimeError': "Error durante la reproducción",
            'ValueError': "Valor inválido proporcionado",
            'Exception': "Ocurrió un error inesperado"
        }
        
        return messages.get(error_type, messages['Exception'])

    def _get_error_details(self, error: Exception, context: Dict[str, Any]) -> str:
        """Genera detalles técnicos del error"""
        details = f"Error: {str(error)}\nType: {type(error).__name__}"
        
        if context:
            details += "\nContext:\n"
            for key, value in context.items():
                details += f"- {key}: {value}\n"
                
        return details
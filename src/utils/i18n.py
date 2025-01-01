from PySide6.QtCore import QTranslator, QLocale, QCoreApplication
import os

class Internationalization:
    def __init__(self):
        self.translator = QTranslator()
        self.current_language = 'en'
        
    def set_language(self, language_code: str):
        """Carga y activa la traducción para el idioma especificado"""
        if self.translator.load(f":/translations/music_manager_{language_code}.qm"):
            QCoreApplication.instance().installTranslator(self.translator)
            self.current_language = language_code
            return True
        return False

    def translate(self, context: str, text: str) -> str:
        """Traduce un texto dado su contexto"""
        return QCoreApplication.translate(context, text)

    def available_languages(self) -> list:
        """Devuelve la lista de idiomas disponibles"""
        translations_dir = os.path.join(os.path.dirname(__file__), 'translations')
        if not os.path.exists(translations_dir):
            return ['en']
            
        languages = []
        for file in os.listdir(translations_dir):
            if file.startswith('music_manager_') and file.endswith('.qm'):
                lang_code = file[len('music_manager_'):-3]
                languages.append(lang_code)
                
        return sorted(languages)
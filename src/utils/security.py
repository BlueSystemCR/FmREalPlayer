import hashlib
import os
from cryptography.fernet import Fernet
from typing import Optional

class SecurityManager:
    def __init__(self):
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)

    def _load_or_generate_key(self) -> bytes:
        """Carga o genera una clave de cifrado de manera segura"""
        key_file = os.path.join(os.path.dirname(__file__), 'music_manager.key')
        
        # Verificar permisos del archivo
        if os.path.exists(key_file):
            if os.stat(key_file).st_mode & 0o777 != 0o600:
                raise PermissionError("Key file has insecure permissions")
                
            with open(key_file, 'rb') as f:
                key = f.read()
                # Validar que la clave sea válida
                try:
                    Fernet(key)
                    return key
                except ValueError:
                    os.remove(key_file)
                    return self._load_or_generate_key()
        else:
            key = Fernet.generate_key()
            # Crear archivo con permisos seguros
            old_umask = os.umask(0o177)
            try:
                with open(key_file, 'wb') as f:
                    f.write(key)
            finally:
                os.umask(old_umask)
            return key

    def encrypt_data(self, data: str) -> str:
        """Cifra datos sensibles de manera segura"""
        if not isinstance(data, str):
            raise TypeError("Data must be a string")
        if not data:
            raise ValueError("Data cannot be empty")
            
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data: str) -> Optional[str]:
        """Descifra datos previamente cifrados de manera segura"""
        if not isinstance(encrypted_data, str):
            raise TypeError("Encrypted data must be a string")
        if not encrypted_data:
            raise ValueError("Encrypted data cannot be empty")
            
        try:
            return self.cipher.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            self._log_security_error(f"Decryption failed: {str(e)}")
            return None
            
    def _log_security_error(self, message: str):
        """Registra errores de seguridad de manera segura"""
        logger = logging.getLogger(__name__)
        logger.error(f"Security Error: {message}")

    def hash_password(self, password: str) -> str:
        """Genera un hash seguro de una contraseña"""
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        return salt.hex() + key.hex()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifica una contraseña contra su hash"""
        salt = bytes.fromhex(hashed_password[:64])
        key = bytes.fromhex(hashed_password[64:])
        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        return key == new_key
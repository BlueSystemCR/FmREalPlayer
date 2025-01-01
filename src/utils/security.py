import hashlib
import os
from cryptography.fernet import Fernet
from typing import Optional

class SecurityManager:
    def __init__(self):
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)

    def _load_or_generate_key(self) -> bytes:
        """Carga o genera una clave de cifrado"""
        key_file = 'music_manager.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key

    def encrypt_data(self, data: str) -> str:
        """Cifra datos sensibles"""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data: str) -> Optional[str]:
        """Descifra datos previamente cifrados"""
        try:
            return self.cipher.decrypt(encrypted_data.encode()).decode()
        except Exception:
            return None

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
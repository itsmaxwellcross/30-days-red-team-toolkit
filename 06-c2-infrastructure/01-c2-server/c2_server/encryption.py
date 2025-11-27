import json
import base64
from cryptography.fernet import Fernet

class EncryptionHandler:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)

    def encrypt(self, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        encrypted = self.cipher.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()

    def decrypt(self, encrypted_data):
        try:
            decoded = base64.b64decode(encrypted_data.encode())
            decrypted = self.cipher.decrypt(decoded)
            return json.loads(decrypted.decode())
        except Exception:
            return None
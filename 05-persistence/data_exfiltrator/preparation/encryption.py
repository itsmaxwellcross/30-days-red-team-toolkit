"""
File encryption functionality
"""

import subprocess


class Encryptor:
    """Handle file encryption"""
    
    def encrypt(self, file_path: str, password: str) -> str:
        """
        Encrypt file with openssl AES-256-CBC
        
        Args:
            file_path: Path to file to encrypt
            password: Encryption password
        
        Returns:
            Path to encrypted file
        """
        encrypted_path = file_path + '.enc'
        
        try:
            subprocess.run([
                'openssl', 'enc', '-aes-256-cbc',
                '-salt', '-in', file_path,
                '-out', encrypted_path,
                '-k', password
            ], check=True, capture_output=True)
            
            return encrypted_path
        except:
            print("  [!] Encryption failed (openssl not available?)")
            return file_path
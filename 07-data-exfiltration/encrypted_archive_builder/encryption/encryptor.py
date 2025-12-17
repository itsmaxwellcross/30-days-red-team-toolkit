"""
File encryption and decryption engine
"""

import secrets
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend

from config import (
    KEY_DERIVATION_ITERATIONS,
    KEY_LENGTH,
    SALT_LENGTH,
    IV_LENGTH,
    BLOCK_SIZE,
    ENCRYPTED_FILE_MAGIC,
    ENCRYPTED_FILE_VERSION
)


class FileEncryptor:
    """Handles file encryption and decryption"""
    
    def __init__(self):
        self.backend = default_backend()
    
    def generate_key(self, password, salt=None):
        """
        Generate encryption key from password using PBKDF2
        
        Args:
            password (str): Password
            salt (bytes): Salt (generated if None)
            
        Returns:
            tuple: (key, salt)
        """
        if salt is None:
            salt = secrets.token_bytes(SALT_LENGTH)
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=KEY_LENGTH,
            salt=salt,
            iterations=KEY_DERIVATION_ITERATIONS,
            backend=self.backend
        )
        
        key = kdf.derive(password.encode())
        
        return key, salt
    
    def encrypt_data(self, plaintext, key, iv):
        """
        Encrypt data using AES-256-CBC
        
        Args:
            plaintext (bytes): Data to encrypt
            key (bytes): Encryption key
            iv (bytes): Initialization vector
            
        Returns:
            bytes: Encrypted data
        """
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=self.backend
        )
        
        encryptor = cipher.encryptor()
        
        # Add PKCS7 padding
        padding_length = BLOCK_SIZE - (len(plaintext) % BLOCK_SIZE)
        padded_plaintext = plaintext + bytes([padding_length] * padding_length)
        
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        
        return ciphertext
    
    def decrypt_data(self, ciphertext, key, iv):
        """
        Decrypt data using AES-256-CBC
        
        Args:
            ciphertext (bytes): Encrypted data
            key (bytes): Encryption key
            iv (bytes): Initialization vector
            
        Returns:
            bytes: Decrypted data
        """
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=self.backend
        )
        
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove PKCS7 padding
        padding_length = padded_plaintext[-1]
        plaintext = padded_plaintext[:-padding_length]
        
        return plaintext
    
    def encrypt_file(self, filepath, password, output_path=None):
        """
        Encrypt a file
        
        Args:
            filepath (str): Path to file to encrypt
            password (str): Encryption password
            output_path (str): Output path (default: filepath.encrypted)
            
        Returns:
            str: Path to encrypted file
        """
        print(f"[*] Encrypting: {filepath}")
        
        # Generate key and IV
        key, salt = self.generate_key(password)
        iv = secrets.token_bytes(IV_LENGTH)
        
        # Read file
        with open(filepath, 'rb') as f:
            plaintext = f.read()
        
        # Encrypt
        ciphertext = self.encrypt_data(plaintext, key, iv)
        
        # Determine output path
        if output_path is None:
            output_path = f"{filepath}.encrypted"
        
        # Write encrypted file with metadata
        with open(output_path, 'wb') as f:
            # Magic bytes (4 bytes)
            f.write(ENCRYPTED_FILE_MAGIC)
            
            # Version (1 byte)
            f.write(bytes([ENCRYPTED_FILE_VERSION]))
            
            # Reserved (3 bytes for future use)
            f.write(b'\x00\x00\x00')
            
            # Salt (16 bytes)
            f.write(salt)
            
            # IV (16 bytes)
            f.write(iv)
            
            # Ciphertext
            f.write(ciphertext)
        
        print(f"[+] Encrypted file created: {output_path}")
        
        return output_path
    
    def decrypt_file(self, encrypted_filepath, password, output_path=None):
        """
        Decrypt a file
        
        Args:
            encrypted_filepath (str): Path to encrypted file
            password (str): Decryption password
            output_path (str): Output path (default: removes .encrypted)
            
        Returns:
            str: Path to decrypted file
        """
        print(f"[*] Decrypting: {encrypted_filepath}")
        
        # Read encrypted file
        with open(encrypted_filepath, 'rb') as f:
            # Read magic bytes
            magic = f.read(4)
            if magic != ENCRYPTED_FILE_MAGIC:
                raise ValueError("Not a valid encrypted file (magic bytes mismatch)")
            
            # Read version
            version = f.read(1)[0]
            if version != ENCRYPTED_FILE_VERSION:
                raise ValueError(f"Unsupported file version: {version}")
            
            # Skip reserved bytes
            f.read(3)
            
            # Read salt and IV
            salt = f.read(SALT_LENGTH)
            iv = f.read(IV_LENGTH)
            
            # Read ciphertext
            ciphertext = f.read()
        
        # Generate key
        key, _ = self.generate_key(password, salt)
        
        # Decrypt
        try:
            plaintext = self.decrypt_data(ciphertext, key, iv)
        except Exception as e:
            raise ValueError(f"Decryption failed (wrong password?): {e}")
        
        # Determine output path
        if output_path is None:
            output_path = encrypted_filepath.replace('.encrypted', '')
        
        # Write decrypted file
        with open(output_path, 'wb') as f:
            f.write(plaintext)
        
        print(f"[+] Decrypted file created: {output_path}")
        
        return output_path
    
    def encrypt_with_layers(self, filepath, passwords, output_path=None):
        """
        Apply multiple layers of encryption
        
        Args:
            filepath (str): File to encrypt
            passwords (list): List of passwords (one per layer)
            output_path (str): Final output path
            
        Returns:
            str: Path to encrypted file
        """
        print(f"[*] Applying {len(passwords)} layer(s) of encryption...")
        
        current_path = filepath
        
        for i, password in enumerate(passwords, 1):
            print(f"[*] Layer {i}/{len(passwords)}")
            
            if i == len(passwords) and output_path:
                # Last layer, use desired output path
                current_path = self.encrypt_file(current_path, password, output_path)
            else:
                # Intermediate layer
                current_path = self.encrypt_file(current_path, password)
            
            # Clean up previous layer (except original file)
            if i > 1:
                try:
                    Path(filepath).unlink()
                except:
                    pass
            
            filepath = current_path
        
        print(f"[+] Multi-layer encryption complete")
        
        return current_path
    
    def decrypt_with_layers(self, encrypted_filepath, passwords, output_path=None):
        """
        Decrypt multiple layers
        
        Args:
            encrypted_filepath (str): Encrypted file
            passwords (list): List of passwords (in reverse order)
            output_path (str): Final output path
            
        Returns:
            str: Path to decrypted file
        """
        print(f"[*] Decrypting {len(passwords)} layer(s)...")
        
        current_path = encrypted_filepath
        
        for i, password in enumerate(passwords, 1):
            print(f"[*] Layer {i}/{len(passwords)}")
            
            if i == len(passwords) and output_path:
                # Last layer, use desired output path
                current_path = self.decrypt_file(current_path, password, output_path)
            else:
                # Intermediate layer
                current_path = self.decrypt_file(current_path, password)
            
            # Clean up previous layer
            if i > 1:
                try:
                    Path(encrypted_filepath).unlink()
                except:
                    pass
            
            encrypted_filepath = current_path
        
        print(f"[+] Multi-layer decryption complete")
        
        return current_path
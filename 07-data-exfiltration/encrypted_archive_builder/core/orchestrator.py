"""
Main orchestrator for Encrypted Archive Builder
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from encryption.encryptor import FileEncryptor
from archiving.archiver import Archiver
from obfuscation.obfuscator import Obfuscator
from core.utils import (
    validate_password,
    get_file_info,
    format_file_size,
    calculate_total_size,
    safe_remove
)
from config import SUPPORTED_FORMATS, ARCHIVE_FORMAT_INFO


class EncryptedArchiveOrchestrator:
    """Main coordinator for archive operations"""
    
    def __init__(self):
        self.encryptor = FileEncryptor()
        self.archiver = Archiver()
        self.obfuscator = Obfuscator()
    
    def display_banner(self):
        """Display framework banner"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           ENCRYPTED ARCHIVE BUILDER                       ║
║               Educational Use Only                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
        print(banner)
    
    def list_formats(self):
        """List supported archive formats"""
        print("\n" + "="*60)
        print("SUPPORTED ARCHIVE FORMATS")
        print("="*60 + "\n")
        
        for fmt, info in ARCHIVE_FORMAT_INFO.items():
            print(f"[{fmt.upper()}]")
            print(f"  Name: {info['name']}")
            print(f"  Extension: {info['extension']}")
            print(f"  Compression: {info['compression']}")
            print(f"  Speed: {info['speed']}")
            print(f"  Ratio: {info['ratio']}")
            print()
    
    def create_encrypted_archive(self, files_or_dirs, output_path, password,
                                 archive_format='zip', layers=1, obfuscate=False):
        """
        Create encrypted archive (complete workflow)
        
        Args:
            files_or_dirs (list): Files/directories to archive
            output_path (str): Output file path
            password (str): Encryption password
            archive_format (str): Archive format
            layers (int): Number of encryption layers
            obfuscate (bool): Obfuscate filename
            
        Returns:
            dict: Operation result
        """
        print("\n" + "="*60)
        print("CREATING ENCRYPTED ARCHIVE")
        print("="*60 + "\n")
        
        # Validate password
        is_valid, msg = validate_password(password)
        if not is_valid:
            print(f"[-] Password validation failed: {msg}")
            return None
        else:
            print(f"[*] {msg}")
        
        # Calculate total size
        total_size = calculate_total_size(files_or_dirs)
        print(f"[*] Total input size: {format_file_size(total_size)}")
        print(f"[*] Files/directories: {len(files_or_dirs)}")
        print()
        
        # Step 1: Create archive
        print("[1/4] Creating archive...")
        archive_path = output_path
        
        # Ensure proper extension
        if not any(archive_path.endswith(ext) for ext in ['.zip', '.tar', '.gz', '.bz2']):
            archive_path += ARCHIVE_FORMAT_INFO[archive_format]['extension']
        
        # Remove .encrypted if present
        archive_path = archive_path.replace('.encrypted', '')
        
        try:
            archive_path = self.archiver.create_archive(
                files_or_dirs,
                archive_path,
                archive_format
            )
        except Exception as e:
            print(f"[-] Archive creation failed: {e}")
            return None
        
        archive_size = Path(archive_path).stat().st_size
        print(f"[*] Archive size: {format_file_size(archive_size)}")
        print(f"[*] Compression ratio: {(1 - archive_size/total_size)*100:.1f}%\n")
        
        # Step 2: Encrypt archive
        print(f"[2/4] Encrypting ({layers} layer(s))...")
        
        try:
            if layers == 1:
                encrypted_path = self.encryptor.encrypt_file(
                    archive_path,
                    password,
                    archive_path + '.encrypted'
                )
            else:
                # Multi-layer encryption
                passwords = [f"{password}_layer{i}" for i in range(1, layers + 1)]
                encrypted_path = self.encryptor.encrypt_with_layers(
                    archive_path,
                    passwords,
                    archive_path + '.encrypted'
                )
        except Exception as e:
            print(f"[-] Encryption failed: {e}")
            safe_remove(archive_path)
            return None
        
        encrypted_size = Path(encrypted_path).stat().st_size
        print(f"[*] Encrypted size: {format_file_size(encrypted_size)}\n")
        
        # Step 3: Clean up unencrypted archive
        print("[3/4] Cleaning up...")
        safe_remove(archive_path)
        print("[+] Unencrypted archive removed\n")
        
        # Step 4: Obfuscate filename (optional)
        final_path = encrypted_path
        if obfuscate:
            print("[4/4] Obfuscating filename...")
            try:
                final_path = self.obfuscator.obfuscate_filename(encrypted_path)
            except Exception as e:
                print(f"[-] Obfuscation failed: {e}")
                final_path = encrypted_path
        else:
            print("[4/4] Skipping obfuscation")
        
        # Summary
        print("\n" + "="*60)
        print("ENCRYPTED ARCHIVE CREATED")
        print("="*60)
        print(f"Output: {final_path}")
        print(f"Original size: {format_file_size(total_size)}")
        print(f"Final size: {format_file_size(Path(final_path).stat().st_size)}")
        print(f"Encryption layers: {layers}")
        print(f"Format: {archive_format.upper()}")
        print("="*60 + "\n")
        
        return {
            'output_path': final_path,
            'original_size': total_size,
            'encrypted_size': Path(final_path).stat().st_size,
            'layers': layers,
            'format': archive_format,
            'obfuscated': obfuscate
        }
    
    def decrypt_and_extract(self, encrypted_file, password, output_dir,
                           layers=1, archive_format='zip'):
        """
        Decrypt and extract archive
        
        Args:
            encrypted_file (str): Encrypted archive file
            password (str): Decryption password
            output_dir (str): Output directory
            layers (int): Number of encryption layers
            archive_format (str): Archive format
            
        Returns:
            str: Output directory path
        """
        print("\n" + "="*60)
        print("DECRYPTING AND EXTRACTING ARCHIVE")
        print("="*60 + "\n")
        
        # Step 1: Decrypt
        print(f"[1/3] Decrypting ({layers} layer(s))...")
        
        try:
            if layers == 1:
                decrypted_path = self.encryptor.decrypt_file(
                    encrypted_file,
                    password
                )
            else:
                # Multi-layer decryption (reverse order)
                passwords = [f"{password}_layer{i}" for i in range(layers, 0, -1)]
                decrypted_path = self.encryptor.decrypt_with_layers(
                    encrypted_file,
                    passwords
                )
        except Exception as e:
            print(f"[-] Decryption failed: {e}")
            return None
        
        print()
        
        # Step 2: Extract archive
        print("[2/3] Extracting archive...")
        
        try:
            self.archiver.extract_archive(decrypted_path, output_dir)
        except Exception as e:
            print(f"[-] Extraction failed: {e}")
            safe_remove(decrypted_path)
            return None
        
        print()
        
        # Step 3: Clean up
        print("[3/3] Cleaning up...")
        safe_remove(decrypted_path)
        print("[+] Temporary files removed\n")
        
        print("="*60)
        print(f"EXTRACTION COMPLETE: {output_dir}")
        print("="*60 + "\n")
        
        return output_dir
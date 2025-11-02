"""
File staging and preparation
"""

import os
import shutil
from typing import List, Dict
from .compression import Compressor
from .encryption import Encryptor
from ..core.utils import calculate_checksum


class Staging:
    """Stage files for exfiltration"""
    
    def __init__(self, staging_dir: str):
        self.staging_dir = staging_dir
        self.compressor = Compressor(staging_dir)
        self.encryptor = Encryptor()
    
    def stage_files(self, file_paths: List[str], 
                   compress: bool = True,
                   encrypt: bool = False,
                   password: str = '') -> List[Dict]:
        """
        Stage files for exfiltration
        
        Args:
            file_paths: List of file paths to stage
            compress: Whether to compress files
            encrypt: Whether to encrypt files
            password: Encryption password
        
        Returns:
            List of staged file information
        """
        print("\n[*] Staging files for exfiltration...")
        
        staged_files = []
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"  [-] File not found: {file_path}")
                continue
            
            print(f"\n  [*] Processing: {file_path}")
            
            staged_file = self._stage_single_file(
                file_path, compress, encrypt, password
            )
            
            if staged_file:
                staged_files.append(staged_file)
        
        return staged_files
    
    def _stage_single_file(self, file_path: str, compress: bool,
                          encrypt: bool, password: str) -> Dict:
        """Stage a single file"""
        current_file = file_path
        
        # Compress if requested
        if compress:
            print("    [*] Compressing...")
            compressed = self.compressor.compress(current_file)
            if compressed:
                current_file = compressed
                print(f"    [+] Compressed: {compressed}")
        
        # Encrypt if requested
        if encrypt and password:
            print("    [*] Encrypting...")
            encrypted = self.encryptor.encrypt(current_file, password)
            if encrypted:
                current_file = encrypted
                print(f"    [+] Encrypted: {encrypted}")
        
        # Calculate checksum
        checksum = calculate_checksum(current_file)
        
        file_info = {
            'original': file_path,
            'staged': current_file,
            'size': os.path.getsize(current_file),
            'checksum': checksum
        }
        
        print(f"    [+] Staged: {current_file}")
        print(f"    [+] Size: {os.path.getsize(current_file)} bytes")
        print(f"    [+] SHA256: {checksum}")
        
        return file_info
    
    def cleanup(self):
        """Clean up staging directory"""
        print("\n[*] Cleaning up staging directory...")
        
        try:
            shutil.rmtree(self.staging_dir)
            print(f"[+] Removed: {self.staging_dir}")
        except Exception as e:
            print(f"[-] Cleanup failed: {e}")

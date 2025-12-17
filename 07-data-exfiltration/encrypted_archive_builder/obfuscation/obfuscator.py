"""
Filename obfuscation and steganography
"""

import os
import random
from pathlib import Path
from datetime import datetime
from config import INNOCENT_FILENAME_TEMPLATES


class Obfuscator:
    """Handles filename obfuscation"""
    
    def __init__(self):
        pass
    
    def obfuscate_filename(self, filepath, extension=None):
        """
        Rename file to innocent-looking name
        
        Args:
            filepath (str): File to rename
            extension (str): Desired extension (None = keep original)
            
        Returns:
            str: New file path
        """
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Determine extension
        if extension is None:
            extension = path.suffix
        
        # Generate innocent filename
        template = random.choice(INNOCENT_FILENAME_TEMPLATES)
        date_str = datetime.now().strftime('%Y%m%d')
        new_filename = template.format(date=date_str)
        
        # Ensure correct extension
        new_filename = Path(new_filename).stem + extension
        
        # Create new path
        new_path = path.parent / new_filename
        
        # Handle collisions
        counter = 1
        while new_path.exists():
            stem = Path(new_filename).stem
            new_filename = f"{stem}_{counter}{extension}"
            new_path = path.parent / new_filename
            counter += 1
        
        # Rename file
        os.rename(filepath, new_path)
        
        print(f"[+] Filename obfuscated: {new_filename}")
        
        return str(new_path)
    
    def generate_innocent_name(self, extension='.zip'):
        """
        Generate innocent-looking filename without renaming
        
        Args:
            extension (str): File extension
            
        Returns:
            str: Generated filename
        """
        template = random.choice(INNOCENT_FILENAME_TEMPLATES)
        date_str = datetime.now().strftime('%Y%m%d')
        filename = template.format(date=date_str)
        
        return Path(filename).stem + extension
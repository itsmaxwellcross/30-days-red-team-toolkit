"""
Helper functions for file validation and directory management
"""

import os
from pathlib import Path


def validate_file_path(filepath):
    """
    Validate that a file path exists and is accessible
    
    Args:
        filepath (str): Path to file to validate
        
    Returns:
        bool: True if valid and accessible, False otherwise
    """
    if not filepath:
        print("[-] No file path provided")
        return False
    
    path = Path(filepath)
    
    if not path.exists():
        print(f"[-] File does not exist: {filepath}")
        return False
    
    if not path.is_file():
        print(f"[-] Path is not a file: {filepath}")
        return False
    
    if not os.access(filepath, os.R_OK):
        print(f"[-] File is not readable: {filepath}")
        return False
    
    return True


def ensure_output_dir(output_path):
    """
    Ensure output directory exists, create if needed
    
    Args:
        output_path (str): Output file path
        
    Returns:
        bool: True if directory exists or was created, False on error
    """
    try:
        output_dir = Path(output_path).parent
        
        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)
            print(f"[+] Created output directory: {output_dir}")
        
        return True
    
    except Exception as e:
        print(f"[-] Failed to create output directory: {e}")
        return False


def get_file_size(filepath):
    """
    Get human-readable file size
    
    Args:
        filepath (str): Path to file
        
    Returns:
        str: Human-readable file size
    """
    try:
        size = Path(filepath).stat().st_size
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        
        return f"{size:.2f} TB"
    
    except Exception as e:
        return f"Unknown ({e})"


def safe_filename(filename):
    """
    Make a filename safe for filesystem
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Safe filename
    """
    # Remove or replace unsafe characters
    unsafe_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    
    safe_name = filename
    for char in unsafe_chars:
        safe_name = safe_name.replace(char, '_')
    
    return safe_name
"""
Helper utility functions
"""
import os
import random
import string
from typing import Optional

def generate_random_filename(extension: str = "exe", 
                            length: int = 8) -> str:
    """
    Generate random filename
    
    Args:
        extension: File extension
        length: Length of random part
        
    Returns:
        Random filename
    """
    random_str = ''.join(
        random.choices(string.ascii_lowercase + string.digits, k=length)
    )
    return f"{random_str}.{extension}"

def validate_file_path(file_path: str) -> bool:
    """
    Validate file path exists
    
    Args:
        file_path: Path to check
        
    Returns:
        True if valid
    """
    return os.path.exists(file_path) and os.path.isfile(file_path)

def get_file_size(file_path: str) -> int:
    """
    Get file size in bytes
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in bytes
    """
    return os.path.getsize(file_path)

def format_file_size(size_bytes: int) -> str:
    """
    Format file size for display
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename
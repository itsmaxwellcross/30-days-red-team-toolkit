"""
Utility functions for Encrypted Archive Builder
"""

import os
import secrets
import hashlib
from pathlib import Path
from datetime import datetime
from config import (
    MINIMUM_PASSWORD_LENGTH,
    RECOMMENDED_PASSWORD_LENGTH,
    INNOCENT_FILENAME_TEMPLATES
)


def validate_password(password):
    """
    Validate password strength
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (is_valid, message)
    """
    if not password:
        return False, "Password cannot be empty"
    
    if len(password) < MINIMUM_PASSWORD_LENGTH:
        return False, f"Password must be at least {MINIMUM_PASSWORD_LENGTH} characters"
    
    if len(password) < RECOMMENDED_PASSWORD_LENGTH:
        return True, f"Warning: Password shorter than recommended {RECOMMENDED_PASSWORD_LENGTH} characters"
    
    return True, "Password strength: Good"


def generate_random_password(length=16):
    """
    Generate a random secure password
    
    Args:
        length (int): Password length
        
    Returns:
        str: Random password
    """
    import string
    
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    
    return password


def calculate_file_hash(filepath, algorithm='sha256'):
    """
    Calculate file hash
    
    Args:
        filepath (str): Path to file
        algorithm (str): Hash algorithm (sha256, md5, sha1)
        
    Returns:
        str: Hex digest of hash
    """
    if algorithm == 'sha256':
        hasher = hashlib.sha256()
    elif algorithm == 'md5':
        hasher = hashlib.md5()
    elif algorithm == 'sha1':
        hasher = hashlib.sha1()
    else:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    
    return hasher.hexdigest()


def format_file_size(size_bytes):
    """
    Format file size in human-readable format
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.2f} PB"


def get_file_info(filepath):
    """
    Get detailed file information
    
    Args:
        filepath (str): Path to file
        
    Returns:
        dict: File information
    """
    path = Path(filepath)
    
    if not path.exists():
        return None
    
    stats = path.stat()
    
    return {
        'path': str(path),
        'name': path.name,
        'size': stats.st_size,
        'size_formatted': format_file_size(stats.st_size),
        'modified': datetime.fromtimestamp(stats.st_mtime),
        'created': datetime.fromtimestamp(stats.st_ctime),
        'is_file': path.is_file(),
        'is_dir': path.is_dir()
    }


def generate_obfuscated_filename(extension='.docx'):
    """
    Generate innocent-looking filename
    
    Args:
        extension (str): File extension
        
    Returns:
        str: Generated filename
    """
    import random
    
    # Get template
    template = random.choice(INNOCENT_FILENAME_TEMPLATES)
    
    # Replace date placeholder
    date_str = datetime.now().strftime('%Y%m%d')
    filename = template.format(date=date_str)
    
    # Ensure correct extension
    filename = Path(filename).stem + extension
    
    return filename


def ensure_directory(directory):
    """
    Ensure directory exists, create if not
    
    Args:
        directory (str): Directory path
    """
    Path(directory).mkdir(parents=True, exist_ok=True)


def safe_remove(filepath):
    """
    Safely remove a file
    
    Args:
        filepath (str): Path to file
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        pass  # Silently fail


def validate_file_path(filepath):
    """
    Validate file path
    
    Args:
        filepath (str): Path to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    path = Path(filepath)
    
    if not path.exists():
        return False, f"Path does not exist: {filepath}"
    
    if not os.access(filepath, os.R_OK):
        return False, f"No read permission: {filepath}"
    
    return True, None


def collect_files(paths):
    """
    Collect all files from given paths (files and directories)
    
    Args:
        paths (list): List of file/directory paths
        
    Returns:
        list: List of file paths
    """
    files = []
    
    for path_str in paths:
        path = Path(path_str)
        
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            # Recursively collect all files
            files.extend([f for f in path.rglob('*') if f.is_file()])
    
    return files


def calculate_total_size(paths):
    """
    Calculate total size of files/directories
    
    Args:
        paths (list): List of paths
        
    Returns:
        int: Total size in bytes
    """
    total = 0
    files = collect_files(paths)
    
    for file_path in files:
        total += file_path.stat().st_size
    
    return total
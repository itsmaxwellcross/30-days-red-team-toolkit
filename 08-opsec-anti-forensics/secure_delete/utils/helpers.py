"""
Helper functions for secure deletion operations
"""

import os
import sys
from pathlib import Path


def validate_file(filepath):
    """
    Validate that a file exists and is accessible
    
    Args:
        filepath (str): Path to file to validate
        
    Returns:
        bool: True if valid, False otherwise
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
    
    if not os.access(filepath, os.W_OK):
        print(f"[-] File is not writable: {filepath}")
        return False
    
    return True


def validate_directory(directory):
    """
    Validate that a directory exists and is accessible
    
    Args:
        directory (str): Path to directory to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not directory:
        print("[-] No directory path provided")
        return False
    
    path = Path(directory)
    
    if not path.exists():
        print(f"[-] Directory does not exist: {directory}")
        return False
    
    if not path.is_dir():
        print(f"[-] Path is not a directory: {directory}")
        return False
    
    return True


def format_size(size_bytes):
    """
    Format byte size to human-readable format
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Human-readable size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.2f} PB"


def confirm_deletion(filepath):
    """
    Ask user to confirm file deletion
    
    Args:
        filepath (str): Path to file
        
    Returns:
        bool: True if user confirms, False otherwise
    """
    try:
        response = input(f"[!] Permanently delete {filepath}? (yes/no): ").strip().lower()
        return response in ['yes', 'y']
    except KeyboardInterrupt:
        print("\n[*] Cancelled")
        return False


def is_system_file(filepath):
    """
    Check if file is a critical system file
    
    Args:
        filepath (str): Path to file
        
    Returns:
        bool: True if system file, False otherwise
    """
    from ..core.constants import EXCLUDE_EXTENSIONS, EXCLUDE_DIRS
    
    path = Path(filepath)
    
    # Check extension
    if path.suffix.lower() in EXCLUDE_EXTENSIONS:
        return True
    
    # Check if in system directory
    path_str = str(path).lower()
    for exclude_dir in EXCLUDE_DIRS:
        if exclude_dir.lower() in path_str:
            return True
    
    return False


def get_file_info(filepath):
    """
    Get detailed information about a file
    
    Args:
        filepath (str): Path to file
        
    Returns:
        dict: File information
    """
    try:
        stat = os.stat(filepath)
        
        info = {
            'size': stat.st_size,
            'size_formatted': format_size(stat.st_size),
            'mode': oct(stat.st_mode)[-3:],
            'is_system': is_system_file(filepath)
        }
        
        return info
    
    except Exception as e:
        print(f"[-] Failed to get file info: {e}")
        return None


def safe_path(path):
    """
    Sanitize and validate file path
    
    Args:
        path (str): Original path
        
    Returns:
        str: Sanitized path
    """
    # Expand user home directory
    path = os.path.expanduser(path)
    
    # Expand environment variables
    path = os.path.expandvars(path)
    
    # Get absolute path
    path = os.path.abspath(path)
    
    return path


def estimate_deletion_time(file_size, passes=3):
    """
    Estimate time for secure deletion
    
    Args:
        file_size (int): File size in bytes
        passes (int): Number of passes
        
    Returns:
        str: Estimated time
    """
    # Rough estimate: 50 MB/s write speed
    write_speed = 50 * 1024 * 1024
    
    total_bytes = file_size * passes
    seconds = total_bytes / write_speed
    
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes"
    else:
        return f"{seconds/3600:.1f} hours"


def list_files_to_delete(directory):
    """
    List all files that would be deleted in directory
    
    Args:
        directory (str): Directory path
        
    Returns:
        list: List of file paths
    """
    try:
        files = list(Path(directory).rglob('*'))
        files = [str(f) for f in files if f.is_file()]
        return files
    except Exception as e:
        print(f"[-] Failed to list files: {e}")
        return []


def get_disk_usage(path):
    """
    Get disk usage statistics
    
    Args:
        path (str): Path to check
        
    Returns:
        dict: Disk usage info
    """
    try:
        import shutil
        total, used, free = shutil.disk_usage(path)
        
        return {
            'total': total,
            'total_formatted': format_size(total),
            'used': used,
            'used_formatted': format_size(used),
            'free': free,
            'free_formatted': format_size(free),
            'percent_used': (used / total) * 100
        }
    except Exception as e:
        print(f"[-] Failed to get disk usage: {e}")
        return None
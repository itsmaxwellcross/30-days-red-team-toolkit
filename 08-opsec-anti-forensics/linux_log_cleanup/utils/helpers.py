"""
Helper functions for log cleanup operations
"""

import os
import sys
from pathlib import Path


def check_root():
    """
    Check if script is running with root privileges
    
    Returns:
        bool: True if running as root, False otherwise
    """
    if os.geteuid() != 0:
        return False
    return True


def require_root():
    """
    Require root privileges or exit
    
    Exits with error message if not running as root
    """
    if not check_root():
        print("[!] This script requires root privileges")
        print("[!] Run with: sudo python3 <script> ...")
        sys.exit(1)


def validate_log_path(log_path):
    """
    Validate that a log path exists and is accessible
    
    Args:
        log_path (str): Path to log file to validate
        
    Returns:
        bool: True if valid and accessible, False otherwise
    """
    if not log_path:
        print("[-] No log path provided")
        return False
    
    path = Path(log_path)
    
    if not path.exists():
        print(f"[-] Log file does not exist: {log_path}")
        return False
    
    if not path.is_file():
        print(f"[-] Path is not a file: {log_path}")
        return False
    
    if not os.access(log_path, os.R_OK):
        print(f"[-] Log file is not readable: {log_path}")
        return False
    
    if not os.access(log_path, os.W_OK):
        print(f"[-] Log file is not writable: {log_path}")
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


def get_file_info(filepath):
    """
    Get detailed information about a file
    
    Args:
        filepath (str): Path to file
        
    Returns:
        dict: File information including size, permissions, etc.
    """
    try:
        stat = os.stat(filepath)
        
        info = {
            'size': stat.st_size,
            'size_formatted': format_size(stat.st_size),
            'mode': oct(stat.st_mode)[-3:],
            'uid': stat.st_uid,
            'gid': stat.st_gid,
            'modified': stat.st_mtime,
            'accessed': stat.st_atime
        }
        
        return info
    
    except Exception as e:
        print(f"[-] Failed to get file info: {e}")
        return None


def safe_path(path):
    """
    Sanitize a file path
    
    Args:
        path (str): Original path
        
    Returns:
        str: Sanitized path
    """
    # Expand user home directory
    path = os.path.expanduser(path)
    
    # Get absolute path
    path = os.path.abspath(path)
    
    return path


def confirm_action(prompt="Continue?"):
    """
    Ask user for confirmation
    
    Args:
        prompt (str): Confirmation prompt
        
    Returns:
        bool: True if user confirms, False otherwise
    """
    response = input(f"{prompt} (y/N): ").strip().lower()
    return response in ['y', 'yes']


def list_log_files(log_dir='/var/log'):
    """
    List all log files in a directory
    
    Args:
        log_dir (str): Directory to search
        
    Returns:
        list: List of log file paths
    """
    log_files = []
    
    try:
        for item in Path(log_dir).iterdir():
            if item.is_file():
                # Common log file extensions
                if any(item.name.endswith(ext) for ext in ['.log', '']) or 'log' in item.name:
                    log_files.append(str(item))
        
        return sorted(log_files)
    
    except Exception as e:
        print(f"[-] Failed to list log files: {e}")
        return []


def count_lines(filepath):
    """
    Count number of lines in a file
    
    Args:
        filepath (str): Path to file
        
    Returns:
        int: Number of lines, or -1 on error
    """
    try:
        with open(filepath, 'r', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return -1
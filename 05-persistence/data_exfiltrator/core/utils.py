"""
Utility functions for data exfiltration
"""

import subprocess
import hashlib
from typing import Optional


def run_command(command: str, timeout: int = 30) -> str:
    """
    Execute system command and return output
    
    Args:
        command: Command to execute
        timeout: Command timeout in seconds
    
    Returns:
        Command output or empty string
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout
    except:
        return ""


def calculate_checksum(file_path: str) -> Optional[str]:
    """
    Calculate SHA256 checksum of file
    
    Args:
        file_path: Path to file
    
    Returns:
        Hex digest of SHA256 hash
    """
    try:
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    except:
        return None


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

"""
Helper functions for timestamp operations
"""

import os
import platform
from pathlib import Path
from datetime import datetime

from ..core.constants import WINDOWS_REFERENCE_FILES, LINUX_REFERENCE_FILES


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
    
    if not os.access(filepath, os.R_OK):
        print(f"[-] File is not readable: {filepath}")
        return False
    
    return True


def format_timestamp(timestamp):
    """
    Format timestamp for display
    
    Args:
        timestamp (datetime): Timestamp to format
        
    Returns:
        str: Formatted timestamp string
    """
    if isinstance(timestamp, datetime):
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return str(timestamp)


def get_reference_files():
    """
    Get list of legitimate reference files for the current platform
    
    Returns:
        list: List of reference file paths
    """
    os_type = platform.system()
    
    if os_type == 'Windows':
        return WINDOWS_REFERENCE_FILES
    else:
        return LINUX_REFERENCE_FILES


def get_legitimate_reference():
    """
    Get a legitimate file to use as timestamp reference
    
    Returns:
        str: Path to a legitimate file, or None if none found
    """
    reference_files = get_reference_files()
    
    for filepath in reference_files:
        if os.path.exists(filepath):
            return filepath
    
    return None


def calculate_time_difference(time1, time2):
    """
    Calculate difference between two timestamps
    
    Args:
        time1 (datetime): First timestamp
        time2 (datetime): Second timestamp
        
    Returns:
        dict: Dictionary with difference in various units
    """
    diff = abs((time1 - time2).total_seconds())
    
    return {
        'seconds': diff,
        'minutes': diff / 60,
        'hours': diff / 3600,
        'days': diff / 86400
    }


def is_suspicious_timestamp(timestamp):
    """
    Check if a timestamp looks suspicious
    
    Args:
        timestamp (datetime): Timestamp to check
        
    Returns:
        tuple: (is_suspicious, reason)
    """
    now = datetime.now()
    
    # Future timestamp
    if timestamp > now:
        return (True, "Timestamp is in the future")
    
    # Very old timestamp (before 1990)
    if timestamp.year < 1990:
        return (True, "Timestamp is unrealistically old")
    
    # Exactly midnight (00:00:00)
    if timestamp.hour == 0 and timestamp.minute == 0 and timestamp.second == 0:
        return (True, "Timestamp is exactly midnight (suspicious precision)")
    
    # Round number timestamp (all zeros)
    if timestamp.minute == 0 and timestamp.second == 0:
        return (True, "Timestamp has suspicious rounding")
    
    return (False, None)


def safe_file_path(filepath):
    """
    Sanitize and validate file path
    
    Args:
        filepath (str): Original file path
        
    Returns:
        str: Sanitized path
    """
    # Expand user home directory
    filepath = os.path.expanduser(filepath)
    
    # Get absolute path
    filepath = os.path.abspath(filepath)
    
    return filepath
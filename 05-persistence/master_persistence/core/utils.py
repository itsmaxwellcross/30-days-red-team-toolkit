"""
Utility functions for Master Persistence Framework
"""

import os
import ctypes


def check_admin():
    """
    Check if running with administrator privileges
    
    Returns:
        bool: True if admin, False otherwise
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def validate_payload_path(payload_path):
    """
    Validate that payload file exists
    
    Args:
        payload_path: Path to payload file
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not payload_path:
        return False
    
    if not os.path.exists(payload_path):
        print(f"[!] Error: Payload file not found: {payload_path}")
        return False
    
    if not os.path.isfile(payload_path):
        print(f"[!] Error: Path is not a file: {payload_path}")
        return False
    
    return True


def get_absolute_path(path):
    """
    Convert relative path to absolute path
    
    Args:
        path: File path
        
    Returns:
        str: Absolute path
    """
    return os.path.abspath(path)


def wrap_payload_command(payload_path, wrapper_type='powershell_hidden'):
    """
    Wrap payload path in execution command
    
    Args:
        payload_path: Path to payload
        wrapper_type: Type of wrapper (powershell_hidden, cmd_hidden, direct)
        
    Returns:
        str: Wrapped command
    """
    from config import PAYLOAD_WRAPPERS
    
    template = PAYLOAD_WRAPPERS.get(wrapper_type, PAYLOAD_WRAPPERS['direct'])
    return template.format(payload_path=payload_path)


def format_method_summary(method_name, status, details=''):
    """
    Format a method installation summary
    
    Args:
        method_name: Name of persistence method
        status: Success status (True/False)
        details: Additional details
        
    Returns:
        str: Formatted summary
    """
    symbol = '[+]' if status else '[-]'
    status_text = 'SUCCESS' if status else 'FAILED'
    
    summary = f"{symbol} {method_name}: {status_text}"
    if details:
        summary += f" - {details}"
    
    return summary


def print_section_header(title, width=60):
    """
    Print a formatted section header
    
    Args:
        title: Section title
        width: Width of header
    """
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width + "\n")


def print_method_header(method_number, method_name):
    """
    Print header for a persistence method
    
    Args:
        method_number: Method number
        method_name: Method name
    """
    print(f"[METHOD {method_number}] {method_name}")
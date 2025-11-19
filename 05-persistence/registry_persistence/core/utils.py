"""
Shared utility functions for Registry Persistence Framework
"""

import subprocess
import random
import os
from config import NAME_PREFIXES, NAME_SUFFIXES, COMMAND_TIMEOUT


def check_admin():
    """
    Check if running with administrator privileges
    
    Returns:
        bool: True if running as admin, False otherwise
    """
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def run_command(command, require_admin=False):
    """
    Execute a shell command and return results
    
    Args:
        command (str): Command to execute
        require_admin (bool): Whether command requires admin privileges
        
    Returns:
        dict: Contains 'success', 'stdout', 'stderr', and optionally 'error'
    """
    if require_admin and not check_admin():
        print("[!] This command requires administrator privileges")
        return {
            'success': False,
            'error': 'Requires administrator privileges'
        }
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT
        )
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'Command timed out'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def generate_random_name(length=12):
    """
    Generate a random legitimate-looking name for registry entries
    
    Args:
        length (int): Desired length (used as guideline)
        
    Returns:
        str: Generated name (e.g., "WindowsUpdateManager")
    """
    prefix = random.choice(NAME_PREFIXES)
    suffix = random.choice(NAME_SUFFIXES)
    return f"{prefix}{suffix}"


def validate_payload_path(payload_path):
    """
    Validate that a payload path exists and is executable
    
    Args:
        payload_path (str): Path to payload
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not payload_path:
        return False, "Payload path cannot be empty"
    
    # For demonstration purposes, we don't check file existence
    # in real scenarios as payload might be created after setup
    
    # Check for suspicious characters that might break reg commands
    dangerous_chars = ['"', '\n', '\r', '\t']
    for char in dangerous_chars:
        if char in payload_path:
            return False, f"Payload path contains invalid character: {repr(char)}"
    
    return True, None


def format_registry_path(path):
    """
    Format registry path for display
    
    Args:
        path (str): Registry path
        
    Returns:
        str: Formatted path
    """
    return path.replace('\\', '\\\\') if path else path


def parse_reg_query_output(output, value_name):
    """
    Parse output from 'reg query' command to extract a specific value
    
    Args:
        output (str): Output from reg query
        value_name (str): Name of the registry value to extract
        
    Returns:
        str: Extracted value or None
    """
    if not output:
        return None
    
    for line in output.split('\n'):
        if value_name in line and 'REG_SZ' in line:
            try:
                # Format: "    ValueName    REG_SZ    Value"
                parts = line.split('REG_SZ')
                if len(parts) >= 2:
                    return parts[1].strip()
            except Exception:
                continue
    
    return None


def create_backup_info(method, original_value=None):
    """
    Create backup information for restoration
    
    Args:
        method (str): Persistence method name
        original_value (str): Original registry value
        
    Returns:
        dict: Backup information
    """
    from datetime import datetime
    
    return {
        'method': method,
        'original_value': original_value,
        'timestamp': datetime.now().isoformat(),
        'admin_required': check_admin()
    }
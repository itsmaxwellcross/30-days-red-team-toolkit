"""
Shared utility functions for Scheduled Task Persistence Framework
"""

import subprocess
import random
import os
from config import TASK_PREFIXES, TASK_SUFFIXES, COMMAND_TIMEOUT


def check_admin():
    """
    Check if running with administrator privileges
    
    Returns:
        bool: True if running as admin
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
        require_admin (bool): Whether command requires admin
        
    Returns:
        dict: Contains 'success', 'stdout', 'stderr'
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


def generate_task_name():
    """
    Generate a random legitimate-looking task name
    
    Returns:
        str: Generated task name
    """
    prefix = random.choice(TASK_PREFIXES)
    suffix = random.choice(TASK_SUFFIXES)
    return f"{prefix}{suffix}"


def get_current_username():
    """
    Get current Windows username
    
    Returns:
        str: Username or 'SYSTEM'
    """
    result = run_command('echo %USERNAME%')
    if result['success'] and result['stdout']:
        return result['stdout'].strip()
    return 'SYSTEM'


def validate_payload_path(payload_path):
    """
    Validate payload path
    
    Args:
        payload_path (str): Path to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not payload_path:
        return False, "Payload path cannot be empty"
    
    # Check for dangerous characters
    dangerous_chars = ['\n', '\r', '\t']
    for char in dangerous_chars:
        if char in payload_path:
            return False, f"Invalid character in path: {repr(char)}"
    
    return True, None


def validate_time_format(time_str):
    """
    Validate time format (HH:MM)
    
    Args:
        time_str (str): Time string to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        parts = time_str.split(':')
        if len(parts) != 2:
            return False, "Time must be in HH:MM format"
        
        hour = int(parts[0])
        minute = int(parts[1])
        
        if hour < 0 or hour > 23:
            return False, "Hour must be between 0-23"
        if minute < 0 or minute > 59:
            return False, "Minute must be between 0-59"
        
        return True, None
    except ValueError:
        return False, "Invalid time format"


def clean_temp_file(file_path):
    """
    Safely remove temporary file
    
    Args:
        file_path (str): Path to file to remove
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass  # Silently fail on cleanup


def parse_task_list_output(output):
    """
    Parse schtasks /Query output into structured data
    
    Args:
        output (str): Command output
        
    Returns:
        list: List of task dictionaries
    """
    tasks = []
    current_task = {}
    
    for line in output.split('\n'):
        line = line.strip()
        if not line:
            if current_task:
                tasks.append(current_task)
                current_task = {}
            continue
        
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            current_task[key] = value
    
    if current_task:
        tasks.append(current_task)
    
    return tasks
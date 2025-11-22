"""
Shared utility functions for Service Persistence Framework
"""

import subprocess
import random
import os
import re
from pathlib import Path

def check_admin():
    """
    Check if running with administrator privileges
    
    Returns:
        bool: True if admin, False otherwise
    """
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def run_command(command, timeout=30):
    """
    Execute a system command and return results
    
    Args:
        command (str): Command to execute
        timeout (int): Command timeout in seconds
        
    Returns:
        dict: Command results with success, stdout, stderr
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'Command timed out',
            'timeout': True
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def generate_service_name(components):
    """
    Generate a legitimate-looking service name
    
    Args:
        components (dict): Service name components from config
        
    Returns:
        str: Generated service name
    """
    prefix = random.choice(components['prefixes'])
    middle = random.choice(components['middles'])
    suffix = random.choice(components['suffixes'])
    
    return f"{prefix}{middle}{suffix}"

def validate_binary_path(path):
    """
    Validate that a binary path exists and is executable
    
    Args:
        path (str): Path to binary
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not path:
        return False, "Binary path is empty"
    
    # Remove quotes if present
    clean_path = path.strip('"').strip("'")
    
    # Check if path exists
    if not os.path.exists(clean_path):
        return False, f"Binary does not exist: {clean_path}"
    
    # Check if it's a file
    if not os.path.isfile(clean_path):
        return False, f"Path is not a file: {clean_path}"
    
    # Check if executable
    if not clean_path.lower().endswith(('.exe', '.bat', '.cmd')):
        return False, f"File is not executable: {clean_path}"
    
    return True, None

def parse_service_output(output):
    """
    Parse sc.exe query output into structured data
    
    Args:
        output (str): Raw sc.exe output
        
    Returns:
        list: List of service dictionaries
    """
    services = []
    current_service = {}
    
    for line in output.split('\n'):
        line = line.strip()
        
        if 'SERVICE_NAME:' in line:
            if current_service:
                services.append(current_service)
            current_service = {
                'name': line.split(':', 1)[1].strip()
            }
        elif 'DISPLAY_NAME:' in line and current_service:
            current_service['display_name'] = line.split(':', 1)[1].strip()
        elif 'STATE' in line and current_service:
            # Extract state (RUNNING, STOPPED, etc.)
            parts = line.split()
            if len(parts) >= 3:
                current_service['state'] = parts[-1]
    
    if current_service:
        services.append(current_service)
    
    return services

def parse_service_config(output):
    """
    Parse sc qc output for service configuration
    
    Args:
        output (str): Raw sc qc output
        
    Returns:
        dict: Service configuration
    """
    config = {}
    
    for line in output.split('\n'):
        line = line.strip()
        
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            if 'SERVICE_NAME' in key:
                config['service_name'] = value
            elif 'DISPLAY_NAME' in key:
                config['display_name'] = value
            elif 'BINARY_PATH_NAME' in key:
                config['binary_path'] = value
            elif 'START_TYPE' in key:
                config['start_type'] = value
            elif 'SERVICE_START_NAME' in key:
                config['account'] = value
            elif 'DEPENDENCIES' in key:
                config['dependencies'] = value
    
    return config

def check_dotnet_compiler():
    """
    Check for available .NET compiler
    
    Returns:
        str: Path to csc.exe or None
    """
    from config import DOTNET_FRAMEWORK_PATHS
    
    for path in DOTNET_FRAMEWORK_PATHS:
        if os.path.exists(path):
            return path
    
    return None

def escape_command_for_wrapper(command):
    """
    Escape command for C# wrapper service
    
    Args:
        command (str): Original command
        
    Returns:
        str: Escaped command
    """
    # Escape backslashes and quotes
    escaped = command.replace('\\', '\\\\')
    escaped = escaped.replace('"', '\\"')
    
    return escaped

def get_service_info(service_name):
    """
    Get detailed information about a service
    
    Args:
        service_name (str): Name of service
        
    Returns:
        dict: Service information or None
    """
    command = f'sc qc "{service_name}"'
    result = run_command(command)
    
    if result['success']:
        return parse_service_config(result['stdout'])
    
    return None

def service_exists(service_name):
    """
    Check if a service exists
    
    Args:
        service_name (str): Name of service
        
    Returns:
        bool: True if service exists
    """
    info = get_service_info(service_name)
    return info is not None

def format_output(data, indent=0):
    """
    Format dictionary data for display
    
    Args:
        data (dict): Data to format
        indent (int): Indentation level
        
    Returns:
        str: Formatted output
    """
    output = []
    spacing = "  " * indent
    
    for key, value in data.items():
        if isinstance(value, dict):
            output.append(f"{spacing}{key}:")
            output.append(format_output(value, indent + 1))
        elif isinstance(value, list):
            output.append(f"{spacing}{key}:")
            for item in value:
                if isinstance(item, dict):
                    output.append(format_output(item, indent + 1))
                else:
                    output.append(f"{spacing}  - {item}")
        else:
            output.append(f"{spacing}{key}: {value}")
    
    return '\n'.join(output)
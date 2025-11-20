"""
Shared utility functions for WMI Persistence Framework
"""

import subprocess
import random
import os
import tempfile

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

def run_powershell(script, execution_policy='Bypass'):
    """
    Execute PowerShell script
    
    Args:
        script (str): PowerShell script content
        execution_policy (str): Execution policy
        
    Returns:
        dict: Execution results
    """
    # Create temporary script file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False) as f:
        script_path = f.name
        f.write(script)
    
    try:
        command = f'powershell.exe -ExecutionPolicy {execution_policy} -File "{script_path}"'
        result = run_command(command, timeout=60)
        return result
    finally:
        # Clean up temp file
        try:
            os.remove(script_path)
        except:
            pass

def run_powershell_command(ps_command, execution_policy='Bypass'):
    """
    Execute PowerShell command directly
    
    Args:
        ps_command (str): PowerShell command
        execution_policy (str): Execution policy
        
    Returns:
        dict: Execution results
    """
    command = f'powershell.exe -ExecutionPolicy {execution_policy} -Command "{ps_command}"'
    return run_command(command, timeout=60)

def generate_event_name(components):
    """
    Generate a legitimate-looking event name
    
    Args:
        components (dict): Event name components
        
    Returns:
        str: Generated event name
    """
    prefix = random.choice(components['prefixes'])
    middle = random.choice(components['middles'])
    suffix = random.choice(components['suffixes'])
    
    return f"{prefix}{middle}{suffix}"

def escape_powershell_command(command):
    """
    Escape command for use in PowerShell
    
    Args:
        command (str): Original command
        
    Returns:
        str: Escaped command
    """
    # Escape double quotes
    escaped = command.replace('"', '""')
    return escaped

def validate_wql_query(query):
    """
    Basic validation of WQL query
    
    Args:
        query (str): WQL query
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not query:
        return False, "Query is empty"
    
    # Check for basic WQL structure
    query_upper = query.upper()
    
    if 'SELECT' not in query_upper:
        return False, "Query must contain SELECT"
    
    if 'FROM' not in query_upper:
        return False, "Query must contain FROM"
    
    # Check for event class
    event_classes = [
        '__InstanceModificationEvent',
        '__InstanceCreationEvent',
        '__InstanceDeletionEvent',
        '__TimerEvent'
    ]
    
    has_event_class = any(cls.upper() in query_upper for cls in event_classes)
    
    if not has_event_class:
        return False, "Query must specify a valid event class"
    
    return True, None

def format_interval(seconds):
    """
    Format interval in human-readable form
    
    Args:
        seconds (int): Interval in seconds
        
    Returns:
        str: Formatted interval
    """
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    else:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''}"

def check_wmi_service():
    """
    Check if WMI service is running
    
    Returns:
        bool: True if WMI service is running
    """
    result = run_command('sc query winmgmt')
    
    if result['success']:
        return 'RUNNING' in result['stdout']
    
    return False

def encode_powershell_command(command):
    """
    Base64 encode PowerShell command
    
    Args:
        command (str): PowerShell command
        
    Returns:
        str: Base64 encoded command
    """
    import base64
    
    # Convert to UTF-16LE (PowerShell's encoding)
    encoded_bytes = command.encode('utf-16le')
    b64_encoded = base64.b64encode(encoded_bytes).decode('ascii')
    
    return b64_encoded
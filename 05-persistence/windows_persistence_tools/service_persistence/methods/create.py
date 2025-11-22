"""
Service creation methods
"""

import sys
import os
import random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import (
    run_command,
    validate_binary_path,
    check_admin,
    service_exists
)
from config import (
    SERVICE_START_TYPES,
    DEFAULT_DESCRIPTIONS
)

def create_service(service_name, binary_path, display_name=None, description=None, 
                  start_type='auto', account='LocalSystem'):
    """
    Create a new Windows service
    
    Args:
        service_name (str): Service name
        binary_path (str): Path to service executable
        display_name (str): Display name (optional)
        description (str): Service description (optional)
        start_type (str): Service start type (auto/delayed/demand)
        account (str): Service account
        
    Returns:
        dict: Result with service information
    """
    print(f"[*] Creating Windows service: {service_name}")
    
    # Check admin privileges
    if not check_admin():
        print("[!] Administrator privileges required")
        return {
            'success': False,
            'error': 'Administrator privileges required'
        }
    
    # Validate binary path
    is_valid, error = validate_binary_path(binary_path)
    if not is_valid:
        print(f"[-] {error}")
        return {
            'success': False,
            'error': error
        }
    
    # Check if service already exists
    if service_exists(service_name):
        print(f"[!] Service already exists: {service_name}")
        return {
            'success': False,
            'error': 'Service already exists'
        }
    
    # Set defaults
    if not display_name:
        display_name = service_name
    
    if not description:
        description = random.choice(DEFAULT_DESCRIPTIONS)
    
    # Get start type value
    start_value = SERVICE_START_TYPES.get(start_type, {}).get('value', 'auto')
    
    # Create service command
    command = (
        f'sc create "{service_name}" '
        f'binPath= "{binary_path}" '
        f'start= {start_value} '
        f'DisplayName= "{display_name}" '
        f'obj= {account}'
    )
    
    result = run_command(command)
    
    if not result['success']:
        print(f"[-] Failed to create service: {result.get('stderr', 'Unknown error')}")
        return {
            'success': False,
            'error': result.get('stderr', 'Unknown error')
        }
    
    print(f"[+] Service created successfully")
    
    # Set description
    desc_result = set_service_description(service_name, description)
    
    # Try to start the service
    start_result = start_service(service_name)
    
    # Generate removal command
    removal_cmd = f'sc stop "{service_name}" & sc delete "{service_name}"'
    
    return {
        'success': True,
        'service_name': service_name,
        'display_name': display_name,
        'binary_path': binary_path,
        'description': description,
        'start_type': start_type,
        'account': account,
        'started': start_result['success'],
        'removal_command': removal_cmd
    }

def create_delayed_service(service_name, binary_path, display_name=None, description=None):
    """
    Create service with delayed automatic start
    
    Args:
        service_name (str): Service name
        binary_path (str): Path to service executable
        display_name (str): Display name
        description (str): Service description
        
    Returns:
        dict: Result with service information
    """
    result = create_service(
        service_name=service_name,
        binary_path=binary_path,
        display_name=display_name,
        description=description,
        start_type='delayed'
    )
    
    if result['success']:
        print("[+] Service configured for delayed automatic start")
    
    return result

def set_service_description(service_name, description):
    """
    Set service description
    
    Args:
        service_name (str): Service name
        description (str): Description text
        
    Returns:
        dict: Command result
    """
    command = f'sc description "{service_name}" "{description}"'
    result = run_command(command)
    
    if result['success']:
        print(f"[+] Description set")
    
    return result

def set_service_failure_actions(service_name):
    """
    Configure service to restart on failure
    
    Args:
        service_name (str): Service name
        
    Returns:
        dict: Command result
    """
    # Set service to restart on failure
    command = (
        f'sc failure "{service_name}" '
        f'reset= 86400 '
        f'actions= restart/60000/restart/60000/restart/60000'
    )
    
    result = run_command(command)
    
    if result['success']:
        print(f"[+] Configured automatic restart on failure")
    
    return result

def start_service(service_name):
    """
    Start a Windows service
    
    Args:
        service_name (str): Service name
        
    Returns:
        dict: Command result
    """
    print(f"[*] Starting service: {service_name}")
    
    command = f'sc start "{service_name}"'
    result = run_command(command)
    
    if result['success']:
        print(f"[+] Service started successfully")
    else:
        # Service might not start if binary isn't a proper service
        error = result.get('stderr', '')
        if 'service-specific' in error.lower():
            print(f"[!] Service created but failed to start")
            print(f"[!] Binary may not be a proper Windows service")
        else:
            print(f"[-] Failed to start service: {error}")
    
    return result

def stop_service(service_name):
    """
    Stop a Windows service
    
    Args:
        service_name (str): Service name
        
    Returns:
        dict: Command result
    """
    print(f"[*] Stopping service: {service_name}")
    
    command = f'sc stop "{service_name}"'
    result = run_command(command)
    
    if result['success']:
        print(f"[+] Service stopped")
    else:
        print(f"[-] Failed to stop service")
    
    return result

def delete_service(service_name):
    """
    Delete a Windows service
    
    Args:
        service_name (str): Service name
        
    Returns:
        dict: Command result
    """
    print(f"[*] Deleting service: {service_name}")
    
    if not check_admin():
        print("[!] Administrator privileges required")
        return {
            'success': False,
            'error': 'Administrator privileges required'
        }
    
    # Stop service first
    stop_service(service_name)
    
    # Delete service
    command = f'sc delete "{service_name}"'
    result = run_command(command)
    
    if result['success']:
        print(f"[+] Service deleted successfully")
    else:
        print(f"[-] Failed to delete service")
    
    return result
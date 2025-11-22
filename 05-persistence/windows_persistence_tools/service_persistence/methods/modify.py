"""
Modify existing Windows services
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import (
    run_command,
    check_admin,
    validate_binary_path,
    get_service_info,
    service_exists
)
from methods.create import stop_service, start_service

def backup_service_config(service_name):
    """
    Backup original service configuration
    
    Args:
        service_name (str): Service name
        
    Returns:
        dict: Original configuration or None
    """
    print(f"[*] Backing up service configuration: {service_name}")
    
    config = get_service_info(service_name)
    
    if config:
        print(f"[+] Configuration backed up")
        return config
    else:
        print(f"[-] Failed to backup configuration")
        return None

def modify_service_binary(service_name, new_binary_path):
    """
    Modify service binary path
    
    Args:
        service_name (str): Service name
        new_binary_path (str): New binary path
        
    Returns:
        dict: Modification result with original config
    """
    print(f"\n[*] Modifying service: {service_name}")
    
    # Check admin privileges
    if not check_admin():
        print("[!] Administrator privileges required")
        return {
            'success': False,
            'error': 'Administrator privileges required'
        }
    
    # Check if service exists
    if not service_exists(service_name):
        print(f"[-] Service not found: {service_name}")
        return {
            'success': False,
            'error': 'Service not found'
        }
    
    # Validate new binary path
    is_valid, error = validate_binary_path(new_binary_path)
    if not is_valid:
        print(f"[-] {error}")
        return {
            'success': False,
            'error': error
        }
    
    # Backup original configuration
    original_config = backup_service_config(service_name)
    
    if not original_config:
        print("[!] Warning: Could not backup original configuration")
    
    # Modify service binary path
    modify_cmd = f'sc config "{service_name}" binPath= "{new_binary_path}"'
    result = run_command(modify_cmd)
    
    if not result['success']:
        print(f"[-] Failed to modify service: {result.get('stderr', 'Unknown error')}")
        return {
            'success': False,
            'error': result.get('stderr', 'Unknown error'),
            'original_config': original_config
        }
    
    print(f"[+] Service binary path modified")
    print(f"    Original: {original_config.get('binary_path', 'Unknown')}")
    print(f"    New: {new_binary_path}")
    
    # Restart service to apply changes
    print(f"[*] Restarting service...")
    stop_service(service_name)
    start_result = start_service(service_name)
    
    # Generate restore command
    restore_cmd = None
    if original_config and 'binary_path' in original_config:
        restore_cmd = f'sc config "{service_name}" binPath= "{original_config["binary_path"]}"'
    
    return {
        'success': True,
        'service_name': service_name,
        'original_binary': original_config.get('binary_path', 'Unknown'),
        'new_binary': new_binary_path,
        'original_config': original_config,
        'restore_command': restore_cmd,
        'started': start_result['success']
    }

def restore_service_config(service_name, original_config):
    """
    Restore service to original configuration
    
    Args:
        service_name (str): Service name
        original_config (dict): Original configuration
        
    Returns:
        dict: Restore result
    """
    print(f"[*] Restoring service configuration: {service_name}")
    
    if not check_admin():
        print("[!] Administrator privileges required")
        return {
            'success': False,
            'error': 'Administrator privileges required'
        }
    
    if not original_config or 'binary_path' not in original_config:
        print("[-] No original configuration available")
        return {
            'success': False,
            'error': 'No original configuration'
        }
    
    # Restore binary path
    binary_path = original_config['binary_path']
    restore_cmd = f'sc config "{service_name}" binPath= "{binary_path}"'
    
    result = run_command(restore_cmd)
    
    if result['success']:
        print(f"[+] Service restored to original configuration")
        print(f"    Binary: {binary_path}")
        
        # Restart service
        stop_service(service_name)
        start_service(service_name)
        
        return {
            'success': True,
            'service_name': service_name,
            'restored_binary': binary_path
        }
    else:
        print(f"[-] Failed to restore service")
        return {
            'success': False,
            'error': result.get('stderr', 'Unknown error')
        }

def modify_service_start_type(service_name, start_type):
    """
    Modify service start type
    
    Args:
        service_name (str): Service name
        start_type (str): New start type (auto/demand/disabled)
        
    Returns:
        dict: Modification result
    """
    print(f"[*] Modifying service start type: {service_name} -> {start_type}")
    
    if not check_admin():
        print("[!] Administrator privileges required")
        return {
            'success': False,
            'error': 'Administrator privileges required'
        }
    
    command = f'sc config "{service_name}" start= {start_type}'
    result = run_command(command)
    
    if result['success']:
        print(f"[+] Start type changed to: {start_type}")
        return {
            'success': True,
            'service_name': service_name,
            'start_type': start_type
        }
    else:
        print(f"[-] Failed to modify start type")
        return {
            'success': False,
            'error': result.get('stderr', 'Unknown error')
        }

def modify_service_dependencies(service_name, dependencies):
    """
    Modify service dependencies
    
    Args:
        service_name (str): Service name
        dependencies (list): List of dependency service names
        
    Returns:
        dict: Modification result
    """
    print(f"[*] Modifying service dependencies: {service_name}")
    
    if not check_admin():
        print("[!] Administrator privileges required")
        return {
            'success': False,
            'error': 'Administrator privileges required'
        }
    
    # Format dependencies (space-separated)
    dep_string = '/'.join(dependencies) if dependencies else ''
    
    command = f'sc config "{service_name}" depend= {dep_string}'
    result = run_command(command)
    
    if result['success']:
        print(f"[+] Dependencies modified")
        return {
            'success': True,
            'service_name': service_name,
            'dependencies': dependencies
        }
    else:
        print(f"[-] Failed to modify dependencies")
        return {
            'success': False,
            'error': result.get('stderr', 'Unknown error')
        }

def disable_service(service_name):
    """
    Disable a service
    
    Args:
        service_name (str): Service name
        
    Returns:
        dict: Result
    """
    print(f"[*] Disabling service: {service_name}")
    
    # Stop the service first
    stop_service(service_name)
    
    # Disable it
    return modify_service_start_type(service_name, 'disabled')
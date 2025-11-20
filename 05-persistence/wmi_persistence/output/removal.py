"""
Generate removal scripts for WMI persistence
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import run_powershell, check_admin
from templates.powershell import generate_removal_script as gen_removal_ps
from config import OUTPUT_PATHS, WMI_NAMESPACES

def remove_wmi_persistence(event_name):
    """
    Remove WMI persistence by event name
    
    Args:
        event_name (str): Event name prefix
        
    Returns:
        dict: Removal result
    """
    print(f"[*] Removing WMI persistence: {event_name}")
    
    if not check_admin():
        print("[!] Administrator privileges required")
        return {
            'success': False,
            'error': 'Administrator privileges required'
        }
    
    # Generate component names
    filter_name = f"_{event_name}_Filter"
    consumer_name = f"_{event_name}_Consumer"
    
    # Generate removal script
    ps_script = gen_removal_ps(
        filter_name=filter_name,
        consumer_name=consumer_name,
        event_name=event_name
    )
    
    # Execute removal
    result = run_powershell(ps_script)
    
    if result['success']:
        print(f"[+] WMI persistence removed: {event_name}")
        return {
            'success': True,
            'event_name': event_name,
            'filter_name': filter_name,
            'consumer_name': consumer_name
        }
    else:
        error = result.get('stderr', result.get('error', 'Unknown error'))
        print(f"[-] Failed to remove WMI persistence: {error}")
        return {
            'success': False,
            'error': error
        }

def generate_removal_script(subscription_data):
    """
    Generate PowerShell removal script file
    
    Args:
        subscription_data (dict): Subscription information
        
    Returns:
        str: Path to removal script
    """
    event_name = subscription_data.get('event_name')
    
    if not event_name:
        return None
    
    script_path = OUTPUT_PATHS['removal_script'].format(event_name=event_name)
    
    filter_name = subscription_data.get('filter_name', f"_{event_name}_Filter")
    consumer_name = subscription_data.get('consumer_name', f"_{event_name}_Consumer")
    
    # Generate script content
    script_content = gen_removal_ps(
        filter_name=filter_name,
        consumer_name=consumer_name,
        event_name=event_name
    )
    
    try:
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        return script_path
    except Exception as e:
        print(f"[-] Failed to create removal script: {e}")
        return None

def remove_all_suspicious(suspicious_data):
    """
    Remove all suspicious WMI subscriptions
    
    Args:
        suspicious_data (dict): Suspicious subscription data from scanner
        
    Returns:
        dict: Removal results
    """
    print("[*] Removing all suspicious WMI subscriptions...")
    
    if not check_admin():
        print("[!] Administrator privileges required")
        return {
            'success': False,
            'error': 'Administrator privileges required'
        }
    
    results = {
        'removed_filters': [],
        'removed_consumers': [],
        'failed': [],
        'total': 0
    }
    
    # Remove suspicious filters
    for filter_data in suspicious_data.get('filters', []):
        filter_name = filter_data.get('name')
        ps_command = f'Get-WmiObject -Namespace {WMI_NAMESPACES["subscription"]} -Class __EventFilter -Filter "name=\'{filter_name}\'" | Remove-WmiObject'
        
        result = run_powershell(ps_command)
        
        if result.get('success'):
            results['removed_filters'].append(filter_name)
        else:
            results['failed'].append(filter_name)
        
        results['total'] += 1
    
    # Remove suspicious consumers
    for consumer_data in suspicious_data.get('consumers', []):
        consumer_name = consumer_data.get('name')
        ps_command = f'Get-WmiObject -Namespace {WMI_NAMESPACES["subscription"]} -Class CommandLineEventConsumer -Filter "name=\'{consumer_name}\'" | Remove-WmiObject'
        
        result = run_powershell(ps_command)
        
        if result.get('success'):
            results['removed_consumers'].append(consumer_name)
        else:
            results['failed'].append(consumer_name)
        
        results['total'] += 1
    
    print(f"[+] Removed {len(results['removed_filters'])} filters")
    print(f"[+] Removed {len(results['removed_consumers'])} consumers")
    
    if results['failed']:
        print(f"[!] Failed to remove {len(results['failed'])} items")
    
    return results

def generate_forensic_report(subscriptions_data, output_path='wmi_persistence_report.txt'):
    """
    Generate forensic report of all WMI operations
    
    Args:
        subscriptions_data (list): List of subscription operations
        output_path (str): Output file path
        
    Returns:
        str: Path to report file
    """
    lines = [
        "="*60,
        "WMI EVENT SUBSCRIPTION PERSISTENCE - FORENSIC REPORT",
        "="*60,
        "",
        f"Total Operations: {len(subscriptions_data)}",
        ""
    ]
    
    for idx, sub in enumerate(subscriptions_data, 1):
        lines.extend([
            f"Subscription #{idx}",
            "-"*40,
            f"Event Name: {sub.get('event_name', 'Unknown')}",
            f"Filter Name: {sub.get('filter_name', 'N/A')}",
            f"Consumer Name: {sub.get('consumer_name', 'N/A')}",
            f"Trigger Type: {sub.get('trigger_type', 'N/A')}",
            f"Command: {sub.get('command', 'N/A')}",
            f"WQL Query: {sub.get('wql_query', 'N/A')}",
            ""
        ])
        
        if sub.get('trigger_type') == 'interval':
            lines.append(f"Interval: {sub.get('interval', 'N/A')} seconds")
            lines.append("")
        
        if sub.get('trigger_type') in ['process_creation', 'process_deletion']:
            lines.append(f"Process: {sub.get('process_name', 'N/A')}")
            lines.append("")
    
    lines.extend([
        "="*60,
        "END OF REPORT",
        "="*60
    ])
    
    try:
        with open(output_path, 'w') as f:
            f.write('\n'.join(lines))
        
        return output_path
    except Exception as e:
        print(f"[-] Failed to create forensic report: {e}")
        return None
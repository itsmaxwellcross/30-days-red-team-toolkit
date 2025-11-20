"""
Detection and scanning for suspicious services
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import (
    run_command,
    parse_service_output,
    get_service_info,
    format_output
)
from config import SUSPICIOUS_INDICATORS

def scan_all_services():
    """
    Enumerate all Windows services
    
    Returns:
        list: List of all services
    """
    print("[*] Enumerating all Windows services...")
    
    command = 'sc query state= all'
    result = run_command(command)
    
    if result['success']:
        services = parse_service_output(result['stdout'])
        print(f"[+] Found {len(services)} services")
        return services
    else:
        print("[-] Failed to enumerate services")
        return []

def check_service_indicators(service_config):
    """
    Check service for suspicious indicators
    
    Args:
        service_config (dict): Service configuration
        
    Returns:
        dict: Detection results
    """
    indicators = []
    binary_path = service_config.get('binary_path', '').lower()
    
    # Check for suspicious paths
    for path_indicator in SUSPICIOUS_INDICATORS['paths']:
        if path_indicator in binary_path:
            indicators.append({
                'type': 'suspicious_path',
                'indicator': path_indicator,
                'severity': 'high'
            })
    
    # Check for suspicious executables
    for exe_indicator in SUSPICIOUS_INDICATORS['executables']:
        if exe_indicator in binary_path:
            indicators.append({
                'type': 'suspicious_executable',
                'indicator': exe_indicator,
                'severity': 'high'
            })
    
    # Check for suspicious command line arguments
    for arg_indicator in SUSPICIOUS_INDICATORS['arguments']:
        if arg_indicator in binary_path:
            indicators.append({
                'type': 'suspicious_argument',
                'indicator': arg_indicator,
                'severity': 'critical'
            })
    
    return {
        'has_indicators': len(indicators) > 0,
        'indicator_count': len(indicators),
        'indicators': indicators
    }

def find_suspicious_services():
    """
    Scan for suspicious services
    
    Returns:
        list: List of suspicious services with details
    """
    print("\n[*] Scanning for suspicious services...")
    
    # Get all services
    services = scan_all_services()
    
    if not services:
        return []
    
    suspicious = []
    
    for service in services:
        service_name = service.get('name')
        
        # Get detailed service configuration
        config = get_service_info(service_name)
        
        if not config:
            continue
        
        # Check for indicators
        detection = check_service_indicators(config)
        
        if detection['has_indicators']:
            suspicious.append({
                'name': service_name,
                'display_name': config.get('display_name', 'N/A'),
                'binary_path': config.get('binary_path', 'N/A'),
                'start_type': config.get('start_type', 'N/A'),
                'state': service.get('state', 'UNKNOWN'),
                'detection': detection
            })
    
    print(f"\n[!] Found {len(suspicious)} suspicious services")
    
    return suspicious

def find_hidden_services():
    """
    Find services with suspicious display names or hidden characteristics
    
    Returns:
        list: List of potentially hidden services
    """
    print("[*] Checking for hidden services...")
    
    services = scan_all_services()
    hidden = []
    
    for service in services:
        service_name = service.get('name', '')
        display_name = service.get('display_name', '')
        
        # Check for suspicious naming patterns
        if (not display_name or 
            display_name == service_name or
            len(display_name) < 3 or
            display_name.startswith('_')):
            
            config = get_service_info(service_name)
            if config:
                hidden.append({
                    'name': service_name,
                    'display_name': display_name,
                    'binary_path': config.get('binary_path', 'N/A'),
                    'reason': 'suspicious_naming'
                })
    
    print(f"[+] Found {len(hidden)} potentially hidden services")
    return hidden

def find_system_services_with_user_binaries():
    """
    Find SYSTEM services running user-writable binaries
    
    Returns:
        list: List of risky services
    """
    print("[*] Checking for SYSTEM services with user binaries...")
    
    services = scan_all_services()
    risky = []
    
    user_paths = ['users\\', 'appdata\\', 'programdata\\']
    
    for service in services:
        config = get_service_info(service.get('name'))
        
        if not config:
            continue
        
        binary_path = config.get('binary_path', '').lower()
        account = config.get('account', '').lower()
        
        # Check if SYSTEM service with user path
        if 'localsystem' in account or 'system' in account:
            for user_path in user_paths:
                if user_path in binary_path:
                    risky.append({
                        'name': service.get('name'),
                        'display_name': config.get('display_name'),
                        'binary_path': config.get('binary_path'),
                        'account': config.get('account'),
                        'reason': 'system_service_user_binary'
                    })
                    break
    
    print(f"[+] Found {len(risky)} risky service configurations")
    return risky

def generate_service_report():
    """
    Generate comprehensive service security report
    
    Returns:
        dict: Complete report
    """
    print("\n" + "="*60)
    print("SERVICE PERSISTENCE DETECTION REPORT")
    print("="*60 + "\n")
    
    # Scan for different types of suspicious services
    suspicious = find_suspicious_services()
    hidden = find_hidden_services()
    risky = find_system_services_with_user_binaries()
    
    report = {
        'suspicious_services': suspicious,
        'hidden_services': hidden,
        'risky_system_services': risky,
        'total_issues': len(suspicious) + len(hidden) + len(risky)
    }
    
    # Display summary
    print("\n[*] SUMMARY")
    print(f"    Suspicious services: {len(suspicious)}")
    print(f"    Hidden services: {len(hidden)}")
    print(f"    Risky SYSTEM services: {len(risky)}")
    print(f"    Total issues: {report['total_issues']}")
    
    # Display details
    if suspicious:
        print("\n[!] SUSPICIOUS SERVICES:")
        for svc in suspicious:
            print(f"\n  Service: {svc['name']}")
            print(f"  Display: {svc['display_name']}")
            print(f"  Binary: {svc['binary_path']}")
            print(f"  Indicators: {svc['detection']['indicator_count']}")
            for indicator in svc['detection']['indicators']:
                print(f"    - {indicator['type']}: {indicator['indicator']} [{indicator['severity']}]")
    
    if hidden:
        print("\n[!] POTENTIALLY HIDDEN SERVICES:")
        for svc in hidden[:10]:  # Show first 10
            print(f"\n  Service: {svc['name']}")
            print(f"  Display: {svc['display_name']}")
            print(f"  Binary: {svc['binary_path']}")
    
    if risky:
        print("\n[!] RISKY SYSTEM SERVICES:")
        for svc in risky[:10]:  # Show first 10
            print(f"\n  Service: {svc['name']}")
            print(f"  Binary: {svc['binary_path']}")
            print(f"  Account: {svc['account']}")
    
    print("\n" + "="*60 + "\n")
    
    return report

def list_services(state='all'):
    """
    List services by state
    
    Args:
        state (str): Service state (all/running/stopped)
        
    Returns:
        list: List of services
    """
    print(f"[*] Listing {state} services...")
    
    command = f'sc query state= {state}'
    result = run_command(command)
    
    if result['success']:
        services = parse_service_output(result['stdout'])
        
        print(f"\n[+] Found {len(services)} {state} services\n")
        
        for svc in services[:50]:  # Show first 50
            print(f"  {svc.get('name', 'Unknown'):<40} {svc.get('state', 'UNKNOWN')}")
        
        if len(services) > 50:
            print(f"\n  ... and {len(services) - 50} more")
        
        return services
    else:
        print("[-] Failed to list services")
        return []
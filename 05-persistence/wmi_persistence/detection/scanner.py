"""
Detection and scanning for suspicious WMI event subscriptions
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import run_powershell_command, run_powershell
from templates.powershell import generate_enumeration_script
from config import SUSPICIOUS_INDICATORS, WMI_NAMESPACES

def enumerate_filters():
    """
    Enumerate all WMI event filters
    
    Returns:
        list: List of event filters
    """
    print("[*] Enumerating WMI event filters...")
    
    ps_command = f'Get-WmiObject -Namespace {WMI_NAMESPACES["subscription"]} -Class __EventFilter | Select-Object Name, Query'
    result = run_powershell_command(ps_command)
    
    if result['success']:
        output = result['stdout']
        print(f"[+] Event filters enumerated")
        return parse_filter_output(output)
    else:
        print("[-] Failed to enumerate filters")
        return []

def enumerate_consumers():
    """
    Enumerate all WMI consumers
    
    Returns:
        list: List of consumers
    """
    print("[*] Enumerating WMI consumers...")
    
    ps_command = f'Get-WmiObject -Namespace {WMI_NAMESPACES["subscription"]} -Class CommandLineEventConsumer | Select-Object Name, CommandLineTemplate'
    result = run_powershell_command(ps_command)
    
    if result['success']:
        output = result['stdout']
        print(f"[+] Consumers enumerated")
        return parse_consumer_output(output)
    else:
        print("[-] Failed to enumerate consumers")
        return []

def enumerate_bindings():
    """
    Enumerate all filter-to-consumer bindings
    
    Returns:
        list: List of bindings
    """
    print("[*] Enumerating WMI bindings...")
    
    ps_command = f'Get-WmiObject -Namespace {WMI_NAMESPACES["subscription"]} -Class __FilterToConsumerBinding'
    result = run_powershell_command(ps_command)
    
    if result['success']:
        print(f"[+] Bindings enumerated")
        return parse_binding_output(result['stdout'])
    else:
        print("[-] Failed to enumerate bindings")
        return []

def parse_filter_output(output):
    """Parse filter enumeration output"""
    filters = []
    current_filter = {}
    
    for line in output.split('\n'):
        line = line.strip()
        
        if line.startswith('Name'):
            if current_filter:
                filters.append(current_filter)
            current_filter = {'name': line.split(':', 1)[1].strip() if ':' in line else ''}
        elif line.startswith('Query'):
            current_filter['query'] = line.split(':', 1)[1].strip() if ':' in line else ''
    
    if current_filter:
        filters.append(current_filter)
    
    return filters

def parse_consumer_output(output):
    """Parse consumer enumeration output"""
    consumers = []
    current_consumer = {}
    
    for line in output.split('\n'):
        line = line.strip()
        
        if line.startswith('Name'):
            if current_consumer:
                consumers.append(current_consumer)
            current_consumer = {'name': line.split(':', 1)[1].strip() if ':' in line else ''}
        elif line.startswith('CommandLineTemplate'):
            current_consumer['command'] = line.split(':', 1)[1].strip() if ':' in line else ''
    
    if current_consumer:
        consumers.append(current_consumer)
    
    return consumers

def parse_binding_output(output):
    """Parse binding enumeration output"""
    # Simplified parsing - bindings are complex objects
    bindings = []
    
    if 'Filter' in output and 'Consumer' in output:
        # Basic parsing - actual implementation would be more sophisticated
        bindings.append({'type': 'binding', 'details': 'Binding exists'})
    
    return bindings

def check_filter_indicators(filter_data):
    """
    Check filter for suspicious indicators
    
    Args:
        filter_data (dict): Filter information
        
    Returns:
        dict: Detection results
    """
    indicators = []
    query = filter_data.get('query', '').lower()
    
    # Check for suspicious query patterns
    for pattern in SUSPICIOUS_INDICATORS['suspicious_filters']:
        if pattern.lower() in query:
            indicators.append({
                'type': 'suspicious_query',
                'indicator': pattern,
                'severity': 'medium'
            })
    
    # Check for very short intervals (aggressive polling)
    if 'within' in query:
        try:
            # Extract interval value
            interval_part = query.split('within')[1].split('where')[0].strip()
            interval = int(''.join(filter(str.isdigit, interval_part)))
            
            if interval < 30:
                indicators.append({
                    'type': 'aggressive_polling',
                    'indicator': f'Interval: {interval} seconds',
                    'severity': 'high'
                })
        except:
            pass
    
    return {
        'has_indicators': len(indicators) > 0,
        'indicator_count': len(indicators),
        'indicators': indicators
    }

def check_consumer_indicators(consumer_data):
    """
    Check consumer for suspicious indicators
    
    Args:
        consumer_data (dict): Consumer information
        
    Returns:
        dict: Detection results
    """
    indicators = []
    command = consumer_data.get('command', '').lower()
    
    # Check for suspicious commands
    for cmd_indicator in SUSPICIOUS_INDICATORS['commands']:
        if cmd_indicator.lower() in command:
            indicators.append({
                'type': 'suspicious_command',
                'indicator': cmd_indicator,
                'severity': 'high'
            })
    
    # Check for suspicious arguments
    for arg_indicator in SUSPICIOUS_INDICATORS['arguments']:
        if arg_indicator.lower() in command:
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

def find_suspicious_subscriptions():
    """
    Scan for suspicious WMI event subscriptions
    
    Returns:
        dict: Detection results
    """
    print("\n[*] Scanning for suspicious WMI subscriptions...")
    
    filters = enumerate_filters()
    consumers = enumerate_consumers()
    
    suspicious_filters = []
    suspicious_consumers = []
    
    # Check filters
    for filter_data in filters:
        detection = check_filter_indicators(filter_data)
        if detection['has_indicators']:
            suspicious_filters.append({
                **filter_data,
                'detection': detection
            })
    
    # Check consumers
    for consumer_data in consumers:
        detection = check_consumer_indicators(consumer_data)
        if detection['has_indicators']:
            suspicious_consumers.append({
                **consumer_data,
                'detection': detection
            })
    
    return {
        'filters': suspicious_filters,
        'consumers': suspicious_consumers,
        'total_suspicious': len(suspicious_filters) + len(suspicious_consumers)
    }

def generate_wmi_report():
    """
    Generate comprehensive WMI subscription report
    
    Returns:
        dict: Complete report
    """
    print("\n" + "="*60)
    print("WMI EVENT SUBSCRIPTION DETECTION REPORT")
    print("="*60 + "\n")
    
    # Get all subscriptions
    all_filters = enumerate_filters()
    all_consumers = enumerate_consumers()
    
    # Find suspicious ones
    suspicious = find_suspicious_subscriptions()
    
    report = {
        'total_filters': len(all_filters),
        'total_consumers': len(all_consumers),
        'suspicious_filters': suspicious['filters'],
        'suspicious_consumers': suspicious['consumers'],
        'total_suspicious': suspicious['total_suspicious']
    }
    
    # Display summary
    print("\n[*] SUMMARY")
    print(f"    Total Filters: {report['total_filters']}")
    print(f"    Total Consumers: {report['total_consumers']}")
    print(f"    Suspicious Filters: {len(report['suspicious_filters'])}")
    print(f"    Suspicious Consumers: {len(report['suspicious_consumers'])}")
    print(f"    Total Issues: {report['total_suspicious']}")
    
    # Display suspicious filters
    if report['suspicious_filters']:
        print("\n[!] SUSPICIOUS FILTERS:")
        for flt in report['suspicious_filters']:
            print(f"\n  Filter: {flt['name']}")
            print(f"  Query: {flt.get('query', 'N/A')}")
            print(f"  Indicators: {flt['detection']['indicator_count']}")
            for indicator in flt['detection']['indicators']:
                print(f"    - {indicator['type']}: {indicator['indicator']} [{indicator['severity']}]")
    
    # Display suspicious consumers
    if report['suspicious_consumers']:
        print("\n[!] SUSPICIOUS CONSUMERS:")
        for cons in report['suspicious_consumers']:
            print(f"\n  Consumer: {cons['name']}")
            print(f"  Command: {cons.get('command', 'N/A')}")
            print(f"  Indicators: {cons['detection']['indicator_count']}")
            for indicator in cons['detection']['indicators']:
                print(f"    - {indicator['type']}: {indicator['indicator']} [{indicator['severity']}]")
    
    print("\n" + "="*60 + "\n")
    
    return report

def list_all_subscriptions():
    """
    List all WMI event subscriptions
    
    Returns:
        dict: All subscriptions
    """
    print("\n[*] Listing all WMI event subscriptions...")
    
    # Use complete enumeration script
    ps_script = generate_enumeration_script()
    result = run_powershell(ps_script)
    
    if result['success']:
        print(result['stdout'])
    else:
        print("[-] Failed to enumerate subscriptions")
    
    return {
        'success': result['success'],
        'output': result.get('stdout', '')
    }
"""
DGA Utilities - Helper functions
"""

import socket
import json
from datetime import datetime


def check_domain_active(domain, timeout=2):
    """
    Check if a domain is active
    
    Args:
        domain (str): Domain to check
        timeout (int): Timeout in seconds
    
    Returns:
        bool: True if domain resolves, False otherwise
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.gethostbyname(domain)
        return True
    except:
        return False


def format_output(domains_data, format_type='text'):
    """
    Format domain data for output
    
    Args:
        domains_data (list): List of domain data
        format_type (str): Output format ('text', 'json', 'csv')
    
    Returns:
        str: Formatted output
    """
    if format_type == 'json':
        return json.dumps(domains_data, indent=2)
    
    elif format_type == 'csv':
        lines = ['date,domain_number,domain']
        for day_data in domains_data:
            date = day_data['date']
            for i, domain in enumerate(day_data['domains'], 1):
                lines.append(f"{date},{i},{domain}")
        return '\n'.join(lines)
    
    else:  # text
        output = []
        for day_data in domains_data:
            output.append(f"\n{day_data['date']}:")
            for i, domain in enumerate(day_data['domains'], 1):
                output.append(f"  {i}. {domain}")
        return '\n'.join(output)


def save_domains_to_file(domains_data, filename, format_type='text'):
    """
    Save domains to file
    
    Args:
        domains_data (list): List of domain data
        filename (str): Output filename
        format_type (str): Output format ('text', 'json', 'csv')
    """
    content = format_output(domains_data, format_type)
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"[+] Domains saved to: {filename}")


def check_domain_list(domains, timeout=2, verbose=True):
    """
    Check multiple domains for availability
    
    Args:
        domains (list): List of domains to check
        timeout (int): Timeout per domain
        verbose (bool): Print progress
    
    Returns:
        dict: Results with active and inactive domains
    """
    active = []
    inactive = []
    
    for domain in domains:
        if verbose:
            print(f"[*] Checking {domain}...", end=' ')
        
        if check_domain_active(domain, timeout):
            active.append(domain)
            if verbose:
                print("✓ Active")
        else:
            inactive.append(domain)
            if verbose:
                print("✗ Inactive")
    
    return {
        'active': active,
        'inactive': inactive,
        'total': len(domains),
        'active_count': len(active),
        'inactive_count': len(inactive)
    }


def generate_registration_commands(domains, registrar='namecheap'):
    """
    Generate domain registration commands
    
    Args:
        domains (list): List of domains to register
        registrar (str): Domain registrar
    
    Returns:
        list: Registration commands
    """
    commands = []
    
    if registrar == 'namecheap':
        for domain in domains:
            commands.append(f"# Register {domain}")
            commands.append(f"namecheap domain register {domain}")
    
    elif registrar == 'godaddy':
        for domain in domains:
            commands.append(f"# Register {domain}")
            commands.append(f"godaddy domain register {domain}")
    
    elif registrar == 'cli':
        # Generic CLI-based registration
        for domain in domains:
            commands.append(f"register_domain {domain}")
    
    return commands


def calculate_dga_cost(num_domains, price_per_domain=10.0, years=1):
    """
    Calculate cost of registering DGA domains
    
    Args:
        num_domains (int): Number of domains
        price_per_domain (float): Price per domain per year
        years (int): Registration period
    
    Returns:
        dict: Cost breakdown
    """
    total_cost = num_domains * price_per_domain * years
    
    return {
        'num_domains': num_domains,
        'price_per_domain': price_per_domain,
        'years': years,
        'total_cost': total_cost,
        'cost_per_month': total_cost / (years * 12),
        'cost_per_day': total_cost / (years * 365)
    }
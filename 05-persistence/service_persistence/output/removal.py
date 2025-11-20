"""
Generate removal and restore scripts
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OUTPUT_PATHS

def generate_removal_script(service_data):
    """
    Generate batch script to remove service
    
    Args:
        service_data (dict): Service creation data
        
    Returns:
        str: Path to removal script
    """
    service_name = service_data.get('service_name')
    
    if not service_name:
        return None
    
    script_path = OUTPUT_PATHS['removal_script'].format(service_name=service_name)
    
    # Build removal script
    script_lines = [
        '@echo off',
        'echo Service Removal Script',
        f'echo Service: {service_name}',
        'echo.',
        'echo Stopping service...',
        f'sc stop "{service_name}"',
        'timeout /t 2 /nobreak >nul',
        'echo.',
        'echo Deleting service...',
        f'sc delete "{service_name}"',
        'echo.',
    ]
    
    # Add wrapper cleanup if applicable
    if 'wrapper' in service_data:
        wrapper_source = OUTPUT_PATHS['wrapper_source'].format(service_name=service_name)
        wrapper_binary = OUTPUT_PATHS['wrapper_binary'].format(service_name=service_name)
        
        script_lines.extend([
            'echo Cleaning up wrapper files...',
            f'del /f /q "{wrapper_source}" 2>nul',
            f'del /f /q "{wrapper_binary}" 2>nul',
            'echo.',
        ])
    
    script_lines.extend([
        'echo Service removed successfully',
        'pause'
    ])
    
    try:
        with open(script_path, 'w') as f:
            f.write('\n'.join(script_lines))
        
        return script_path
    except Exception as e:
        print(f"[-] Failed to create removal script: {e}")
        return None

def generate_restore_script(service_data):
    """
    Generate batch script to restore original service configuration
    
    Args:
        service_data (dict): Service modification data
        
    Returns:
        str: Path to restore script
    """
    service_name = service_data.get('service_name')
    original_binary = service_data.get('original_binary')
    
    if not service_name or not original_binary:
        return None
    
    script_path = OUTPUT_PATHS['restore_script'].format(service_name=service_name)
    
    # Build restore script
    script_lines = [
        '@echo off',
        'echo Service Restore Script',
        f'echo Service: {service_name}',
        'echo.',
        'echo Stopping service...',
        f'sc stop "{service_name}"',
        'timeout /t 2 /nobreak >nul',
        'echo.',
        'echo Restoring original configuration...',
        f'sc config "{service_name}" binPath= "{original_binary}"',
        'echo.',
        'echo Starting service...',
        f'sc start "{service_name}"',
        'echo.',
        'echo Service restored successfully',
        'pause'
    ]
    
    try:
        with open(script_path, 'w') as f:
            f.write('\n'.join(script_lines))
        
        return script_path
    except Exception as e:
        print(f"[-] Failed to create restore script: {e}")
        return None

def generate_forensic_report(services_data, output_path='service_persistence_report.txt'):
    """
    Generate forensic report of all service operations
    
    Args:
        services_data (list): List of service operations
        output_path (str): Output file path
        
    Returns:
        str: Path to report file
    """
    lines = [
        "="*60,
        "SERVICE PERSISTENCE - FORENSIC REPORT",
        "="*60,
        "",
        f"Total Operations: {len(services_data)}",
        ""
    ]
    
    for idx, service in enumerate(services_data, 1):
        lines.extend([
            f"Operation #{idx}",
            "-"*40,
            f"Service Name: {service.get('service_name', 'Unknown')}",
            f"Display Name: {service.get('display_name', 'N/A')}",
            f"Binary Path: {service.get('binary_path', 'N/A')}",
            f"Start Type: {service.get('start_type', 'N/A')}",
            ""
        ])
        
        if 'wrapper' in service:
            lines.extend([
                "Wrapper Information:",
                f"  Command: {service['wrapper'].get('command', 'N/A')}",
                f"  Source: {service['wrapper'].get('source_path', 'N/A')}",
                f"  Binary: {service['wrapper'].get('binary_path', 'N/A')}",
                ""
            ])
        
        if 'removal_command' in service:
            lines.extend([
                f"Removal Command: {service['removal_command']}",
                ""
            ])
    
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
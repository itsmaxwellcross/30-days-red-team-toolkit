#!/usr/bin/env python3
"""
Windows Service Persistence Framework - CLI Interface
Educational tool for demonstrating service persistence techniques
"""

import sys
import os
import argparse

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.orchestrator import ServicePersistenceOrchestrator
from core.utils import check_admin

def print_banner():
    """Print tool banner"""
    banner = """
╔═══════════════════════════════════════════════════════╗
║     Windows Service Persistence Framework             ║
║     Educational & Authorized Testing Only             ║
╚═══════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(
        description='Windows Service Persistence Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create new service with executable
  python main.py --create C:\\payload.exe --service-name MyService
  
  # Create wrapped service (for non-service binaries)
  python main.py --create-wrapper "powershell -enc BASE64PAYLOAD"
  
  # Create delayed-start service
  python main.py --create C:\\payload.exe --start-type delayed
  
  # Modify existing service
  python main.py --modify UpdateOrchestrator --new-binary C:\\malicious.exe
  
  # Scan for suspicious services
  python main.py --check-suspicious
  
  # List all services
  python main.py --list
  
  # Delete service
  python main.py --delete MyService
        """
    )
    
    # Action arguments
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--create', type=str, metavar='BINARY_PATH',
                            help='Create new service with executable')
    action_group.add_argument('--create-wrapper', type=str, metavar='COMMAND',
                            help='Create wrapped service for non-service binary')
    action_group.add_argument('--modify', type=str, metavar='SERVICE_NAME',
                            help='Modify existing service')
    action_group.add_argument('--list', action='store_true',
                            help='List all services')
    action_group.add_argument('--list-running', action='store_true',
                            help='List running services only')
    action_group.add_argument('--check-suspicious', action='store_true',
                            help='Scan for suspicious services')
    action_group.add_argument('--delete', type=str, metavar='SERVICE_NAME',
                            help='Delete a service')
    
    # Service configuration arguments
    parser.add_argument('--service-name', type=str,
                       help='Custom service name (auto-generated if not specified)')
    parser.add_argument('--display-name', type=str,
                       help='Service display name')
    parser.add_argument('--description', type=str,
                       help='Service description')
    parser.add_argument('--start-type', type=str, choices=['auto', 'delayed', 'demand'],
                       default='auto', help='Service start type (default: auto)')
    parser.add_argument('--new-binary', type=str,
                       help='New binary path for service modification')
    
    args = parser.parse_args()
    
    # Check admin for operations that require it
    if args.create or args.create_wrapper or args.modify or args.delete:
        if not check_admin():
            print("\n[!] ERROR: This operation requires administrator privileges")
            print("[!] Please run as administrator\n")
            sys.exit(1)
    
    # Initialize orchestrator
    orchestrator = ServicePersistenceOrchestrator()
    
    try:
        # Execute requested action
        if args.create:
            result = orchestrator.create_service(
                payload_path=args.create,
                service_name=args.service_name,
                display_name=args.display_name,
                description=args.description,
                method='create',
                start_type=args.start_type
            )
            
            if result.get('success'):
                print("\n[+] SUCCESS")
                print(f"[+] Service Name: {result['service_name']}")
                print(f"[+] Binary: {result['binary_path']}")
                if 'removal_script_path' in result:
                    print(f"[+] Removal Script: {result['removal_script_path']}")
            else:
                print(f"\n[-] FAILED: {result.get('error', 'Unknown error')}")
                sys.exit(1)
        
        elif args.create_wrapper:
            result = orchestrator.create_service(
                payload_command=args.create_wrapper,
                service_name=args.service_name,
                display_name=args.display_name,
                description=args.description,
                method='wrapper'
            )
            
            if result.get('success'):
                print("\n[+] SUCCESS")
                print(f"[+] Service Name: {result['service_name']}")
                print(f"[+] Wrapper Binary: {result['binary_path']}")
                print(f"[+] Executing: {args.create_wrapper}")
                if 'removal_script_path' in result:
                    print(f"[+] Removal Script: {result['removal_script_path']}")
            else:
                print(f"\n[-] FAILED: {result.get('error', 'Unknown error')}")
                sys.exit(1)
        
        elif args.modify:
            if not args.new_binary:
                print("\n[-] ERROR: --new-binary required for modification")
                sys.exit(1)
            
            result = orchestrator.modify_service(args.modify, args.new_binary)
            
            if result.get('success'):
                print("\n[+] SUCCESS")
                print(f"[+] Service Modified: {result['service_name']}")
                print(f"[+] Original: {result['original_binary']}")
                print(f"[+] New: {result['new_binary']}")
                if 'restore_script_path' in result:
                    print(f"[+] Restore Script: {result['restore_script_path']}")
            else:
                print(f"\n[-] FAILED: {result.get('error', 'Unknown error')}")
                sys.exit(1)
        
        elif args.list:
            orchestrator.list_all_services()
        
        elif args.list_running:
            orchestrator.list_running_services()
        
        elif args.check_suspicious:
            report = orchestrator.scan_services()
            
            if report['total_issues'] > 0:
                print(f"\n[!] Detection complete - {report['total_issues']} issues found")
            else:
                print("\n[+] No obvious issues detected")
        
        elif args.delete:
            result = orchestrator.delete_service(args.delete)
            
            if result.get('success'):
                print(f"\n[+] Service deleted: {args.delete}")
            else:
                print(f"\n[-] FAILED: {result.get('error', 'Unknown error')}")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n[!] Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[-] ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
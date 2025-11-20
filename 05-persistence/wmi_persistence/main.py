"""
WMI Event Subscription Persistence Framework - CLI Interface
Educational tool for demonstrating WMI persistence techniques
"""

import sys
import os
import argparse

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.orchestrator import WMIPersistenceOrchestrator
from core.utils import check_admin

def print_banner():
    """Print tool banner"""
    banner = """
╔═══════════════════════════════════════════════════════╗
║   WMI Event Subscription Persistence Framework       ║
║        Educational & Authorized Testing Only          ║
╚═══════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(
        description='WMI Event Subscription Persistence Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create interval-based persistence (every 60 seconds)
  python main.py --create "powershell -enc BASE64" --interval 60
  
  # Create logon-triggered persistence
  python main.py --create-logon "cmd /c payload.exe"
  
  # Create process-triggered persistence
  python main.py --create-process "rundll32 mal.dll,Start" --process notepad.exe
  
  # Create custom WQL query persistence
  python main.py --create-custom "cmd /c beacon.exe" --wql "SELECT * FROM..."
  
  # List all WMI subscriptions
  python main.py --list
  
  # Scan for suspicious subscriptions
  python main.py --check-suspicious
  
  # Remove specific persistence
  python main.py --remove SystemMonitor
        """
    )
    
    # Action arguments
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--create', type=str, metavar='COMMAND',
                            help='Create interval-based persistence')
    action_group.add_argument('--create-logon', type=str, metavar='COMMAND',
                            help='Create logon-triggered persistence')
    action_group.add_argument('--create-process', type=str, metavar='COMMAND',
                            help='Create process-triggered persistence')
    action_group.add_argument('--create-custom', type=str, metavar='COMMAND',
                            help='Create custom WQL query persistence')
    action_group.add_argument('--list', action='store_true',
                            help='List all WMI event subscriptions')
    action_group.add_argument('--check-suspicious', action='store_true',
                            help='Scan for suspicious WMI subscriptions')
    action_group.add_argument('--remove', type=str, metavar='EVENT_NAME',
                            help='Remove WMI persistence by event name')
    
    # Configuration arguments
    parser.add_argument('--event-name', type=str,
                       help='Custom event name (auto-generated if not specified)')
    parser.add_argument('--interval', type=int, default=60,
                       help='Trigger interval in seconds (default: 60)')
    parser.add_argument('--process', type=str,
                       help='Process name to monitor (for process-triggered)')
    parser.add_argument('--trigger-on', type=str, choices=['creation', 'deletion'],
                       default='creation',
                       help='Process trigger type (default: creation)')
    parser.add_argument('--wql', type=str,
                       help='Custom WQL query (for custom method)')
    
    args = parser.parse_args()
    
    # Check admin for operations that require it
    if args.create or args.create_logon or args.create_process or args.create_custom or args.remove:
        if not check_admin():
            print("\n[!] ERROR: This operation requires administrator privileges")
            print("[!] Please run as administrator\n")
            sys.exit(1)
    
    # Initialize orchestrator
    orchestrator = WMIPersistenceOrchestrator()
    
    try:
        # Execute requested action
        if args.create:
            result = orchestrator.create_persistence(
                payload_command=args.create,
                method='interval',
                event_name=args.event_name,
                interval=args.interval
            )
            
            if result.get('success'):
                print("\n[+] SUCCESS")
                print(f"[+] Event Name: {result['event_name']}")
                print(f"[+] Filter: {result['filter_name']}")
                print(f"[+] Consumer: {result['consumer_name']}")
                print(f"[+] Trigger: Every {result['interval']} seconds")
                if 'removal_script_path' in result:
                    print(f"[+] Removal Script: {result['removal_script_path']}")
            else:
                print(f"\n[-] FAILED: {result.get('error', 'Unknown error')}")
                sys.exit(1)
        
        elif args.create_logon:
            result = orchestrator.create_persistence(
                payload_command=args.create_logon,
                method='logon',
                event_name=args.event_name
            )
            
            if result.get('success'):
                print("\n[+] SUCCESS")
                print(f"[+] Event Name: {result['event_name']}")
                print(f"[+] Trigger: User logon")
                if 'removal_script_path' in result:
                    print(f"[+] Removal Script: {result['removal_script_path']}")
            else:
                print(f"\n[-] FAILED: {result.get('error', 'Unknown error')}")
                sys.exit(1)
        
        elif args.create_process:
            if not args.process:
                print("\n[-] ERROR: --process required for process-triggered persistence")
                sys.exit(1)
            
            result = orchestrator.create_persistence(
                payload_command=args.create_process,
                method='process',
                event_name=args.event_name,
                process_name=args.process,
                trigger_on=args.trigger_on
            )
            
            if result.get('success'):
                print("\n[+] SUCCESS")
                print(f"[+] Event Name: {result['event_name']}")
                print(f"[+] Process: {result['process_name']}")
                print(f"[+] Trigger: Process {args.trigger_on}")
                if 'removal_script_path' in result:
                    print(f"[+] Removal Script: {result['removal_script_path']}")
            else:
                print(f"\n[-] FAILED: {result.get('error', 'Unknown error')}")
                sys.exit(1)
        
        elif args.create_custom:
            if not args.wql:
                print("\n[-] ERROR: --wql required for custom query persistence")
                sys.exit(1)
            
            result = orchestrator.create_persistence(
                payload_command=args.create_custom,
                method='custom',
                event_name=args.event_name,
                wql_query=args.wql
            )
            
            if result.get('success'):
                print("\n[+] SUCCESS")
                print(f"[+] Event Name: {result['event_name']}")
                print(f"[+] WQL Query: {result['wql_query']}")
                if 'removal_script_path' in result:
                    print(f"[+] Removal Script: {result['removal_script_path']}")
            else:
                print(f"\n[-] FAILED: {result.get('error', 'Unknown error')}")
                sys.exit(1)
        
        elif args.list:
            orchestrator.list_all()
        
        elif args.check_suspicious:
            report = orchestrator.scan_subscriptions()
            
            if report['total_suspicious'] > 0:
                print(f"\n[!] Detection complete - {report['total_suspicious']} suspicious items found")
            else:
                print("\n[+] No suspicious WMI subscriptions detected")
        
        elif args.remove:
            result = orchestrator.remove_persistence(args.remove)
            
            if result.get('success'):
                print(f"\n[+] WMI persistence removed: {args.remove}")
            else:
                print(f"\n[-] FAILED: {result.get('error', 'Unknown error')}")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n[!] Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[-] ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
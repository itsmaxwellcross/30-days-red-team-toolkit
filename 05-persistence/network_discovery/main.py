"""
Main CLI entry point for Network Discovery
"""

import argparse
import sys
from .core.base import NetworkDiscovery


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Network Discovery & Lateral Movement Reconnaissance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 -m network_discovery
  python3 -m network_discovery --quick
  python3 -m network_discovery --targets-only

Warning: Only use on networks you have authorization to scan.
        """
    )
    
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Quick scan (local network only, no domain enum)'
    )
    
    parser.add_argument(
        '--targets-only',
        action='store_true',
        help='Only save lateral movement targets file'
    )
    
    parser.add_argument(
        '--max-hosts',
        type=int,
        default=10,
        help='Maximum hosts to port scan (default: 10)'
    )
    
    args = parser.parse_args()
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║      Network Discovery & Lateral Movement Recon v1.0     ║
    ║      Internal Network Mapping from Compromised Host      ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        discovery = NetworkDiscovery()
        discovery.run_network_discovery()
    
    except KeyboardInterrupt:
        print("\n[!] Discovery interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Error during discovery: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
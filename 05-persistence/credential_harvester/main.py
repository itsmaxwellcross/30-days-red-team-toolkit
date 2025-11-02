"""
Main CLI entry point for Credential Harvester
"""

import argparse
import sys
from .core.base import CredentialHarvester


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Credential Harvesting Framework - Post-Exploitation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 -m credential_harvester
  python3 -m credential_harvester --verbose

Warning: Only use on systems you have authorization to test.
        """
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--output-dir',
        default='.',
        help='Directory to save output files (default: current directory)'
    )
    
    args = parser.parse_args()
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║         Credential Harvesting Framework v1.0             ║
    ║         Post-Exploitation Credential Extraction          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        harvester = CredentialHarvester()
        harvester.run_full_harvest()
    
    except KeyboardInterrupt:
        print("\n[!] Harvesting interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Error during harvesting: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
"""
Main CLI entry point for Situational Awareness Suite
"""

import argparse
import sys
from .core.base import SituationalAwareness


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Situational Awareness Suite - Post-Exploitation Enumeration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 -m situational_awareness --quick
  python3 -m situational_awareness --full
  python3 -m situational_awareness --full --output json
        """
    )
    
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Run quick enumeration (system, user, network only)'
    )
    
    parser.add_argument(
        '--full',
        action='store_true',
        help='Run full enumeration (all modules)'
    )
    
    parser.add_argument(
        '--output',
        choices=['json', 'text'],
        default='json',
        help='Output format (default: json)'
    )
    
    args = parser.parse_args()
    
    # Create instance
    sa = SituationalAwareness(output_format=args.output)
    
    try:
        if args.quick:
            sa.run_quick_enumeration()
        elif args.full:
            sa.run_full_enumeration()
        else:
            parser.print_help()
            sys.exit(0)
    
    except KeyboardInterrupt:
        print("\n[!] Enumeration interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Error during enumeration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
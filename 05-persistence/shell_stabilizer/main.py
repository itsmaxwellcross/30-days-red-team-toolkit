"""Main entry point for shell stabilizer"""

import argparse
from stabilizer import ShellStabilizer
from config import SHELL_TYPES, DEFAULT_SHELL_TYPE, DEFAULT_GUIDE_FILENAME

def main():
    parser = argparse.ArgumentParser(description="Shell Stabilization Toolkit")
    parser.add_argument('--type', choices=SHELL_TYPES, default=DEFAULT_SHELL_TYPE,
                       help='Shell type (linux or windows)')
    parser.add_argument('--generate-guide', action='store_true',
                       help='Generate stabilization guide')
    parser.add_argument('--persistence', action='store_true',
                       help='Show persistence methods')
    parser.add_argument('--test', action='store_true',
                       help='Show shell feature tests')
    parser.add_argument('--output', default=DEFAULT_GUIDE_FILENAME,
                       help='Output file for guide')
    
    args = parser.parse_args()
    
    stabilizer = ShellStabilizer(args.type)
    
    if args.generate_guide:
        guide = stabilizer.generate_stabilization_guide(args.output)
        print(guide)
        print(f"\n[+] Guide saved to {args.output}")
    
    if args.persistence:
        stabilizer.print_persistence_methods()
    
    if args.test:
        stabilizer.test_shell_features()
    
    if not args.generate_guide and not args.persistence and not args.test:
        print_usage()

def print_usage():
    """Print usage information"""
    print("[*] Shell Stabilization Toolkit")
    print("="*60)
    print("\nUsage:")
    print("  --generate-guide     Generate full stabilization guide")
    print("  --persistence        Show persistence methods")
    print("  --test               Show shell feature tests")
    print("  --type linux/windows Specify shell type")
    print("  --output FILE        Output filename for guide")
    print("\nExamples:")
    print("  python3 main.py --type linux --generate-guide")
    print("  python3 main.py --type windows --persistence")
    print("  python3 main.py --type linux --test")

if __name__ == "__main__":
    main()
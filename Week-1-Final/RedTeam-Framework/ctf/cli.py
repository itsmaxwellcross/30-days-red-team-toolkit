#!/usr/bin/env python3
"""
Week 1 CTF Challenge - Command Line Interface
"""

import argparse
from ctf.generator import CTFGenerator
from ctf.server import CTFServer
from ctf.validator import FlagValidator


def main():
    parser = argparse.ArgumentParser(
        description="Week 1 CTF Challenge Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate challenge files
  python3 -m ctf.cli --generate

  # Start challenge server
  python3 -m ctf.cli --serve

  # Validate a flag submission
  python3 -m ctf.cli --validate "FLAG{...}"

  # Show challenge information
  python3 -m ctf.cli --info

  # Reset challenge
  python3 -m ctf.cli --reset
        """
    )
    
    # Challenge management
    parser.add_argument('--generate', action='store_true',
                       help='Generate CTF challenge files')
    parser.add_argument('--serve', action='store_true',
                       help='Start CTF challenge server')
    parser.add_argument('--port', type=int, default=8080,
                       help='Server port (default: 8080)')
    parser.add_argument('--host', default='0.0.0.0',
                       help='Server host (default: 0.0.0.0)')
    
    # Flag validation
    parser.add_argument('--validate', metavar='FLAG',
                       help='Validate a flag submission')
    parser.add_argument('--validate-all', action='store_true',
                       help='Run validation tests on all flags')
    
    # Information
    parser.add_argument('--info', action='store_true',
                       help='Show challenge information')
    parser.add_argument('--hints', action='store_true',
                       help='Show hints for current stage')
    parser.add_argument('--progress', action='store_true',
                       help='Show completion progress')
    
    # Management
    parser.add_argument('--reset', action='store_true',
                       help='Reset challenge to initial state')
    parser.add_argument('--show-flags', action='store_true',
                       help='Show all flags (admin only)')
    
    # Output options
    parser.add_argument('--output-dir', default='06-integration/ctf_challenge',
                       help='Output directory for challenge files')
    
    args = parser.parse_args()
    
    # Initialize components
    generator = CTFGenerator(args.output_dir)
    
    # Handle commands
    if args.generate:
        print("[*] Generating Week 1 CTF Challenge...")
        generator.generate_full_challenge()
        print("\n[+] Challenge generated successfully!")
        print(f"[+] Challenge directory: {args.output_dir}")
        print("\n[*] Next steps:")
        print("    1. Start the server: python3 -m ctf.cli --serve")
        print("    2. Access challenge at: http://localhost:8080")
        print("    3. Read README.md for objectives")
    
    elif args.serve:
        server = CTFServer(args.output_dir, args.host, args.port)
        print(f"[*] Starting CTF Challenge Server...")
        print(f"[+] Server running at: http://{args.host}:{args.port}")
        print(f"[+] Press Ctrl+C to stop")
        server.start()
    
    elif args.validate:
        validator = FlagValidator(args.output_dir)
        result = validator.validate_flag(args.validate)
        
        if result['valid']:
            print(f"[+] Correct! Flag {result['flag_number']} captured!")
            print(f"[+] Description: {result['description']}")
            print(f"[+] Points: {result['points']}")
        else:
            print(f"[-] Invalid flag")
    
    elif args.validate_all:
        validator = FlagValidator(args.output_dir)
        validator.test_all_flags()
    
    elif args.info:
        show_challenge_info(generator)
    
    elif args.hints:
        show_hints()
    
    elif args.progress:
        validator = FlagValidator(args.output_dir)
        validator.show_progress()
    
    elif args.reset:
        print("[*] Resetting challenge...")
        generator.reset_challenge()
        print("[+] Challenge reset to initial state")
    
    elif args.show_flags:
        import getpass
        password = getpass.getpass("[!] Admin password: ")
        if password == "admin123":  # Simple admin check
            generator.show_all_flags()
        else:
            print("[-] Incorrect password")
    
    else:
        parser.print_help()


def show_challenge_info(generator):
    """Display challenge information"""
    print("\n" + "="*70)
    print("WEEK 1 CTF CHALLENGE")
    print("="*70)
    print("\nObjective: Complete all 6 flags to demonstrate Week 1 mastery")
    print("\nFlags:")
    print("  1. Flag 1 (RECON) - 10 points")
    print("  2. Flag 2 (EXPLOIT) - 15 points")
    print("  3. Flag 3 (SHELL) - 20 points")
    print("  4. Flag 4 (CREDENTIALS) - 20 points")
    print("  5. Flag 5 (PRIVESC) - 25 points")
    print("  6. Flag 6 (COMPLETE) - 10 points")
    print("\nTotal: 100 points")
    print("\nEstimated Time: 2-4 hours")
    print("\nDifficulty: Beginner to Intermediate")
    print("\n" + "="*70)


def show_hints():
    """Display current hints"""
    print("\n[*] General Hints:")
    print("  - Start with reconnaissance tools")
    print("  - Check HTML source code")
    print("  - Look for exposed configuration files")
    print("  - Try SQL injection on login forms")
    print("  - Enumerate thoroughly after getting shell")
    print("  - Check SUID binaries for privilege escalation")


if __name__ == '__main__':
    main()
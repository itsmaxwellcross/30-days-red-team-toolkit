#!/usr/bin/env python3
"""
C2 Payload Generator - CLI Entry Point
Professional-grade agent generation with embedded configuration
"""

import argparse
import sys
import os

# Add project root to path if running from scripts/
if __name__ == "__main__" and not __package__:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from c2_payload_generator.generator import PayloadGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Custom C2 Payload Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all agents (recommended)
  ./scripts/c2generator --generate-all

  # Generate specific agent
  ./scripts/c2generator --generate-powershell agents/agent.ps1

  # Generate with custom beacon settings
  ./scripts/c2generator --generate-all --interval 120 --jitter 60

  # Create full deployment package
  ./scripts/c2generator --create-package
        """
    )

    # Beacon timing options (shared)
    parser.add_argument('--interval', type=int, default=60,
                        help='Beacon interval in seconds (default: 60)')
    parser.add_argument('--jitter', type=int, default=30,
                        help='Jitter range in seconds (±value) (default: 30)')

    # Generator modes
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--generate-all', action='store_true',
                       help='Generate all agent types (PowerShell, Bash, Python)')
    group.add_argument('--generate-powershell', type=str, metavar='FILE',
                       help='Generate PowerShell agent only')
    group.add_argument('--generate-bash', type=str, metavar='FILE',
                       help='Generate Bash agent only')
    group.add_argument('--generate-python', type=str, metavar='FILE',
                       help='Generate Python agent only')
    group.add_argument('--create-package', action='store_true',
                       help='Generate all agents + create deployment package with README')

    args = parser.parse_args()

    print("=" * 70)
    print(" CUSTOM C2 PAYLOAD GENERATOR")
    print("=" * 70)

    try:
        generator = PayloadGenerator()
    except FileNotFoundError as e:
        print(f"[!] Config error: {e}")
        print("[!] Run the C2 server first to generate config/c2_config.json")
        print("    ./01-c2-server/scripts/c2server --server")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Failed to initialize generator: {e}")
        sys.exit(1)

    try:
        if args.generate_all:
            print(f"[*] Generating all agents (interval: {args.interval}s, jitter: ±{args.jitter}s)")
            generator.generate_all_agents(interval=args.interval, jitter=args.jitter)

        elif args.generate_powershell:
            print(f"[*] Generating PowerShell agent → {args.generate_powershell}")
            generator.generate_powershell_agent(args.generate_powershell, args.interval, args.jitter)

        elif args.generate_bash:
            print(f"[*] Generating Bash agent → {args.generate_bash}")
            generator.generate_bash_agent(args.generate_bash, args.interval, args.jitter)

        elif args.generate_python:
            print(f"[*] Generating Python agent → {args.generate_python}")
            generator.generate_python_agent(args.generate_python, args.interval, args.jitter)

        elif args.create_package:
            print(f"[*] Creating full deployment package...")
            generator.create_deployment_package()

        print("=" * 70)
        print(" GENERATION COMPLETE")
        print("=" * 70)

    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Generation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
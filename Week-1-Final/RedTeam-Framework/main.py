#!/usr/bin/env python3
"""
Red Team Automation Framework - Main Entry Point
"""

import argparse
from core.framework import RedTeamFramework


def main():
    parser = argparse.ArgumentParser(description="Red Team Master Framework")
    parser.add_argument('--config', default='config/engagement.json',
                       help='Engagement configuration file')
    parser.add_argument('--phase', choices=['recon', 'weapon', 'deliver', 'exploit', 'post'],
                       help='Run specific phase only')
    parser.add_argument('--full', action='store_true',
                       help='Run full engagement')
    
    args = parser.parse_args()
    
    framework = RedTeamFramework(args.config)
    
    if args.phase == 'recon':
        framework.phase_1_reconnaissance()
    elif args.phase == 'weapon':
        framework.phase_2_weaponization()
    elif args.phase == 'deliver':
        framework.phase_3_delivery()
    elif args.phase == 'exploit':
        framework.phase_4_exploitation()
    elif args.phase == 'post':
        framework.phase_5_post_exploitation()
    elif args.full:
        framework.run_full_engagement()
    else:
        print_usage()


def print_usage():
    print("[*] Red Team Master Framework")
    print("="*60)
    print("\nUsage:")
    print("  --full                Run complete engagement")
    print("  --phase recon         Run reconnaissance only")
    print("  --phase weapon        Run weaponization only")
    print("  --phase deliver       Run delivery setup")
    print("  --phase exploit       Run exploitation")
    print("  --phase post          Run post-exploitation")
    print("\nExample:")
    print("  python3 main.py --full")
    print("  python3 main.py --phase recon")


if __name__ == "__main__":
    main()
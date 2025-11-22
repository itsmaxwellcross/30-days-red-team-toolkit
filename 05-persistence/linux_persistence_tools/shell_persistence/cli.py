#!/usr/bin/env python3
import argparse
from .persistence.bashrc import BashrcInjector
from .persistence.profile import ProfileInjector
from .persistence.system_profile import SystemProfileInjector
from .persistence.motd import MOTDInjector
from .detection.scanner import ProfileScanner

def main():
    parser = argparse.ArgumentParser(description="Linux Shell Profile Persistence")
    parser.add_argument('--check', action='store_true', help="Scan for suspicious profile entries")
    parser.add_argument('--inject-bashrc', type=str, help="Inject into .bashrc")
    parser.add_argument('--inject-profile', type=str, help="Inject into .profile")
    parser.add_argument('--inject-system', type=str, help="Inject system-wide (root)")
    parser.add_argument('--inject-motd', type=str, help="Inject into MOTD (root)")
    parser.add_argument('--stealthy', action='store_true', help="Use stealthy .bashrc injection")

    args = parser.parse_args()

    if args.check:
        ProfileScanner().check_suspicious()

    elif args.inject_bashrc:
        BashrcInjector().inject(args.inject_bashrc, args.stealthy)

    elif args.inject_profile:
        ProfileInjector().inject(args.inject_profile)

    elif args.inject_system:
        SystemProfileInjector().inject(args.inject_system)

    elif args.inject_motd:
        MOTDInjector().inject(args.inject_motd)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
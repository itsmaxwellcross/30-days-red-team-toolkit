#!/usr/bin/env python3
"""
Linux Log Cleanup Framework - Main Entry Point
Command-line interface for log cleanup operations
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from linux_log_cleanup.core import LinuxLogCleaner
from linux_log_cleanup.cleaners import LogRotationCleaner
from linux_log_cleanup.utils import check_root, require_root


def main():
    """Main entry point for the application"""
    
    parser = argparse.ArgumentParser(
        description="Linux Log Cleanup Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Comprehensive cleanup (requires root)
  sudo python main.py --comprehensive --username attacker --ip 10.10.14.5

  # Clean auth log only
  sudo python main.py --clean-auth --username attacker

  # Clean wtmp (login records)
  sudo python main.py --clean-wtmp --username attacker

  # Clean bash history
  sudo python main.py --clean-bash-history --username attacker

  # Clean rotated logs
  sudo python main.py --clean-rotated

  # Dry run (show what would be deleted)
  sudo python main.py --clean-rotated --dry-run
        """
    )
    
    # Target specification
    parser.add_argument(
        '--username',
        type=str,
        metavar='USER',
        help='Username to remove from logs'
    )
    
    parser.add_argument(
        '--ip',
        type=str,
        metavar='IP',
        help='IP address to remove from logs'
    )
    
    parser.add_argument(
        '--keywords',
        nargs='+',
        metavar='KEYWORD',
        help='Keywords to remove from logs (space-separated)'
    )
    
    # Cleanup operations
    parser.add_argument(
        '--comprehensive',
        action='store_true',
        help='Run comprehensive cleanup across all log types'
    )
    
    parser.add_argument(
        '--clean-auth',
        action='store_true',
        help='Clean authentication logs only'
    )
    
    parser.add_argument(
        '--clean-syslog',
        action='store_true',
        help='Clean system log only'
    )
    
    parser.add_argument(
        '--clean-wtmp',
        action='store_true',
        help='Clean wtmp (login records) only'
    )
    
    parser.add_argument(
        '--clean-utmp',
        action='store_true',
        help='Clean utmp (current logins) only'
    )
    
    parser.add_argument(
        '--clean-lastlog',
        action='store_true',
        help='Clean lastlog only'
    )
    
    parser.add_argument(
        '--clean-bash-history',
        action='store_true',
        help='Clean bash history'
    )
    
    parser.add_argument(
        '--clean-audit',
        action='store_true',
        help='Clean audit log only'
    )
    
    parser.add_argument(
        '--clean-rotated',
        action='store_true',
        help='Clean rotated log files (*.1, *.2, *.gz, etc.)'
    )
    
    # Options
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Skip backup creation (dangerous!)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    
    parser.add_argument(
        '--log-dir',
        type=str,
        default='/var/log',
        metavar='DIR',
        help='Log directory (default: /var/log)'
    )
    
    # Information
    parser.add_argument(
        '--list-rotated',
        action='store_true',
        help='List rotated log files'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Linux Log Cleanup Framework v1.0.0'
    )
    
    args = parser.parse_args()
    
    # Check root privileges (skip for list operations and dry-run info)
    if not args.list_rotated and not args.version:
        if not check_root():
            print("[!] This script requires root privileges")
            print("[!] Run with: sudo python3 main.py ...")
            print("[*] Use --list-rotated to list files without root")
            return 1
    
    # Initialize cleaners
    cleaner = LinuxLogCleaner()
    preserve_backup = not args.no_backup
    
    # Handle list operations
    if args.list_rotated:
        return handle_list_rotated(args.log_dir)
    
    # Handle comprehensive cleanup
    if args.comprehensive:
        return handle_comprehensive(cleaner, args)
    
    # Handle specific cleanup operations
    if args.clean_auth:
        return handle_clean_auth(cleaner, args, preserve_backup)
    
    if args.clean_syslog:
        return handle_clean_syslog(cleaner, args, preserve_backup)
    
    if args.clean_wtmp:
        return handle_clean_wtmp(cleaner, args, preserve_backup)
    
    if args.clean_utmp:
        return handle_clean_utmp(cleaner, args, preserve_backup)
    
    if args.clean_lastlog:
        return handle_clean_lastlog(cleaner, args, preserve_backup)
    
    if args.clean_bash_history:
        return handle_clean_bash_history(cleaner, args)
    
    if args.clean_audit:
        return handle_clean_audit(cleaner, args, preserve_backup)
    
    if args.clean_rotated:
        return handle_clean_rotated(args)
    
    # No action specified
    if len(sys.argv) == 1:
        parser.print_help()
        return 1
    
    return 0


def handle_comprehensive(cleaner, args):
    """Handle comprehensive cleanup"""
    if not args.username:
        print("[!] --comprehensive requires --username")
        return 1
    
    results = cleaner.comprehensive_cleanup(
        args.username,
        args.ip,
        args.keywords
    )
    
    # Check if any operation failed
    if all(results.values()):
        return 0
    else:
        return 1


def handle_clean_auth(cleaner, args, preserve_backup):
    """Handle auth log cleaning"""
    success = cleaner.clean_auth_log(args.username, args.ip, preserve_backup)
    return 0 if success else 1


def handle_clean_syslog(cleaner, args, preserve_backup):
    """Handle syslog cleaning"""
    success = cleaner.clean_syslog(args.keywords, preserve_backup)
    return 0 if success else 1


def handle_clean_wtmp(cleaner, args, preserve_backup):
    """Handle wtmp cleaning"""
    success = cleaner.clean_wtmp(args.username, preserve_backup)
    return 0 if success else 1


def handle_clean_utmp(cleaner, args, preserve_backup):
    """Handle utmp cleaning"""
    success = cleaner.clean_utmp(args.username, preserve_backup)
    return 0 if success else 1


def handle_clean_lastlog(cleaner, args, preserve_backup):
    """Handle lastlog cleaning"""
    success = cleaner.clean_lastlog(args.username, preserve_backup)
    return 0 if success else 1


def handle_clean_bash_history(cleaner, args):
    """Handle bash history cleaning"""
    success = cleaner.clean_bash_history(args.username)
    return 0 if success else 1


def handle_clean_audit(cleaner, args, preserve_backup):
    """Handle audit log cleaning"""
    success = cleaner.clean_audit_log(args.keywords, preserve_backup)
    return 0 if success else 1


def handle_clean_rotated(args):
    """Handle rotated log cleaning"""
    rotation_cleaner = LogRotationCleaner()
    
    count = rotation_cleaner.clean_rotated_logs(
        args.log_dir,
        dry_run=args.dry_run
    )
    
    return 0 if count >= 0 else 1


def handle_list_rotated(log_dir):
    """Handle listing rotated logs"""
    rotation_cleaner = LogRotationCleaner()
    
    print(f"\n[*] Scanning for rotated logs in: {log_dir}")
    
    files = rotation_cleaner.list_rotated_logs(log_dir)
    
    if files:
        print(f"\n[+] Found {len(files)} rotated log files:\n")
        for filepath in files:
            print(f"    {filepath}")
        
        # Get stats
        stats = rotation_cleaner.get_rotation_stats(log_dir)
        print(f"\n[*] Total size: {stats['total_size_mb']:.2f} MB")
    else:
        print(f"\n[-] No rotated log files found")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
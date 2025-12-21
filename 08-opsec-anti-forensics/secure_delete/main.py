#!/usr/bin/env python3
"""
Secure File Deletion Framework - Main Entry Point
Command-line interface for secure file deletion
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from secure_delete import SecureDelete, ArtifactCleaner, OverwriteMethods
from secure_delete.core.constants import DEFAULT_PASSES, DELETION_METHODS
from secure_delete.utils import validate_file, validate_directory, confirm_deletion


def main():
    """Main entry point for the application"""
    
    parser = argparse.ArgumentParser(
        description="Secure File Deletion Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Securely delete a file with 3 random passes
  python main.py --file malware.exe --passes 3 --method random

  # Delete using DoD standard (3 passes: ones, zeros, random)
  python main.py --file sensitive.doc --method dod

  # Securely delete entire directory
  python main.py --directory /path/to/tools --passes 3

  # Wipe free space on drive
  python main.py --wipe-free-space C:\\ --size-mb 100

  # Clean forensic artifacts
  python main.py --clean-artifacts

  # Get information about deletion method
  python main.py --method-info dod
        """
    )
    
    # File operations
    parser.add_argument(
        '--file',
        type=str,
        metavar='FILE',
        help='File to securely delete'
    )
    
    parser.add_argument(
        '--directory',
        type=str,
        metavar='DIR',
        help='Directory to securely delete (recursive)'
    )
    
    # Deletion parameters
    parser.add_argument(
        '--passes',
        type=int,
        default=DEFAULT_PASSES,
        metavar='N',
        help=f'Number of overwrite passes (default: {DEFAULT_PASSES})'
    )
    
    parser.add_argument(
        '--method',
        type=str,
        default='random',
        choices=DELETION_METHODS,
        help='Overwrite method (default: random)'
    )
    
    # Free space operations
    parser.add_argument(
        '--wipe-free-space',
        type=str,
        metavar='DRIVE',
        help='Drive or directory to wipe free space'
    )
    
    parser.add_argument(
        '--size-mb',
        type=int,
        default=100,
        metavar='MB',
        help='Size in MB for free space wipe (default: 100)'
    )
    
    # Artifact cleaning
    parser.add_argument(
        '--clean-artifacts',
        action='store_true',
        help='Clean forensic artifacts (temp, browser, etc.)'
    )
    
    parser.add_argument(
        '--clean-temp',
        action='store_true',
        help='Clean temporary files only'
    )
    
    parser.add_argument(
        '--clean-browser',
        action='store_true',
        help='Clean browser history only'
    )
    
    parser.add_argument(
        '--clean-prefetch',
        action='store_true',
        help='Clean Windows Prefetch only'
    )
    
    parser.add_argument(
        '--clean-mru',
        action='store_true',
        help='Clean Windows MRU lists only'
    )
    
    # Information
    parser.add_argument(
        '--method-info',
        type=str,
        metavar='METHOD',
        help='Display information about a deletion method'
    )
    
    parser.add_argument(
        '--file-info',
        type=str,
        metavar='FILE',
        help='Display information about a file'
    )
    
    # Safety options
    parser.add_argument(
        '--no-confirm',
        action='store_true',
        help='Skip deletion confirmation prompt'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Secure File Deletion Framework v1.0.0'
    )
    
    args = parser.parse_args()
    
    # Handle information requests
    if args.method_info:
        return handle_method_info(args.method_info)
    
    if args.file_info:
        return handle_file_info(args.file_info)
    
    # Handle artifact cleaning
    if args.clean_artifacts:
        return handle_comprehensive_cleanup()
    
    if args.clean_temp:
        return handle_clean_temp()
    
    if args.clean_browser:
        return handle_clean_browser()
    
    if args.clean_prefetch:
        return handle_clean_prefetch()
    
    if args.clean_mru:
        return handle_clean_mru()
    
    # Handle file operations
    if args.file:
        return handle_delete_file(args)
    
    if args.directory:
        return handle_delete_directory(args)
    
    if args.wipe_free_space:
        return handle_wipe_free_space(args)
    
    # No action specified
    if len(sys.argv) == 1:
        parser.print_help()
        return 1
    
    return 0


def handle_method_info(method):
    """Display information about a deletion method"""
    methods = OverwriteMethods()
    info = methods.get_method_info(method)
    
    print(f"\n[*] Method: {info['name']}")
    print(f"[*] Passes: {info['passes']}")
    print(f"[*] Description: {info['description']}")
    print(f"[*] Security: {info['security']}")
    print(f"[*] Speed: {info['speed']}")
    print()
    
    return 0


def handle_file_info(filepath):
    """Display information about a file"""
    if not validate_file(filepath):
        return 1
    
    deleter = SecureDelete()
    stats = deleter.get_deletion_stats(filepath)
    
    if stats:
        print(f"\n[*] File: {filepath}")
        print(f"[*] Size: {stats['size_mb']:.2f} MB ({stats['size']} bytes)")
        print(f"[*] Recommended passes: {stats['passes_recommended']}")
        print(f"[*] Recommended method: {stats['method_recommended']}")
        print()
    
    return 0


def handle_delete_file(args):
    """Handle file deletion"""
    if not validate_file(args.file):
        return 1
    
    # Confirmation
    if not args.no_confirm:
        if not confirm_deletion(args.file):
            print("[*] Cancelled")
            return 0
    
    deleter = SecureDelete()
    success = deleter.secure_delete_file(args.file, args.passes, args.method)
    
    return 0 if success else 1


def handle_delete_directory(args):
    """Handle directory deletion"""
    if not validate_directory(args.directory):
        return 1
    
    # Confirmation
    if not args.no_confirm:
        response = input(f"[!] Permanently delete entire directory {args.directory}? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("[*] Cancelled")
            return 0
    
    deleter = SecureDelete()
    success = deleter.secure_delete_directory(args.directory, args.passes, args.method)
    
    return 0 if success else 1


def handle_wipe_free_space(args):
    """Handle free space wiping"""
    deleter = SecureDelete()
    success = deleter.wipe_free_space(args.wipe_free_space, args.size_mb)
    
    return 0 if success else 1


def handle_comprehensive_cleanup():
    """Handle comprehensive artifact cleanup"""
    cleaner = ArtifactCleaner()
    results = cleaner.comprehensive_cleanup()
    
    return 0


def handle_clean_temp():
    """Handle temp file cleaning"""
    cleaner = ArtifactCleaner()
    count = cleaner.clean_temp_files()
    
    return 0


def handle_clean_browser():
    """Handle browser history cleaning"""
    cleaner = ArtifactCleaner()
    count = cleaner.clean_browser_history()
    
    return 0


def handle_clean_prefetch():
    """Handle prefetch cleaning"""
    cleaner = ArtifactCleaner()
    count = cleaner.clean_prefetch()
    
    return 0


def handle_clean_mru():
    """Handle MRU cleaning"""
    cleaner = ArtifactCleaner()
    count = cleaner.clean_mru()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
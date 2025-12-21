#!/usr/bin/env python3
"""
Timestamp Stomping Toolkit - Main Entry Point
Command-line interface for timestamp manipulation
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from timestamp_stomper import TimestampStomper, MACBAnalysis
from timestamp_stomper.core.constants import DEFAULT_DAYS_MIN, DEFAULT_DAYS_MAX
from timestamp_stomper.utils import validate_file, get_legitimate_reference


def main():
    """Main entry point for the application"""
    
    parser = argparse.ArgumentParser(
        description="Timestamp Stomping Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Display current timestamps
  python main.py --file malware.exe --display

  # Copy timestamps from legitimate file
  python main.py --file malware.exe --copy-from C:\\Windows\\System32\\notepad.exe

  # Match timestamps to directory average
  python main.py --file malware.exe --match-dir C:\\Users\\Public\\Documents

  # Set random past timestamp
  python main.py --file malware.exe --random-past --days-min 60 --days-max 180

  # Analyze for timestamp anomalies
  python main.py --file suspicious.exe --analyze

  # Bulk stomp entire directory
  python main.py --bulk-stomp /path/to/tools --reference /etc/passwd

  # Set specific timestamp
  python main.py --file test.txt --specific 2023 6 15 14 30 0
        """
    )
    
    # File operations
    parser.add_argument(
        '--file',
        type=str,
        metavar='FILE',
        help='Target file to modify'
    )
    
    parser.add_argument(
        '--display',
        action='store_true',
        help='Display current timestamps'
    )
    
    # Timestamp manipulation
    parser.add_argument(
        '--copy-from',
        type=str,
        metavar='SOURCE',
        help='Copy timestamps from this file'
    )
    
    parser.add_argument(
        '--match-dir',
        type=str,
        metavar='DIR',
        help='Match timestamps to directory average'
    )
    
    parser.add_argument(
        '--random-past',
        action='store_true',
        help='Set random past timestamp'
    )
    
    parser.add_argument(
        '--days-min',
        type=int,
        default=DEFAULT_DAYS_MIN,
        metavar='N',
        help=f'Minimum days ago for random (default: {DEFAULT_DAYS_MIN})'
    )
    
    parser.add_argument(
        '--days-max',
        type=int,
        default=DEFAULT_DAYS_MAX,
        metavar='N',
        help=f'Maximum days ago for random (default: {DEFAULT_DAYS_MAX})'
    )
    
    parser.add_argument(
        '--future',
        type=int,
        metavar='DAYS',
        help='Set timestamp N days in the future (suspicious!)'
    )
    
    parser.add_argument(
        '--specific',
        nargs=6,
        type=int,
        metavar=('YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND'),
        help='Set specific timestamp (year month day hour minute second)'
    )
    
    # Analysis
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Analyze MACB times for anomalies'
    )
    
    parser.add_argument(
        '--compare',
        type=str,
        metavar='FILE2',
        help='Compare timestamps with another file'
    )
    
    parser.add_argument(
        '--batch-analyze',
        type=str,
        metavar='DIR',
        help='Analyze all files in directory for anomalies'
    )
    
    # Bulk operations
    parser.add_argument(
        '--bulk-stomp',
        type=str,
        metavar='DIR',
        help='Bulk stomp directory'
    )
    
    parser.add_argument(
        '--reference',
        type=str,
        metavar='FILE',
        help='Reference file for bulk stomp'
    )
    
    # Utilities
    parser.add_argument(
        '--find-reference',
        action='store_true',
        help='Find legitimate reference file on system'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Timestamp Stomping Toolkit v1.0.0'
    )
    
    args = parser.parse_args()
    
    # Handle find reference
    if args.find_reference:
        return handle_find_reference()
    
    # Handle batch analyze
    if args.batch_analyze:
        return handle_batch_analyze(args.batch_analyze)
    
    # Handle bulk stomp
    if args.bulk_stomp:
        return handle_bulk_stomp(args)
    
    # Handle file-specific operations
    if args.file:
        return handle_file_operations(args)
    
    # No action specified
    if len(sys.argv) == 1:
        parser.print_help()
        return 1
    
    return 0


def handle_find_reference():
    """Find and display legitimate reference file"""
    print("[*] Searching for legitimate reference files...")
    
    reference = get_legitimate_reference()
    
    if reference:
        print(f"[+] Found reference file: {reference}")
        
        stomper = TimestampStomper()
        times = stomper.get_file_times(reference)
        
        if times:
            print(f"\n[*] Timestamps:")
            print(f"    Created:  {times['created']}")
            print(f"    Modified: {times['modified']}")
            print(f"    Accessed: {times['accessed']}")
        
        return 0
    else:
        print("[-] No legitimate reference files found")
        return 1


def handle_batch_analyze(directory):
    """Handle batch analysis"""
    print(f"[*] Batch analyzing: {directory}")
    MACBAnalysis.batch_analyze(directory)
    return 0


def handle_bulk_stomp(args):
    """Handle bulk stomping"""
    stomper = TimestampStomper()
    
    success = stomper.bulk_stomp(
        args.bulk_stomp,
        reference_file=args.reference,
        days_min=args.days_min,
        days_max=args.days_max
    )
    
    return 0 if success else 1


def handle_file_operations(args):
    """Handle file-specific operations"""
    
    # Validate file
    if not validate_file(args.file):
        return 1
    
    stomper = TimestampStomper()
    
    # Display timestamps
    if args.display:
        stomper.display_file_times(args.file)
        return 0
    
    # Analyze timestamps
    if args.analyze:
        MACBAnalysis.analyze_macb(args.file)
        return 0
    
    # Compare timestamps
    if args.compare:
        if not validate_file(args.compare):
            return 1
        MACBAnalysis.compare_timestamps(args.file, args.compare)
        return 0
    
    # Copy timestamps
    if args.copy_from:
        if not validate_file(args.copy_from):
            return 1
        
        success = stomper.copy_timestamps(args.copy_from, args.file)
        if success:
            stomper.display_file_times(args.file)
        return 0 if success else 1
    
    # Match directory
    if args.match_dir:
        success = stomper.match_directory_times(args.file, args.match_dir)
        if success:
            stomper.display_file_times(args.file)
        return 0 if success else 1
    
    # Random past
    if args.random_past:
        success = stomper.set_random_past_time(args.file, args.days_min, args.days_max)
        if success:
            stomper.display_file_times(args.file)
        return 0 if success else 1
    
    # Future timestamp
    if args.future:
        success = stomper.set_future_time(args.file, args.future)
        if success:
            stomper.display_file_times(args.file)
        return 0 if success else 1
    
    # Specific timestamp
    if args.specific:
        year, month, day, hour, minute, second = args.specific
        success = stomper.set_specific_time(args.file, year, month, day, hour, minute, second)
        if success:
            stomper.display_file_times(args.file)
        return 0 if success else 1
    
    # No operation specified, just display
    stomper.display_file_times(args.file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
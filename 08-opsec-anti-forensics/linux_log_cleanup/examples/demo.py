#!/usr/bin/env python3
"""
Linux Log Cleanup Framework - Example Usage

This script demonstrates how to use the framework programmatically.

WARNING: This is for demonstration only. Running these examples
         on a production system will modify/delete logs!
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from linux_log_cleanup import (
    LinuxLogCleaner,
    LogRotationCleaner,
    TextLogCleaner,
    BinaryLogCleaner
)
from linux_log_cleanup.core import LOG_PATHS
from linux_log_cleanup.utils import check_root, format_size


def example_1_basic_cleanup():
    """Example: Basic log cleanup operations"""
    print("\n" + "="*60)
    print("Example 1: Basic Log Cleanup")
    print("="*60)
    
    # Initialize cleaner
    cleaner = LinuxLogCleaner()
    
    # Note: These would actually clean logs - demonstration only
    print("\n[*] Would clean auth.log for user 'testuser'")
    print("    Command: cleaner.clean_auth_log(username='testuser')")
    
    print("\n[*] Would clean wtmp for user 'testuser'")
    print("    Command: cleaner.clean_wtmp(username='testuser')")
    
    print("\n[*] Would clean bash history")
    print("    Command: cleaner.clean_bash_history(username='testuser')")


def example_2_comprehensive_cleanup():
    """Example: Comprehensive cleanup across all logs"""
    print("\n" + "="*60)
    print("Example 2: Comprehensive Cleanup")
    print("="*60)
    
    cleaner = LinuxLogCleaner()
    
    print("\n[*] Comprehensive cleanup would:")
    print("    - Clean auth.log (username + IP)")
    print("    - Clean syslog (keywords)")
    print("    - Clean wtmp (username)")
    print("    - Clean utmp (username)")
    print("    - Clean lastlog (username)")
    print("    - Clean bash history (username)")
    print("    - Clean audit.log (keywords)")
    
    print("\n[*] Example code:")
    print("""
    results = cleaner.comprehensive_cleanup(
        username='attacker',
        ip_address='10.10.14.5',
        keywords=['sudo', 'ssh', 'failed']
    )
    
    for log_type, success in results.items():
        print(f"{log_type}: {'✅' if success else '❌'}")
    """)


def example_3_rotation_cleaning():
    """Example: Clean rotated log files"""
    print("\n" + "="*60)
    print("Example 3: Rotated Log Cleaning")
    print("="*60)
    
    rotation_cleaner = LogRotationCleaner()
    
    # List rotated logs (safe - read-only)
    print("\n[*] Listing rotated logs...")
    files = rotation_cleaner.list_rotated_logs('/var/log')
    
    if files:
        print(f"\n[+] Found {len(files)} rotated log files")
        print(f"[*] First 5 files:")
        for filepath in files[:5]:
            print(f"    {filepath}")
    else:
        print("\n[-] No rotated log files found")
        print("[*] (This is expected if no logs have been rotated)")
    
    # Get stats
    stats = rotation_cleaner.get_rotation_stats('/var/log')
    print(f"\n[*] Rotation statistics:")
    print(f"    Total files: {stats['count']}")
    print(f"    Total size: {stats['total_size_mb']:.2f} MB")
    
    print("\n[*] To clean rotated logs:")
    print("    count = rotation_cleaner.clean_rotated_logs('/var/log', dry_run=True)")


def example_4_text_log_filtering():
    """Example: Advanced text log filtering"""
    print("\n" + "="*60)
    print("Example 4: Text Log Filtering")
    print("="*60)
    
    text_cleaner = TextLogCleaner()
    
    print("\n[*] Text log cleaning capabilities:")
    print("    - Filter by username")
    print("    - Filter by IP address")
    print("    - Filter by keywords")
    print("    - Filter by regex patterns")
    
    print("\n[*] Example: Filter auth.log by patterns")
    print("""
    patterns = [
        r"Failed password.*",
        r"authentication failure.*",
        r"session opened.*testuser"
    ]
    
    text_cleaner.clean_by_pattern('/var/log/auth.log', patterns)
    """)


def example_5_binary_log_analysis():
    """Example: Binary log analysis"""
    print("\n" + "="*60)
    print("Example 5: Binary Log Analysis")
    print("="*60)
    
    binary_cleaner = BinaryLogCleaner()
    
    # Try to get record count from wtmp
    if os.path.exists('/var/log/wtmp'):
        record_count = binary_cleaner.get_record_count('/var/log/wtmp', 'wtmp')
        print(f"\n[*] wtmp contains {record_count} login records")
        
        # Dump first few records
        print("\n[*] Dumping first 10 usernames from wtmp:")
        usernames = binary_cleaner.dump_records('/var/log/wtmp', 'wtmp', max_records=10)
        
        unique_users = set(filter(None, usernames))
        if unique_users:
            for user in unique_users:
                print(f"    - {user}")
        else:
            print("    (No usernames found in first 10 records)")
    else:
        print("\n[-] wtmp not found (this is normal on some systems)")
    
    print("\n[*] Binary log cleaning example:")
    print("""
    # Clean wtmp for specific user
    binary_cleaner.clean_wtmp('/var/log/wtmp', username='testuser')
    
    # Clean lastlog for specific user
    binary_cleaner.clean_lastlog('/var/log/lastlog', username='testuser')
    """)


def example_6_log_paths():
    """Example: Display configured log paths"""
    print("\n" + "="*60)
    print("Example 6: Configured Log Paths")
    print("="*60)
    
    print("\n[*] Log file locations:")
    print("-" * 60)
    
    for log_name, log_path in LOG_PATHS.items():
        exists = "✅" if os.path.exists(log_path) else "❌"
        size = ""
        
        if os.path.exists(log_path):
            try:
                file_size = os.path.getsize(log_path)
                size = f" ({format_size(file_size)})"
            except:
                size = " (size unknown)"
        
        print(f"{exists} {log_name:12s} {log_path}{size}")


def example_7_safety_features():
    """Example: Safety features and backups"""
    print("\n" + "="*60)
    print("Example 7: Safety Features")
    print("="*60)
    
    cleaner = LinuxLogCleaner()
    
    print("\n[*] Automatic backup creation:")
    print("    - Backups created by default before any modification")
    print("    - Format: <logfile>.backup-YYYYMMDDHHmmss")
    print("    - Example: /var/log/auth.log.backup-20241220143022")
    
    print("\n[*] Disable backups (not recommended):")
    print("    cleaner.clean_auth_log(username='test', preserve_backup=False)")
    
    print("\n[*] Root privilege checking:")
    if check_root():
        print("    ✅ Running with root privileges")
    else:
        print("    ❌ NOT running with root privileges")
        print("    [*] Most operations require root/sudo")


def example_8_custom_workflow():
    """Example: Custom cleanup workflow"""
    print("\n" + "="*60)
    print("Example 8: Custom Cleanup Workflow")
    print("="*60)
    
    print("\n[*] Example custom workflow:")
    print("""
    from linux_log_cleanup import LinuxLogCleaner
    from linux_log_cleanup.utils import check_root, confirm_action
    
    # Check privileges
    if not check_root():
        print("Please run with sudo")
        exit(1)
    
    # Initialize
    cleaner = LinuxLogCleaner()
    
    # Confirm with user
    if not confirm_action("Clean logs for user 'attacker'?"):
        print("Cancelled")
        exit(0)
    
    # Custom cleanup sequence
    steps = [
        ('auth.log', lambda: cleaner.clean_auth_log(username='attacker')),
        ('wtmp', lambda: cleaner.clean_wtmp(username='attacker')),
        ('bash history', lambda: cleaner.clean_bash_history(username='attacker'))
    ]
    
    for step_name, step_func in steps:
        print(f"Cleaning {step_name}...")
        success = step_func()
        if success:
            print(f"✅ {step_name} cleaned")
        else:
            print(f"❌ {step_name} failed")
    
    print("Cleanup complete!")
    """)


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("Linux Log Cleanup Framework - Examples")
    print("="*60)
    print("\n[!] WARNING: These are demonstrations only")
    print("[!] Actual cleanup operations will modify system logs")
    print("[!] Always test on non-production systems first")
    
    if not check_root():
        print("\n[*] Note: Not running as root - some examples limited")
        print("[*] Run with 'sudo python examples/demo.py' for full examples")
    
    try:
        example_1_basic_cleanup()
        example_2_comprehensive_cleanup()
        example_3_rotation_cleaning()
        example_4_text_log_filtering()
        example_5_binary_log_analysis()
        example_6_log_paths()
        example_7_safety_features()
        example_8_custom_workflow()
        
        print("\n" + "="*60)
        print("All Examples Completed")
        print("="*60)
        print("\n[*] Next steps:")
        print("    1. Review the main.py CLI for command-line usage")
        print("    2. Read README.md for complete documentation")
        print("    3. Test on isolated systems before production use")
        print("    4. Always create backups (default behavior)")
        
    except Exception as e:
        print(f"\n[-] Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
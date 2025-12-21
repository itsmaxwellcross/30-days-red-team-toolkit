#!/usr/bin/env python3
"""
Timestamp Stomping Toolkit - Example Usage

This script demonstrates how to use the framework programmatically.

WARNING: This is for demonstration only. Test on non-critical files!
"""

import sys
import os
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from timestamp_stomper import TimestampStomper, MACBAnalysis
from timestamp_stomper.utils import get_legitimate_reference


def create_test_file():
    """Create a temporary test file"""
    fd, path = tempfile.mkstemp(suffix='.txt', prefix='test_')
    with os.fdopen(fd, 'w') as f:
        f.write("Test file for timestamp stomping demonstration\n")
    return path


def example_1_basic_operations():
    """Example: Basic timestamp operations"""
    print("\n" + "="*60)
    print("Example 1: Basic Timestamp Operations")
    print("="*60)
    
    # Create test file
    test_file = create_test_file()
    print(f"\n[*] Created test file: {test_file}")
    
    # Initialize stomper
    stomper = TimestampStomper()
    
    # Display original timestamps
    print("\n[*] Original timestamps:")
    stomper.display_file_times(test_file)
    
    # Set random past time
    print("[*] Setting random past timestamp...")
    stomper.set_random_past_time(test_file, days_ago_min=30, days_ago_max=90)
    
    # Display modified timestamps
    print("\n[*] Modified timestamps:")
    stomper.display_file_times(test_file)
    
    # Cleanup
    os.remove(test_file)
    print(f"[*] Cleaned up test file")


def example_2_copy_timestamps():
    """Example: Copy timestamps from legitimate file"""
    print("\n" + "="*60)
    print("Example 2: Copy Timestamps from Legitimate File")
    print("="*60)
    
    # Find legitimate reference
    reference = get_legitimate_reference()
    
    if not reference:
        print("[-] No legitimate reference file found")
        return
    
    print(f"\n[*] Using reference file: {reference}")
    
    # Create test file
    test_file = create_test_file()
    print(f"[*] Created test file: {test_file}")
    
    # Initialize stomper
    stomper = TimestampStomper()
    
    # Copy timestamps
    print("\n[*] Copying timestamps...")
    stomper.copy_timestamps(reference, test_file)
    
    # Verify
    print("\n[*] Verification:")
    stomper.display_file_times(test_file)
    
    # Cleanup
    os.remove(test_file)


def example_3_match_directory():
    """Example: Match directory average"""
    print("\n" + "="*60)
    print("Example 3: Match Directory Average")
    print("="*60)
    
    # Use temp directory
    temp_dir = tempfile.gettempdir()
    print(f"\n[*] Using directory: {temp_dir}")
    
    # Create test file
    test_file = create_test_file()
    print(f"[*] Created test file: {test_file}")
    
    # Initialize stomper
    stomper = TimestampStomper()
    
    # Match directory
    print("\n[*] Matching to directory average...")
    stomper.match_directory_times(test_file, temp_dir)
    
    # Display result
    print("\n[*] Result:")
    stomper.display_file_times(test_file)
    
    # Cleanup
    os.remove(test_file)


def example_4_specific_timestamp():
    """Example: Set specific timestamp"""
    print("\n" + "="*60)
    print("Example 4: Set Specific Timestamp")
    print("="*60)
    
    # Create test file
    test_file = create_test_file()
    print(f"\n[*] Created test file: {test_file}")
    
    # Initialize stomper
    stomper = TimestampStomper()
    
    # Set specific timestamp: June 15, 2023 at 14:30:00
    print("\n[*] Setting specific timestamp: 2023-06-15 14:30:00")
    stomper.set_specific_time(test_file, 2023, 6, 15, 14, 30, 0)
    
    # Display result
    print("\n[*] Result:")
    stomper.display_file_times(test_file)
    
    # Cleanup
    os.remove(test_file)


def example_5_macb_analysis():
    """Example: MACB analysis"""
    print("\n" + "="*60)
    print("Example 5: MACB Analysis")
    print("="*60)
    
    # Create test file with suspicious timestamps
    test_file = create_test_file()
    print(f"\n[*] Created test file: {test_file}")
    
    # Initialize stomper
    stomper = TimestampStomper()
    
    # Make all timestamps identical (suspicious)
    print("\n[*] Making all timestamps identical (suspicious)...")
    specific_time = datetime(2023, 6, 15, 14, 30, 0)
    stomper.set_file_times(test_file, specific_time, specific_time, specific_time)
    
    # Analyze
    print("\n[*] Running MACB analysis:")
    MACBAnalysis.analyze_macb(test_file)
    
    # Cleanup
    os.remove(test_file)


def example_6_compare_timestamps():
    """Example: Compare timestamps between files"""
    print("\n" + "="*60)
    print("Example 6: Compare Timestamps")
    print("="*60)
    
    # Create two test files
    file1 = create_test_file()
    file2 = create_test_file()
    
    print(f"\n[*] Created test files:")
    print(f"    File 1: {file1}")
    print(f"    File 2: {file2}")
    
    # Initialize stomper
    stomper = TimestampStomper()
    
    # Copy timestamps from file1 to file2
    print("\n[*] Copying timestamps from file1 to file2...")
    stomper.copy_timestamps(file1, file2)
    
    # Compare
    print("\n[*] Comparing timestamps:")
    MACBAnalysis.compare_timestamps(file1, file2)
    
    # Cleanup
    os.remove(file1)
    os.remove(file2)


def example_7_bulk_operations():
    """Example: Bulk timestamp stomping"""
    print("\n" + "="*60)
    print("Example 7: Bulk Operations")
    print("="*60)
    
    # Create temporary directory with test files
    temp_dir = tempfile.mkdtemp(prefix='stomp_test_')
    print(f"\n[*] Created test directory: {temp_dir}")
    
    # Create multiple test files
    test_files = []
    for i in range(5):
        test_file = os.path.join(temp_dir, f'test_{i}.txt')
        with open(test_file, 'w') as f:
            f.write(f"Test file {i}\n")
        test_files.append(test_file)
    
    print(f"[*] Created {len(test_files)} test files")
    
    # Initialize stomper
    stomper = TimestampStomper()
    
    # Bulk stomp with random timestamps
    print("\n[*] Performing bulk timestamp stomping...")
    stomper.bulk_stomp(temp_dir, days_min=30, days_max=90)
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)
    print(f"\n[*] Cleaned up test directory")


def example_8_platform_awareness():
    """Example: Platform-aware operations"""
    print("\n" + "="*60)
    print("Example 8: Platform-Aware Operations")
    print("="*60)
    
    stomper = TimestampStomper()
    
    print(f"\n[*] Operating System: {stomper.os_type}")
    print(f"[*] Platform Handler: {stomper.platform_handler.__class__.__name__}")
    
    if stomper.os_type == 'Windows':
        print("\n[*] Windows-specific features:")
        print("    - Full creation time support")
        print("    - Requires pywin32 for full functionality")
    else:
        print("\n[*] Unix/Linux features:")
        print("    - Access and modification time support")
        print("    - Limited creation time support")
    
    # Show reference files for platform
    from timestamp_stomper.utils import get_reference_files
    reference_files = get_reference_files()
    
    print(f"\n[*] Legitimate reference files for {stomper.os_type}:")
    for ref in reference_files[:3]:  # Show first 3
        if os.path.exists(ref):
            print(f"    ✅ {ref}")
        else:
            print(f"    ❌ {ref} (not found)")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("Timestamp Stomping Toolkit - Examples")
    print("="*60)
    print("\n[!] These examples use temporary files and are safe to run")
    
    try:
        example_1_basic_operations()
        example_2_copy_timestamps()
        example_3_match_directory()
        example_4_specific_timestamp()
        example_5_macb_analysis()
        example_6_compare_timestamps()
        example_7_bulk_operations()
        example_8_platform_awareness()
        
        print("\n" + "="*60)
        print("All Examples Completed")
        print("="*60)
        print("\n[*] Next steps:")
        print("    1. Review main.py CLI for command-line usage")
        print("    2. Read README.md for complete documentation")
        print("    3. Test on isolated systems before production use")
        print("    4. Always verify timestamps after manipulation")
        
    except Exception as e:
        print(f"\n[-] Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
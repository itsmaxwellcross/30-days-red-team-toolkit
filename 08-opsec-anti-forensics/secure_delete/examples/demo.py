#!/usr/bin/env python3
"""
Secure File Deletion Framework - Example Usage

This script demonstrates how to use the framework programmatically.

WARNING: This is for demonstration only. Test on non-critical files!
"""

import sys
import os
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from secure_delete import SecureDelete, ArtifactCleaner, OverwriteMethods


def create_test_file(content="Test file for secure deletion\n"):
    """Create a temporary test file"""
    fd, path = tempfile.mkstemp(suffix='.txt', prefix='test_delete_')
    with os.fdopen(fd, 'w') as f:
        f.write(content)
    return path


def example_1_basic_deletion():
    """Example: Basic secure file deletion"""
    print("\n" + "="*60)
    print("Example 1: Basic Secure Deletion")
    print("="*60)
    
    # Create test file
    test_file = create_test_file()
    print(f"\n[*] Created test file: {test_file}")
    
    # Get file size
    size = os.path.getsize(test_file)
    print(f"[*] File size: {size} bytes")
    
    # Initialize secure delete
    deleter = SecureDelete()
    
    # Securely delete with 3 random passes
    print("\n[*] Deleting with 3 random passes...")
    deleter.secure_delete_file(test_file, passes=3, method='random')
    
    # Verify deletion
    if not os.path.exists(test_file):
        print(f"\n[+] File successfully deleted")
    else:
        print(f"\n[-] File still exists!")


def example_2_deletion_methods():
    """Example: Different deletion methods"""
    print("\n" + "="*60)
    print("Example 2: Deletion Methods")
    print("="*60)
    
    methods = OverwriteMethods()
    
    # Display info about each method
    for method_name in ['random', 'zeros', 'ones', 'dod', 'gutmann']:
        info = methods.get_method_info(method_name)
        print(f"\n[*] {info['name']}")
        print(f"    Passes: {info['passes']}")
        print(f"    Description: {info['description']}")
        print(f"    Security: {info['security']}")
        print(f"    Speed: {info['speed']}")


def example_3_dod_standard():
    """Example: DoD 5220.22-M standard deletion"""
    print("\n" + "="*60)
    print("Example 3: DoD 5220.22-M Standard")
    print("="*60)
    
    # Create test file
    test_file = create_test_file("Classified document\n" * 100)
    print(f"\n[*] Created test file: {test_file}")
    
    # Initialize secure delete
    deleter = SecureDelete()
    
    # Delete using DoD standard (3 passes: ones, zeros, random)
    print("\n[*] Deleting using DoD 5220.22-M standard...")
    deleter.secure_delete_file(test_file, passes=3, method='dod')
    
    # Verify
    if not os.path.exists(test_file):
        print(f"\n[+] File securely wiped using DoD standard")


def example_4_directory_deletion():
    """Example: Secure directory deletion"""
    print("\n" + "="*60)
    print("Example 4: Directory Deletion")
    print("="*60)
    
    # Create temp directory with files
    temp_dir = tempfile.mkdtemp(prefix='test_delete_')
    print(f"\n[*] Created test directory: {temp_dir}")
    
    # Create multiple test files
    for i in range(5):
        test_file = os.path.join(temp_dir, f'file_{i}.txt')
        with open(test_file, 'w') as f:
            f.write(f"Test file {i}\n" * 10)
    
    print(f"[*] Created 5 test files")
    
    # Initialize secure delete
    deleter = SecureDelete()
    
    # Securely delete directory
    print("\n[*] Securely deleting directory...")
    deleter.secure_delete_directory(temp_dir, passes=3, method='random')


def example_5_file_statistics():
    """Example: Get file deletion statistics"""
    print("\n" + "="*60)
    print("Example 5: File Statistics")
    print("="*60)
    
    # Create test files of different sizes
    test_files = []
    
    # Small file
    small_file = create_test_file("Small\n" * 10)
    test_files.append(("Small", small_file))
    
    # Medium file
    medium_file = create_test_file("Medium\n" * 1000)
    test_files.append(("Medium", medium_file))
    
    # Large file
    large_file = create_test_file("Large\n" * 100000)
    test_files.append(("Large", large_file))
    
    # Get stats for each
    deleter = SecureDelete()
    
    for name, filepath in test_files:
        stats = deleter.get_deletion_stats(filepath)
        
        if stats:
            print(f"\n[*] {name} file: {filepath}")
            print(f"    Size: {stats['size_mb']:.2f} MB")
            print(f"    Recommended passes: {stats['passes_recommended']}")
            print(f"    Recommended method: {stats['method_recommended']}")
        
        # Clean up
        os.remove(filepath)


def example_6_artifact_cleaning():
    """Example: Forensic artifact cleaning"""
    print("\n" + "="*60)
    print("Example 6: Artifact Cleaning")
    print("="*60)
    
    cleaner = ArtifactCleaner()
    
    print("\n[*] Artifact cleaner capabilities:")
    print("    - Clean temporary files")
    print("    - Clean browser history")
    print("    - Clean Windows Prefetch")
    print("    - Clean Windows MRU lists")
    print("    - Clean Recycle Bin")
    
    print("\n[!] Note: This is just a demonstration")
    print("[!] To actually clean artifacts, run:")
    print("[!]   python main.py --clean-artifacts")


def example_7_free_space_wiping():
    """Example: Free space wiping"""
    print("\n" + "="*60)
    print("Example 7: Free Space Wiping")
    print("="*60)
    
    print("\n[*] Free space wiping fills unused disk space with random data")
    print("[*] This prevents recovery of previously deleted files")
    
    print("\n[*] Example usage:")
    print("    deleter = SecureDelete()")
    print("    deleter.wipe_free_space('/tmp', size_mb=10)")
    
    print("\n[!] Not executing in demo (to avoid filling disk)")


def example_8_overwrite_patterns():
    """Example: Different overwrite patterns"""
    print("\n" + "="*60)
    print("Example 8: Overwrite Patterns")
    print("="*60)
    
    methods = OverwriteMethods()
    
    # Generate sample data
    print("\n[*] Sample overwrite patterns:")
    
    print("\n  Random data (first 16 bytes):")
    random_data = methods.random_data(16)
    print(f"    {random_data.hex()}")
    
    print("\n  Zero data (first 16 bytes):")
    zero_data = methods.zero_data(16)
    print(f"    {zero_data.hex()}")
    
    print("\n  One data (first 16 bytes):")
    one_data = methods.one_data(16)
    print(f"    {one_data.hex()}")
    
    print("\n  DoD Pass 1 (ones):")
    dod_pass1 = methods.dod_pattern(16, 0)
    print(f"    {dod_pass1.hex()}")
    
    print("\n  DoD Pass 2 (zeros):")
    dod_pass2 = methods.dod_pattern(16, 1)
    print(f"    {dod_pass2.hex()}")
    
    print("\n  DoD Pass 3 (random):")
    dod_pass3 = methods.dod_pattern(16, 2)
    print(f"    {dod_pass3.hex()}")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("Secure File Deletion Framework - Examples")
    print("="*60)
    print("\n[!] These examples use temporary files and are safe to run")
    
    try:
        example_1_basic_deletion()
        example_2_deletion_methods()
        example_3_dod_standard()
        example_4_directory_deletion()
        example_5_file_statistics()
        example_6_artifact_cleaning()
        example_7_free_space_wiping()
        example_8_overwrite_patterns()
        
        print("\n" + "="*60)
        print("All Examples Completed")
        print("="*60)
        print("\n[*] Next steps:")
        print("    1. Review main.py CLI for command-line usage")
        print("    2. Read README.md for complete documentation")
        print("    3. Test on non-critical files first")
        print("    4. Always verify files are actually deleted")
        
    except Exception as e:
        print(f"\n[-] Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
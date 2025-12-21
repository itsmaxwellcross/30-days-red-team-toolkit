"""
Main Timestamp Stomper Class
Provides high-level interface for timestamp manipulation
"""

import os
import platform
from pathlib import Path
from datetime import datetime, timedelta
import random

from .constants import DEFAULT_DAYS_MIN, DEFAULT_DAYS_MAX, MAX_BULK_FILES, BULK_PROGRESS_INTERVAL
from ..platforms.handler import get_platform_handler


class TimestampStomper:
    """
    Main class for timestamp manipulation
    
    Provides functionality to:
    - Get and set file timestamps
    - Copy timestamps between files
    - Match timestamps to directories
    - Set random or specific timestamps
    - Bulk timestamp operations
    """
    
    def __init__(self):
        """Initialize timestamp stomper"""
        self.os_type = platform.system()
        self.platform_handler = get_platform_handler()
        
        print(f"[+] Timestamp Stomper initialized")
        print(f"[+] OS: {self.os_type}")
    
    def get_file_times(self, filepath):
        """
        Get file timestamps using platform-specific handler
        
        Args:
            filepath (str): Path to file
            
        Returns:
            dict: Dictionary with 'accessed', 'modified', 'created' timestamps
        """
        return self.platform_handler.get_file_times(filepath)
    
    def set_file_times(self, filepath, accessed=None, modified=None, created=None):
        """
        Set file timestamps using platform-specific handler
        
        Args:
            filepath (str): Path to file
            accessed (datetime, optional): Access time to set
            modified (datetime, optional): Modification time to set
            created (datetime, optional): Creation time to set
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.platform_handler.set_file_times(filepath, accessed, modified, created)
    
    def copy_timestamps(self, source_file, target_file):
        """
        Copy all timestamps from source file to target file
        
        Args:
            source_file (str): Source file to copy timestamps from
            target_file (str): Target file to apply timestamps to
            
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"[*] Copying timestamps from {source_file} to {target_file}")
        
        # Get source timestamps
        source_times = self.get_file_times(source_file)
        
        if not source_times:
            return False
        
        print(f"[*] Source file times:")
        print(f"    Created:  {source_times['created']}")
        print(f"    Modified: {source_times['modified']}")
        print(f"    Accessed: {source_times['accessed']}")
        
        # Apply to target
        success = self.set_file_times(
            target_file,
            accessed=source_times['accessed'],
            modified=source_times['modified'],
            created=source_times['created']
        )
        
        if success:
            print(f"[+] Timestamps copied successfully")
        
        return success
    
    def match_directory_times(self, target_file, directory):
        """
        Match file timestamps to average of directory contents
        
        Args:
            target_file (str): File to modify
            directory (str): Directory to calculate average from
            
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"[*] Matching timestamps to directory: {directory}")
        
        # Get all files in directory
        try:
            files = list(Path(directory).iterdir())
        except Exception as e:
            print(f"[-] Error reading directory: {e}")
            return False
        
        if not files:
            print(f"[-] No files in directory")
            return False
        
        # Calculate average timestamps
        total_accessed = 0
        total_modified = 0
        count = 0
        
        for filepath in files:
            if filepath.is_file():
                times = self.get_file_times(str(filepath))
                if times:
                    total_accessed += times['accessed'].timestamp()
                    total_modified += times['modified'].timestamp()
                    count += 1
        
        if count == 0:
            print(f"[-] No valid files in directory")
            return False
        
        # Calculate averages
        avg_accessed = datetime.fromtimestamp(total_accessed / count)
        avg_modified = datetime.fromtimestamp(total_modified / count)
        
        print(f"[*] Average directory times (from {count} files):")
        print(f"    Modified: {avg_modified}")
        print(f"    Accessed: {avg_accessed}")
        
        # Apply to target
        return self.set_file_times(
            target_file,
            accessed=avg_accessed,
            modified=avg_modified,
            created=avg_modified
        )
    
    def set_random_past_time(self, filepath, days_ago_min=DEFAULT_DAYS_MIN, 
                            days_ago_max=DEFAULT_DAYS_MAX):
        """
        Set random past timestamp
        
        Args:
            filepath (str): File to modify
            days_ago_min (int): Minimum days in the past
            days_ago_max (int): Maximum days in the past
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Random time in the past
        days_ago = random.randint(days_ago_min, days_ago_max)
        hours = random.randint(0, 23)
        minutes = random.randint(0, 59)
        seconds = random.randint(0, 59)
        
        past_time = datetime.now() - timedelta(
            days=days_ago, 
            hours=hours, 
            minutes=minutes, 
            seconds=seconds
        )
        
        print(f"[*] Setting random past time: {past_time}")
        print(f"[*] ({days_ago} days ago)")
        
        return self.set_file_times(
            filepath,
            accessed=past_time,
            modified=past_time,
            created=past_time
        )
    
    def set_future_time(self, filepath, days_ahead=1):
        """
        Set future timestamp (suspicious but sometimes useful)
        
        Args:
            filepath (str): File to modify
            days_ahead (int): Days into the future
            
        Returns:
            bool: True if successful, False otherwise
        """
        future_time = datetime.now() + timedelta(days=days_ahead)
        
        print(f"[*] Setting future time: {future_time}")
        print(f"[!] Warning: Future timestamps are suspicious and easily detected")
        
        return self.set_file_times(
            filepath,
            accessed=future_time,
            modified=future_time,
            created=future_time
        )
    
    def display_file_times(self, filepath):
        """
        Display all file timestamps
        
        Args:
            filepath (str): File to display timestamps for
        """
        times = self.get_file_times(filepath)
        
        if times:
            print(f"\n[*] File: {filepath}")
            print(f"    Created:  {times['created']}")
            print(f"    Modified: {times['modified']}")
            print(f"    Accessed: {times['accessed']}")
            print()
    
    def bulk_stomp(self, directory, reference_file=None, days_min=None, days_max=None):
        """
        Stomp timestamps for all files in directory
        
        Args:
            directory (str): Directory containing files to stomp
            reference_file (str, optional): Reference file to copy timestamps from
            days_min (int, optional): Minimum days for random timestamps
            days_max (int, optional): Maximum days for random timestamps
            
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"[*] Bulk timestamp stomping: {directory}")
        
        # Get reference timestamps if provided
        ref_times = None
        if reference_file:
            ref_times = self.get_file_times(reference_file)
            if not ref_times:
                print(f"[-] Failed to read reference file")
                return False
            print(f"[*] Using reference file: {reference_file}")
        
        # Get all files recursively
        try:
            files = list(Path(directory).rglob('*'))
        except Exception as e:
            print(f"[-] Error reading directory: {e}")
            return False
        
        # Filter to only files
        files = [f for f in files if f.is_file()]
        
        # Safety check
        if len(files) > MAX_BULK_FILES:
            print(f"[!] Warning: {len(files)} files found (max: {MAX_BULK_FILES})")
            print(f"[!] Limiting to first {MAX_BULK_FILES} files")
            files = files[:MAX_BULK_FILES]
        
        stomped_count = 0
        failed_count = 0
        
        print(f"[*] Processing {len(files)} files...")
        
        for i, filepath in enumerate(files):
            try:
                if reference_file and ref_times:
                    # Use reference file timestamps
                    self.set_file_times(
                        str(filepath),
                        accessed=ref_times['accessed'],
                        modified=ref_times['modified'],
                        created=ref_times['created']
                    )
                else:
                    # Use random timestamps
                    self.set_random_past_time(
                        str(filepath),
                        days_ago_min=days_min or DEFAULT_DAYS_MIN,
                        days_ago_max=days_max or DEFAULT_DAYS_MAX
                    )
                
                stomped_count += 1
                
                # Show progress
                if (i + 1) % BULK_PROGRESS_INTERVAL == 0:
                    print(f"[*] Progress: {i + 1}/{len(files)} files processed")
            
            except Exception as e:
                failed_count += 1
                print(f"[-] Failed to stomp {filepath.name}: {e}")
        
        print(f"\n[+] Bulk operation complete:")
        print(f"    Success: {stomped_count} files")
        print(f"    Failed:  {failed_count} files")
        
        return failed_count == 0
    
    def set_specific_time(self, filepath, year, month, day, hour=12, minute=0, second=0):
        """
        Set specific timestamp
        
        Args:
            filepath (str): File to modify
            year (int): Year
            month (int): Month
            day (int): Day
            hour (int): Hour (default: 12)
            minute (int): Minute (default: 0)
            second (int): Second (default: 0)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            specific_time = datetime(year, month, day, hour, minute, second)
            
            print(f"[*] Setting specific time: {specific_time}")
            
            return self.set_file_times(
                filepath,
                accessed=specific_time,
                modified=specific_time,
                created=specific_time
            )
        
        except ValueError as e:
            print(f"[-] Invalid date/time: {e}")
            return False
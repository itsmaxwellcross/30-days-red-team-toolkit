"""
Log Rotation Cleaner
Handles cleaning of rotated log files (*.1, *.2, *.gz, etc.)
"""

import os
import glob
from pathlib import Path

from ..core.constants import ROTATED_PATTERNS


class LogRotationCleaner:
    """
    Clean rotated log files
    
    Provides functionality to:
    - Find and delete rotated logs
    - Clean compressed logs
    - Recursive directory cleaning
    """
    
    def __init__(self):
        """Initialize rotation cleaner"""
        self.patterns = ROTATED_PATTERNS.copy()
    
    def clean_rotated_logs(self, log_dir='/var/log', patterns=None, dry_run=False):
        """
        Clean all rotated versions of logs in a directory
        
        Args:
            log_dir (str): Directory containing log files
            patterns (list, optional): Custom patterns to match
            dry_run (bool): If True, only show what would be deleted
            
        Returns:
            int: Number of files deleted (or would be deleted in dry run)
        """
        if patterns is None:
            patterns = self.patterns
        
        print(f"[*] {'[DRY RUN] ' if dry_run else ''}Cleaning rotated logs in: {log_dir}")
        
        cleaned_count = 0
        
        for pattern in patterns:
            # Find files matching pattern recursively
            search_pattern = f"{log_dir}/**/{pattern}"
            files = glob.glob(search_pattern, recursive=True)
            
            for filepath in files:
                try:
                    if dry_run:
                        print(f"[*] Would delete: {filepath}")
                        cleaned_count += 1
                    else:
                        os.remove(filepath)
                        print(f"[+] Deleted: {filepath}")
                        cleaned_count += 1
                
                except PermissionError:
                    print(f"[-] Permission denied: {filepath}")
                except Exception as e:
                    print(f"[-] Failed to delete {filepath}: {e}")
        
        if dry_run:
            print(f"[*] Would delete {cleaned_count} rotated log files")
        else:
            print(f"[+] Deleted {cleaned_count} rotated log files")
        
        return cleaned_count
    
    def clean_specific_log_rotations(self, log_name, log_dir='/var/log', dry_run=False):
        """
        Clean rotations of a specific log file
        
        Args:
            log_name (str): Base name of log file (e.g., 'auth.log')
            log_dir (str): Directory containing log files
            dry_run (bool): If True, only show what would be deleted
            
        Returns:
            int: Number of files deleted
        """
        print(f"[*] Cleaning rotations of {log_name}")
        
        cleaned_count = 0
        
        # Find all variations of this log
        patterns = [
            f"{log_name}.*",
            f"{log_name}-*"
        ]
        
        for pattern in patterns:
            search_path = os.path.join(log_dir, pattern)
            files = glob.glob(search_path)
            
            for filepath in files:
                # Don't delete the main log file
                if filepath == os.path.join(log_dir, log_name):
                    continue
                
                try:
                    if dry_run:
                        print(f"[*] Would delete: {filepath}")
                        cleaned_count += 1
                    else:
                        os.remove(filepath)
                        print(f"[+] Deleted: {filepath}")
                        cleaned_count += 1
                
                except Exception as e:
                    print(f"[-] Failed to delete {filepath}: {e}")
        
        return cleaned_count
    
    def list_rotated_logs(self, log_dir='/var/log'):
        """
        List all rotated log files in a directory
        
        Args:
            log_dir (str): Directory to search
            
        Returns:
            list: List of rotated log file paths
        """
        rotated_files = []
        
        for pattern in self.patterns:
            search_pattern = f"{log_dir}/**/{pattern}"
            files = glob.glob(search_pattern, recursive=True)
            rotated_files.extend(files)
        
        return sorted(set(rotated_files))
    
    def get_rotation_stats(self, log_dir='/var/log'):
        """
        Get statistics about rotated logs
        
        Args:
            log_dir (str): Directory to analyze
            
        Returns:
            dict: Statistics including count, total size, etc.
        """
        rotated_files = self.list_rotated_logs(log_dir)
        
        total_size = 0
        for filepath in rotated_files:
            try:
                total_size += os.path.getsize(filepath)
            except:
                pass
        
        stats = {
            'count': len(rotated_files),
            'total_size': total_size,
            'total_size_mb': total_size / (1024 * 1024),
            'files': rotated_files[:10]  # First 10 files as sample
        }
        
        return stats
    
    def clean_compressed_logs(self, log_dir='/var/log', dry_run=False):
        """
        Clean only compressed log files (.gz, .bz2, .xz)
        
        Args:
            log_dir (str): Directory containing log files
            dry_run (bool): If True, only show what would be deleted
            
        Returns:
            int: Number of files deleted
        """
        compressed_patterns = ['*.gz', '*.bz2', '*.xz']
        
        return self.clean_rotated_logs(log_dir, compressed_patterns, dry_run)
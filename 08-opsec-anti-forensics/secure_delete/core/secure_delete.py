"""
Main Secure Delete Class
Provides high-level interface for secure file deletion
"""

import os
from pathlib import Path

from .constants import DEFAULT_PASSES, DEFAULT_CHUNK_SIZE, MAX_BULK_FILES, PROGRESS_INTERVAL
from ..methods.overwrite_methods import OverwriteMethods


class SecureDelete:
    """
    Main class for secure file deletion
    
    Provides functionality to:
    - Securely delete individual files
    - Securely delete directories
    - Wipe free space
    - Multiple overwrite methods
    - Progress tracking for bulk operations
    """
    
    def __init__(self):
        """Initialize secure deletion framework"""
        self.methods = OverwriteMethods()
        print(f"[+] Secure Delete initialized")
    
    def secure_delete_file(self, filepath, passes=DEFAULT_PASSES, method='random'):
        """
        Securely delete file with multiple overwrite passes
        
        Args:
            filepath (str): Path to file to delete
            passes (int): Number of overwrite passes
            method (str): Overwrite method ('random', 'zeros', 'ones', 'dod', 'gutmann')
            
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"[*] Secure delete: {filepath}")
        print(f"[*] Passes: {passes}")
        print(f"[*] Method: {method}")
        
        try:
            # Get file size
            file_size = os.path.getsize(filepath)
            print(f"[*] File size: {file_size} bytes")
            
            # Perform overwrite passes
            for pass_num in range(passes):
                print(f"[*] Pass {pass_num + 1}/{passes}...")
                
                if not self._overwrite_file(filepath, file_size, method, pass_num, passes):
                    return False
            
            # Delete file
            os.remove(filepath)
            print(f"[+] File securely deleted: {filepath}")
            
            return True
        
        except FileNotFoundError:
            print(f"[-] File not found: {filepath}")
            return False
        except PermissionError:
            print(f"[-] Permission denied: {filepath}")
            return False
        except Exception as e:
            print(f"[-] Secure delete failed: {e}")
            return False
    
    def _overwrite_file(self, filepath, file_size, method, pass_num, total_passes):
        """
        Overwrite file with specified method
        
        Args:
            filepath (str): Path to file
            file_size (int): Size of file in bytes
            method (str): Overwrite method
            pass_num (int): Current pass number
            total_passes (int): Total number of passes
            
        Returns:
            bool: True if successful
        """
        try:
            with open(filepath, 'r+b') as f:  # r+b to avoid truncating
                remaining = file_size
                
                while remaining > 0:
                    write_size = min(DEFAULT_CHUNK_SIZE, remaining)
                    
                    # Get data based on method and pass
                    if method == 'random':
                        data = self.methods.random_data(write_size)
                    elif method == 'zeros':
                        data = self.methods.zero_data(write_size)
                    elif method == 'ones':
                        data = self.methods.one_data(write_size)
                    elif method == 'dod':
                        data = self.methods.dod_pattern(write_size, pass_num)
                    elif method == 'gutmann':
                        data = self.methods.gutmann_pattern(write_size, pass_num)
                    else:
                        data = self.methods.random_data(write_size)
                    
                    f.write(data)
                    remaining -= write_size
                
                # Flush to disk
                f.flush()
                os.fsync(f.fileno())
            
            return True
        
        except Exception as e:
            print(f"[-] Overwrite failed: {e}")
            return False
    
    def secure_delete_directory(self, directory, passes=DEFAULT_PASSES, method='random'):
        """
        Securely delete entire directory
        
        Args:
            directory (str): Path to directory to delete
            passes (int): Number of overwrite passes
            method (str): Overwrite method
            
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"[*] Secure delete directory: {directory}")
        
        # Get all files recursively
        try:
            files = list(Path(directory).rglob('*'))
            files = [f for f in files if f.is_file()]
        except Exception as e:
            print(f"[-] Error reading directory: {e}")
            return False
        
        # Safety check
        if len(files) > MAX_BULK_FILES:
            print(f"[!] Warning: {len(files)} files found (max: {MAX_BULK_FILES})")
            print(f"[!] Limiting to first {MAX_BULK_FILES} files")
            files = files[:MAX_BULK_FILES]
        
        deleted_count = 0
        failed_count = 0
        
        print(f"[*] Processing {len(files)} files...")
        
        for i, filepath in enumerate(files):
            try:
                if self.secure_delete_file(str(filepath), passes, method):
                    deleted_count += 1
                else:
                    failed_count += 1
                
                # Show progress
                if (i + 1) % PROGRESS_INTERVAL == 0:
                    print(f"[*] Progress: {i + 1}/{len(files)} files processed")
            
            except Exception as e:
                print(f"[-] Failed to delete {filepath.name}: {e}")
                failed_count += 1
        
        # Remove empty directories
        try:
            import shutil
            shutil.rmtree(directory)
            print(f"[+] Directory removed: {directory}")
        except Exception as e:
            print(f"[-] Failed to remove directory: {e}")
        
        print(f"\n[+] Deletion complete:")
        print(f"    Success: {deleted_count} files")
        print(f"    Failed:  {failed_count} files")
        
        return failed_count == 0
    
    def wipe_free_space(self, drive, size_mb=100):
        """
        Wipe free space on drive by creating and deleting large file
        
        Args:
            drive (str): Drive or directory to wipe free space
            size_mb (int): Size in MB to wipe
            
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"[*] Wiping {size_mb} MB of free space on {drive}")
        
        temp_file = os.path.join(drive, '.wipe_temp_file')
        
        try:
            size_bytes = size_mb * 1024 * 1024
            
            with open(temp_file, 'wb') as f:
                remaining = size_bytes
                
                while remaining > 0:
                    write_size = min(DEFAULT_CHUNK_SIZE, remaining)
                    data = self.methods.random_data(write_size)
                    f.write(data)
                    remaining -= write_size
                
                f.flush()
                os.fsync(f.fileno())
            
            # Delete temp file
            os.remove(temp_file)
            print(f"[+] Free space wiped")
            
            return True
        
        except PermissionError:
            print(f"[-] Permission denied: {drive}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False
        except Exception as e:
            print(f"[-] Free space wipe failed: {e}")
            
            # Clean up temp file if it exists
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
            
            return False
    
    def get_deletion_stats(self, filepath):
        """
        Get information about a file before deletion
        
        Args:
            filepath (str): Path to file
            
        Returns:
            dict: File statistics
        """
        try:
            stat = os.stat(filepath)
            
            stats = {
                'size': stat.st_size,
                'size_mb': stat.st_size / (1024 * 1024),
                'passes_recommended': self._recommend_passes(stat.st_size),
                'method_recommended': self._recommend_method(stat.st_size)
            }
            
            return stats
        
        except Exception as e:
            print(f"[-] Failed to get file stats: {e}")
            return None
    
    def _recommend_passes(self, file_size):
        """Recommend number of passes based on file size"""
        if file_size < 1024 * 1024:  # < 1 MB
            return 7
        elif file_size < 100 * 1024 * 1024:  # < 100 MB
            return 3
        else:
            return 1  # Large files, single pass for speed
    
    def _recommend_method(self, file_size):
        """Recommend deletion method based on file size"""
        if file_size < 10 * 1024 * 1024:  # < 10 MB
            return 'dod'
        else:
            return 'random'
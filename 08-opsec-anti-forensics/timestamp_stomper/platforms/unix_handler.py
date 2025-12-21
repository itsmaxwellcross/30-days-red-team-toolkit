"""
Unix Platform Handler
Handles Unix/Linux-specific timestamp operations
"""

import os
from datetime import datetime

from .handler import BasePlatformHandler


class UnixHandler(BasePlatformHandler):
    """
    Unix/Linux-specific timestamp handler
    
    Note: On Unix systems, st_ctime is metadata change time, not creation time.
    True creation time (birth time) is only available on some filesystems.
    """
    
    def get_file_times(self, filepath):
        """
        Get file timestamps on Unix/Linux
        
        Args:
            filepath (str): Path to file
            
        Returns:
            dict: Dictionary with 'accessed', 'modified', 'created' timestamps
            
        Note:
            'created' is actually metadata change time (ctime) on most Unix systems
        """
        try:
            stat = os.stat(filepath)
            
            times = {
                'accessed': datetime.fromtimestamp(stat.st_atime),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'created': datetime.fromtimestamp(stat.st_ctime)  # Actually change time
            }
            
            # Try to get birth time if available (requires Python 3.3+, macOS/BSD/some Linux)
            if hasattr(stat, 'st_birthtime'):
                times['created'] = datetime.fromtimestamp(stat.st_birthtime)
            
            return times
        
        except FileNotFoundError:
            print(f"[-] File not found: {filepath}")
            return None
        except PermissionError:
            print(f"[-] Permission denied: {filepath}")
            return None
        except Exception as e:
            print(f"[-] Error getting file times: {e}")
            return None
    
    def set_file_times(self, filepath, accessed=None, modified=None, created=None):
        """
        Set file timestamps on Unix/Linux
        
        Args:
            filepath (str): Path to file
            accessed (datetime, optional): Access time to set
            modified (datetime, optional): Modification time to set
            created (datetime, optional): Creation time to set (limited support)
            
        Returns:
            bool: True if successful, False otherwise
            
        Note:
            Creation time cannot be easily modified on most Unix systems.
            Only access and modification times can be reliably set.
        """
        try:
            # Set access and modified times
            if accessed and modified:
                atime = accessed.timestamp()
                mtime = modified.timestamp()
                
                os.utime(filepath, (atime, mtime))
                
                print(f"[+] Set access time: {accessed}")
                print(f"[+] Set modified time: {modified}")
            
            # Creation time modification on Unix is limited
            if created:
                print(f"[!] Warning: Creation time cannot be directly modified on Unix/Linux")
                print(f"[!] Setting modification time instead")
                
                # Set modification time to the "creation" time as a workaround
                if not accessed:
                    os.utime(filepath, (created.timestamp(), created.timestamp()))
            
            return True
        
        except PermissionError:
            print(f"[-] Permission denied: {filepath}")
            return False
        except Exception as e:
            print(f"[-] Error setting file times: {e}")
            return False
    
    def set_times_advanced(self, filepath, accessed=None, modified=None):
        """
        Advanced timestamp setting with nanosecond precision
        
        Args:
            filepath (str): Path to file
            accessed (datetime, optional): Access time
            modified (datetime, optional): Modification time
            
        Returns:
            bool: True if successful
        """
        try:
            if accessed and modified:
                # Use os.utime with nanosecond precision
                atime_ns = int(accessed.timestamp() * 1e9)
                mtime_ns = int(modified.timestamp() * 1e9)
                
                os.utime(filepath, ns=(atime_ns, mtime_ns))
                
                print(f"[+] Set times with nanosecond precision")
                return True
            
            return False
        
        except Exception as e:
            print(f"[-] Advanced timestamp setting failed: {e}")
            return False
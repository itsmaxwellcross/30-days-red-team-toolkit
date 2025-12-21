"""
Windows Platform Handler
Handles Windows-specific timestamp operations using win32file
"""

import os
from datetime import datetime

from .handler import BasePlatformHandler


class WindowsHandler(BasePlatformHandler):
    """
    Windows-specific timestamp handler
    
    Uses win32file API for full timestamp control including creation time
    """
    
    def __init__(self):
        """Initialize Windows handler"""
        self.has_win32 = False
        
        try:
            import win32file
            import win32con
            import pywintypes
            self.has_win32 = True
            self.win32file = win32file
            self.win32con = win32con
            self.pywintypes = pywintypes
        except ImportError:
            print("[!] Warning: pywin32 not available")
            print("[!] Creation time modification not supported")
            print("[!] Install with: pip install pywin32")
    
    def get_file_times(self, filepath):
        """
        Get file timestamps on Windows
        
        Args:
            filepath (str): Path to file
            
        Returns:
            dict: Dictionary with 'accessed', 'modified', 'created' timestamps
        """
        try:
            stat = os.stat(filepath)
            
            times = {
                'accessed': datetime.fromtimestamp(stat.st_atime),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'created': datetime.fromtimestamp(stat.st_ctime)
            }
            
            # Try to get more accurate creation time using win32file
            if self.has_win32:
                try:
                    handle = self.win32file.CreateFile(
                        filepath,
                        self.win32con.GENERIC_READ,
                        self.win32con.FILE_SHARE_READ | self.win32con.FILE_SHARE_WRITE,
                        None,
                        self.win32con.OPEN_EXISTING,
                        self.win32con.FILE_ATTRIBUTE_NORMAL,
                        None
                    )
                    
                    creation_time, access_time, write_time = self.win32file.GetFileTime(handle)
                    self.win32file.CloseHandle(handle)
                    
                    times['created'] = datetime.fromtimestamp(creation_time.timestamp())
                except Exception:
                    pass  # Fall back to stat values
            
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
        Set file timestamps on Windows
        
        Args:
            filepath (str): Path to file
            accessed (datetime, optional): Access time to set
            modified (datetime, optional): Modification time to set
            created (datetime, optional): Creation time to set
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Set access and modified times using os.utime (works on all platforms)
            if accessed and modified:
                atime = accessed.timestamp()
                mtime = modified.timestamp()
                
                os.utime(filepath, (atime, mtime))
                
                print(f"[+] Set access time: {accessed}")
                print(f"[+] Set modified time: {modified}")
            
            # Set creation time using win32file (Windows-specific)
            if created:
                if not self.has_win32:
                    print(f"[-] Cannot set creation time: pywin32 not available")
                    return False
                
                try:
                    handle = self.win32file.CreateFile(
                        filepath,
                        self.win32con.GENERIC_WRITE,
                        self.win32con.FILE_SHARE_READ | self.win32con.FILE_SHARE_WRITE,
                        None,
                        self.win32con.OPEN_EXISTING,
                        self.win32con.FILE_ATTRIBUTE_NORMAL,
                        None
                    )
                    
                    # Convert to pywintypes.TimeType
                    creation_time = self.pywintypes.Time(int(created.timestamp()))
                    
                    self.win32file.SetFileTime(handle, creation_time, None, None)
                    self.win32file.CloseHandle(handle)
                    
                    print(f"[+] Set creation time: {created}")
                
                except Exception as e:
                    print(f"[-] Error setting creation time: {e}")
                    return False
            
            return True
        
        except PermissionError:
            print(f"[-] Permission denied: {filepath}")
            return False
        except Exception as e:
            print(f"[-] Error setting file times: {e}")
            return False
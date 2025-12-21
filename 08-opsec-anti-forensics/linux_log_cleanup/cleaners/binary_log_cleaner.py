"""
Binary Log Cleaner
Handles cleaning of binary log files (wtmp, utmp, lastlog, btmp)
"""

from ..core.constants import RECORD_SIZES, USERNAME_OFFSET, USERNAME_SIZE


class BinaryLogCleaner:
    """
    Clean binary log files
    
    Provides functionality to clean:
    - wtmp (login records)
    - utmp (current logins)
    - lastlog (last login times)
    - btmp (failed login attempts)
    """
    
    def __init__(self):
        """Initialize binary log cleaner"""
        self.record_sizes = RECORD_SIZES.copy()
    
    def clean_wtmp(self, log_path, username=None):
        """
        Clean wtmp (login records)
        
        Args:
            log_path (str): Path to wtmp file
            username (str, optional): Username to remove
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self._clean_utmp_style_log(log_path, username, 'wtmp')
    
    def clean_utmp(self, log_path, username=None):
        """
        Clean utmp (current login records)
        
        Args:
            log_path (str): Path to utmp file
            username (str, optional): Username to remove
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self._clean_utmp_style_log(log_path, username, 'utmp')
    
    def clean_btmp(self, log_path, username=None):
        """
        Clean btmp (failed login attempts)
        
        Args:
            log_path (str): Path to btmp file
            username (str, optional): Username to remove
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self._clean_utmp_style_log(log_path, username, 'btmp')
    
    def _clean_utmp_style_log(self, log_path, username, log_type):
        """
        Internal method to clean utmp-style binary logs
        
        Args:
            log_path (str): Path to log file
            username (str): Username to remove
            log_type (str): Type of log (for record size)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read log file
            with open(log_path, 'rb') as f:
                data = f.read()
            
            # Get record size
            record_size = self.record_sizes.get(log_type, 384)
            num_records = len(data) // record_size
            
            print(f"[*] Found {num_records} {log_type} records")
            
            cleaned_data = bytearray()
            removed_count = 0
            
            # Process each record
            for i in range(num_records):
                offset = i * record_size
                record = data[offset:offset + record_size]
                
                # Extract username from record
                record_username = self._extract_username(record)
                
                if username and username == record_username:
                    removed_count += 1
                else:
                    cleaned_data.extend(record)
            
            # Write cleaned log
            with open(log_path, 'wb') as f:
                f.write(cleaned_data)
            
            print(f"[+] Removed {removed_count} entries from {log_type}")
            return True
        
        except PermissionError:
            print(f"[-] Permission denied: {log_path}")
            return False
        except FileNotFoundError:
            print(f"[-] File not found: {log_path}")
            return False
        except Exception as e:
            print(f"[-] {log_type} cleaning failed: {e}")
            return False
    
    def _extract_username(self, record):
        """
        Extract username from utmp-style record
        
        Args:
            record (bytes): Binary record data
            
        Returns:
            str: Username extracted from record
        """
        try:
            # Username is at offset 32, size 32 bytes
            username_bytes = record[USERNAME_OFFSET:USERNAME_OFFSET + USERNAME_SIZE]
            # Split at null byte and decode
            username = username_bytes.split(b'\x00')[0].decode('utf-8', errors='ignore')
            return username
        except Exception:
            return ""
    
    def clean_lastlog(self, log_path, username=None):
        """
        Clean lastlog (last login times)
        
        lastlog is a sparse file with fixed-size records indexed by UID
        
        Args:
            log_path (str): Path to lastlog file
            username (str, optional): Username to clear from lastlog
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not username:
                print(f"[-] Username required for lastlog cleaning")
                return False
            
            # Get UID for username
            import pwd
            try:
                uid = pwd.getpwnam(username).pw_uid
            except KeyError:
                print(f"[-] User not found: {username}")
                return False
            
            # lastlog record size
            record_size = self.record_sizes['lastlog']
            offset = uid * record_size
            
            # Clear record for this UID
            with open(log_path, 'r+b') as f:
                f.seek(offset)
                f.write(b'\x00' * record_size)
            
            print(f"[+] Cleared lastlog entry for {username} (UID {uid})")
            return True
        
        except PermissionError:
            print(f"[-] Permission denied: {log_path}")
            return False
        except FileNotFoundError:
            print(f"[-] File not found: {log_path}")
            return False
        except Exception as e:
            print(f"[-] lastlog cleaning failed: {e}")
            return False
    
    def get_record_count(self, log_path, log_type):
        """
        Get number of records in a binary log file
        
        Args:
            log_path (str): Path to log file
            log_type (str): Type of log (wtmp, utmp, etc.)
            
        Returns:
            int: Number of records, or -1 on error
        """
        try:
            import os
            file_size = os.path.getsize(log_path)
            record_size = self.record_sizes.get(log_type, 384)
            
            record_count = file_size // record_size
            return record_count
        
        except Exception as e:
            print(f"[-] Failed to get record count: {e}")
            return -1
    
    def dump_records(self, log_path, log_type, max_records=10):
        """
        Dump records from binary log for inspection
        
        Args:
            log_path (str): Path to log file
            log_type (str): Type of log
            max_records (int): Maximum number of records to dump
            
        Returns:
            list: List of extracted usernames
        """
        try:
            with open(log_path, 'rb') as f:
                data = f.read()
            
            record_size = self.record_sizes.get(log_type, 384)
            num_records = min(len(data) // record_size, max_records)
            
            usernames = []
            
            for i in range(num_records):
                offset = i * record_size
                record = data[offset:offset + record_size]
                username = self._extract_username(record)
                if username:
                    usernames.append(username)
            
            return usernames
        
        except Exception as e:
            print(f"[-] Failed to dump records: {e}")
            return []
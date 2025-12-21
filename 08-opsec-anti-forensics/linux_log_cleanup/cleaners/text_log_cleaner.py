"""
Text Log Cleaner
Handles cleaning of text-based logs (auth.log, syslog, audit.log, etc.)
"""


class TextLogCleaner:
    """
    Clean text-based log files
    
    Provides functionality to:
    - Filter logs by username
    - Filter logs by IP address
    - Filter logs by keywords
    - Remove specific patterns
    """
    
    def __init__(self):
        """Initialize text log cleaner"""
        pass
    
    def clean_log_file(self, log_path, filters, case_sensitive=False):
        """
        Clean a text log file by removing lines matching filters
        
        Args:
            log_path (str): Path to log file to clean
            filters (list): List of strings to filter out
            case_sensitive (bool): Whether filtering is case-sensitive
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read log
            with open(log_path, 'r', errors='ignore') as f:
                lines = f.readlines()
            
            # Filter out lines containing any of the filter strings
            cleaned_lines = []
            removed_count = 0
            
            for line in lines:
                should_remove = False
                
                for filter_str in filters:
                    if case_sensitive:
                        if filter_str in line:
                            should_remove = True
                            break
                    else:
                        if filter_str.lower() in line.lower():
                            should_remove = True
                            break
                
                if should_remove:
                    removed_count += 1
                else:
                    cleaned_lines.append(line)
            
            # Write cleaned log
            with open(log_path, 'w') as f:
                f.writelines(cleaned_lines)
            
            print(f"[+] Removed {removed_count} entries from {log_path}")
            return True
        
        except PermissionError:
            print(f"[-] Permission denied: {log_path}")
            return False
        except FileNotFoundError:
            print(f"[-] File not found: {log_path}")
            return False
        except Exception as e:
            print(f"[-] Log cleaning failed: {e}")
            return False
    
    def clean_by_pattern(self, log_path, patterns):
        """
        Clean log file using regex patterns
        
        Args:
            log_path (str): Path to log file
            patterns (list): List of regex patterns to remove
            
        Returns:
            bool: True if successful, False otherwise
        """
        import re
        
        try:
            with open(log_path, 'r', errors='ignore') as f:
                lines = f.readlines()
            
            cleaned_lines = []
            removed_count = 0
            
            for line in lines:
                should_remove = False
                
                for pattern in patterns:
                    if re.search(pattern, line):
                        should_remove = True
                        break
                
                if should_remove:
                    removed_count += 1
                else:
                    cleaned_lines.append(line)
            
            with open(log_path, 'w') as f:
                f.writelines(cleaned_lines)
            
            print(f"[+] Removed {removed_count} entries matching patterns")
            return True
        
        except Exception as e:
            print(f"[-] Pattern-based cleaning failed: {e}")
            return False
    
    def clean_by_timerange(self, log_path, start_time=None, end_time=None):
        """
        Clean log entries within a specific time range
        
        Args:
            log_path (str): Path to log file
            start_time (datetime, optional): Start of time range
            end_time (datetime, optional): End of time range
            
        Returns:
            bool: True if successful, False otherwise
            
        Note:
            This is a simplified implementation. Real implementation would
            need to parse log timestamps which vary by log type.
        """
        print(f"[*] Time-based filtering not fully implemented")
        print(f"[*] This would require parsing log-specific timestamp formats")
        return False
    
    def get_log_stats(self, log_path):
        """
        Get statistics about a log file
        
        Args:
            log_path (str): Path to log file
            
        Returns:
            dict: Statistics including line count, size, etc.
        """
        try:
            import os
            
            with open(log_path, 'r', errors='ignore') as f:
                lines = f.readlines()
            
            stats = {
                'line_count': len(lines),
                'file_size': os.path.getsize(log_path),
                'path': log_path
            }
            
            return stats
        
        except Exception as e:
            print(f"[-] Failed to get stats: {e}")
            return None
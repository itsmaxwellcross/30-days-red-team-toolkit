"""
System information enumeration
"""

import os
import platform
import socket
from ..core.utils import run_command


class SystemEnumerator:
    """Enumerate system information"""
    
    def __init__(self, os_type: str):
        self.os_type = os_type
    
    def enumerate(self) -> dict:
        """Run system enumeration"""
        print("\n[*] Enumerating system information...")
        
        info = {
            'hostname': socket.gethostname(),
            'os': platform.system(),
            'os_version': platform.version(),
            'architecture': platform.machine(),
            'python_version': platform.python_version()
        }
        
        if self.os_type == 'linux':
            info.update(self._enumerate_linux())
        elif self.os_type == 'windows':
            info.update(self._enumerate_windows())
        
        self._print_results(info)
        return info
    
    def _enumerate_linux(self) -> dict:
        """Linux-specific system enumeration"""
        info = {}
        info['kernel'] = run_command('uname -r').strip()
        info['distribution'] = run_command('cat /etc/os-release').strip()
        
        # Check for container
        if os.path.exists('/.dockerenv'):
            info['container'] = 'docker'
        elif os.path.exists('/run/systemd/container'):
            info['container'] = run_command('cat /run/systemd/container').strip()
        
        return info
    
    def _enumerate_windows(self) -> dict:
        """Windows-specific system enumeration"""
        info = {}
        info['windows_version'] = run_command('ver').strip()
        info['hotfixes'] = run_command('wmic qfe get HotFixID,InstalledOn').strip()
        return info
    
    def _print_results(self, info: dict):
        """Print enumeration results"""
        for key, value in info.items():
            if key != 'hotfixes':  # Skip long output
                print(f"  {key}: {value}")
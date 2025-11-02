"""
Base class for Situational Awareness Suite
"""

import datetime
import socket
import platform
from typing import Dict, Any
from ..modules import (
    SystemEnumerator,
    UserEnumerator,
    NetworkEnumerator,
    ProcessEnumerator,
    FileEnumerator,
    SecurityEnumerator,
    TaskEnumerator
)
from ..output.formatters import OutputFormatter


class SituationalAwareness:
    """Main orchestrator for enumeration modules"""
    
    def __init__(self, output_format='json'):
        self.output_format = output_format
        self.os_type = platform.system().lower()
        self.results = {
            'timestamp': datetime.datetime.now().isoformat(),
            'hostname': socket.gethostname(),
            'os_type': self.os_type,
            'system_info': {},
            'user_info': {},
            'network_info': {},
            'processes': {},
            'files': {},
            'security_products': {},
            'scheduled_tasks': {},
            'writable_directories': []
        }
        
        # Initialize modules
        self.system = SystemEnumerator(self.os_type)
        self.user = UserEnumerator(self.os_type)
        self.network = NetworkEnumerator(self.os_type)
        self.processes = ProcessEnumerator(self.os_type)
        self.files = FileEnumerator(self.os_type)
        self.security = SecurityEnumerator(self.os_type)
        self.tasks = TaskEnumerator(self.os_type)
        
        # Output formatter
        self.formatter = OutputFormatter(output_format)
    
    def run_quick_enumeration(self):
        """Run essential enumeration only"""
        print("="*60)
        print("SITUATIONAL AWARENESS - QUICK ENUMERATION")
        print("="*60)
        self._print_header()
        
        self.results['system_info'] = self.system.enumerate()
        self.results['user_info'] = self.user.enumerate()
        self.results['network_info'] = self.network.enumerate()
        
        self._save_results()
    
    def run_full_enumeration(self):
        """Run comprehensive enumeration"""
        print("="*60)
        print("SITUATIONAL AWARENESS - FULL ENUMERATION")
        print("="*60)
        self._print_header()
        
        # Run all modules
        self.results['system_info'] = self.system.enumerate()
        self.results['user_info'] = self.user.enumerate()
        self.results['network_info'] = self.network.enumerate()
        self.results['processes'] = self.processes.enumerate()
        self.results['files'] = self.files.enumerate()
        self.results['security_products'] = self.security.enumerate()
        self.results['scheduled_tasks'] = self.tasks.enumerate()
        self.results['writable_directories'] = self.files.check_writable()
        
        print("\n" + "="*60)
        print("ENUMERATION COMPLETE")
        print("="*60)
        
        self._save_results()
    
    def _print_header(self):
        """Print enumeration header"""
        print(f"Target: {self.results['hostname']}")
        print(f"OS: {self.results['os_type']}")
        print(f"Timestamp: {self.results['timestamp']}")
        print("="*60)
    
    def _save_results(self):
        """Save results using formatter"""
        self.formatter.save(self.results)
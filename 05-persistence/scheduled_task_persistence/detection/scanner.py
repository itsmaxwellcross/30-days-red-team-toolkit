"""
Detection and scanning for scheduled task persistence
"""

import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import run_command, parse_task_list_output
from config import SUSPICIOUS_INDICATORS, LEGITIMATE_TASK_PATTERNS


class TaskScanner:
    """Scans for existing and suspicious scheduled tasks"""
    
    def __init__(self):
        self.findings = []
    
    def list_all_tasks(self):
        """
        List all scheduled tasks
        
        Returns:
            list: All tasks
        """
        print("[*] Listing all scheduled tasks...")
        
        command = 'schtasks /Query /FO LIST /V'
        result = run_command(command)
        
        if result['success']:
            tasks = parse_task_list_output(result['stdout'])
            print(f"[+] Found {len(tasks)} scheduled tasks")
            return tasks
        else:
            print("[-] Failed to query scheduled tasks")
            return []
    
    def scan_suspicious(self):
        """
        Scan for suspicious scheduled tasks
        
        Returns:
            list: Suspicious tasks found
        """
        print("\n" + "="*60)
        print("SCANNING FOR SUSPICIOUS SCHEDULED TASKS")
        print("="*60 + "\n")
        
        command = 'schtasks /Query /FO CSV /V'
        result = run_command(command)
        
        if not result['success']:
            print("[-] Failed to query tasks")
            return []
        
        suspicious_tasks = []
        lines = result['stdout'].split('\n')[1:]  # Skip header
        
        for line in lines:
            if not line.strip():
                continue
            
            # Check if it's a legitimate Windows task
            is_legitimate = any(
                re.search(pattern, line, re.IGNORECASE)
                for pattern in LEGITIMATE_TASK_PATTERNS
            )
            
            if is_legitimate:
                continue
            
            # Check for suspicious indicators
            suspicious_indicators_found = []
            for indicator in SUSPICIOUS_INDICATORS:
                if indicator.lower() in line.lower():
                    suspicious_indicators_found.append(indicator)
            
            if suspicious_indicators_found:
                suspicious_tasks.append({
                    'task_info': line,
                    'indicators': suspicious_indicators_found
                })
        
        # Display findings
        if suspicious_tasks:
            print(f"[!] Found {len(suspicious_tasks)} suspicious task(s):\n")
            
            for i, task in enumerate(suspicious_tasks, 1):
                print(f"Task #{i}:")
                print(f"  Info: {task['task_info'][:200]}...")
                print(f"  Suspicious Indicators: {', '.join(task['indicators'])}")
                print()
        else:
            print("[*] No obviously suspicious tasks found")
        
        self.findings = suspicious_tasks
        return suspicious_tasks
    
    def check_hidden_tasks(self):
        """
        Find hidden scheduled tasks
        
        Returns:
            list: Hidden tasks
        """
        print("[*] Checking for hidden scheduled tasks...")
        
        command = 'schtasks /Query /FO CSV /V'
        result = run_command(command)
        
        if not result['success']:
            print("[-] Failed to query tasks")
            return []
        
        hidden_tasks = []
        
        for line in result['stdout'].split('\n')[1:]:
            if not line.strip():
                continue
            
            # CSV format: TaskName,NextRunTime,Status,LogonMode,...,Hidden,...
            # Hidden field is typically near the end
            if '"true"' in line.lower() or '"yes"' in line.lower():
                # Check if this is the Hidden field
                parts = line.split('","')
                task_name = parts[0].strip('"') if parts else "Unknown"
                
                # Filter out legitimate hidden tasks
                is_legitimate = any(
                    re.search(pattern, task_name, re.IGNORECASE)
                    for pattern in LEGITIMATE_TASK_PATTERNS
                )
                
                if not is_legitimate:
                    hidden_tasks.append(task_name)
        
        if hidden_tasks:
            print(f"[+] Found {len(hidden_tasks)} hidden task(s):")
            for task in hidden_tasks:
                print(f"    {task}")
        else:
            print("[*] No suspicious hidden tasks found")
        
        return hidden_tasks
    
    def check_system_tasks(self):
        """
        Find tasks running as SYSTEM
        
        Returns:
            list: SYSTEM tasks
        """
        print("[*] Checking for tasks running as SYSTEM...")
        
        command = 'schtasks /Query /FO CSV /V'
        result = run_command(command)
        
        if not result['success']:
            return []
        
        system_tasks = []
        
        for line in result['stdout'].split('\n')[1:]:
            if not line.strip():
                continue
            
            if 'SYSTEM' in line.upper():
                parts = line.split('","')
                task_name = parts[0].strip('"') if parts else "Unknown"
                
                # Filter legitimate tasks
                is_legitimate = any(
                    re.search(pattern, task_name, re.IGNORECASE)
                    for pattern in LEGITIMATE_TASK_PATTERNS
                )
                
                if not is_legitimate:
                    system_tasks.append(task_name)
        
        if system_tasks:
            print(f"[+] Found {len(system_tasks)} non-standard SYSTEM task(s):")
            for task in system_tasks[:10]:  # Show first 10
                print(f"    {task}")
        else:
            print("[*] No suspicious SYSTEM tasks found")
        
        return system_tasks
    
    def get_task_details(self, task_name):
        """
        Get detailed information about a specific task
        
        Args:
            task_name (str): Name of task
            
        Returns:
            dict: Task details
        """
        print(f"[*] Getting details for task: {task_name}")
        
        command = f'schtasks /Query /TN "{task_name}" /V /FO LIST'
        result = run_command(command)
        
        if result['success']:
            print(result['stdout'])
            return parse_task_list_output(result['stdout'])
        else:
            print(f"[-] Task not found or access denied")
            return None
    
    def export_task_xml(self, task_name, output_file):
        """
        Export task definition to XML for analysis
        
        Args:
            task_name (str): Task name
            output_file (str): Output XML file path
            
        Returns:
            bool: Success status
        """
        print(f"[*] Exporting task to XML: {output_file}")
        
        command = f'schtasks /Query /TN "{task_name}" /XML > "{output_file}"'
        result = run_command(command)
        
        if result['success']:
            print(f"[+] Task exported to: {output_file}")
            return True
        else:
            print("[-] Failed to export task")
            return False
    
    def scan_all(self):
        """
        Run all scans and compile report
        
        Returns:
            dict: Complete scan results
        """
        print("\n" + "="*60)
        print("COMPREHENSIVE SCHEDULED TASK SCAN")
        print("="*60 + "\n")
        
        results = {
            'suspicious': self.scan_suspicious(),
            'hidden': self.check_hidden_tasks(),
            'system': self.check_system_tasks()
        }
        
        # Summary
        total_issues = (
            len(results['suspicious']) +
            len(results['hidden']) +
            len(results['system'])
        )
        
        print("\n" + "="*60)
        print(f"SCAN COMPLETE")
        print("="*60)
        print(f"Suspicious tasks: {len(results['suspicious'])}")
        print(f"Hidden tasks: {len(results['hidden'])}")
        print(f"SYSTEM tasks: {len(results['system'])}")
        print(f"Total issues: {total_issues}")
        print("="*60 + "\n")
        
        return results
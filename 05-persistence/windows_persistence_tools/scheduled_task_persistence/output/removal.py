"""
Generate removal scripts for installed tasks
"""

from datetime import datetime
from config import DEFAULT_STAGING_DIR
import os


class RemovalScriptGenerator:
    """Generates removal scripts for cleanup"""
    
    def __init__(self, output_dir=DEFAULT_STAGING_DIR):
        self.output_dir = output_dir
    
    def generate(self, installed_tasks):
        """Generate batch script to remove all tasks"""
        if not installed_tasks:
            print("[!] No tasks to remove")
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        script_name = f"remove_tasks_{timestamp}.bat"
        script_path = os.path.join(self.output_dir, script_name)
        
        script_content = f'''@echo off
REM Scheduled Task Removal Script
REM Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
REM Tasks: {len(installed_tasks)}

echo.
echo Removing {len(installed_tasks)} scheduled task(s)...
echo.

'''
        
        for i, task in enumerate(installed_tasks, 1):
            task_name = task.get('task_name', 'unknown')
            script_content += f'''
REM Task {i}: {task_name}
schtasks /Delete /TN "{task_name}" /F
if %ERRORLEVEL% EQU 0 (
    echo [+] Removed: {task_name}
) else (
    echo [-] Failed: {task_name}
)

'''
        
        script_content += '''
echo.
echo Removal complete.
pause
'''
        
        try:
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            print(f"[+] Removal script created: {script_path}")
            return script_path
        except Exception as e:
            print(f"[-] Error creating removal script: {e}")
            return None
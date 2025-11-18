"""
Command execution utilities
"""

import subprocess
from pathlib import Path


class CommandExecutor:
    """Handles execution of system commands and scripts"""
    
    def __init__(self, logger, base_dir=None):
        self.logger = logger
        self.base_dir = base_dir or Path(__file__).parent.parent
    
    def run_command(self, command, timeout=300):
        """Execute command and capture output"""
        self.logger.debug(f"Executing: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.base_dir
            )
            
            if result.returncode == 0:
                self.logger.success(f"Command succeeded: {command}")
                return {
                    'success': True,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'returncode': result.returncode
                }
            else:
                self.logger.error(f"Command failed: {command}")
                return {
                    'success': False,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'returncode': result.returncode
                }
        
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timed out: {command}")
            return {'success': False, 'error': 'timeout'}
        
        except Exception as e:
            self.logger.error(f"Command error: {e}")
            return {'success': False, 'error': str(e)}
    
    def run_python_script(self, script_path, args='', timeout=300):
        """Execute a Python script with arguments"""
        command = f"python3 {script_path} {args}".strip()
        return self.run_command(command, timeout)
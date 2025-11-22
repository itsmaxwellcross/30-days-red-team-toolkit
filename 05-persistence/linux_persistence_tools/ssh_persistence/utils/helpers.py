import subprocess
import os

def run_command(command: str, shell: bool = True, timeout: int = 30) -> dict:
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True, timeout=timeout)
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout.strip(),
            'stderr': result.stderr.strip()
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}
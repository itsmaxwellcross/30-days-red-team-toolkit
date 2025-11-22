import subprocess
import os
import random
import string

def run_command(command: str, shell: bool = True, timeout: int = 30) -> dict:
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True, timeout=timeout)
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def generate_service_name() -> str:
    prefixes = ['system', 'network', 'update', 'monitor', 'service', 'log', 'security']
    suffixes = ['manager', 'daemon', 'handler', 'agent', 'watcher', 'd', 'helper']
    return f"{random.choice(prefixes)}-{random.choice(suffixes)}"
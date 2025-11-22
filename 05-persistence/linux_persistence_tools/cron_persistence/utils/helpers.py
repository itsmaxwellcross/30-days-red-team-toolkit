import subprocess
import os
import pwd
import random
import string
from typing import Dict, Any

def get_current_user() -> str:
    return pwd.getpwuid(os.getuid()).pw_name

def run_command(command: str, shell: bool = True, timeout: int = 30) -> Dict[str, Any]:
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def generate_random_name(length: int = 10) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))
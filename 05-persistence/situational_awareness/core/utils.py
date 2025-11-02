"""
Utility functions shared across modules
"""

import subprocess
from typing import Optional


def run_command(command: str, shell: bool = True, timeout: int = 30) -> str:
    """
    Execute system command and return output
    
    Args:
        command: Command to execute
        shell: Whether to use shell execution
        timeout: Command timeout in seconds
    
    Returns:
        Command output as string, or error message
    """
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Error: Command timed out"
    except Exception as e:
        return f"Error: {str(e)}"


def safe_read_file(filepath: str) -> Optional[str]:
    """
    Safely read file contents
    
    Args:
        filepath: Path to file
    
    Returns:
        File contents or None if error
    """
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except:
        return None
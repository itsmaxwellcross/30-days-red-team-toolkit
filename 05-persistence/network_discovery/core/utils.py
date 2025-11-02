"""
Utility functions for network operations
"""

import subprocess
import socket
from typing import Optional


def run_command(command: list, timeout: int = 30) -> Optional[str]:
    """
    Execute system command and return output
    
    Args:
        command: Command as list of arguments
        timeout: Command timeout in seconds
    
    Returns:
        Command output or None if error
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        return None


def is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """
    Check if a port is open on target host
    
    Args:
        host: Target IP address
        port: Target port
        timeout: Connection timeout
    
    Returns:
        True if port is open, False otherwise
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False


def get_platform() -> str:
    """
    Get current platform
    
    Returns:
        'linux', 'windows', or 'darwin'
    """
    import platform
    return platform.system().lower()
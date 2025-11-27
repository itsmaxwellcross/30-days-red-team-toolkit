import os
import sys
import socket
import platform

def get_system_info(session_id=None):
    info = {
        'hostname': socket.gethostname(),
        'username': os.getenv('USER') or os.getenv('USERNAME') or 'unknown',
        'os_type': platform.system(),
        'os_version': platform.version(),
        'architecture': platform.machine(),
        'python_version': sys.version.split()[0],
        'processor': platform.processor() or 'unknown'
    }

    # Privilege check
    if platform.system() == 'Windows':
        try:
            import ctypes
            info['is_admin'] = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            info['is_admin'] = False
    else:
        info['is_admin'] = os.geteuid() == 0

    if session_id:
        info['session_id'] = session_id

    return info
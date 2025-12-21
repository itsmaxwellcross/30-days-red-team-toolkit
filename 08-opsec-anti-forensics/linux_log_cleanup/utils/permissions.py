"""
Log file permissions management
"""

import os
import stat


def get_permissions(filepath):
    """
    Get current permissions of a file
    
    Args:
        filepath (str): Path to file
        
    Returns:
        dict: Permission information
    """
    try:
        st = os.stat(filepath)
        
        perms = {
            'mode': st.st_mode,
            'octal': oct(st.st_mode)[-3:],
            'uid': st.st_uid,
            'gid': st.st_gid
        }
        
        return perms
    
    except Exception as e:
        print(f"[-] Failed to get permissions: {e}")
        return None


def set_log_permissions(filepath, mode=0o640, uid=None, gid=None):
    """
    Set permissions on a log file
    
    Args:
        filepath (str): Path to log file
        mode (int): Permission mode (default: 0o640 = rw-r-----)
        uid (int, optional): User ID to set
        gid (int, optional): Group ID to set
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Set file mode
        os.chmod(filepath, mode)
        print(f"[+] Set permissions {oct(mode)[-3:]} on {filepath}")
        
        # Set ownership if specified
        if uid is not None or gid is not None:
            current_uid = os.stat(filepath).st_uid if uid is None else uid
            current_gid = os.stat(filepath).st_gid if gid is None else gid
            
            os.chown(filepath, current_uid, current_gid)
            print(f"[+] Set ownership {current_uid}:{current_gid} on {filepath}")
        
        return True
    
    except PermissionError:
        print(f"[-] Permission denied setting permissions on: {filepath}")
        return False
    except Exception as e:
        print(f"[-] Failed to set permissions: {e}")
        return False


def restore_permissions(filepath, saved_perms):
    """
    Restore previously saved permissions
    
    Args:
        filepath (str): Path to file
        saved_perms (dict): Permissions from get_permissions()
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not saved_perms:
            print(f"[-] No permissions to restore")
            return False
        
        # Restore mode
        os.chmod(filepath, saved_perms['mode'])
        
        # Restore ownership
        os.chown(filepath, saved_perms['uid'], saved_perms['gid'])
        
        print(f"[+] Restored permissions on {filepath}")
        return True
    
    except Exception as e:
        print(f"[-] Failed to restore permissions: {e}")
        return False


def make_readable_by_owner_only(filepath):
    """
    Make log file readable/writable by owner only
    
    Args:
        filepath (str): Path to file
        
    Returns:
        bool: True if successful, False otherwise
    """
    return set_log_permissions(filepath, mode=0o600)


def make_readable_by_group(filepath):
    """
    Make log file readable/writable by owner, readable by group
    
    Args:
        filepath (str): Path to file
        
    Returns:
        bool: True if successful, False otherwise
    """
    return set_log_permissions(filepath, mode=0o640)


def is_world_readable(filepath):
    """
    Check if file is world-readable
    
    Args:
        filepath (str): Path to file
        
    Returns:
        bool: True if world-readable, False otherwise
    """
    try:
        st = os.stat(filepath)
        return bool(st.st_mode & stat.S_IROTH)
    except:
        return False


def is_world_writable(filepath):
    """
    Check if file is world-writable
    
    Args:
        filepath (str): Path to file
        
    Returns:
        bool: True if world-writable, False otherwise
    """
    try:
        st = os.stat(filepath)
        return bool(st.st_mode & stat.S_IWOTH)
    except:
        return False
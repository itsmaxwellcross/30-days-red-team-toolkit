"""
User and privilege enumeration
"""

import os
import pwd
import grp
from ..core.utils import run_command


class UserEnumerator:
    """Enumerate user information and privileges"""
    
    def __init__(self, os_type: str):
        self.os_type = os_type
    
    def enumerate(self) -> dict:
        """Run user enumeration"""
        print("\n[*] Enumerating current user...")
        
        if self.os_type == 'linux':
            user_info = self._enumerate_linux_user()
        elif self.os_type == 'windows':
            user_info = self._enumerate_windows_user()
        else:
            user_info = {}
        
        self._print_results(user_info)
        return user_info
    
    def _enumerate_linux_user(self) -> dict:
        """Linux user enumeration"""
        user_info = {
            'username': os.getenv('USER') or os.getenv('USERNAME'),
            'uid': os.getuid(),
            'gid': os.getgid(),
            'home': os.getenv('HOME'),
            'shell': os.getenv('SHELL')
        }
        
        # Get group memberships
        try:
            groups = [g.gr_name for g in grp.getgrall() 
                     if user_info['username'] in g.gr_mem]
            primary_gid = pwd.getpwuid(os.getuid()).pw_gid
            groups.append(grp.getgrgid(primary_gid).gr_name)
            user_info['groups'] = list(set(groups))
        except:
            user_info['groups'] = []
        
        # Check sudo rights
        sudo_check = run_command('sudo -l 2>/dev/null')
        user_info['can_sudo'] = 'may run' in sudo_check.lower()
        if user_info['can_sudo']:
            user_info['sudo_rights'] = sudo_check
        
        return user_info
    
    def _enumerate_windows_user(self) -> dict:
        """Windows user enumeration"""
        user_info = {
            'username': os.getenv('USERNAME'),
            'domain': os.getenv('USERDOMAIN'),
            'profile': os.getenv('USERPROFILE')
        }
        
        # Check privileges
        user_info['privileges'] = run_command('whoami /priv')
        
        # Check if admin
        is_admin = run_command('net session 2>&1')
        user_info['is_admin'] = 'Access is denied' not in is_admin
        
        return user_info
    
    def _print_results(self, user_info: dict):
        """Print user information"""
        print(f"  Username: {user_info.get('username')}")
        print(f"  Groups: {user_info.get('groups', 'N/A')}")
        admin_status = user_info.get('can_sudo') or user_info.get('is_admin')
        print(f"  Sudo/Admin: {admin_status}")

"""
Active Directory domain enumeration
"""

import subprocess
import re
from ..core.utils import get_platform, run_command


class DomainEnumerator:
    """Enumerate Active Directory information"""
    
    def enumerate_domain(self) -> dict:
        """Run all domain enumeration"""
        domain_info = {}
        
        # Check domain membership
        domain_info.update(self.check_domain_membership())
        
        # If domain-joined, enumerate details
        if domain_info.get('is_domain_joined'):
            domain_info.update(self.enumerate_domain_users())
            domain_info.update(self.enumerate_domain_computers())
            domain_info.update(self.find_domain_admins())
        
        return domain_info
    
    def check_domain_membership(self) -> dict:
        """Check if system is domain-joined"""
        print("\n[*] Checking domain membership...")
        
        platform = get_platform()
        
        if platform == 'windows':
            return self._check_domain_windows()
        else:
            return self._check_domain_linux()
    
    def _check_domain_windows(self) -> dict:
        """Check domain membership on Windows"""
        result = run_command(['wmic', 'computersystem', 'get', 'domain'])
        
        if result:
            domain = result.strip().split('\n')[-1].strip()
            
            if domain and domain.upper() != 'WORKGROUP':
                print(f"  [+] System is domain-joined: {domain}")
                
                domain_info = {
                    'domain': domain,
                    'is_domain_joined': True
                }
                
                # Get domain controller
                dc_result = run_command(['nltest', '/dcname:'])
                if dc_result:
                    dc_match = re.search(r'\\\\(\S+)', dc_result)
                    if dc_match:
                        dc = dc_match.group(1)
                        domain_info['domain_controller'] = dc
                        print(f"  [+] Domain Controller: {dc}")
                
                return domain_info
            else:
                print(f"  [-] System is not domain-joined (Workgroup: {domain})")
        
        return {'is_domain_joined': False}
    
    def _check_domain_linux(self) -> dict:
        """Check domain membership on Linux"""
        result = run_command(['realm', 'list'])
        
        if result and 'configured:' in result:
            print(f"  [+] System appears to be domain-joined")
            print(f"{result}")
            return {'is_domain_joined': True}
        
        print(f"  [-] System does not appear domain-joined")
        return {'is_domain_joined': False}
    
    def enumerate_domain_users(self) -> dict:
        """Enumerate domain users"""
        print("\n[*] Enumerating domain users...")
        
        platform = get_platform()
        
        if platform != 'windows':
            return {}
        
        result = run_command(['net', 'user', '/domain'])
        
        if not result:
            return {}
        
        print(f"  [+] Domain users:")
        
        # Parse user list
        users = []
        in_user_section = False
        
        for line in result.split('\n'):
            if '----' in line:
                in_user_section = True
                continue
            
            if in_user_section and line.strip():
                line_users = [u.strip() for u in line.split() if u.strip()]
                users.extend(line_users)
        
        for user in users[:20]:  # Show first 20
            print(f"    - {user}")
        
        print(f"  [*] Total domain users: {len(users)}")
        
        return {'users': users}
    
    def enumerate_domain_computers(self) -> dict:
        """Enumerate domain computers"""
        print("\n[*] Enumerating domain computers...")
        
        platform = get_platform()
        
        if platform != 'windows':
            return {}
        
        result = run_command(['net', 'group', '"Domain Computers"', '/domain'])
        
        if result:
            print(f"  [+] Domain computers found")
            print(f"{result[:500]}")
            
            return {'computers': result}
        
        return {}
    
    def find_domain_admins(self) -> dict:
        """Find domain admin accounts"""
        print("\n[*] Enumerating domain admins...")
        
        platform = get_platform()
        
        if platform != 'windows':
            return {}
        
        result = run_command(['net', 'group', '"Domain Admins"', '/domain'])
        
        if not result:
            return {}
        
        print(f"  [+] Domain Admins:")
        
        admins = []
        in_members_section = False
        
        for line in result.split('\n'):
            if 'Members' in line:
                in_members_section = True
                continue
            
            if in_members_section and line.strip() and not line.startswith('The command'):
                admins.append(line.strip())
                print(f"    - {line.strip()}")
        
        return {'domain_admins': admins}

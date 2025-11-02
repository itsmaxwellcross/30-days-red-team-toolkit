"""
Access checking functionality
"""

import subprocess
from ..core.utils import get_platform, run_command


class AccessChecker:
    """Check access levels on targets"""
    
    def check_admin_access(self, target_ip: str) -> bool:
        """
        Check if we have admin access to target
        
        Args:
            target_ip: Target IP address
        
        Returns:
            True if admin access available
        """
        print(f"\n[*] Checking local admin access to {target_ip}...")
        
        platform = get_platform()
        
        if platform != 'windows':
            return False
        
        # Try to access C$ share
        result = subprocess.run(
            ['net', 'use', f'\\\\{target_ip}\\C$'],
            capture_output=True,
            text=True
        )
        
        has_access = result.returncode == 0
        
        if has_access:
            print(f"  [+] Have admin access to {target_ip}")
            
            # Clean up
            subprocess.run(
                ['net', 'use', f'\\\\{target_ip}\\C$', '/delete'],
                capture_output=True
            )
        else:
            print(f"  [-] No admin access to {target_ip}")
        
        return has_access
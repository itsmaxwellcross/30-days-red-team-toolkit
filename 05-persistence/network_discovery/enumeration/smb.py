"""
SMB share enumeration
"""

import subprocess
from ..core.utils import get_platform, run_command


class SMBEnumerator:
    """Enumerate SMB shares"""
    
    def enumerate_shares(self, target_ip: str) -> dict:
        """
        Enumerate SMB shares on target
        
        Args:
            target_ip: Target IP address
        
        Returns:
            Dictionary with IP and share information
        """
        print(f"\n[*] Enumerating SMB shares on {target_ip}...")
        
        platform = get_platform()
        
        if platform == 'windows':
            return self._enumerate_shares_windows(target_ip)
        else:
            return self._enumerate_shares_linux(target_ip)
    
    def _enumerate_shares_windows(self, target_ip: str) -> dict:
        """Enumerate shares using Windows net view"""
        result = run_command(['net', 'view', f'\\\\{target_ip}'])
        
        if result:
            print(f"  [+] Shares found:")
            print(f"{result}")
            
            return {
                'ip': target_ip,
                'shares': result
            }
        
        return None
    
    def _enumerate_shares_linux(self, target_ip: str) -> dict:
        """Enumerate shares using smbclient"""
        try:
            result = subprocess.run(
                ['smbclient', '-L', target_ip, '-N'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if 'Sharename' in result.stdout:
                print(f"  [+] Shares found:")
                
                for line in result.stdout.split('\n'):
                    if '\t' in line and 'Disk' in line:
                        print(f"    {line.strip()}")
                
                return {
                    'ip': target_ip,
                    'shares': result.stdout
                }
        
        except FileNotFoundError:
            print("  [!] smbclient not installed")
        except Exception as e:
            print(f"  [-] Could not enumerate shares: {e}")
        
        return None
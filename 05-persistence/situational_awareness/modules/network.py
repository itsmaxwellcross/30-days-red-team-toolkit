"""
Network configuration and connection enumeration
"""

import re
from ..core.utils import run_command


class NetworkEnumerator:
    """Enumerate network configuration"""
    
    def __init__(self, os_type: str):
        self.os_type = os_type
    
    def enumerate(self) -> dict:
        """Run network enumeration"""
        print("\n[*] Enumerating network configuration...")
        
        if self.os_type == 'linux':
            network_info = self._enumerate_linux_network()
        elif self.os_type == 'windows':
            network_info = self._enumerate_windows_network()
        else:
            network_info = {}
        
        self._print_results(network_info)
        return network_info
    
    def _enumerate_linux_network(self) -> dict:
        """Linux network enumeration"""
        return {
            'interfaces': run_command('ip addr show 2>/dev/null || ifconfig'),
            'routes': run_command('ip route 2>/dev/null || route -n'),
            'connections': run_command('ss -tunap 2>/dev/null || netstat -tunap 2>/dev/null'),
            'dns': run_command('cat /etc/resolv.conf'),
            'arp': run_command('ip neigh 2>/dev/null || arp -a')
        }
    
    def _enumerate_windows_network(self) -> dict:
        """Windows network enumeration"""
        return {
            'interfaces': run_command('ipconfig /all'),
            'routes': run_command('route print'),
            'connections': run_command('netstat -ano'),
            'arp': run_command('arp -a')
        }
    
    def _print_results(self, network_info: dict):
        """Print network information"""
        interfaces = network_info.get('interfaces', '')
        
        if self.os_type == 'linux':
            ip_addresses = re.findall(r'inet (\d+\.\d+\.\d+\.\d+)', interfaces)
        else:
            ip_addresses = re.findall(
                r'IPv4 Address[.\s]+: (\d+\.\d+\.\d+\.\d+)', 
                interfaces
            )
        
        print(f"  IP Addresses: {', '.join(set(ip_addresses))}")


"""
Network interface discovery
"""

import subprocess
import re
import ipaddress
from ..core.utils import get_platform


class InterfaceScanner:
    """Discover local network interfaces and IP addresses"""
    
    def get_interfaces(self) -> list:
        """Get all local network interfaces"""
        print("[*] Discovering local network interfaces...")
        
        try:
            return self._get_interfaces_netifaces()
        except ImportError:
            return self._get_interfaces_fallback()
    
    def _get_interfaces_netifaces(self) -> list:
        """Get interfaces using netifaces library"""
        import netifaces
        
        interfaces = []
        
        for interface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(interface)
            
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    ip = addr['addr']
                    if ip != '127.0.0.1':
                        interfaces.append({
                            'interface': interface,
                            'ip': ip,
                            'netmask': addr.get('netmask'),
                            'broadcast': addr.get('broadcast')
                        })
                        print(f"  [+] {interface}: {ip}/{addr.get('netmask')}")
        
        return interfaces
    
    def _get_interfaces_fallback(self) -> list:
        """Fallback to command-line tools"""
        platform = get_platform()
        
        if platform == 'linux':
            return self._get_interfaces_linux()
        elif platform == 'windows':
            return self._get_interfaces_windows()
        
        return []
    
    def _get_interfaces_linux(self) -> list:
        """Get interfaces on Linux"""
        interfaces = []
        
        result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
        
        for line in result.stdout.split('\n'):
            if 'inet ' in line and '127.0.0.1' not in line:
                match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/(\d+)', line)
                if match:
                    ip = match.group(1)
                    cidr = match.group(2)
                    interfaces.append({'ip': ip, 'cidr': cidr})
                    print(f"  [+] Found: {ip}/{cidr}")
        
        return interfaces
    
    def _get_interfaces_windows(self) -> list:
        """Get interfaces on Windows"""
        interfaces = []
        
        result = subprocess.run(['ipconfig'], capture_output=True, text=True)
        
        for line in result.stdout.split('\n'):
            if 'IPv4 Address' in line:
                match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                if match:
                    ip = match.group(1)
                    if ip != '127.0.0.1':
                        interfaces.append({'ip': ip})
                        print(f"  [+] Found: {ip}")
        
        return interfaces
    
    def calculate_network_range(self, ip: str, netmask: str) -> str:
        """Calculate network range from IP and netmask"""
        try:
            network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
            return str(network)
        except:
            return None
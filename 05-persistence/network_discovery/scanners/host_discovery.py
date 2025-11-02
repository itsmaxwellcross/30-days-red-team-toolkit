"""
Host discovery via ping and ARP
"""

import subprocess
import concurrent.futures
import ipaddress
import re
from ..core.utils import get_platform, run_command


class HostDiscovery:
    """Discover live hosts on the network"""
    
    def ping_sweep(self, network_range: str, timeout: int = 1) -> list:
        """
        Perform ping sweep on network range
        
        Args:
            network_range: CIDR network range (e.g., '192.168.1.0/24')
            timeout: Ping timeout in seconds
        
        Returns:
            List of discovered host dictionaries
        """
        print(f"\n[*] Performing ping sweep on {network_range}...")
        
        try:
            network = ipaddress.IPv4Network(network_range, strict=False)
        except ValueError:
            print("  [-] Invalid network range")
            return []
        
        # Limit scan to reasonable size
        hosts_to_scan = list(network.hosts())[:254]
        
        print(f"  [*] Scanning {len(hosts_to_scan)} hosts...")
        
        live_hosts = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = {
                executor.submit(self._ping_host, str(ip), timeout): ip 
                for ip in hosts_to_scan
            }
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    live_hosts.append({
                        'ip': result,
                        'status': 'alive',
                        'discovery_method': 'ping'
                    })
                    print(f"    [+] Host alive: {result}")
        
        print(f"  [*] Found {len(live_hosts)} live hosts")
        return live_hosts
    
    def _ping_host(self, ip: str, timeout: int) -> str:
        """Ping a single host"""
        platform = get_platform()
        
        if platform == 'windows':
            command = ['ping', '-n', '1', '-w', str(timeout * 1000), ip]
        else:
            command = ['ping', '-c', '1', '-W', str(timeout), ip]
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                timeout=timeout + 1
            )
            
            if result.returncode == 0:
                return ip
        except:
            pass
        
        return None
    
    def arp_scan(self) -> list:
        """Scan ARP table for hosts"""
        print("\n[*] Performing ARP scan...")
        
        platform = get_platform()
        
        if platform == 'linux':
            return self._arp_scan_linux()
        elif platform == 'windows':
            return self._arp_scan_windows()
        
        return []
    
    def _arp_scan_linux(self) -> list:
        """ARP scan on Linux"""
        hosts = []
        
        try:
            with open('/proc/net/arp', 'r') as f:
                arp_table = f.read()
            
            for line in arp_table.split('\n')[1:]:  # Skip header
                parts = line.split()
                if len(parts) >= 4:
                    ip = parts[0]
                    mac = parts[3]
                    
                    if mac != '00:00:00:00:00:00' and ip != '0.0.0.0':
                        hosts.append({
                            'ip': ip,
                            'mac': mac,
                            'discovery_method': 'arp'
                        })
                        print(f"  [+] Found: {ip} ({mac})")
        except:
            # Fallback to arp command
            result = run_command(['arp', '-a'])
            if result:
                print(f"  {result[:500]}")
        
        return hosts
    
    def _arp_scan_windows(self) -> list:
        """ARP scan on Windows"""
        hosts = []
        
        result = run_command(['arp', '-a'])
        
        if result:
            for line in result.split('\n'):
                match = re.search(r'(\d+\.\d+\.\d+\.\d+)\s+([\w-]+)', line)
                if match:
                    ip = match.group(1)
                    mac = match.group(2)
                    
                    hosts.append({
                        'ip': ip,
                        'mac': mac,
                        'discovery_method': 'arp'
                    })
                    print(f"  [+] Found: {ip} ({mac})")
        
        return hosts
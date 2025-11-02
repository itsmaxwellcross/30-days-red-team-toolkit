"""
Port scanning functionality
"""

import concurrent.futures
from ..core.utils import is_port_open


class PortScanner:
    """Scan ports on target hosts"""
    
    # Common ports for lateral movement
    DEFAULT_PORTS = [
        21,    # FTP
        22,    # SSH
        23,    # Telnet
        25,    # SMTP
        80,    # HTTP
        110,   # POP3
        135,   # RPC
        139,   # NetBIOS
        143,   # IMAP
        443,   # HTTPS
        445,   # SMB
        1433,  # MSSQL
        3306,  # MySQL
        3389,  # RDP
        5432,  # PostgreSQL
        5900,  # VNC
        8080,  # HTTP Alt
        8443   # HTTPS Alt
    ]
    
    SERVICE_MAP = {
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        80: 'HTTP',
        110: 'POP3',
        135: 'RPC',
        139: 'NetBIOS-SSN',
        143: 'IMAP',
        443: 'HTTPS',
        445: 'SMB',
        1433: 'MSSQL',
        3306: 'MySQL',
        3389: 'RDP',
        5432: 'PostgreSQL',
        5900: 'VNC',
        8080: 'HTTP-Alt',
        8443: 'HTTPS-Alt'
    }
    
    def scan_host(self, target_ip: str, ports: list = None) -> list:
        """
        Scan ports on target host
        
        Args:
            target_ip: Target IP address
            ports: List of ports to scan (uses DEFAULT_PORTS if None)
        
        Returns:
            List of open service dictionaries
        """
        if ports is None:
            ports = self.DEFAULT_PORTS
        
        print(f"\n[*] Scanning ports on {target_ip}...")
        
        open_services = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {
                executor.submit(is_port_open, target_ip, port): port 
                for port in ports
            }
            
            for future in concurrent.futures.as_completed(futures):
                port = futures[future]
                if future.result():
                    service = self.identify_service(port)
                    
                    service_entry = {
                        'ip': target_ip,
                        'port': port,
                        'service': service,
                        'state': 'open'
                    }
                    
                    open_services.append(service_entry)
                    print(f"  [+] {target_ip}:{port} - {service}")
        
        return open_services
    
    def identify_service(self, port: int) -> str:
        """Identify service by port number"""
        return self.SERVICE_MAP.get(port, f'Unknown ({port})')

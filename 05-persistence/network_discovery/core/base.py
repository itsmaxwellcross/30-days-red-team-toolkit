"""
Main orchestrator for network discovery
"""

from typing import List, Dict
from ..scanners import InterfaceScanner, HostDiscovery, PortScanner
from ..enumeration import SMBEnumerator, DomainEnumerator, AccessChecker
from ..output.formatters import OutputFormatter


class NetworkDiscovery:
    """Main class coordinating network discovery operations"""
    
    def __init__(self):
        self.discovered_hosts = []
        self.discovered_services = []
        self.domain_info = {}
        self.shares = []
        self.local_ips = []
        
        # Initialize scanners
        self.interface_scanner = InterfaceScanner()
        self.host_discovery = HostDiscovery()
        self.port_scanner = PortScanner()
        
        # Initialize enumerators
        self.smb_enum = SMBEnumerator()
        self.domain_enum = DomainEnumerator()
        self.access_checker = AccessChecker()
        
        # Output formatter
        self.formatter = OutputFormatter()
    
    def run_network_discovery(self):
        """Run complete network discovery workflow"""
        print("="*60)
        print("NETWORK DISCOVERY & LATERAL MOVEMENT RECON")
        print("="*60)
        
        # Phase 1: Discover local interfaces
        self.local_ips = self.interface_scanner.get_interfaces()
        
        # Phase 2: ARP scan
        arp_hosts = self.host_discovery.arp_scan()
        self.discovered_hosts.extend(arp_hosts)
        
        # Phase 3: Ping sweep on local networks
        for interface in self.local_ips:
            if 'netmask' in interface:
                network_range = self.interface_scanner.calculate_network_range(
                    interface['ip'],
                    interface['netmask']
                )
                
                if network_range:
                    ping_hosts = self.host_discovery.ping_sweep(network_range)
                    self.discovered_hosts.extend(ping_hosts)
        
        # Phase 4: Port scan discovered hosts
        for host in self.discovered_hosts[:10]:  # Limit to first 10
            services = self.port_scanner.scan_host(host['ip'])
            self.discovered_services.extend(services)
        
        # Phase 5: SMB enumeration
        smb_hosts = [s for s in self.discovered_services if s['port'] == 445]
        for smb_host in smb_hosts[:5]:  # Limit to first 5
            shares = self.smb_enum.enumerate_shares(smb_host['ip'])
            if shares:
                self.shares.append(shares)
        
        # Phase 6: Domain enumeration
        self.domain_info = self.domain_enum.enumerate_domain()
        
        # Print and save results
        self._print_summary()
        self.formatter.save(
            self.local_ips,
            self.discovered_hosts,
            self.discovered_services,
            self.shares,
            self.domain_info
        )
    
    def _print_summary(self):
        """Print discovery summary"""
        print("\n" + "="*60)
        print("NETWORK DISCOVERY COMPLETE")
        print("="*60)
        
        print(f"\n[*] Discovery Summary:")
        print(f"  Live Hosts: {len(self.discovered_hosts)}")
        print(f"  Open Services: {len(self.discovered_services)}")
        print(f"  SMB Shares: {len(self.shares)}")
        print(f"  Domain Joined: {self.domain_info.get('is_domain_joined', False)}")
        
        if self.domain_info.get('domain'):
            print(f"  Domain: {self.domain_info['domain']}")
            print(f"  Domain Users: {len(self.domain_info.get('users', []))}")
            print(f"  Domain Admins: {len(self.domain_info.get('domain_admins', []))}")

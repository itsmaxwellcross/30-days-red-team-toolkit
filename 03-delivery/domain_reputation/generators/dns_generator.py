"""
DNS record generator
"""
from typing import Optional

class DNSGenerator:
    """Generate recommended DNS records"""
    
    def __init__(self, domain: str):
        """
        Initialize DNS generator
        
        Args:
            domain: Domain for record generation
        """
        self.domain = domain
    
    def generate_spf(self, server_ip: Optional[str] = None) -> str:
        """
        Generate SPF record
        
        Args:
            server_ip: Server IP address (optional)
            
        Returns:
            SPF record string
        """
        if server_ip:
            record = f"v=spf1 a mx ip4:{server_ip} ~all"
        else:
            record = "v=spf1 a mx ip4:YOUR_SERVER_IP ~all"
        
        return record
    
    def generate_dkim(self, selector: str = 'default') -> str:
        """
        Generate DKIM record template
        
        Args:
            selector: DKIM selector
            
        Returns:
            DKIM record string
        """
        return "v=DKIM1; k=rsa; p=YOUR_PUBLIC_KEY"
    
    def generate_dmarc(self, policy: str = 'none') -> str:
        """
        Generate DMARC record
        
        Args:
            policy: DMARC policy (none/quarantine/reject)
            
        Returns:
            DMARC record string
        """
        return f"v=DMARC1; p={policy}; rua=mailto:dmarc@{self.domain}"
    
    def generate_all(self, server_ip: Optional[str] = None):
        """
        Generate and print all recommended DNS records
        
        Args:
            server_ip: Server IP for SPF record
        """
        print("\n[*] Recommended DNS Records:")
        print("=" * 60)
        
        # SPF Record
        spf = self.generate_spf(server_ip)
        print(f"\nTXT Record for {self.domain}:")
        print(f"  {spf}")
        
        # DKIM Record
        dkim = self.generate_dkim()
        print(f"\nTXT Record for default._domainkey.{self.domain}:")
        print(f"  {dkim}")
        print("  [!] Generate DKIM keys with: opendkim-genkey -d {self.domain}")
        
        # DMARC Record
        dmarc = self.generate_dmarc()
        print(f"\nTXT Record for _dmarc.{self.domain}:")
        print(f"  {dmarc}")
        
        print("\n[*] Setup Instructions:")
        print("  1. Add these records to your DNS provider")
        print("  2. Wait 24-48 hours for DNS propagation")
        print("  3. Re-run this tool to verify configuration")
        print("  4. Start domain warmup process")
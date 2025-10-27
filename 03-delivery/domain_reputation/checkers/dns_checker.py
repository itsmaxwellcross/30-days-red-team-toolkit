"""
DNS record checker
"""
import dns.resolver
from typing import Optional

class DNSChecker:
    """Check DNS records for email authentication"""
    
    def __init__(self, domain: str):
        """
        Initialize DNS checker
        
        Args:
            domain: Domain to check
        """
        self.domain = domain
    
    def check_spf(self) -> Optional[str]:
        """
        Check if SPF record is configured
        
        Returns:
            SPF record string or None
        """
        try:
            answers = dns.resolver.resolve(self.domain, 'TXT')
            for rdata in answers:
                txt = str(rdata).strip('"')
                if 'v=spf1' in txt:
                    print(f"[+] SPF Record found: {txt}")
                    return txt
            print("[-] No SPF record found")
            return None
        except dns.resolver.NXDOMAIN:
            print("[-] Domain does not exist")
            return None
        except dns.resolver.NoAnswer:
            print("[-] No TXT records found")
            return None
        except Exception as e:
            print(f"[-] Error checking SPF record: {e}")
            return None
    
    def check_dkim(self, selector: str = 'default') -> Optional[str]:
        """
        Check if DKIM is configured
        
        Args:
            selector: DKIM selector (default: 'default')
            
        Returns:
            DKIM record string or None
        """
        try:
            dkim_domain = f"{selector}._domainkey.{self.domain}"
            answers = dns.resolver.resolve(dkim_domain, 'TXT')
            for rdata in answers:
                txt = str(rdata).strip('"')
                if 'v=DKIM1' in txt:
                    print(f"[+] DKIM Record found: {txt[:80]}...")
                    return txt
            print("[-] No DKIM record found")
            return None
        except dns.resolver.NXDOMAIN:
            print(f"[-] No DKIM record found (selector: {selector})")
            return None
        except Exception as e:
            print(f"[-] No DKIM record found: {e}")
            return None
    
    def check_dmarc(self) -> Optional[str]:
        """
        Check if DMARC is configured
        
        Returns:
            DMARC record string or None
        """
        try:
            dmarc_domain = f"_dmarc.{self.domain}"
            answers = dns.resolver.resolve(dmarc_domain, 'TXT')
            for rdata in answers:
                txt = str(rdata).strip('"')
                if 'v=DMARC1' in txt:
                    print(f"[+] DMARC Record found: {txt}")
                    return txt
            print("[-] No DMARC record found")
            return None
        except dns.resolver.NXDOMAIN:
            print("[-] No DMARC record found")
            return None
        except Exception as e:
            print(f"[-] No DMARC record found: {e}")
            return None
    
    def check_mx(self) -> list:
        """
        Check MX records
        
        Returns:
            List of MX records
        """
        try:
            answers = dns.resolver.resolve(self.domain, 'MX')
            mx_records = []
            for rdata in answers:
                mx_records.append({
                    'priority': rdata.preference,
                    'server': str(rdata.exchange)
                })
                print(f"[+] MX Record: {rdata.preference} {rdata.exchange}")
            return mx_records
        except Exception as e:
            print(f"[-] No MX records found: {e}")
            return []
"""
Domain blacklist checker
"""
import dns.resolver
from typing import Dict
from ..config.settings import Settings

class BlacklistChecker:
    """Check domain against common blacklists"""
    
    def __init__(self, domain: str):
        """
        Initialize blacklist checker
        
        Args:
            domain: Domain to check
        """
        self.domain = domain
    
    def check_blacklist(self, blacklist: str) -> bool:
        """
        Check if domain is on a specific blacklist
        
        Args:
            blacklist: Blacklist hostname
            
        Returns:
            True if blacklisted, False otherwise
        """
        try:
            query = f"{self.domain}.{blacklist}"
            dns.resolver.resolve(query, 'A')
            return True  # Listed
        except dns.resolver.NXDOMAIN:
            return False  # Not listed
        except Exception:
            return False  # Assume not listed on error
    
    def check_all(self) -> Dict[str, bool]:
        """
        Check domain against all configured blacklists
        
        Returns:
            Dict mapping blacklist name to status (True = blacklisted)
        """
        results = {}
        
        for blacklist in Settings.BLACKLISTS:
            is_listed = self.check_blacklist(blacklist)
            results[blacklist] = is_listed
            
            if is_listed:
                print(f"[-] BLACKLISTED on {blacklist}")
            else:
                print(f"[+] Clean on {blacklist}")
        
        return results
    
    def get_clean_count(self, results: Dict[str, bool]) -> int:
        """Get count of clean blacklists"""
        return sum(1 for listed in results.values() if not listed)
    
    def get_blacklisted_count(self, results: Dict[str, bool]) -> int:
        """Get count of blacklists where domain is listed"""
        return sum(1 for listed in results.values() if listed)
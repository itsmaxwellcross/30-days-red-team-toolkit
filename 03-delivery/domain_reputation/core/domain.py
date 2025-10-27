"""
Domain data model
"""
from dataclasses import dataclass
from typing import Optional, Dict, List

@dataclass
class Domain:
    """Represents a domain for reputation analysis"""
    
    name: str
    spf_record: Optional[str] = None
    dkim_selector: str = 'default'
    dkim_record: Optional[str] = None
    dmarc_record: Optional[str] = None
    blacklist_status: Dict[str, bool] = None
    reputation_score: Optional[int] = None
    
    def __post_init__(self):
        if self.blacklist_status is None:
            self.blacklist_status = {}
    
    def is_clean(self) -> bool:
        """Check if domain is not on any blacklists"""
        if not self.blacklist_status:
            return None
        return all(not status for status in self.blacklist_status.values())
    
    def has_email_auth(self) -> bool:
        """Check if domain has proper email authentication"""
        return all([
            self.spf_record is not None,
            self.dkim_record is not None,
            self.dmarc_record is not None
        ])
    
    def get_summary(self) -> Dict:
        """Get domain summary"""
        return {
            'domain': self.name,
            'spf_configured': self.spf_record is not None,
            'dkim_configured': self.dkim_record is not None,
            'dmarc_configured': self.dmarc_record is not None,
            'is_clean': self.is_clean(),
            'has_email_auth': self.has_email_auth()
        }
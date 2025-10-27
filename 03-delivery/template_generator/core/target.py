"""
Target data model
"""
from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class TargetData:
    """Represents target information for personalized templates"""
    
    # Required fields
    name: str
    email: str
    
    # Optional fields
    title: Optional[str] = None
    department: Optional[str] = None
    company_name: Optional[str] = None
    company_domain: Optional[str] = None
    technologies_used: List[str] = field(default_factory=list)
    recent_news: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'email': self.email,
            'title': self.title,
            'department': self.department,
            'company_name': self.company_name,
            'company_domain': self.company_domain,
            'technologies_used': self.technologies_used,
            'recent_news': self.recent_news
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TargetData':
        """Create from dictionary"""
        return cls(
            name=data['name'],
            email=data['email'],
            title=data.get('title'),
            department=data.get('department'),
            company_name=data.get('company_name'),
            company_domain=data.get('company_domain'),
            technologies_used=data.get('technologies_used', []),
            recent_news=data.get('recent_news', [])
        )
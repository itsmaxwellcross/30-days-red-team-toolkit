"""
Base template class
"""
from abc import ABC, abstractmethod
from typing import Dict
from ..core.target import TargetData

class BaseTemplate(ABC):
    """Base class for all email templates"""
    
    def __init__(self, target: TargetData):
        """
        Initialize with target data
        
        Args:
            target: TargetData object
        """
        self.target = target
    
    @abstractmethod
    def generate(self) -> Dict:
        """
        Generate the template
        
        Returns:
            Dict with keys: subject, body, template_type, urgency
        """
        pass
    
    def _format_template(self, subject: str, body: str, 
                        template_type: str, urgency: str) -> Dict:
        """
        Format template into standard structure
        
        Args:
            subject: Email subject
            body: Email body
            template_type: Type identifier
            urgency: Urgency level (low/medium/high)
            
        Returns:
            Formatted template dict
        """
        return {
            'subject': subject,
            'body': body,
            'template_type': template_type,
            'urgency': urgency
        }
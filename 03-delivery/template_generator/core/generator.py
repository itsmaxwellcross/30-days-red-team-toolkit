"""
Main template generator orchestrator
"""
from typing import List, Dict, Optional
from ..templates import (
    CEOFraudTemplate,
    SecurityAlertTemplate,
    HRDocumentTemplate,
    VendorInvoiceTemplate,
    ITRequestTemplate,
    CollaborationTemplate,
    SocialMediaTemplate
)
from .target import TargetData

class TemplateGenerator:
    """Main template generator that orchestrates all template types"""
    
    def __init__(self, target_data: TargetData):
        """
        Initialize with target data
        
        Args:
            target_data: TargetData object or dict with target information
        """
        if isinstance(target_data, dict):
            self.target = TargetData.from_dict(target_data)
        else:
            self.target = target_data
        
        # Initialize all template generators
        self.templates = {
            'ceo_fraud': CEOFraudTemplate(self.target),
            'security_alert': SecurityAlertTemplate(self.target),
            'hr_document': HRDocumentTemplate(self.target),
            'vendor_invoice': VendorInvoiceTemplate(self.target),
            'it_request': ITRequestTemplate(self.target),
            'collaboration': CollaborationTemplate(self.target),
            'linkedin': SocialMediaTemplate(self.target)
        }
    
    def generate(self, template_type: str) -> Dict:
        """
        Generate a specific template type
        
        Args:
            template_type: Type of template to generate
            
        Returns:
            Dict with subject, body, template_type, and urgency
        """
        if template_type not in self.templates:
            raise ValueError(f"Unknown template type: {template_type}")
        
        return self.templates[template_type].generate()
    
    def get_all_templates(self) -> List[Dict]:
        """Generate all available template types"""
        return [template.generate() for template in self.templates.values()]
    
    def get_available_types(self) -> List[str]:
        """Get list of available template types"""
        return list(self.templates.keys())
    
    def generate_variants(self, template_type: str, count: int = 3) -> List[Dict]:
        """
        Generate multiple variants of a template
        
        Args:
            template_type: Type of template
            count: Number of variants to generate
            
        Returns:
            List of template variants
        """
        if template_type not in self.templates:
            raise ValueError(f"Unknown template type: {template_type}")
        
        template = self.templates[template_type]
        return [template.generate() for _ in range(count)]
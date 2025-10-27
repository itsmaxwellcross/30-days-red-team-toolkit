"""
Configuration settings
"""
from typing import List

class Settings:
    """Global settings for template generator"""
    
    # Template types available
    TEMPLATE_TYPES: List[str] = [
        'ceo_fraud',
        'security_alert',
        'hr_document',
        'vendor_invoice',
        'it_request',
        'collaboration',
        'linkedin'
    ]
    
    # Urgency levels
    URGENCY_LEVELS: List[str] = ['low', 'medium', 'high']
    
    # Default company info (when not provided)
    DEFAULT_COMPANY = 'Company'
    DEFAULT_DOMAIN = 'company.com'
    
    # Template variations count
    DEFAULT_VARIANTS = 3
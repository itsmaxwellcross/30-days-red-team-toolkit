"""
Helper utility functions
"""
import re
from typing import Dict

def format_email(template: Dict, tracking_link: str = None) -> str:
    """
    Format email body with tracking links
    
    Args:
        template: Template dict with body
        tracking_link: Actual tracking URL
        
    Returns:
        Formatted email body
    """
    body = template['body']
    
    if tracking_link:
        body = body.replace('[TRACKING_LINK:', f'<a href="{tracking_link}">')
        body = body.replace(']', '</a>')
    
    return body

def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection
    
    Args:
        text: Input text
        
    Returns:
        Sanitized text
    """
    # Remove potentially dangerous characters
    text = re.sub(r'[<>\'\"&]', '', text)
    return text.strip()
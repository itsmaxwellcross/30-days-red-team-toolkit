#!/usr/bin/env python3
"""
Helper utility functions
"""

import random
import string

def generate_token(length: int = 16) -> str:
    """Generate random tracking token"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_tracking_pixel(tracking_domain: str, token: str) -> str:
    """Generate invisible tracking pixel HTML"""
    tracking_url = f"{tracking_domain}/track/{token}.png"
    return f'<img src="{tracking_url}" width="1" height="1" style="display:none" />'

def generate_tracking_link(tracking_domain: str, token: str, text: str = "Click here") -> str:
    """Generate tracked link HTML"""
    tracking_url = f"{tracking_domain}/click/{token}"
    return f'<a href="{tracking_url}" style="color: #0066cc; text-decoration: none;">{text}</a>'
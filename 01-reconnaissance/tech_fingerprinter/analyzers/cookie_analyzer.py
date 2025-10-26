#!/usr/bin/env python3
"""
Cookie analysis for technology detection
"""

from typing import Dict, Any
from config.settings import COOKIE_INDICATORS

class CookieAnalyzer:
    """Analyze cookies for technology indicators"""
    
    @staticmethod
    def analyze(cookies: Dict[str, str]) -> Dict[str, Any]:
        """
        Analyze cookies
        
        Args:
            cookies: Dictionary of cookies
            
        Returns:
            Dictionary of detected technologies
        """
        tech = {}
        
        for cookie_name, technology in COOKIE_INDICATORS.items():
            if cookie_name in cookies:
                tech['backend'] = technology
                break
        
        return tech
#!/usr/bin/env python3
"""
HTTP header analysis for technology detection
"""

from typing import Dict, Any
from config.settings import CDN_HEADERS, SECURITY_HEADERS

class HeaderAnalyzer:
    """Analyze HTTP headers for technology indicators"""
    
    @staticmethod
    def analyze(headers: Dict[str, str]) -> Dict[str, Any]:
        """
        Analyze HTTP headers
        
        Args:
            headers: Dictionary of HTTP headers
            
        Returns:
            Dictionary of detected technologies
        """
        tech = {}
        
        # Server header
        if 'Server' in headers:
            tech['server'] = headers['Server']
        
        # X-Powered-By header
        if 'X-Powered-By' in headers:
            tech['powered_by'] = headers['X-Powered-By']
        
        # Framework indicators
        if 'X-AspNet-Version' in headers:
            tech['framework'] = f"ASP.NET {headers['X-AspNet-Version']}"
        
        if 'X-AspNetMvc-Version' in headers:
            tech['mvc'] = f"ASP.NET MVC {headers['X-AspNetMvc-Version']}"
        
        # Django detection
        if 'X-Django-Version' in headers:
            tech['framework'] = f"Django {headers['X-Django-Version']}"
        
        # CDN detection
        for header, cdn in CDN_HEADERS.items():
            if header in headers:
                tech['cdn'] = cdn
                break
        
        # Security headers analysis
        security = HeaderAnalyzer._analyze_security_headers(headers)
        if security:
            tech['security_headers'] = security
        
        return tech
    
    @staticmethod
    def _analyze_security_headers(headers: Dict[str, str]) -> Dict[str, str]:
        """Extract security-related headers"""
        security = {}
        
        for header in SECURITY_HEADERS:
            if header in headers:
                security[header] = headers[header]
        
        return security
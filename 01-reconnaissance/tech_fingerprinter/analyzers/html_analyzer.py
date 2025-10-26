#!/usr/bin/env python3
"""
HTML content analysis for technology detection
"""

import re
from typing import Dict, Any, List
from bs4 import BeautifulSoup
from config.settings import JS_FRAMEWORKS
from utils.signatures import TechnologySignatures

class HTMLAnalyzer:
    """Analyze HTML content for technology indicators"""
    
    @staticmethod
    def analyze(html: str) -> Dict[str, Any]:
        """
        Analyze HTML content
        
        Args:
            html: HTML content as string
            
        Returns:
            Dictionary of detected technologies
        """
        tech = {}
        soup = BeautifulSoup(html, 'html.parser')
        
        # Meta generator detection
        generator = soup.find('meta', attrs={'name': 'generator'})
        if generator and generator.get('content'):
            tech['cms'] = generator['content']
        
        # CMS detection
        cms_info = HTMLAnalyzer._detect_cms(html, soup)
        if cms_info:
            tech.update(cms_info)
        
        # JavaScript framework detection
        js_frameworks = HTMLAnalyzer._detect_js_frameworks(html)
        if js_frameworks:
            tech['javascript'] = js_frameworks
        
        # CSS framework detection
        css_framework = HTMLAnalyzer._detect_css_framework(html)
        if css_framework:
            tech['css_framework'] = css_framework
        
        return tech
    
    @staticmethod
    def _detect_cms(html: str, soup: BeautifulSoup) -> Dict[str, Any]:
        """Detect CMS from HTML patterns"""
        cms_signatures = TechnologySignatures.get_cms_signatures()
        
        for cms_name, signatures in cms_signatures.items():
            # Check HTML patterns
            html_patterns = signatures.get('html_patterns', [])
            if any(pattern in html for pattern in html_patterns):
                result = {'cms': cms_name}
                
                # Try to extract version if available
                version_regex = signatures.get('version_regex')
                if version_regex:
                    version_match = re.search(version_regex, html)
                    if version_match:
                        result['cms_version'] = version_match.group(1)
                
                return result
        
        return {}
    
    @staticmethod
    def _detect_js_frameworks(html: str) -> List[str]:
        """Detect JavaScript frameworks"""
        detected = []
        
        for framework, indicators in JS_FRAMEWORKS.items():
            if any(indicator in html for indicator in indicators):
                detected.append(framework)
        
        return detected
    
    @staticmethod
    def _detect_css_framework(html: str) -> str:
        """Detect CSS framework"""
        html_lower = html.lower()
        
        if 'bootstrap' in html_lower:
            return 'Bootstrap'
        elif 'tailwind' in html_lower:
            return 'Tailwind CSS'
        elif 'bulma' in html_lower:
            return 'Bulma'
        elif 'foundation' in html_lower:
            return 'Foundation'
        
        return ''
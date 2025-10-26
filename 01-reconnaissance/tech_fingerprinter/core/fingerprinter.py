#!/usr/bin/env python3
"""
Main fingerprinting orchestrator
"""

from typing import Dict, Any
from core.http_client import HTTPClient
from analyzers import (
    HeaderAnalyzer,
    HTMLAnalyzer,
    CookieAnalyzer,
    PathChecker,
    SSLAnalyzer
)
from utils.output import OutputFormatter

class TechFingerprinter:
    """Orchestrate technology fingerprinting"""
    
    def __init__(self, url: str):
        self.url = url if url.startswith('http') else f'https://{url}'
        self.http_client = HTTPClient(self.url)
        self.technologies = {}
    
    def run_fingerprint(self) -> Dict[str, Any]:
        """
        Run complete fingerprinting process
        
        Returns:
            Dictionary of detected technologies
        """
        print(f"[*] Fingerprinting {self.url}")
        print("=" * 50 + "\n")
        
        # HTTP header analysis
        print("[*] Analyzing HTTP headers...")
        headers = self.http_client.get_headers()
        header_tech = HeaderAnalyzer.analyze(headers)
        self.technologies.update(header_tech)
        
        # HTML content analysis
        print("[*] Analyzing HTML content...")
        html = self.http_client.get_html()
        html_tech = HTMLAnalyzer.analyze(html)
        self.technologies.update(html_tech)
        
        # Cookie analysis
        print("[*] Analyzing cookies...")
        cookies = self.http_client.get_cookies()
        cookie_tech = CookieAnalyzer.analyze(cookies)
        self.technologies.update(cookie_tech)
        
        # Path checking
        print()
        path_checker = PathChecker(self.http_client)
        common_paths = path_checker.check_paths()
        if common_paths:
            self.technologies['exposed_paths'] = common_paths
        
        # SSL analysis
        print("\n[*] Checking SSL certificate...")
        ssl_info = SSLAnalyzer.analyze(self.url)
        if ssl_info:
            self.technologies['ssl'] = ssl_info
        
        return self.technologies
    
    def print_results(self) -> None:
        """Print formatted results"""
        print("\n" + "=" * 50)
        print("TECHNOLOGY STACK SUMMARY")
        print("=" * 50 + "\n")
        
        OutputFormatter.print_results(self.technologies)
    
    def export_results(self, format: str = 'json') -> None:
        """
        Export results to file
        
        Args:
            format: Output format ('json' or 'markdown')
        """
        base_filename = OutputFormatter.get_sanitized_filename(self.url)
        
        if format == 'json':
            filename = f'{base_filename}_fingerprint.json'
            OutputFormatter.export_json(self.technologies, filename)
            print(f"\n[+] Results saved to: {filename}")
        elif format == 'markdown':
            filename = f'{base_filename}_fingerprint.md'
            OutputFormatter.export_markdown(self.technologies, filename)
            print(f"\n[+] Results saved to: {filename}")
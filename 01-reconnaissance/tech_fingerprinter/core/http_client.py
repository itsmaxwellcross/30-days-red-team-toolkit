#!/usr/bin/env python3
"""
HTTP client for making requests and handling responses
"""

import requests
from typing import Optional, Dict
from config.settings import REQUEST_TIMEOUT

class HTTPClient:
    """Handle HTTP requests with proper error handling"""
    
    def __init__(self, url: str):
        self.url = url if url.startswith('http') else f'https://{url}'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get(self, path: str = '', timeout: int = REQUEST_TIMEOUT) -> Optional[requests.Response]:
        """
        Make GET request to URL
        
        Args:
            path: Optional path to append to base URL
            timeout: Request timeout in seconds
            
        Returns:
            Response object or None on error
        """
        try:
            url = self.url + path if path else self.url
            response = self.session.get(
                url,
                timeout=timeout,
                allow_redirects=True,
                verify=False
            )
            return response
        except requests.RequestException as e:
            print(f"[-] Request error for {url}: {e}")
            return None
    
    def head(self, path: str = '', timeout: int = REQUEST_TIMEOUT) -> Optional[requests.Response]:
        """Make HEAD request to check path existence"""
        try:
            url = self.url + path if path else self.url
            response = self.session.head(
                url,
                timeout=timeout,
                allow_redirects=False,
                verify=False
            )
            return response
        except requests.RequestException:
            return None
    
    def get_headers(self) -> Dict[str, str]:
        """Get response headers from main URL"""
        response = self.get()
        return dict(response.headers) if response else {}
    
    def get_cookies(self) -> Dict[str, str]:
        """Get cookies from main URL"""
        response = self.get()
        return dict(response.cookies) if response else {}
    
    def get_html(self) -> str:
        """Get HTML content from main URL"""
        response = self.get()
        return response.text if response else ""
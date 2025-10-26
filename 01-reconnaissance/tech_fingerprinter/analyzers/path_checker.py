#!/usr/bin/env python3
"""
Common path checking for technology detection
"""

from typing import Dict, Any
from config.settings import COMMON_PATHS, PATH_CHECK_TIMEOUT
from core.http_client import HTTPClient

class PathChecker:
    """Check for common framework/CMS paths"""
    
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
    
    def check_paths(self) -> Dict[str, Dict[str, Any]]:
        """
        Check for existence of common paths
        
        Returns:
            Dictionary of found paths with details
        """
        found = {}
        
        print("[*] Checking common paths...")
        
        for path, description in COMMON_PATHS.items():
            response = self.http_client.head(path, timeout=PATH_CHECK_TIMEOUT)
            
            if response and response.status_code in [200, 301, 302, 403]:
                found[path] = {
                    'description': description,
                    'status': response.status_code
                }
                print(f"    [+] Found: {path} ({description}) - Status: {response.status_code}")
        
        return found
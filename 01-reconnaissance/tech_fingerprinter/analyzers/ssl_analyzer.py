#!/usr/bin/env python3
"""
SSL/TLS certificate analysis
"""

import ssl
import socket
from typing import Optional, Dict, Any
from config.settings import SSL_TIMEOUT

class SSLAnalyzer:
    """Analyze SSL/TLS certificates"""
    
    @staticmethod
    def analyze(url: str) -> Optional[Dict[str, Any]]:
        """
        Get SSL certificate information
        
        Args:
            url: Target URL
            
        Returns:
            Dictionary of certificate info or None
        """
        try:
            hostname = url.split('://')[1].split('/')[0].split(':')[0]
            
            # Handle port if specified
            if ':' in url.split('://')[1]:
                port = int(url.split('://')[1].split(':')[1].split('/')[0])
            else:
                port = 443
            
            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, port), timeout=SSL_TIMEOUT) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        'subject': dict(x[0] for x in cert.get('subject', [])),
                        'issuer': dict(x[0] for x in cert.get('issuer', [])),
                        'version': cert.get('version'),
                        'serial_number': cert.get('serialNumber'),
                        'not_before': cert.get('notBefore'),
                        'not_after': cert.get('notAfter'),
                        'san': SSLAnalyzer._get_san(cert)
                    }
        except Exception as e:
            print(f"[-] SSL analysis error: {e}")
            return None
    
    @staticmethod
    def _get_san(cert: Dict) -> list:
        """Extract Subject Alternative Names"""
        try:
            san = cert.get('subjectAltName', [])
            return [name[1] for name in san if name[0] == 'DNS']
        except:
            return []
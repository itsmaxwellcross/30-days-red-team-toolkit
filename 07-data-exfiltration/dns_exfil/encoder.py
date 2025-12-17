#!/usr/bin/env python3
"""
Data encoding for DNS exfiltration
"""

import base64

class DNSEncoder:
    """Encode data for DNS transmission"""
    
    @staticmethod
    def encode_data(data):
        """
        Encode data to base64 for DNS transmission
        
        Args:
            data: String or bytes to encode
            
        Returns:
            Base64 encoded string
        """
        if isinstance(data, str):
            data = data.encode()
        
        return base64.b64encode(data).decode()
    
    @staticmethod
    def decode_data(encoded):
        """
        Decode base64 data
        
        Args:
            encoded: Base64 encoded string
            
        Returns:
            Original bytes
        """
        return base64.b64decode(encoded)
    
    @staticmethod
    def chunk_data(encoded_data, chunk_size=50):
        """
        Split encoded data into chunks
        
        Args:
            encoded_data: Base64 encoded string
            chunk_size: Maximum size per chunk (DNS label limit: 63)
            
        Returns:
            List of chunks
        """
        chunks = []
        for i in range(0, len(encoded_data), chunk_size):
            chunks.append(encoded_data[i:i+chunk_size])
        
        return chunks
    
    @staticmethod
    def prepare_for_dns(data, chunk_size=50):
        """
        Prepare data for DNS exfiltration
        
        Args:
            data: Raw data to exfiltrate
            chunk_size: Chunk size
            
        Returns:
            Tuple of (encoded_data, chunks)
        """
        encoded = DNSEncoder.encode_data(data)
        chunks = DNSEncoder.chunk_data(encoded, chunk_size)
        
        return encoded, chunks
    
    @staticmethod
    def calculate_chunks_needed(data, chunk_size=50):
        """
        Calculate number of chunks needed for data
        
        Args:
            data: Raw data
            chunk_size: Chunk size
            
        Returns:
            Number of chunks required
        """
        encoded = DNSEncoder.encode_data(data)
        return (len(encoded) + chunk_size - 1) // chunk_size
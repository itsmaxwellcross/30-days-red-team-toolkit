#!/usr/bin/env python3
"""
Cryptographic utilities for chunked exfiltration
"""

import hashlib
from pathlib import Path

class HashCalculator:
    """Calculate cryptographic hashes for files and chunks"""
    
    @staticmethod
    def calculate_file_hash(filepath, algorithm='sha256', chunk_size=8192):
        """
        Calculate hash of entire file
        
        Args:
            filepath: Path to file
            algorithm: Hash algorithm (sha256, sha1, md5)
            chunk_size: Read buffer size
            
        Returns:
            Hex digest of hash
        """
        hash_obj = hashlib.new(algorithm)
        
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hash_obj.update(chunk)
        
        return hash_obj.hexdigest()
    
    @staticmethod
    def calculate_data_hash(data, algorithm='sha256'):
        """
        Calculate hash of data in memory
        
        Args:
            data: Bytes to hash
            algorithm: Hash algorithm
            
        Returns:
            Hex digest of hash
        """
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(data)
        return hash_obj.hexdigest()
    
    @staticmethod
    def verify_chunk_hash(chunk_data, expected_hash, algorithm='sha256'):
        """
        Verify chunk data matches expected hash
        
        Args:
            chunk_data: Bytes to verify
            expected_hash: Expected hash value
            algorithm: Hash algorithm
            
        Returns:
            True if hash matches, False otherwise
        """
        actual_hash = HashCalculator.calculate_data_hash(chunk_data, algorithm)
        return actual_hash == expected_hash
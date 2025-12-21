"""
Overwrite Methods for Secure Deletion
Implements various data overwrite patterns and standards
"""

import os
from ..core.constants import DOD_PATTERN


class OverwriteMethods:
    """
    Data overwrite methods
    
    Implements various secure deletion standards:
    - Random data
    - All zeros
    - All ones
    - DoD 5220.22-M (3 passes)
    - Gutmann method (35 passes)
    """
    
    def random_data(self, size):
        """
        Generate cryptographically secure random data
        
        Args:
            size (int): Number of bytes to generate
            
        Returns:
            bytes: Random data
        """
        return os.urandom(size)
    
    def zero_data(self, size):
        """
        Generate all zeros
        
        Args:
            size (int): Number of bytes to generate
            
        Returns:
            bytes: Zero data (0x00)
        """
        return b'\x00' * size
    
    def one_data(self, size):
        """
        Generate all ones
        
        Args:
            size (int): Number of bytes to generate
            
        Returns:
            bytes: One data (0xFF)
        """
        return b'\xff' * size
    
    def dod_pattern(self, size, pass_num):
        """
        DoD 5220.22-M standard pattern
        
        3-pass method:
        - Pass 1: All ones (0xFF)
        - Pass 2: All zeros (0x00)
        - Pass 3: Random data
        
        Args:
            size (int): Number of bytes to generate
            pass_num (int): Current pass number (0-indexed)
            
        Returns:
            bytes: Data for this pass
        """
        pattern = DOD_PATTERN[pass_num % len(DOD_PATTERN)]
        
        if pattern == 'ones':
            return self.one_data(size)
        elif pattern == 'zeros':
            return self.zero_data(size)
        else:  # random
            return self.random_data(size)
    
    def gutmann_pattern(self, size, pass_num):
        """
        Gutmann method (35 passes)
        
        The Gutmann method is a more thorough deletion algorithm
        designed to defeat forensic recovery attempts.
        
        Pattern:
        - Passes 0-3: Random data
        - Passes 4-30: Specific patterns for various encoding schemes
        - Passes 31-34: Random data
        
        Args:
            size (int): Number of bytes to generate
            pass_num (int): Current pass number (0-indexed)
            
        Returns:
            bytes: Data for this pass
        """
        # Simplified Gutmann implementation
        # Full implementation would include all 27 specific patterns
        
        if pass_num < 4 or pass_num > 30:
            # First 4 and last 4 passes: random
            return self.random_data(size)
        else:
            # Middle passes: use patterns
            # This is a simplified version
            pattern_num = pass_num - 4
            return self._gutmann_specific_pattern(size, pattern_num)
    
    def _gutmann_specific_pattern(self, size, pattern_num):
        """
        Generate specific Gutmann pattern
        
        Args:
            size (int): Number of bytes
            pattern_num (int): Pattern number (0-26)
            
        Returns:
            bytes: Pattern data
        """
        # Simplified patterns (real Gutmann has 27 specific patterns)
        patterns = [
            b'\x55' * size,  # 0x55
            b'\xAA' * size,  # 0xAA
            b'\x92' * size,  # Various patterns
            b'\x49' * size,
            b'\x24' * size,
            b'\x92' * size,
            b'\x49' * size,
            b'\x24' * size,
        ]
        
        # Cycle through patterns
        pattern = patterns[pattern_num % len(patterns)]
        
        # Ensure correct size
        if len(pattern) > size:
            return pattern[:size]
        elif len(pattern) < size:
            # Repeat pattern to fill size
            return (pattern * (size // len(pattern) + 1))[:size]
        
        return pattern
    
    def custom_pattern(self, size, pattern_byte):
        """
        Generate custom pattern
        
        Args:
            size (int): Number of bytes
            pattern_byte (int): Byte value to repeat (0-255)
            
        Returns:
            bytes: Pattern data
        """
        return bytes([pattern_byte]) * size
    
    def get_method_info(self, method):
        """
        Get information about a deletion method
        
        Args:
            method (str): Method name
            
        Returns:
            dict: Method information
        """
        info = {
            'random': {
                'name': 'Random Data',
                'passes': 'User-defined',
                'description': 'Cryptographically secure random data',
                'security': 'High',
                'speed': 'Fast'
            },
            'zeros': {
                'name': 'All Zeros',
                'passes': 'User-defined',
                'description': 'Overwrite with 0x00',
                'security': 'Low',
                'speed': 'Very Fast'
            },
            'ones': {
                'name': 'All Ones',
                'passes': 'User-defined',
                'description': 'Overwrite with 0xFF',
                'security': 'Low',
                'speed': 'Very Fast'
            },
            'dod': {
                'name': 'DoD 5220.22-M',
                'passes': 3,
                'description': 'US Department of Defense standard',
                'security': 'High',
                'speed': 'Fast'
            },
            'gutmann': {
                'name': 'Gutmann Method',
                'passes': 35,
                'description': 'Thorough 35-pass method',
                'security': 'Very High',
                'speed': 'Slow'
            }
        }
        
        return info.get(method, {'name': 'Unknown', 'description': 'Unknown method'})
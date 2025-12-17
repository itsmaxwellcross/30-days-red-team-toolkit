#!/usr/bin/env python3
"""
Binary data conversion utilities
"""

class BinaryConverter:
    """Convert between binary and byte representations"""
    
    @staticmethod
    def bytes_to_binary(data):
        """
        Convert bytes to binary string
        
        Args:
            data: Bytes to convert
            
        Returns:
            Binary string (e.g., "01001000")
        """
        return ''.join(format(byte, '08b') for byte in data)
    
    @staticmethod
    def binary_to_bytes(binary_string):
        """
        Convert binary string to bytes
        
        Args:
            binary_string: Binary string to convert
            
        Returns:
            Bytes object
        """
        data_bytes = bytearray()
        
        for i in range(0, len(binary_string), 8):
            byte = binary_string[i:i+8]
            if len(byte) == 8:  # Ensure full byte
                data_bytes.append(int(byte, 2))
        
        return bytes(data_bytes)
    
    @staticmethod
    def int_to_bytes(value, num_bytes=4, byteorder='big'):
        """
        Convert integer to bytes
        
        Args:
            value: Integer to convert
            num_bytes: Number of bytes to use
            byteorder: Byte order ('big' or 'little')
            
        Returns:
            Bytes object
        """
        return value.to_bytes(num_bytes, byteorder)
    
    @staticmethod
    def bytes_to_int(data, byteorder='big'):
        """
        Convert bytes to integer
        
        Args:
            data: Bytes to convert
            byteorder: Byte order ('big' or 'little')
            
        Returns:
            Integer value
        """
        return int.from_bytes(data, byteorder)
    
    @staticmethod
    def prepare_data_with_header(data):
        """
        Prepare data for encoding by adding length header
        
        Args:
            data: Raw data bytes
            
        Returns:
            Data with 4-byte length header prepended
        """
        data_len = len(data)
        length_header = BinaryConverter.int_to_bytes(data_len, 4)
        return length_header + data
    
    @staticmethod
    def extract_length_from_bits(bit_string):
        """
        Extract data length from first 32 bits
        
        Args:
            bit_string: Binary string starting with length header
            
        Returns:
            Integer length value
        """
        if len(bit_string) < 32:
            return None
        
        length_bits = bit_string[:32]
        return int(length_bits, 2)
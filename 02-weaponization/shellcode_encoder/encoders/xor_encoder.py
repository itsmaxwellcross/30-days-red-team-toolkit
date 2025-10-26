#!/usr/bin/env python3
import random

class XOREncoder:
    """XOR encoding for shellcode obfuscation"""
    
    def __init__(self, key=None):
        self.key = key if key else random.randint(1, 255)
    
    def encode(self, data):
        """XOR encode binary data"""
        encoded = bytearray()
        for byte in data:
            encoded.append(byte ^ self.key)
        return bytes(encoded)
    
    def get_key(self):
        """Return the encoding key"""
        return self.key
    
    def decode(self, encoded_data):
        """Decode XOR encoded data (same operation as encode)"""
        return self.encode(encoded_data)
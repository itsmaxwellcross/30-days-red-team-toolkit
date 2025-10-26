#!/usr/bin/env python3
import base64
from ..utils.helpers import RandomGenerator

class XOREncoder:
    """XOR encoding operations"""
    
    def __init__(self):
        self.key = RandomGenerator.random_int(1, 255)
    
    def encode(self, data):
        """XOR encode data with key"""
        return bytes([b ^ self.key for b in data.encode()])
    
    def get_key(self):
        """Return the encoding key"""
        return self.key
    
    def create_decoder_stub(self):
        """Create PowerShell XOR decoder function"""
        func_name = RandomGenerator.random_string()
        
        decoder = f'''
function {func_name}($data, $key) {{
    $decoded = @()
    for ($i = 0; $i -lt $data.Length; $i++) {{
        $decoded += $data[$i] -bxor $key
    }}
    return [System.Text.Encoding]::ASCII.GetString($decoded)
}}
'''
        return decoder.strip(), func_name
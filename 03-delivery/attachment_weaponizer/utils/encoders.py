"""
Encoding utilities for payloads
"""
import base64
from typing import Union

def encode_payload(payload: Union[bytes, str], encoding: str = 'base64') -> str:
    """
    Encode payload for embedding
    
    Args:
        payload: Payload bytes or string
        encoding: Encoding type (base64, hex, etc.)
        
    Returns:
        Encoded payload string
    """
    if isinstance(payload, str):
        payload = payload.encode()
    
    if encoding == 'base64':
        return base64.b64encode(payload).decode()
    elif encoding == 'hex':
        return payload.hex()
    else:
        raise ValueError(f"Unsupported encoding: {encoding}")

def decode_payload(encoded: str, encoding: str = 'base64') -> bytes:
    """
    Decode payload
    
    Args:
        encoded: Encoded payload string
        encoding: Encoding type
        
    Returns:
        Decoded payload bytes
    """
    if encoding == 'base64':
        return base64.b64decode(encoded)
    elif encoding == 'hex':
        return bytes.fromhex(encoded)
    else:
        raise ValueError(f"Unsupported encoding: {encoding}")

def chunk_base64(encoded: str, chunk_size: int = 76) -> str:
    """
    Chunk base64 string into lines (for readability)
    
    Args:
        encoded: Base64 string
        chunk_size: Characters per line
        
    Returns:
        Chunked base64 string
    """
    return '\n'.join(
        encoded[i:i+chunk_size] 
        for i in range(0, len(encoded), chunk_size)
    )
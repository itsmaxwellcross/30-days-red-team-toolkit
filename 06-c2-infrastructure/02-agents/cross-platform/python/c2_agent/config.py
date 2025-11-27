import json
import os

DEFAULT_CONFIG = {
    "server_url": "https://10.10.14.5:443",
    "auth_token": "your-auth-token-here",
    "encryption_password": "your-encryption-password-here",
    "beacon_interval": 60,
    "jitter": 30,
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    ]
}

def load_config(config_path="config/agent_config.json"):
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    return DEFAULT_CONFIG
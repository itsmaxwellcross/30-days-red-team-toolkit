"""
Configuration management for red team engagements
"""

import json
import os
from pathlib import Path


class ConfigManager:
    """Handles loading and validation of engagement configurations"""
    
    DEFAULT_CONFIG = {
        'target': {
            'domain': 'example.com',
            'company_name': 'Example Corporation',
            'ip_ranges': ['10.0.0.0/24']
        },
        'attacker': {
            'ip': '10.10.14.5',
            'port': 4444,
            'email': 'attacker@evil.com'
        },
        'options': {
            'stealth_mode': False,
            'auto_exploit': False,
            'auto_lateral': False,
            'delay_between_phases': 60,
            'continue_on_error': False
        },
        'scope': {
            'subdomains': True,
            'email_enum': True,
            'port_scan': True,
            'vulnerability_scan': True,
            'exploitation': True,
            'post_exploitation': True,
            'delivery': False
        }
    }
    
    def __init__(self, config_file='config/engagement.json'):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Load engagement configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._create_default_config()
    
    def _create_default_config(self):
        """Create default configuration file"""
        os.makedirs('config', exist_ok=True)
        
        with open(self.config_file, 'w') as f:
            json.dump(self.DEFAULT_CONFIG, f, indent=2)
        
        print(f"[!] Created default config: {self.config_file}")
        print(f"[!] Please customize it for your engagement")
        
        return self.DEFAULT_CONFIG
    
    def get(self, key, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        
        return value
    
    def validate(self):
        """Validate configuration completeness"""
        required_keys = ['target.domain', 'attacker.ip', 'attacker.port']
        missing = []
        
        for key in required_keys:
            if self.get(key) is None:
                missing.append(key)
        
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        
        return True
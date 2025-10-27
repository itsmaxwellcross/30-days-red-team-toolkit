#!/usr/bin/env python3
"""
Configuration management for phishing framework
"""

import json
import os
from pathlib import Path

class ConfigManager:
    """Handle configuration loading and management with auto-setup"""
    
    DEFAULT_CONFIG = {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "your-email@gmail.com",
        "sender_password": "your-app-password",
        "sender_name": "IT Security Team",
        "tracking_domain": "http://your-server.com",
        "landing_page_port": 8080,
        "database_path": "phishing_campaign.db",
        "redirect_url": "https://www.microsoft.com",
        "company_name": "Company Portal"
    }
    
    def __init__(self, config_file='config/phishing_config.json'):
        self.config_file = config_file
        self.config = self.load_config()
        
        # Validate critical fields
        if not self._is_configured():
            self._show_setup_instructions()
    
    def load_config(self):
        """Load configuration from file or create default"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                merged_config = self.DEFAULT_CONFIG.copy()
                merged_config.update(config)
                return merged_config
        except FileNotFoundError:
            print(f"[!] Config file not found: {self.config_file}")
            self._create_default_config()
            return self.DEFAULT_CONFIG.copy()
        except json.JSONDecodeError as e:
            print(f"[!] Error parsing config file: {e}")
            print("[!] Using default configuration")
            return self.DEFAULT_CONFIG.copy()
    
    def _create_default_config(self):
        """Create default configuration file with instructions"""
        config_dir = os.path.dirname(self.config_file)
        
        # Create config directory if it doesn't exist
        if config_dir:
            os.makedirs(config_dir, exist_ok=True)
        
        # Add helpful notes to config
        config_with_notes = self.DEFAULT_CONFIG.copy()
        config_with_notes['_setup_instructions'] = {
            "1_smtp_setup": "For Gmail: Enable 2FA and create App Password at https://myaccount.google.com/apppasswords",
            "2_sender_email": "Replace 'your-email@gmail.com' with your actual email",
            "3_sender_password": "Use app-specific password, not your regular password",
            "4_tracking_domain": "Change to your server's public IP (e.g., http://10.10.14.5 or http://phishing.example.com)",
            "5_security": "After configuring, remove this '_setup_instructions' section"
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config_with_notes, f, indent=2)
        
        print(f"[*] Created default config: {self.config_file}")
        print("[!] Please update the configuration with your settings before proceeding")

    def _is_configured(self):
        """Check if config has been customized from defaults"""
        # Check if critical fields still have default values
        if self.config.get('sender_email') == 'your-email@gmail.com':
            return False
        if self.config.get('sender_password') == 'your-app-password':
            return False
        if self.config.get('tracking_domain') == 'http://your-server.com':
            return False
        return True
    
    def _show_setup_instructions(self):
        """Display setup instructions"""
        print("\n" + "="*60)
        print("⚠️  CONFIGURATION REQUIRED")
        print("="*60)
        print(f"\nPlease configure: {self.config_file}")
        print("\nRequired changes:")
        print("  1. sender_email: Your email address")
        print("  2. sender_password: Your app-specific password")
        print("  3. tracking_domain: Your server's public URL/IP")
        print("\nFor Gmail:")
        print("  • Enable 2FA: https://myaccount.google.com/security")
        print("  • Create App Password: https://myaccount.google.com/apppasswords")
        print("\nExample tracking_domain:")
        print("  • http://10.10.14.5")
        print("  • http://phishing.example.com")
        print("="*60 + "\n")
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def update(self, key, value):
        """Update configuration value"""
        self.config[key] = value
    
    def save(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def validate(self):
        """Validate configuration"""
        errors = []
        
        # Check required fields
        required_fields = [
            'smtp_server', 'smtp_port', 'sender_email', 
            'sender_password', 'tracking_domain'
        ]
        
        for field in required_fields:
            if not self.config.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Check if still using defaults
        if self.config.get('sender_email') == 'your-email@gmail.com':
            errors.append("sender_email is still set to default value")
        
        if self.config.get('sender_password') == 'your-app-password':
            errors.append("sender_password is still set to default value")
        
        if self.config.get('tracking_domain') == 'http://your-server.com':
            errors.append("tracking_domain is still set to default value")
        
        return errors
    
    def print_config(self, hide_sensitive=True):
        """Print current configuration"""
        print("\n" + "="*60)
        print("Current Configuration")
        print("="*60)
        
        for key, value in self.config.items():
            if key.startswith('_'):  # Skip internal keys
                continue
            
            if hide_sensitive and key in ['sender_password']:
                print(f"  {key}: {'*' * len(str(value))}")
            else:
                print(f"  {key}: {value}")
        
        print("="*60 + "\n")
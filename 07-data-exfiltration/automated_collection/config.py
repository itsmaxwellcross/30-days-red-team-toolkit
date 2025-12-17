#!/usr/bin/env python3
"""
Configuration management
"""

import json
import os
from pathlib import Path

class ConfigManager:
    """Manage collection configuration"""
    
    DEFAULT_CONFIG_FILE = 'collection_config.json'
    
    @staticmethod
    def create_rule(name, source_paths, file_patterns, 
                   schedule='daily', max_age_days=None):
        """
        Create a collection rule
        
        Args:
            name: Rule name
            source_paths: List of source paths
            file_patterns: List of file patterns
            schedule: Schedule interval
            max_age_days: Maximum file age
            
        Returns:
            Rule dict
        """
        return {
            'name': name,
            'source_paths': source_paths if isinstance(source_paths, list) else [source_paths],
            'file_patterns': file_patterns if isinstance(file_patterns, list) else [file_patterns],
            'schedule': schedule,
            'max_age_days': max_age_days,
            'last_run': None,
            'files_collected': 0
        }
    
    @staticmethod
    def save_config(rules, config_file=None):
        """
        Save configuration to file
        
        Args:
            rules: List of rules
            config_file: Config file path
        """
        if config_file is None:
            config_file = ConfigManager.DEFAULT_CONFIG_FILE
        
        config = {'rules': rules}
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"[+] Configuration saved to {config_file}")
    
    @staticmethod
    def load_config(config_file=None):
        """
        Load configuration from file
        
        Args:
            config_file: Config file path
            
        Returns:
            List of rules or empty list
        """
        if config_file is None:
            config_file = ConfigManager.DEFAULT_CONFIG_FILE
        
        if not os.path.exists(config_file):
            return []
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        return config.get('rules', [])
    
    @staticmethod
    def add_rule_to_config(rule, config_file=None):
        """
        Add rule to existing configuration
        
        Args:
            rule: Rule dict
            config_file: Config file path
        """
        rules = ConfigManager.load_config(config_file)
        rules.append(rule)
        ConfigManager.save_config(rules, config_file)
    
    @staticmethod
    def remove_rule_from_config(rule_name, config_file=None):
        """
        Remove rule from configuration
        
        Args:
            rule_name: Name of rule to remove
            config_file: Config file path
            
        Returns:
            True if removed, False if not found
        """
        rules = ConfigManager.load_config(config_file)
        original_len = len(rules)
        
        rules = [r for r in rules if r['name'] != rule_name]
        
        if len(rules) < original_len:
            ConfigManager.save_config(rules, config_file)
            print(f"[+] Removed rule: {rule_name}")
            return True
        else:
            print(f"[-] Rule not found: {rule_name}")
            return False
    
    @staticmethod
    def list_rules(config_file=None):
        """
        List all configured rules
        
        Args:
            config_file: Config file path
            
        Returns:
            List of rule names
        """
        rules = ConfigManager.load_config(config_file)
        return [rule['name'] for rule in rules]
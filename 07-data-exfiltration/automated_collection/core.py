#!/usr/bin/env python3
"""
Core automated collection class
"""

from pathlib import Path
from .collector import FileCollector
from .scheduler import CollectionScheduler
from .config import ConfigManager

class AutomatedCollector:
    """Main interface for automated collection"""
    
    def __init__(self, staging_dir='collection_staging'):
        """
        Initialize automated collector
        
        Args:
            staging_dir: Directory for staging collected files
        """
        self.staging_dir = Path(staging_dir)
        self.staging_dir.mkdir(exist_ok=True)
        
        self.collector = FileCollector(staging_dir)
        self.scheduler = CollectionScheduler()
        self.config_manager = ConfigManager()
        
        self.collections = []
        self.running = False
        
        print(f"[+] Automated collector initialized")
        print(f"[+] Staging directory: {self.staging_dir}")
    
    def add_collection_rule(self, name, source_paths, file_patterns, 
                           schedule_interval='daily', max_age_days=None):
        """
        Add collection rule
        
        Args:
            name: Rule name
            source_paths: List of source paths
            file_patterns: List of file patterns
            schedule_interval: Schedule ('hourly', 'daily', 'weekly')
            max_age_days: Maximum file age
        """
        rule = self.config_manager.create_rule(
            name, source_paths, file_patterns,
            schedule_interval, max_age_days
        )
        
        self.collections.append(rule)
        
        print(f"[+] Added collection rule: {name}")
        print(f"    Sources: {len(rule['source_paths'])} paths")
        print(f"    Patterns: {rule['file_patterns']}")
        print(f"    Schedule: {schedule_interval}")
    
    def collect_files(self, rule):
        """
        Collect files based on rule
        
        Args:
            rule: Collection rule dict
            
        Returns:
            Manifest dict
        """
        manifest = self.collector.collect_files(rule)
        
        # Update rule statistics
        rule['last_run'] = manifest['created_at']
        rule['files_collected'] = rule.get('files_collected', 0) + manifest['total_files']
        
        return manifest
    
    def schedule_collections(self):
        """Schedule all collection rules"""
        self.scheduler.schedule_all(self.collections, self.collect_files)
    
    def run(self):
        """Run automated collector"""
        if not self.collections:
            print("[!] No collection rules defined")
            return
        
        self.schedule_collections()
        self.running = True
        
        print(f"\n[*] Automated collector running")
        
        self.scheduler.run()
        
        self.running = False
    
    def run_once(self):
        """Run all collections once"""
        print(f"[*] Running all collections once")
        
        for rule in self.collections:
            self.collect_files(rule)
    
    def load_config(self, config_file=None):
        """Load configuration from file"""
        rules = self.config_manager.load_config(config_file)
        self.collections = rules
        print(f"[+] Loaded {len(rules)} rules from configuration")
    
    def save_config(self, config_file=None):
        """Save configuration to file"""
        self.config_manager.save_config(self.collections, config_file)
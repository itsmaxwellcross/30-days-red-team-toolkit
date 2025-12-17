#!/usr/bin/env python3
"""
File collection logic
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from .manifest import ManifestManager

class FileCollector:
    """Collect files based on rules"""
    
    def __init__(self, staging_dir='collection_staging'):
        """
        Initialize file collector
        
        Args:
            staging_dir: Directory for staging collected files
        """
        self.staging_dir = Path(staging_dir)
        self.staging_dir.mkdir(exist_ok=True)
    
    def should_collect_file(self, filepath, max_age_days=None):
        """
        Check if file meets collection criteria
        
        Args:
            filepath: Path to file
            max_age_days: Maximum file age (None = no limit)
            
        Returns:
            True if file should be collected
        """
        if not os.path.exists(filepath):
            return False
        
        # Check age if specified
        if max_age_days is not None:
            file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            age_days = (datetime.now() - file_mtime).days
            
            if age_days > max_age_days:
                return False
        
        return True
    
    def find_matching_files(self, source_path, file_patterns):
        """
        Find files matching patterns
        
        Args:
            source_path: Source directory or file
            file_patterns: List of glob patterns
            
        Returns:
            List of matching file paths
        """
        source = Path(source_path)
        matches = []
        
        if not source.exists():
            return matches
        
        for pattern in file_patterns:
            if source.is_dir():
                # Search recursively in directory
                matches.extend(source.rglob(pattern))
            else:
                # Check if single file matches
                if source.match(pattern):
                    matches.append(source)
        
        return matches
    
    def collect_file(self, source_file, dest_dir, relative_path):
        """
        Copy file to collection directory
        
        Args:
            source_file: Source file path
            dest_dir: Destination directory
            relative_path: Relative path for destination
            
        Returns:
            Destination path or None on error
        """
        try:
            dest_path = dest_dir / relative_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(source_file, dest_path)
            
            return dest_path
        
        except Exception as e:
            print(f"[-] Error copying {source_file}: {e}")
            return None
    
    def collect_files(self, rule):
        """
        Collect files based on rule
        
        Args:
            rule: Collection rule dict
            
        Returns:
            Manifest dict
        """
        print(f"\n[*] Running collection: {rule['name']}")
        print(f"[*] Time: {datetime.now().isoformat()}")
        
        # Create collection directory
        collection_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        collection_dir = self.staging_dir / rule['name'] / collection_time
        collection_dir.mkdir(parents=True, exist_ok=True)
        
        collected_files = []
        
        # Process each source path
        for source_path in rule['source_paths']:
            source = Path(source_path)
            
            if not source.exists():
                print(f"[-] Source not found: {source}")
                continue
            
            print(f"[*] Searching: {source}")
            
            # Find matching files
            matches = self.find_matching_files(source_path, rule['file_patterns'])
            
            # Collect each matching file
            for match in matches:
                if not match.is_file():
                    continue
                
                if not self.should_collect_file(match, rule.get('max_age_days')):
                    continue
                
                # Determine relative path
                try:
                    relative_path = match.relative_to(source) if source.is_dir() else match.name
                except ValueError:
                    relative_path = match.name
                
                # Collect file
                dest_path = self.collect_file(match, collection_dir, relative_path)
                
                if dest_path:
                    # Create manifest entry
                    file_entry = ManifestManager.create_file_entry(match, dest_path)
                    collected_files.append(file_entry)
                    
                    size_mb = file_entry['size'] / 1024 / 1024
                    print(f"[+] Collected: {match.name} ({size_mb:.2f} MB)")
        
        # Create and save manifest
        manifest = ManifestManager.create_manifest(
            rule['name'],
            collection_time,
            collected_files
        )
        
        manifest_path = collection_dir / 'manifest.json'
        ManifestManager.save_manifest(manifest, manifest_path)
        
        # Print summary
        total_size_mb = manifest['total_size'] / 1024 / 1024
        print(f"[+] Collection complete: {manifest['total_files']} files ({total_size_mb:.2f} MB)")
        print(f"[+] Staged at: {collection_dir}")
        
        return manifest
#!/usr/bin/env python3
"""
Data filtering and prioritization
"""

import json
from pathlib import Path

class DataFilter:
    """Filter and prioritize collected data"""
    
    # Sensitive keywords
    SENSITIVE_KEYWORDS = [
        'password', 'passwd', 'credential', 'secret', 'private',
        'confidential', 'api_key', 'token', 'auth', 'backup',
        'database', 'sql', 'dump', 'finance', 'salary', 'ssn',
        'credit', 'card', 'social', 'security'
    ]
    
    # High value file extensions
    HIGH_VALUE_EXTENSIONS = [
        '.sql', '.db', '.sqlite', '.mdb', '.accdb',  # Databases
        '.key', '.pem', '.pfx', '.p12', '.crt',      # Certificates
        '.kdbx', '.wallet', '.keychain',             # Password managers
        '.doc', '.docx', '.xls', '.xlsx',            # Office documents
        '.pdf', '.ppt', '.pptx'
    ]
    
    # Medium value file extensions
    MEDIUM_VALUE_EXTENSIONS = [
        '.txt', '.csv', '.log',
        '.config', '.conf', '.ini', '.env',
        '.json', '.xml', '.yml', '.yaml'
    ]
    
    @staticmethod
    def is_sensitive(filepath):
        """
        Check if file contains sensitive data
        
        Args:
            filepath: Path to file
            
        Returns:
            True if sensitive
        """
        filename_lower = Path(filepath).name.lower()
        
        for keyword in DataFilter.SENSITIVE_KEYWORDS:
            if keyword in filename_lower:
                return True
        
        return False
    
    @staticmethod
    def get_priority(filepath):
        """
        Get collection priority (higher = more important)
        
        Args:
            filepath: Path to file
            
        Returns:
            Priority score (1-10)
        """
        ext = Path(filepath).suffix.lower()
        
        if DataFilter.is_sensitive(filepath):
            return 10
        elif ext in DataFilter.HIGH_VALUE_EXTENSIONS:
            return 7
        elif ext in DataFilter.MEDIUM_VALUE_EXTENSIONS:
            return 5
        else:
            return 1
    
    @staticmethod
    def filter_files(files, min_priority=5):
        """
        Filter files by priority
        
        Args:
            files: List of file info dicts
            min_priority: Minimum priority threshold
            
        Returns:
            Filtered and sorted list
        """
        filtered = []
        
        for file_info in files:
            priority = DataFilter.get_priority(file_info.get('original_path', ''))
            file_info['priority'] = priority
            
            if priority >= min_priority:
                filtered.append(file_info)
        
        # Sort by priority (highest first)
        filtered.sort(key=lambda x: x['priority'], reverse=True)
        
        return filtered
    
    @staticmethod
    def filter_collection(collection_dir, min_priority=5):
        """
        Filter collection by priority and save filtered manifest
        
        Args:
            collection_dir: Directory containing manifest
            min_priority: Minimum priority threshold
            
        Returns:
            Filtered manifest dict or None
        """
        from .manifest import ManifestManager
        
        print(f"[*] Filtering collection: {collection_dir}")
        
        manifest_path = Path(collection_dir) / 'manifest.json'
        manifest = ManifestManager.load_manifest(manifest_path)
        
        if not manifest:
            print(f"[-] Manifest not found")
            return None
        
        # Filter files
        filtered_files = DataFilter.filter_files(manifest['files'], min_priority)
        
        # Create filtered manifest
        filtered_manifest = manifest.copy()
        filtered_manifest['files'] = filtered_files
        filtered_manifest['total_files'] = len(filtered_files)
        filtered_manifest['total_size'] = sum(f['size'] for f in filtered_files)
        filtered_manifest['filtered'] = True
        filtered_manifest['min_priority'] = min_priority
        
        # Save filtered manifest
        filtered_path = Path(collection_dir) / 'manifest_filtered.json'
        ManifestManager.save_manifest(filtered_manifest, filtered_path)
        
        print(f"[+] Filtered: {len(filtered_files)}/{len(manifest['files'])} files")
        
        # Show high priority files
        if filtered_files:
            print(f"[+] High priority files:")
            for file_info in filtered_files[:10]:
                filename = Path(file_info['original_path']).name
                priority = file_info['priority']
                size_mb = file_info['size'] / 1024 / 1024
                print(f"    [{priority}] {filename} ({size_mb:.2f} MB)")
        
        return filtered_manifest
    
    @staticmethod
    def get_statistics(files):
        """
        Get statistics about file priorities
        
        Args:
            files: List of file info dicts
            
        Returns:
            Statistics dict
        """
        if not files:
            return {}
        
        priorities = [DataFilter.get_priority(f.get('original_path', '')) for f in files]
        
        return {
            'total_files': len(files),
            'high_priority': sum(1 for p in priorities if p >= 7),
            'medium_priority': sum(1 for p in priorities if 5 <= p < 7),
            'low_priority': sum(1 for p in priorities if p < 5),
            'avg_priority': sum(priorities) / len(priorities) if priorities else 0
        }
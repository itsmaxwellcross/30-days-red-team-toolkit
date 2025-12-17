#!/usr/bin/env python3
"""
Manifest creation and management
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime

class ManifestManager:
    """Manage collection manifests"""
    
    @staticmethod
    def calculate_hash(filepath):
        """
        Calculate SHA256 hash of file
        
        Args:
            filepath: Path to file
            
        Returns:
            Hex digest of hash
        """
        sha256 = hashlib.sha256()
        
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        
        return sha256.hexdigest()
    
    @staticmethod
    def create_file_entry(original_path, collected_path):
        """
        Create manifest entry for collected file
        
        Args:
            original_path: Original file path
            collected_path: Path where file was collected
            
        Returns:
            Dict with file information
        """
        original = Path(original_path)
        
        return {
            'original_path': str(original),
            'collected_path': str(collected_path),
            'size': original.stat().st_size,
            'hash': ManifestManager.calculate_hash(original),
            'collected_at': datetime.now().isoformat()
        }
    
    @staticmethod
    def create_manifest(rule_name, collection_time, collected_files):
        """
        Create collection manifest
        
        Args:
            rule_name: Name of collection rule
            collection_time: Timestamp of collection
            collected_files: List of file entries
            
        Returns:
            Manifest dict
        """
        return {
            'rule_name': rule_name,
            'collection_time': collection_time,
            'files': collected_files,
            'total_files': len(collected_files),
            'total_size': sum(f['size'] for f in collected_files),
            'created_at': datetime.now().isoformat()
        }
    
    @staticmethod
    def save_manifest(manifest, output_path):
        """
        Save manifest to file
        
        Args:
            manifest: Manifest dict
            output_path: Path to save manifest
        """
        with open(output_path, 'w') as f:
            json.dump(manifest, f, indent=2)
    
    @staticmethod
    def load_manifest(manifest_path):
        """
        Load manifest from file
        
        Args:
            manifest_path: Path to manifest file
            
        Returns:
            Manifest dict or None
        """
        manifest_path = Path(manifest_path)
        
        if not manifest_path.exists():
            return None
        
        with open(manifest_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def get_manifest_summary(manifest):
        """
        Get summary of manifest
        
        Args:
            manifest: Manifest dict
            
        Returns:
            Summary string
        """
        return (
            f"Collection: {manifest['rule_name']}\n"
            f"Time: {manifest['collection_time']}\n"
            f"Files: {manifest['total_files']}\n"
            f"Total Size: {manifest['total_size'] / 1024 / 1024:.2f} MB"
        )
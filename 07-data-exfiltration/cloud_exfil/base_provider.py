#!/usr/bin/env python3
"""
Base cloud provider interface
"""

from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime

class BaseCloudProvider(ABC):
    """Base class for cloud storage providers"""
    
    def __init__(self, service_name):
        """
        Initialize provider
        
        Args:
            service_name: Name of the cloud service
        """
        self.service_name = service_name
    
    @abstractmethod
    def upload_file(self, filepath, **kwargs):
        """
        Upload file to cloud service
        
        Args:
            filepath: Path to file to upload
            **kwargs: Provider-specific arguments
            
        Returns:
            Upload result dict or None on failure
        """
        pass
    
    @abstractmethod
    def check_credentials(self, **kwargs):
        """
        Verify credentials are valid
        
        Args:
            **kwargs: Provider-specific credentials
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    def generate_backup_path(self, filename):
        """
        Generate standard backup path
        
        Args:
            filename: Original filename
            
        Returns:
            Backup path string
        """
        date_str = datetime.now().strftime('%Y%m%d')
        return f"backups/{date_str}/{filename}"
    
    def get_file_info(self, filepath):
        """
        Get file information
        
        Args:
            filepath: Path to file
            
        Returns:
            Dict with file info
        """
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        return {
            'filename': path.name,
            'size': path.stat().st_size,
            'size_mb': path.stat().st_size / (1024 * 1024),
            'path': str(path)
        }
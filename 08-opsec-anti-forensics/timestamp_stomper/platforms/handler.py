"""
Platform Handler Factory
Returns appropriate platform-specific handler
"""

import platform


def get_platform_handler():
    """
    Get platform-specific timestamp handler
    
    Returns:
        Platform-specific handler instance
    """
    os_type = platform.system()
    
    if os_type == 'Windows':
        from .windows_handler import WindowsHandler
        return WindowsHandler()
    else:
        from .unix_handler import UnixHandler
        return UnixHandler()


class BasePlatformHandler:
    """
    Base class for platform-specific handlers
    Defines interface that all handlers must implement
    """
    
    def get_file_times(self, filepath):
        """
        Get file timestamps
        
        Args:
            filepath (str): Path to file
            
        Returns:
            dict: Dictionary with timestamps
        """
        raise NotImplementedError("Subclass must implement get_file_times()")
    
    def set_file_times(self, filepath, accessed=None, modified=None, created=None):
        """
        Set file timestamps
        
        Args:
            filepath (str): Path to file
            accessed (datetime, optional): Access time
            modified (datetime, optional): Modification time
            created (datetime, optional): Creation time
            
        Returns:
            bool: True if successful
        """
        raise NotImplementedError("Subclass must implement set_file_times()")
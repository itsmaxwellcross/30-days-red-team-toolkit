"""
Logging functionality for red team operations
"""

import os
from datetime import datetime
from pathlib import Path


class EngagementLogger:
    """Centralized logging for engagement activities"""
    
    def __init__(self, engagement_id):
        self.engagement_id = engagement_id
        self.log_dir = Path('logs')
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / f"{engagement_id}.log"
    
    def log(self, message, level='INFO'):
        """Log message to console and file"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] [{level}] {message}"
        
        # Console output
        print(log_message)
        
        # File output
        with open(self.log_file, 'a') as f:
            f.write(log_message + '\n')
    
    def debug(self, message):
        """Log debug message"""
        self.log(message, 'DEBUG')
    
    def info(self, message):
        """Log info message"""
        self.log(message, 'INFO')
    
    def success(self, message):
        """Log success message"""
        self.log(message, 'SUCCESS')
    
    def warning(self, message):
        """Log warning message"""
        self.log(message, 'WARNING')
    
    def error(self, message):
        """Log error message"""
        self.log(message, 'ERROR')
    
    def separator(self, char='=', length=60):
        """Log separator line"""
        self.log(char * length)
    
    def section_header(self, title):
        """Log section header"""
        self.separator()
        self.log(title)
        self.separator()
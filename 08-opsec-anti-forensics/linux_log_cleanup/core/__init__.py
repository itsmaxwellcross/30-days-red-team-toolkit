"""
Core functionality for Linux log cleanup
"""

from .base_cleaner import LinuxLogCleaner
from .constants import LOG_PATHS, RECORD_SIZES

__all__ = ['LinuxLogCleaner', 'LOG_PATHS', 'RECORD_SIZES']
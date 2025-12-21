"""
Linux Log Cleanup Framework
Clean auth logs, syslog, wtmp, utmp, and more
"""

__version__ = "1.0.0"
__author__ = "Red Team Operations"

from .core.base_cleaner import LinuxLogCleaner
from .cleaners.rotation_cleaner import LogRotationCleaner
from .cleaners.text_log_cleaner import TextLogCleaner
from .cleaners.binary_log_cleaner import BinaryLogCleaner

__all__ = [
    'LinuxLogCleaner',
    'LogRotationCleaner',
    'TextLogCleaner',
    'BinaryLogCleaner'
]
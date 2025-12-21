"""
Timestamp Stomping Toolkit
Modify file timestamps to avoid forensic detection
"""

__version__ = "1.0.0"
__author__ = "Red Team Operations"

from .core.timestamp_stomper import TimestampStomper
from .analyzers.macb_analyzer import MACBAnalysis
from .platforms.handler import get_platform_handler

__all__ = [
    'TimestampStomper',
    'MACBAnalysis',
    'get_platform_handler'
]
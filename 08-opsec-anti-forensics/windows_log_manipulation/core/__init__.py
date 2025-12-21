"""
Core functionality for EVTX parsing and manipulation
"""

from .evtx_parser import WindowsEventLog
from .constants import EVENT_IDS, LOG_NAMES

__all__ = ['WindowsEventLog', 'EVENT_IDS', 'LOG_NAMES']
"""
Windows Event Log Manipulation Framework
Selectively delete, modify, and inject events
"""

__version__ = "1.0.0"
__author__ = "Red Team Operations"

from .core.evtx_parser import WindowsEventLog
from .generators.cleaner import PowerShellLogCleaner
from .generators.injector import EventLogInjector

__all__ = [
    'WindowsEventLog',
    'PowerShellLogCleaner',
    'EventLogInjector'
]
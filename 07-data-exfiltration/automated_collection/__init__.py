#!/usr/bin/env python3
"""
Automated Collection Framework
Schedule and automate data collection and exfiltration
"""

from .core import AutomatedCollector
from .collector import FileCollector
from .scheduler import CollectionScheduler
from .filter import DataFilter
from .manifest import ManifestManager
from .config import ConfigManager

__version__ = '1.0.0'
__all__ = [
    'AutomatedCollector',
    'FileCollector',
    'CollectionScheduler',
    'DataFilter',
    'ManifestManager',
    'ConfigManager'
]
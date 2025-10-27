"""
Phishing Framework
For authorized security testing only
"""

__version__ = '2.0.0'
__author__ = 'Red Team Toolkit'

from .core.campaign import Campaign
from .core.database import Database
from .core.config_manager import ConfigManager
from .tracking.tracker import Tracker
from .tracking.analytics import Analytics
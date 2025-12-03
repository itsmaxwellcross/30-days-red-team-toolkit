"""
DGA Framework - Domain Generation Algorithm
Modular structure for generating pseudo-random C2 domains
"""

from .generator import DGAGenerator
from .agent import DGAAgent
from .utils import check_domain_active, format_output

__version__ = '1.0.0'
__all__ = ['DGAGenerator', 'DGAAgent', 'check_domain_active', 'format_output']

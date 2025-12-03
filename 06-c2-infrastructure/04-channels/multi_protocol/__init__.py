"""
Multi-Protocol C2 Agent
Automatic failover between HTTP, DNS, ICMP, and Cloud protocols
"""

from .agent import MultiProtocolAgent
from .utils import execute_command

__version__ = '1.0.0'
__all__ = ['MultiProtocolAgent', 'execute_command']
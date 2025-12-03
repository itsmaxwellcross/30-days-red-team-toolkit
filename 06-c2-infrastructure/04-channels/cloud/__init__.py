"""
Cloud C2 Framework - AWS S3-based Command and Control
Modular structure for cloud-based C2 operations
"""

from .c2 import CloudC2
from .agent import CloudC2Agent
from .operator import CloudC2Operator
from .utils import validate_bucket_name, estimate_costs, list_all_sessions

__version__ = '1.0.0'
__all__ = ['CloudC2', 'CloudC2Agent', 'CloudC2Operator']
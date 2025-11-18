"""
Attack Chain Templates Package
Pre-configured workflows for common attack scenarios
"""

from .manager import AttackChainTemplateManager
from .executor import TemplateExecutor
from .web_app import WebAppTemplates
from .domain import DomainTemplates
from .lateral import LateralMovementTemplates
from .exfiltration import ExfiltrationTemplates
from .ransomware import RansomwareTemplates

__all__ = [
    'AttackChainTemplateManager',
    'TemplateExecutor',
    'WebAppTemplates',
    'DomainTemplates',
    'LateralMovementTemplates',
    'ExfiltrationTemplates',
    'RansomwareTemplates',
]

__version__ = '1.0.0'
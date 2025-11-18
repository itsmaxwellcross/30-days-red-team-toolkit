"""
Practice Lab Management Package
Automated setup and management of vulnerable environments
"""

from .manager import LabManager
from .scenarios import ScenarioGenerator
from .documentation import DocumentationGenerator
from .definitions import LAB_DEFINITIONS, get_docker_labs, get_beginner_labs

__all__ = [
    'LabManager',
    'ScenarioGenerator',
    'DocumentationGenerator',
    'LAB_DEFINITIONS',
    'get_docker_labs',
    'get_beginner_labs',
]

__version__ = '1.0.0'
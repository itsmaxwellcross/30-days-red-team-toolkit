"""
Secure File Deletion Framework
Overwrite and delete files to prevent recovery
"""

__version__ = "1.0.0"
__author__ = "Red Team Operations"

from .core.secure_delete import SecureDelete
from .cleaners.artifact_cleaner import ArtifactCleaner
from .methods.overwrite_methods import OverwriteMethods

__all__ = [
    'SecureDelete',
    'ArtifactCleaner',
    'OverwriteMethods'
]
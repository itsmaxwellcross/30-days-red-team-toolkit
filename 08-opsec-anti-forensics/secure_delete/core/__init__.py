"""
Core secure deletion functionality
"""

from .secure_delete import SecureDelete
from .constants import DEFAULT_PASSES, DELETION_METHODS

__all__ = ['SecureDelete', 'DEFAULT_PASSES', 'DELETION_METHODS']
"""
Memory-Only Execution Toolkit
Execute payloads entirely in memory without touching disk

Techniques:
- Reflective DLL Loading
- Process Hollowing
- In-Memory PE Execution
- Shellcode Injection
- PowerShell Reflective Loading
"""

__version__ = "1.0.0"
__author__ = "Red Team Operations"

from .core.memory_executor import MemoryExecutor

__all__ = [
    'MemoryExecutor'
]
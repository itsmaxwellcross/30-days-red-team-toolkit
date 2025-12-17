#!/usr/bin/env python3
"""
Chunked File Exfiltration Framework
Split large files and exfiltrate in small pieces
"""

from .core import ChunkedExfiltration
from .file_ops import FileSplitter, FileAssembler
from .chunk_manager import ChunkManager
from .crypto import HashCalculator

__version__ = '1.0.0'
__all__ = ['ChunkedExfiltration', 'FileSplitter', 'FileAssembler', 'ChunkManager', 'HashCalculator']
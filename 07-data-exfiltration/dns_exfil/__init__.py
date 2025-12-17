#!/usr/bin/env python3
"""
DNS Exfiltration Engine
Exfiltrate data through DNS queries
"""

from .core import DNSExfiltration
from .encoder import DNSEncoder
from .query_builder import DNSQueryBuilder
from .transmitter import DNSTransmitter
from .timing import TimingController

__version__ = '1.0.0'
__all__ = ['DNSExfiltration', 'DNSEncoder', 'DNSQueryBuilder', 'DNSTransmitter', 'TimingController']
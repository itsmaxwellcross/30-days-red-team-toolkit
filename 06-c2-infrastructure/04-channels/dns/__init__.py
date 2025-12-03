# c2_frameworks/dns/__init__.py
"""
DNS C2 Framework – The Crown Jewel of Covert Channels
Exfiltrates data via DNS queries, delivers commands via DNS responses
Works from anywhere: locked-down kiosks, air-gapped networks, double-NAT hell
Uses only legitimate-looking DNS traffic → invisible to 99.9% of defenses
Real attackers have used this for years. Today, you own it.
"""

__all__ = ["DNSC2Agent", "DNSC2Server", "DNSResolver"]
# c2_frameworks/icmp/__init__.py
"""
ICMP C2 Framework – Pure Layer 3 Covert Channel
No open ports, no callbacks, no DNS queries
Works through stateful firewalls, NAT, air-gaps, and most NGFWs
Uses ICMP echo request/reply as data transport
Defenders see nothing but "normal" pings
"""

__all__ = ["ICMPC2Agent", "ICMPC2Server"]
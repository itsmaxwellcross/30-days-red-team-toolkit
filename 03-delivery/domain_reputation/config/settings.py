"""
Configuration settings
"""
from typing import List, Tuple

class Settings:
    """Global configuration settings"""
    
    # Blacklists to check
    BLACKLISTS: List[str] = [
        'zen.spamhaus.org',
        'bl.spamcop.net',
        'dnsbl.sorbs.net',
        'b.barracudacentral.org',
        'bl.mailspike.net'
    ]
    
    # Default warmup schedule (day, volume, audience)
    WARMUP_SCHEDULE: List[Tuple[int, int, str]] = [
        (1, 10, "Internal team members"),
        (2, 20, "Internal team members"),
        (3, 30, "Known contacts"),
        (4, 50, "Known contacts"),
        (5, 75, "Newsletter subscribers"),
        (7, 100, "Mixed recipients"),
        (9, 150, "Mixed recipients"),
        (10, 200, "Broader audience"),
        (12, 300, "Broader audience"),
        (14, 500, "Full volume"),
        (21, 1000, "Full volume"),
        (28, 2000, "Full volume")
    ]
    
    # DNS record defaults
    DEFAULT_DKIM_SELECTOR = 'default'
    DEFAULT_DMARC_POLICY = 'none'  # Start permissive, tighten later
    
    # SMTP defaults
    DEFAULT_SMTP_PORT = 587
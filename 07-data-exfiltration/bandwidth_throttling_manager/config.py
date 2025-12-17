"""
Configuration and constants for Bandwidth Throttling Manager
"""

# Default transfer rates (in Mbps)
DEFAULT_MAX_RATE_MBPS = 1.0
CONSERVATIVE_RATE_MBPS = 0.5
AGGRESSIVE_RATE_MBPS = 5.0

# Rate presets for different scenarios
RATE_PRESETS = {
    'stealth': {
        'name': 'Stealth Mode',
        'rate_mbps': 0.25,
        'description': 'Very slow, minimal network impact'
    },
    'conservative': {
        'name': 'Conservative',
        'rate_mbps': 0.5,
        'description': 'Slow transfer, low detection risk'
    },
    'normal': {
        'name': 'Normal',
        'rate_mbps': 1.0,
        'description': 'Balanced speed and stealth'
    },
    'moderate': {
        'name': 'Moderate',
        'rate_mbps': 2.0,
        'description': 'Faster transfer, moderate risk'
    },
    'aggressive': {
        'name': 'Aggressive',
        'rate_mbps': 5.0,
        'description': 'Fast transfer, higher detection risk'
    },
    'maximum': {
        'name': 'Maximum',
        'rate_mbps': 10.0,
        'description': 'Maximum speed, high detection risk'
    }
}

# Transfer window presets
SCHEDULE_PRESETS = {
    'night': {
        'name': 'Night Hours',
        'start_hour': 22,  # 10 PM
        'end_hour': 6,     # 6 AM
        'description': 'Transfer during night hours'
    },
    'lunch': {
        'name': 'Lunch Break',
        'start_hour': 12,  # 12 PM
        'end_hour': 14,    # 2 PM
        'description': 'Transfer during lunch break'
    },
    'off_hours': {
        'name': 'Off Hours',
        'start_hour': 18,  # 6 PM
        'end_hour': 8,     # 8 AM
        'description': 'Transfer outside business hours'
    },
    'business': {
        'name': 'Business Hours',
        'start_hour': 9,   # 9 AM
        'end_hour': 17,    # 5 PM
        'description': 'Transfer during business hours'
    },
    'weekend': {
        'name': 'Weekend',
        'start_hour': 0,
        'end_hour': 23,
        'description': 'Transfer anytime on weekends'
    }
}

# Chunk sizes for different transfer types
CHUNK_SIZES = {
    'tiny': 64 * 1024,        # 64 KB
    'small': 256 * 1024,      # 256 KB
    'medium': 1024 * 1024,    # 1 MB
    'large': 5 * 1024 * 1024, # 5 MB
    'huge': 10 * 1024 * 1024  # 10 MB
}

DEFAULT_CHUNK_SIZE = CHUNK_SIZES['medium']

# Queue priorities
PRIORITY_CRITICAL = 100
PRIORITY_HIGH = 75
PRIORITY_NORMAL = 50
PRIORITY_LOW = 25
PRIORITY_LOWEST = 10

# Timing settings
SCHEDULE_CHECK_INTERVAL = 300  # Check every 5 minutes
THROTTLE_PRECISION = 0.01      # Sleep precision in seconds
MIN_SLEEP_TIME = 0.001         # Minimum sleep time

# Statistics settings
STATS_UPDATE_INTERVAL = 10     # Update stats every 10 seconds
PROGRESS_BAR_WIDTH = 50        # Characters for progress bar

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 5                # Seconds between retries

# File queue settings
MAX_QUEUE_SIZE = 1000
DEFAULT_QUEUE_TIMEOUT = 3600   # 1 hour timeout for queued items
"""
Constants for Timestamp Stomping Toolkit
"""

# Default timestamp modification ranges
DEFAULT_DAYS_MIN = 30
DEFAULT_DAYS_MAX = 365

# Timestamp types
TIMESTAMP_TYPES = ['accessed', 'modified', 'created', 'changed']

# Common legitimate files for reference
WINDOWS_REFERENCE_FILES = [
    r'C:\Windows\System32\notepad.exe',
    r'C:\Windows\System32\cmd.exe',
    r'C:\Windows\System32\calc.exe',
    r'C:\Windows\explorer.exe'
]

LINUX_REFERENCE_FILES = [
    '/bin/ls',
    '/bin/cat',
    '/bin/bash',
    '/usr/bin/vim'
]

# Anomaly detection thresholds
TIMESTAMP_IDENTICAL_THRESHOLD = 1  # seconds
FUTURE_TIMESTAMP_WARNING = True
PAST_CREATION_WARNING = True

# Bulk operation settings
MAX_BULK_FILES = 10000  # Safety limit
BULK_PROGRESS_INTERVAL = 100  # Show progress every N files
"""
Configuration and constants for Scheduled Task Persistence Framework
"""

# Task trigger types
TRIGGER_TYPES = {
    'logon': {
        'name': 'User Logon',
        'description': 'Executes when user logs on',
        'requires_admin': False,
        'detection_difficulty': 'Easy',
        'survives_reboot': True
    },
    'boot': {
        'name': 'System Boot',
        'description': 'Executes at system startup',
        'requires_admin': True,
        'detection_difficulty': 'Easy',
        'survives_reboot': True
    },
    'schedule': {
        'name': 'Time-based Schedule',
        'description': 'Executes at specified intervals',
        'requires_admin': False,
        'detection_difficulty': 'Medium',
        'survives_reboot': True
    },
    'daily': {
        'name': 'Daily Schedule',
        'description': 'Executes daily at specified time',
        'requires_admin': False,
        'detection_difficulty': 'Medium',
        'survives_reboot': True
    },
    'idle': {
        'name': 'System Idle',
        'description': 'Executes when system is idle',
        'requires_admin': False,
        'detection_difficulty': 'Medium',
        'survives_reboot': True
    },
    'multi': {
        'name': 'Multiple Triggers',
        'description': 'Combines multiple trigger types',
        'requires_admin': False,
        'detection_difficulty': 'Hard',
        'survives_reboot': True
    }
}

# Task name generation components
TASK_PREFIXES = [
    'Windows',
    'Microsoft',
    'System',
    'Update',
    'Security',
    'Maintenance',
    'Telemetry',
    'Defender'
]

TASK_SUFFIXES = [
    'Update',
    'Sync',
    'Service',
    'Monitor',
    'Handler',
    'Manager',
    'Helper',
    'Scheduler',
    'Agent'
]

# Default settings
DEFAULT_INTERVAL_MINUTES = 10
DEFAULT_IDLE_MINUTES = 10
DEFAULT_DAILY_TIME = "02:00"
DEFAULT_STAGING_DIR = r"C:\Users\Public"
COMMAND_TIMEOUT = 30

# Task priority levels
TASK_PRIORITIES = {
    'realtime': 0,
    'high': 1,
    'above_normal': 4,
    'normal': 7,
    'below_normal': 8,
    'low': 10
}

# Suspicious indicators for detection
SUSPICIOUS_INDICATORS = [
    'powershell',
    'cmd.exe',
    'hidden',
    'bypass',
    'encodedcommand',
    'iex',
    'downloadstring',
    'invoke-expression',
    'webclient',
    'net.webclient',
    'start-process',
    '-nop',
    '-w hidden',
    '-windowstyle hidden',
    'exec bypass',
    'base64'
]

# Common legitimate task patterns (to filter out)
LEGITIMATE_TASK_PATTERNS = [
    r'Microsoft\\Windows\\',
    r'\\Adobe\\',
    r'\\Google\\',
    r'\\MicrosoftEdge',
    r'\\OneDrive',
    r'\\Office'
]
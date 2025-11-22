"""
Configuration and constants for WMI Persistence Framework
"""

# WMI namespaces
WMI_NAMESPACES = {
    'subscription': r'root\subscription',
    'cimv2': r'root\CimV2',
    'default': r'root\default'
}

# WMI class names
WMI_CLASSES = {
    'filter': '__EventFilter',
    'consumer': 'CommandLineEventConsumer',
    'binding': '__FilterToConsumerBinding',
    'active_script_consumer': 'ActiveScriptEventConsumer'
}

# Event trigger intervals (in seconds)
TRIGGER_INTERVALS = {
    'fast': 30,
    'normal': 60,
    'slow': 300,
    'very_slow': 900
}

# WQL query templates for different trigger types
WQL_QUERIES = {
    'interval': 'SELECT * FROM __InstanceModificationEvent WITHIN {interval} WHERE TargetInstance ISA "Win32_PerfFormattedData_PerfOS_System"',
    'logon': 'SELECT * FROM __InstanceCreationEvent WITHIN 15 WHERE TargetInstance ISA "Win32_LogonSession"',
    'process_creation': 'SELECT * FROM __InstanceCreationEvent WITHIN 10 WHERE TargetInstance ISA "Win32_Process" AND TargetInstance.Name = "{process_name}"',
    'process_deletion': 'SELECT * FROM __InstanceDeletionEvent WITHIN 10 WHERE TargetInstance ISA "Win32_Process" AND TargetInstance.Name = "{process_name}"',
    'service_start': 'SELECT * FROM __InstanceModificationEvent WITHIN 10 WHERE TargetInstance ISA "Win32_Service" AND TargetInstance.Name = "{service_name}" AND TargetInstance.State = "Running"',
    'registry': 'SELECT * FROM RegistryValueChangeEvent WHERE Hive="HKEY_LOCAL_MACHINE" AND KeyPath="SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run"',
    'file_creation': 'SELECT * FROM __InstanceCreationEvent WITHIN 10 WHERE TargetInstance ISA "CIM_DataFile" AND TargetInstance.Drive = "{drive}" AND TargetInstance.Path = "{path}"'
}

# Event name components for generation
EVENT_NAME_COMPONENTS = {
    'prefixes': [
        'System', 'Windows', 'Microsoft', 'Security',
        'Network', 'Update', 'Monitor', 'Service'
    ],
    'middles': [
        'Update', 'Monitor', 'Manager', 'Handler',
        'Controller', 'Provider', 'Sync', 'Check'
    ],
    'suffixes': [
        'Task', 'Service', 'Agent', 'Monitor',
        'Handler', 'Provider', 'Manager', 'Controller'
    ]
}

# Suspicious WMI indicators for detection
SUSPICIOUS_INDICATORS = {
    'commands': [
        'powershell',
        'cmd.exe',
        'rundll32',
        'regsvr32',
        'mshta',
        'wscript',
        'cscript',
        'certutil',
        'bitsadmin'
    ],
    'arguments': [
        '-enc',
        '-encodedcommand',
        '-nop',
        '-noprofile',
        '-w hidden',
        '-windowstyle hidden',
        'downloadstring',
        'downloadfile',
        'invoke-expression',
        'iex',
        'bypass'
    ],
    'suspicious_filters': [
        '__InstanceModificationEvent WITHIN',
        '__TimerEvent',
        'Win32_PerfFormattedData'
    ]
}

# Common legitimate WMI subscription names (for evasion)
LEGITIMATE_NAMES = [
    'SCM Event Log Consumer',
    'BVTConsumer',
    'NTEventLogEventConsumer',
    'CommandLineEventConsumer',
    'Windows Update',
    'Windows Defender'
]

# PowerShell execution policies
EXECUTION_POLICIES = {
    'bypass': 'Bypass',
    'unrestricted': 'Unrestricted',
    'remotesigned': 'RemoteSigned'
}

# Trigger method metadata
TRIGGER_METHODS = {
    'interval': {
        'name': 'Interval-Based',
        'description': 'Triggers at regular time intervals',
        'stealthy': True,
        'requires_admin': True
    },
    'logon': {
        'name': 'Logon-Triggered',
        'description': 'Triggers on user logon',
        'stealthy': True,
        'requires_admin': True
    },
    'process': {
        'name': 'Process-Triggered',
        'description': 'Triggers on process creation/deletion',
        'stealthy': True,
        'requires_admin': True
    },
    'custom': {
        'name': 'Custom WQL Query',
        'description': 'Custom WQL event query',
        'stealthy': True,
        'requires_admin': True
    }
}

# Output paths
OUTPUT_PATHS = {
    'ps_script': r'C:\Users\Public\wmi_{operation}.ps1',
    'removal_script': 'remove_wmi_{event_name}.ps1',
    'backup_file': 'wmi_backup_{event_name}.xml'
}

# Default descriptions for stealth
DEFAULT_DESCRIPTIONS = [
    'System performance monitoring',
    'Security event handler',
    'Update notification service',
    'Network connectivity monitor',
    'Service health check',
    'Application compatibility handler'
]
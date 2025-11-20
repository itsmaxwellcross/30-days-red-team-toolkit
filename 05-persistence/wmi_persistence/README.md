# WMI Event Subscription Persistence Framework

**Educational tool for demonstrating WMI-based persistence techniques**

⚠️ **WARNING**: This tool is for educational purposes and authorized security testing only. Unauthorized use is illegal and unethical.

## Overview

Comprehensive framework for creating, detecting, and removing Windows Management Instrumentation (WMI) event subscription persistence. WMI persistence is highly stealthy and survives reboots, making it a favorite technique for advanced attackers.

## Features

- **4 Trigger Methods**
  - Interval-based (time-based polling)
  - Logon-triggered
  - Process creation/deletion
  - Custom WQL queries

- **Detection & Scanning**
  - Enumerate all WMI subscriptions
  - Identify suspicious patterns
  - Detect aggressive polling
  - Find malicious command patterns

- **Automatic Cleanup**
  - Generate removal PowerShell scripts
  - Remove by event name
  - Bulk removal of suspicious subscriptions

- **Flexible Usage**
  - Command-line interface
  - Python API
  - PowerShell template system

## Installation
```bash
# Clone repository
git clone https://github.com/yourusername/wmi-persistence.git
cd wmi-persistence

# Install package
pip install -e .

# Or run directly
python main.py --help
```

## Usage

### Command Line Interface
```bash
# Create interval-based persistence (every 60 seconds)
python main.py --create "powershell -enc BASE64PAYLOAD" --interval 60

# Create logon-triggered persistence
python main.py --create-logon "cmd /c C:\payload.exe"

# Create process-triggered persistence
python main.py --create-process "rundll32 malicious.dll,Start" --process notepad.exe

# Create custom WQL query
python main.py --create-custom "cmd /c beacon.exe" --wql "SELECT * FROM __InstanceCreationEvent WITHIN 30 WHERE TargetInstance ISA 'Win32_Process'"

# List all WMI subscriptions
python main.py --list

# Scan for suspicious subscriptions
python main.py --check-suspicious

# Remove specific persistence
python main.py --remove SystemMonitor
```

### Python API
```python
from wmi_persistence import WMIPersistenceOrchestrator

orchestrator = WMIPersistenceOrchestrator()

# Create interval-based persistence
result = orchestrator.create_persistence(
    payload_command='powershell -enc BASE64',
    method='interval',
    interval=60,
    event_name='SystemMonitor'
)

# Create logon-triggered persistence
result = orchestrator.create_persistence(
    payload_command='cmd /c payload.exe',
    method='logon',
    event_name='UserProfileSync'
)

# Create process-triggered persistence
result = orchestrator.create_persistence(
    payload_command='rundll32 payload.dll,Start',
    method='process',
    process_name='notepad.exe'
)

# Custom WQL query
result = orchestrator.create_persistence(
    payload_command='cmd /c beacon.exe',
    method='custom',
    wql_query='SELECT * FROM __InstanceCreationEvent...'
)

# Scan for suspicious subscriptions
report = orchestrator.scan_subscriptions()

# Remove persistence
orchestrator.remove_persistence('SystemMonitor')

# Remove all created subscriptions
orchestrator.remove_all_created()
```

## Architecture
wmi_persistence/
├── config.py                  # Configuration and constants
├── main.py                    # CLI entry point
│
├── core/
│   ├── utils.py              # Shared utilities
│   └── orchestrator.py       # Main coordinator
│
├── templates/
│   └── powershell.py         # PowerShell script templates
│
├── methods/
│   ├── interval.py           # Interval-based triggers
│   ├── logon.py              # Logon triggers
│   ├── process.py            # Process triggers
│   └── custom.py             # Custom WQL queries
│
├── detection/
│   └── scanner.py            # Suspicious subscription detection
│
└── output/
└── removal.py            # Removal script generation

## WMI Persistence Methods

### 1. Interval-Based Triggers
Executes payload at regular intervals using performance counter queries:
```python
orchestrator.create_persistence(
    payload_command='cmd /c payload.exe',
    method='interval',
    interval=60  # seconds
)
```

### 2. Logon-Triggered
Executes payload when any user logs on:
```python
orchestrator.create_persistence(
    payload_command='cmd /c payload.exe',
    method='logon'
)
```

### 3. Process-Triggered
Executes payload when specific process starts or stops:
```python
orchestrator.create_persistence(
    payload_command='cmd /c payload.exe',
    method='process',
    process_name='notepad.exe',
    trigger_on='creation'  # or 'deletion'
)
```

### 4. Custom WQL Queries
Full control with custom WQL event queries:
```python
orchestrator.create_persistence(
    payload_command='cmd /c payload.exe',
    method='custom',
    wql_query='SELECT * FROM __InstanceCreationEvent WITHIN 30...'
)
```

## Detection Capabilities

The framework identifies suspicious WMI subscriptions by checking:

- **Aggressive Polling**: Intervals < 30 seconds
- **Suspicious Commands**: PowerShell, cmd.exe, LOLBins
- **Suspicious Arguments**: -enc, -nop, IEX, DownloadString
- **Performance Queries**: Common persistence patterns

## Output & Cleanup

### Automatic Removal Scripts
Each creation generates a PowerShell removal script:
```powershell
Get-WmiObject -Namespace root\subscription -Class __EventFilter -Filter "name='_SystemMonitor_Filter'" | Remove-WmiObject
Get-WmiObject -Namespace root\subscription -Class CommandLineEventConsumer -Filter "name='_SystemMonitor_Consumer'" | Remove-WmiObject
```

### Manual Removal
```bash
python main.py --remove SystemMonitor
```

## Requirements

- **Operating System**: Windows 7+ (Windows 10/11 recommended)
- **Privileges**: Administrator rights required
- **Python**: Python 3.7+
- **PowerShell**: PowerShell 3.0+

## Security Considerations

### Legitimate Use Cases
- Security research and education
- Penetration testing (authorized)
- Red team exercises (authorized)
- Defensive blue team training
- Malware analysis research

### Detection Methods
WMI persistence may be detected by:
- **Event Logs**: WMI-Activity/Operational logs (Event ID 5861)
- **EDR Solutions**: Behavioral monitoring
- **SIEM Correlation**: WMI subscription creation patterns
- **Security Tools**: Sysinternals Autoruns, WMI Explorer
- **PowerShell Logging**: Script block logging

### Ethical Guidelines
- Only use on systems you own or have explicit permission to test
- Document all operations for audit trails
- Use generated cleanup scripts to remove persistence
- Follow responsible disclosure practices
- Comply with all applicable laws and regulations

## Detection Indicators

### Event Logs
- **Event ID 5861**: WMI event subscription creation
- **Event ID 5859**: WMI consumer creation
- **Event ID 5860**: WMI consumer binding

### Registry Locations
HKLM\SOFTWARE\Microsoft\WBEM\ESS

### WMI Classes to Monitor
- `__EventFilter`
- `CommandLineEventConsumer`
- `ActiveScriptEventConsumer`
- `__FilterToConsumerBinding`

## Troubleshooting

### "Access denied" errors
- Ensure running with administrator privileges
- Check User Account Control (UAC) settings
- Verify WMI service is running

### "WMI service unavailable"
```bash
# Check WMI service status
sc query winmgmt

# Start WMI service if stopped
net start winmgmt
```

### PowerShell execution policy
```powershell
# Check current policy
Get-ExecutionPolicy

# Temporarily bypass (admin required)
Set-ExecutionPolicy Bypass -Scope Process
```

## References

- [MITRE ATT&CK T1546.003](https://attack.mitre.org/techniques/T1546/003/) - WMI Event Subscription
- [Microsoft WMI Documentation](https://docs.microsoft.com/en-us/windows/win32/wmisdk/)
- [WMI Event Subscriptions](https://docs.microsoft.com/en-us/windows/win32/wmisdk/receiving-event-notifications-through-wmi)

## License

MIT License - See LICENSE file for details

## Disclaimer

This tool is provided for educational and research purposes only. The authors assume no liability for misuse or damage caused by this program. Use responsibly and only on systems you are authorized to test.

## Author

Maxwell Cross - 30 Days of Red Team Series

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.
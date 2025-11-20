# Windows Service Persistence Framework

**Educational tool for demonstrating Windows service persistence techniques**

⚠️ **WARNING**: This tool is for educational purposes and authorized security testing only. Unauthorized use is illegal and unethical.

## Overview

Comprehensive framework for creating, modifying, and detecting Windows service-based persistence mechanisms. Part of the "30 Days of Red Team" series.

## Features

- **3 Service Creation Methods**
  - Direct service creation
  - C# wrapper for non-service binaries
  - Modify existing services

- **Detection & Scanning**
  - Scan for suspicious services
  - Identify hidden services
  - Find risky SYSTEM service configurations

- **Automatic Cleanup**
  - Generate removal scripts
  - Generate restore scripts
  - Complete forensic reporting

- **Flexible Usage**
  - Command-line interface
  - Python API
  - Batch operations

## Installation
```bash
# Clone repository
git clone https://github.com/yourusername/service-persistence.git
cd service-persistence

# Install package
pip install -e .

# Or run directly
python main.py --help
```

## Usage

### Command Line Interface
```bash
# Create new service
python main.py --create C:\payload.exe --service-name WindowsUpdateService

# Create service with C# wrapper (for non-service binaries)
python main.py --create-wrapper "powershell -enc BASE64PAYLOAD"

# Create delayed-start service
python main.py --create C:\payload.exe --start-type delayed

# Modify existing service
python main.py --modify UpdateOrchestrator --new-binary C:\malicious.exe

# Scan for suspicious services
python main.py --check-suspicious

# List all services
python main.py --list

# List running services only
python main.py --list-running

# Delete service
python main.py --delete WindowsUpdateService
```

### Python API
```python
from service_persistence import ServicePersistenceOrchestrator

orchestrator = ServicePersistenceOrchestrator()

# Create new service
result = orchestrator.create_service(
    payload_path=r"C:\payload.exe",
    service_name="WindowsUpdateService",
    display_name="Windows Update Service",
    description="Provides system update functionality",
    method="create",
    start_type="auto"
)

# Create wrapped service (for non-service binaries)
result = orchestrator.create_service(
    payload_command="powershell -enc BASE64PAYLOAD",
    service_name="TelemetryService",
    method="wrapper"
)

# Modify existing service
result = orchestrator.modify_service(
    service_name="UpdateOrchestrator",
    new_binary_path=r"C:\malicious.exe"
)

# Scan for suspicious services
report = orchestrator.scan_services()

# List all services
services = orchestrator.list_all_services()

# Delete service
result = orchestrator.delete_service("WindowsUpdateService")

# Cleanup all created/modified services
cleanup_results = orchestrator.cleanup_all()
```

## Architecture
```
service_persistence/
├── config.py                  # Configuration and constants
├── main.py                    # CLI entry point
│
├── core/
│   ├── utils.py              # Shared utilities
│   └── orchestrator.py       # Main coordinator
│
├── methods/
│   ├── create.py             # Direct service creation
│   ├── wrapper.py            # C# wrapper creation
│   └── modify.py             # Modify existing services
│
├── detection/
│   └── scanner.py            # Suspicious service detection
│
└── output/
└── removal.py            # Script generation
```

## Service Creation Methods

### 1. Direct Service Creation
Creates a Windows service directly from a service-compatible executable:
```python
orchestrator.create_service(
    payload_path=r"C:\service.exe",
    method="create"
)
```

### 2. C# Wrapper Method
Creates a C# wrapper service that executes non-service binaries:
```python
orchestrator.create_service(
    payload_command="powershell -enc BASE64",
    method="wrapper"
)
```

### 3. Service Modification
Modifies an existing service's binary path:
```python
orchestrator.modify_service(
    service_name="ExistingService",
    new_binary_path=r"C:\malicious.exe"
)
```

## Detection Capabilities

The framework includes comprehensive detection features:

- **Suspicious Path Detection**: Identifies services in unusual locations
- **Suspicious Executable Detection**: Flags services using LOLBins
- **Command Argument Analysis**: Detects suspicious command patterns
- **Hidden Service Detection**: Finds services with suspicious naming
- **SYSTEM Service Risk Analysis**: Identifies risky privilege configurations

## Output & Cleanup

### Automatic Removal Scripts
Each service creation generates a removal batch script:
```batch
@echo off
sc stop "ServiceName"
sc delete "ServiceName"
del /f /q "C:\Users\Public\ServiceName.cs"
del /f /q "C:\Users\Public\ServiceName.exe"
```

### Restore Scripts
Service modifications generate restore scripts:
```batch
@echo off
sc stop "ServiceName"
sc config "ServiceName" binPath= "C:\original\path.exe"
sc start "ServiceName"
```

### Forensic Reports
Generate comprehensive reports of all operations:
```python
from output.removal import generate_forensic_report

report_path = generate_forensic_report(
    services_data=orchestrator.created_services
)
```

## Requirements

- **Operating System**: Windows 7+ (Windows 10/11 recommended)
- **Privileges**: Administrator rights required for service operations
- **Python**: Python 3.7+
- **.NET Framework**: Required for wrapper method (typically pre-installed)

## Security Considerations

### Legitimate Use Cases
- Security research and education
- Penetration testing (authorized)
- Red team exercises (authorized)
- Defensive security testing
- Malware analysis research

### Detection Evasion
This tool demonstrates techniques that may be detected by:
- Windows Event Logs (Service Control Manager events)
- EDR/AV solutions
- SIEM correlation rules
- Service configuration monitoring
- Binary reputation systems

### Ethical Guidelines
- Only use on systems you own or have explicit permission to test
- Document all operations for review and cleanup
- Use generated cleanup scripts to remove persistence
- Follow responsible disclosure practices
- Comply with all applicable laws and regulations

## Detection Indicators

### Event Logs
- Event ID 7045: New service installed
- Event ID 7040: Service start type changed
- Event ID 4697: Service installed (Security log)

### Suspicious Indicators
- Services in user-writable directories
- Services executing PowerShell/cmd.exe
- Services with encoded commands
- Hidden or misnamed services
- SYSTEM services with user-writable binaries

## Troubleshooting

### "Service failed to start"
- Ensure binary is service-compatible or use wrapper method
- Check binary exists at specified path
- Verify service account permissions

### "Compilation failed"
- Ensure .NET Framework is installed
- Check compiler paths in config.py
- Verify source code syntax

### "Access denied"
- Run with administrator privileges
- Check UAC settings
- Verify user has service creation rights

## References

- [MITRE ATT&CK T1543.003](https://attack.mitre.org/techniques/T1543/003/) - Windows Service
- [Windows Service Control Manager](https://docs.microsoft.com/en-us/windows/win32/services/service-control-manager)
- [sc.exe Command Reference](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/sc-create)

## License

MIT License - See LICENSE file for details

## Disclaimer

This tool is provided for educational and research purposes only. The authors assume no liability for misuse or damage caused by this program. Use responsibly and only on systems you are authorized to test.

## Author

Maxwell Cross - 30 Days of Red Team Series

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.
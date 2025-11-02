"""
# Situational Awareness Suite

Comprehensive post-exploitation enumeration framework for red team operations.

## Installation

```bash
# Method 1: Install as package
pip install -e .

# Method 2: Run directly
python3 -m situational_awareness --help
```

## Usage

### Quick Enumeration
```bash
# Essential enumeration only (system, user, network)
python3 -m situational_awareness --quick
```

### Full Enumeration
```bash
# Comprehensive enumeration (all modules)
python3 -m situational_awareness --full
```

### Output Formats
```bash
# JSON output (default)
python3 -m situational_awareness --full --output json

# Text output
python3 -m situational_awareness --full --output text
```

## Module Structure

```
situational_awareness/
├── __init__.py              # Package initialization
├── main.py                  # CLI entry point
├── core/
│   ├── __init__.py
│   ├── base.py             # Main orchestrator
│   └── utils.py            # Shared utilities
├── modules/
│   ├── __init__.py
│   ├── system.py           # System information
│   ├── user.py             # User & privileges
│   ├── network.py          # Network configuration
│   ├── processes.py        # Running processes
│   ├── files.py            # File system enumeration
│   ├── security.py         # Security products
│   └── tasks.py            # Scheduled tasks
└── output/
    ├── __init__.py
    └── formatters.py       # Output formatting
```

## Features

### System Enumeration
- OS type, version, and architecture
- Kernel version (Linux)
- Installed hotfixes (Windows)
- Container detection (Docker, etc.)

### User Enumeration
- Current user and privileges
- Group memberships
- Sudo rights (Linux)
- Admin status (Windows)

### Network Enumeration
- Network interfaces and IP addresses
- Routing tables
- Active connections
- DNS configuration
- ARP table

### Process Enumeration
- All running processes
- Interesting processes (databases, web servers, etc.)
- Process details

### File Enumeration
- Configuration files
- Credential files
- SSH keys
- Database files
- Backup files
- Writable directories

### Security Detection
- Antivirus products
- EDR solutions
- Firewall status

### Task Enumeration
- Cron jobs (Linux)
- Scheduled tasks (Windows)
- System-wide scheduled tasks

## Output Files

### JSON Output
Complete enumeration results in JSON format:
```
enum_hostname_20251030_143215.json
```

### Summary Output
Human-readable summary with key findings:
```
enum_hostname_20251030_143215_summary.txt
```

## Examples

### Example 1: Quick Check on Compromised Host
```bash
# Run quick enumeration
python3 -m situational_awareness --quick

# Review results
cat enum_*_summary.txt
```

### Example 2: Full Enterprise Assessment
```bash
# Run full enumeration
python3 -m situational_awareness --full

# Analyze JSON for automation
python3 -c "import json; data = json.load(open('enum_*.json')); print(data['user_info'])"
```

### Example 3: Programmatic Usage
```python
from situational_awareness import SituationalAwareness

# Create instance
sa = SituationalAwareness(output_format='json')

# Run enumeration
sa.run_full_enumeration()

# Access results
print(sa.results['user_info'])
print(sa.results['network_info'])
```

## Platform Support

- ✅ Linux (Ubuntu, CentOS, Debian, etc.)
- ✅ Windows (7, 8, 10, 11, Server)
- ⚠️ macOS (partial support)

## Requirements

- Python 3.7+
- Standard library only (no external dependencies)

## Security & Ethics

**WARNING**: This tool is designed for authorized penetration testing and red team operations only.

- ✅ Only use on systems you have explicit written permission to test
- ✅ Follow all applicable laws and regulations
- ✅ Protect all collected data appropriately
- ❌ Never use on systems without authorization
- ❌ Do not use for malicious purposes

Unauthorized access to computer systems is illegal and unethical.

## License

[Your License Here]

## Contributing

Contributions welcome! Please follow the existing code structure and include tests.
"""
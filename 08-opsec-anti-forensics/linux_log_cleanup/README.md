# Linux Log Cleanup Framework

A modular Python framework for comprehensive Linux log cleaning and anti-forensics operations.

## 📁 Project Structure

```
linux_log_cleanup/
├── __init__.py                      # Main package initialization
├── main.py                          # CLI entry point
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── core/                            # Core functionality
│   ├── __init__.py
│   ├── constants.py                 # Log paths and constants
│   └── base_cleaner.py             # Main LinuxLogCleaner class
├── cleaners/                        # Specialized cleaners
│   ├── __init__.py
│   ├── text_log_cleaner.py         # Text log cleaner (auth, syslog)
│   ├── binary_log_cleaner.py       # Binary log cleaner (wtmp, utmp)
│   └── rotation_cleaner.py         # Rotated log cleaner
├── utils/                           # Utility functions
│   ├── __init__.py
│   ├── helpers.py                   # General helpers
│   └── permissions.py               # Permission management
└── examples/                        # Example scripts
    └── demo.py                      # Usage demonstrations
```

## 🚀 Features

### Text Log Cleaning
- Clean authentication logs (auth.log, secure)
- Clean system logs (syslog, messages)
- Clean audit logs
- Filter by username, IP address, or keywords
- Pattern-based filtering

### Binary Log Cleaning
- Clean wtmp (login records)
- Clean utmp (current logins)
- Clean lastlog (last login times)
- Clean btmp (failed login attempts)
- Preserve record structure

### Rotated Log Management
- Delete rotated logs (*.1, *.2, etc.)
- Delete compressed logs (*.gz, *.bz2, *.xz)
- Recursive directory cleaning
- Dry-run mode for safety

### Additional Features
- Bash history cleaning
- Automatic backup creation
- Permission management
- Comprehensive cleanup mode
- Root privilege checking

## 📋 Requirements

- Python 3.6+
- Linux operating system
- Root/sudo privileges (for most operations)

## 🔧 Installation

### Option 1: Direct Usage
```bash
# Clone or download the project
cd linux_log_cleanup

# Install dependencies (minimal)
pip install -r requirements.txt

# Run with sudo
sudo python main.py --help
```

### Option 2: Install as Package
```bash
# From project directory
pip install -e .

# Use from anywhere
sudo python -m linux_log_cleanup --help
```

## 💻 Usage

### Comprehensive Cleanup
```bash
# Clean all logs for specific user
sudo python main.py --comprehensive --username attacker --ip 10.10.14.5 --keywords "sudo" "ssh"
```

### Clean Specific Logs

**Authentication logs:**
```bash
sudo python main.py --clean-auth --username attacker --ip 192.168.1.100
```

**System logs:**
```bash
sudo python main.py --clean-syslog --keywords "failed" "error"
```

**Binary logs:**
```bash
# wtmp (login records)
sudo python main.py --clean-wtmp --username attacker

# utmp (current logins)
sudo python main.py --clean-utmp --username attacker

# lastlog (last login times)
sudo python main.py --clean-lastlog --username attacker
```

**Shell history:**
```bash
sudo python main.py --clean-bash-history --username attacker
```

**Rotated logs:**
```bash
# Clean all rotated logs
sudo python main.py --clean-rotated

# Dry run (see what would be deleted)
sudo python main.py --clean-rotated --dry-run

# List rotated logs (no root required)
python main.py --list-rotated
```

### Safety Options

**Skip backups (dangerous!):**
```bash
sudo python main.py --clean-auth --username attacker --no-backup
```

**Dry run:**
```bash
sudo python main.py --clean-rotated --dry-run
```

## 📚 Module Usage

### Using as Python Library

```python
from linux_log_cleanup import LinuxLogCleaner, LogRotationCleaner

# Initialize cleaner
cleaner = LinuxLogCleaner()

# Clean auth log
cleaner.clean_auth_log(username="attacker", ip_address="10.10.14.5")

# Clean wtmp
cleaner.clean_wtmp(username="attacker")

# Comprehensive cleanup
results = cleaner.comprehensive_cleanup(
    username="attacker",
    ip_address="10.10.14.5",
    keywords=["sudo", "ssh"]
)

# Clean rotated logs
rotation_cleaner = LogRotationCleaner()
count = rotation_cleaner.clean_rotated_logs("/var/log")
```

### Advanced Usage

```python
from linux_log_cleanup.cleaners import TextLogCleaner, BinaryLogCleaner

# Text log cleaning with patterns
text_cleaner = TextLogCleaner()
text_cleaner.clean_by_pattern(
    "/var/log/auth.log",
    [r"Failed password.*", r"authentication failure.*"]
)

# Binary log analysis
binary_cleaner = BinaryLogCleaner()
usernames = binary_cleaner.dump_records("/var/log/wtmp", "wtmp", max_records=10)
print(f"Found users: {usernames}")
```

## 🔍 Log File Locations

### Common Linux Logs

| Log File | Location | Purpose |
|----------|----------|---------|
| auth.log | /var/log/auth.log | Authentication (Debian/Ubuntu) |
| secure | /var/log/secure | Authentication (RHEL/CentOS) |
| syslog | /var/log/syslog | System messages (Debian/Ubuntu) |
| messages | /var/log/messages | System messages (RHEL/CentOS) |
| wtmp | /var/log/wtmp | Login records (binary) |
| utmp | /var/run/utmp | Current logins (binary) |
| lastlog | /var/log/lastlog | Last login times (binary) |
| btmp | /var/log/btmp | Failed login attempts (binary) |
| audit.log | /var/log/audit/audit.log | Audit daemon logs |

## ⚠️ Important Notes

### Binary Log Structure

The framework handles binary logs (wtmp, utmp, lastlog) with:
- **Record Size**: 384 bytes (64-bit systems)
- **Username Offset**: 32 bytes
- **Username Size**: 32 bytes

Different architectures may have different record sizes.

### Backup Files

By default, backups are created as:
```
/var/log/auth.log.backup-20241220143022
```

Timestamp format: `YYYYMMDDHHmmss`

### Rotated Log Patterns

Automatically detects and cleans:
- Numbered rotations: `*.1`, `*.2`, `*.3`
- Compressed rotations: `*.gz`, `*.bz2`, `*.xz`

## 🛡️ Security Considerations

### Authorization Required
- **Only use on systems you own** or have explicit permission to test
- **Legal compliance**: Log manipulation may be illegal in many jurisdictions
- **Audit trail**: Actions may be logged on remote systems

### Best Practices
- Always create backups (don't use `--no-backup`)
- Test on isolated systems first
- Understand log structure before manipulation
- Use selective deletion over full log clearing
- Check for remote logging (syslog forwarding)

### Detection Risks
- Sudden log size changes can trigger alerts
- Missing log entries create timeline gaps
- Backup files may be detected if not cleaned
- Remote logging systems retain copies

## 🛠️ Development

### Adding New Log Types

**Add log path:**
```python
# Edit core/constants.py
LOG_PATHS = {
    'new_log': '/var/log/new.log',
    # ...
}
```

**Add cleaning method:**
```python
# Edit core/base_cleaner.py
def clean_new_log(self, preserve_backup=True):
    log_path = self.log_files['new_log']
    # Implementation...
```

### Testing

```bash
# Test with dry run
sudo python main.py --clean-rotated --dry-run

# Test on non-critical logs
sudo python main.py --clean-syslog --keywords "test"

# Verify backups created
ls -la /var/log/*.backup-*
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
  - Text log cleaning
  - Binary log cleaning
  - Rotation cleaning
  - Comprehensive cleanup mode

## 🎯 Roadmap

- [ ] Systemd journal cleaning
- [ ] Time-based filtering for text logs
- [ ] Cloud logging integration
- [ ] Automated cleanup scheduling
- [ ] Log injection (false entries)
- [ ] Multi-system cleanup
- [ ] GUI interface

## 🔗 Related Projects

- Windows Log Manipulation Framework (companion project)
- Timestamp Stomping Toolkit
- Secure File Deletion Framework
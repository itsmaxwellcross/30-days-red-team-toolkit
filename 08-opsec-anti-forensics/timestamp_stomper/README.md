# Timestamp Stomping Toolkit

A modular Python framework for file timestamp manipulation and forensic anti-detection.

## 📁 Project Structure

```
timestamp_stomper/
├── __init__.py                      # Main package initialization
├── main.py                          # CLI entry point
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── core/                            # Core functionality
│   ├── __init__.py
│   ├── constants.py                 # Configuration and constants
│   └── timestamp_stomper.py        # Main TimestampStomper class
├── platforms/                       # Platform-specific handlers
│   ├── __init__.py
│   ├── handler.py                   # Base handler and factory
│   ├── windows_handler.py          # Windows implementation
│   └── unix_handler.py             # Unix/Linux implementation
├── analyzers/                       # Timestamp analysis
│   ├── __init__.py
│   └── macb_analyzer.py            # MACB anomaly detection
├── utils/                           # Utility functions
│   ├── __init__.py
│   └── helpers.py                   # Helper functions
└── examples/                        # Example scripts
    └── demo.py                      # Usage demonstrations
```

## 🚀 Features

### Timestamp Manipulation
- **Copy timestamps** from legitimate files
- **Match timestamps** to directory averages
- **Set random past** timestamps
- **Set specific** timestamps
- **Bulk operations** on entire directories
- **Platform-specific** handling (Windows/Unix)

### Timestamp Analysis
- **MACB analysis** (Modified, Accessed, Changed, Birth)
- **Anomaly detection** for tampered files
- **Batch analysis** of directories
- **Timestamp comparison** between files

### Platform Support
- **Windows**: Full support including creation time via win32file
- **Unix/Linux**: Access and modification time (creation time limited)
- **Automatic detection** of platform and appropriate handler

## 📋 Requirements

- Python 3.6+
- Windows or Unix/Linux operating system

**Optional (for Windows creation time):**
- `pywin32` - For Windows creation time manipulation

## 🔧 Installation

### Option 1: Direct Usage
```bash
# Clone or download the project
cd timestamp_stomper

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
python -m timestamp_stomper --help
```

### Windows-Specific Setup
For full Windows support (including creation time):
```bash
pip install pywin32
```

## 💻 Usage

### Display Timestamps
```bash
python main.py --file malware.exe --display
```

### Copy Timestamps from Legitimate File
```bash
# Windows
python main.py --file malware.exe --copy-from C:\Windows\System32\notepad.exe

# Linux
python main.py --file malware.sh --copy-from /bin/ls
```

### Match Directory Average
```bash
python main.py --file suspicious.dll --match-dir C:\Windows\System32
```

### Set Random Past Timestamp
```bash
# Random between 30-365 days ago
python main.py --file tool.exe --random-past

# Custom range (60-180 days ago)
python main.py --file tool.exe --random-past --days-min 60 --days-max 180
```

### Set Specific Timestamp
```bash
# Format: year month day hour minute second
python main.py --file document.doc --specific 2023 6 15 14 30 0
```

### Analyze for Anomalies
```bash
# Single file
python main.py --file suspicious.exe --analyze

# Compare two files
python main.py --file file1.txt --compare file2.txt

# Batch analyze directory
python main.py --batch-analyze /path/to/directory
```

### Bulk Operations
```bash
# Bulk stomp with reference file
python main.py --bulk-stomp /path/to/tools --reference /bin/ls

# Bulk stomp with random timestamps
python main.py --bulk-stomp /path/to/tools --days-min 90 --days-max 180
```

### Find Legitimate Reference
```bash
# Find legitimate system file for reference
python main.py --find-reference
```

## 📚 Module Usage

### Using as Python Library

```python
from timestamp_stomper import TimestampStomper, MACBAnalysis

# Initialize stomper
stomper = TimestampStomper()

# Display timestamps
stomper.display_file_times("file.exe")

# Copy timestamps
stomper.copy_timestamps("legitimate.exe", "malware.exe")

# Set random past timestamp
stomper.set_random_past_time("file.exe", days_ago_min=30, days_ago_max=365)

# Match directory average
stomper.match_directory_times("file.exe", "C:\\Windows\\System32")

# Analyze for anomalies
MACBAnalysis.analyze_macb("suspicious.exe")
```

### Advanced Usage

```python
# Set specific timestamp
stomper.set_specific_time("file.txt", 2023, 6, 15, 14, 30, 0)

# Bulk operation
stomper.bulk_stomp("/path/to/directory", reference_file="/bin/ls")

# Compare timestamps
MACBAnalysis.compare_timestamps("file1.txt", "file2.txt")

# Batch analyze
MACBAnalysis.batch_analyze("/path/to/directory")
```

## 🔍 MACB Analysis

### What is MACB?

MACB stands for:
- **M**odified - Last modification time
- **A**ccessed - Last access time
- **C**hanged - Metadata change time (Unix) or Creation time (Windows)
- **B**irth - True creation time (where available)

### Detected Anomalies

The analyzer detects:
- ⚠️ File accessed before creation
- ⚠️ File modified before creation
- ⚠️ Timestamps in the future
- ⚠️ Identical timestamps (suspicious)
- ⚠️ All timestamps identical (likely stomped)
- ⚠️ Modified after last access (unusual)

### Example Output

```
[*] MACB Analysis: suspicious.exe
============================================================
Modified: 2024-01-15 14:23:17
Accessed: 2024-01-15 14:23:17
Created:  2024-01-15 14:23:17

[!] ANOMALIES DETECTED:
    ⚠️  Access and modify times identical (suspicious)
    ⚠️  All timestamps identical (likely stomped)
```

## ⚠️ Platform Differences

### Windows
- ✅ Full support for all timestamps
- ✅ Can modify creation time (with pywin32)
- ✅ Accurate MACB analysis

### Unix/Linux
- ✅ Full support for access and modification times
- ⚠️ Limited creation time support
  - `st_ctime` is metadata change time, not creation time
  - True birth time only available on some filesystems
- ⚠️ Cannot directly modify creation/birth time

## 🛡️ OPSEC Considerations

### Best Practices

1. **Match Legitimate Files**
   - Copy timestamps from similar legitimate files
   - Use system files as reference

2. **Match Directory Context**
   - Match timestamps to surrounding files
   - Avoid standing out in timeline analysis

3. **Avoid Obvious Patterns**
   - Don't make all timestamps identical
   - Don't use future timestamps
   - Don't use obviously rounded times

4. **Test Before Use**
   - Test on isolated systems first
   - Verify timestamps after manipulation
   - Check for anomalies

### Detection Risks

Forensic investigators look for:
- Future timestamps
- Timestamps before file creation
- All timestamps identical
- Timestamps that don't match file context
- Clustered timestamp modifications

## 🛠️ Development

### Adding Custom Platform Handler

```python
# Create new handler in platforms/
from .handler import BasePlatformHandler

class CustomHandler(BasePlatformHandler):
    def get_file_times(self, filepath):
        # Implementation
        pass
    
    def set_file_times(self, filepath, accessed, modified, created):
        # Implementation
        pass

# Update handler.py factory
def get_platform_handler():
    if condition:
        return CustomHandler()
```

### Adding Custom Analysis

```python
# Add to analyzers/macb_analyzer.py
@staticmethod
def custom_analysis(filepath):
    # Custom analysis logic
    pass
```

## 📄 License

For authorized security testing and educational purposes only.

## ⚖️ Legal Disclaimer

This tool is provided for **authorized security testing and educational purposes only**.

- Timestamp manipulation may be illegal in many jurisdictions
- Always obtain written permission before testing
- Evidence tampering is a serious crime
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
  - Timestamp manipulation
  - MACB analysis
  - Platform-specific handlers
  - Bulk operations

## 🎯 Roadmap

- [ ] Extended filesystem support
- [ ] Timeline generation
- [ ] Integration with forensic tools
- [ ] Cloud file timestamp manipulation
- [ ] Automated OPSEC recommendations
- [ ] GUI interface

## 🔗 Related Projects

- Linux Log Cleanup Framework
- Windows Log Manipulation Framework
- Secure File Deletion Framework
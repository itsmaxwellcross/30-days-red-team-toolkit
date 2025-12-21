# Secure File Deletion Framework

A modular Python framework for secure file deletion and forensic artifact cleanup.

## 📁 Project Structure

```
secure_delete/
├── __init__.py                      # Main package initialization
├── main.py                          # CLI entry point
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── core/                            # Core functionality
│   ├── __init__.py
│   ├── constants.py                 # Configuration and standards
│   └── secure_delete.py            # Main SecureDelete class
├── methods/                         # Overwrite methods
│   ├── __init__.py
│   └── overwrite_methods.py        # Deletion standards (DoD, Gutmann)
├── cleaners/                        # Artifact cleaners
│   ├── __init__.py
│   └── artifact_cleaner.py         # Forensic artifact cleanup
├── utils/                           # Utility functions
│   ├── __init__.py
│   └── helpers.py                   # Helper functions
└── examples/                        # Example scripts
    └── demo.py                      # Usage demonstrations
```

## 🚀 Features

### Secure Deletion Methods
- **Random Data**: Cryptographically secure random overwriting
- **Zeros/Ones**: Simple pattern overwriting
- **DoD 5220.22-M**: US Department of Defense standard (3 passes)
- **Gutmann Method**: Thorough 35-pass deletion
- **Custom Patterns**: Define your own overwrite patterns

### File Operations
- **Single File Deletion**: Securely delete individual files
- **Directory Deletion**: Recursive secure deletion
- **Free Space Wiping**: Overwrite unused disk space
- **Bulk Operations**: Process multiple files efficiently

### Artifact Cleaning
- **Temporary Files**: Clean system temp directories
- **Browser History**: Remove browser artifacts
- **Windows Prefetch**: Clean Windows Prefetch files
- **Windows MRU**: Clean Most Recently Used lists
- **Recycle Bin**: Empty Recycle Bin

## 📋 Requirements

- Python 3.6+
- Operating System: Windows, Linux, or macOS

**Optional (for Windows features):**
- `pywin32` - For Windows registry operations

## 🔧 Installation

### Option 1: Direct Usage
```bash
# Clone or download the project
cd secure_delete

# Install dependencies (optional)
pip install -r requirements.txt

# Run directly
python main.py --help
```

### Option 2: Install as Package
```bash
# From project directory
pip install -e .

# Use from anywhere
python -m secure_delete --help
```

## 💻 Usage

### Secure File Deletion

**Basic deletion (3 random passes):**
```bash
python main.py --file sensitive.doc
```

**Specify number of passes:**
```bash
python main.py --file document.pdf --passes 7
```

**Use specific method:**
```bash
# DoD standard (3 passes: ones, zeros, random)
python main.py --file data.txt --method dod

# Gutmann method (35 passes)
python main.py --file classified.docx --method gutmann

# Simple zeros
python main.py --file temp.log --method zeros
```

### Directory Deletion

```bash
# Securely delete entire directory
python main.py --directory /path/to/tools --passes 3 --method random
```

### Free Space Wiping

```bash
# Wipe 100 MB of free space
python main.py --wipe-free-space C:\ --size-mb 100

# Wipe 1 GB of free space
python main.py --wipe-free-space /tmp --size-mb 1024
```

### Artifact Cleaning

```bash
# Comprehensive cleanup (all artifacts)
python main.py --clean-artifacts

# Clean specific artifacts
python main.py --clean-temp           # Temp files only
python main.py --clean-browser        # Browser history only
python main.py --clean-prefetch       # Windows Prefetch only
python main.py --clean-mru            # Windows MRU only
```

### Information Commands

```bash
# Get information about a deletion method
python main.py --method-info dod

# Get file statistics
python main.py --file-info document.pdf
```

### Safety Options

```bash
# Skip confirmation prompt
python main.py --file data.txt --no-confirm
```

## 📚 Module Usage

### Using as Python Library

```python
from secure_delete import SecureDelete, ArtifactCleaner, OverwriteMethods

# Initialize secure delete
deleter = SecureDelete()

# Delete file with 3 random passes
deleter.secure_delete_file("sensitive.doc", passes=3, method='random')

# Delete using DoD standard
deleter.secure_delete_file("classified.pdf", passes=3, method='dod')

# Delete entire directory
deleter.secure_delete_directory("/path/to/tools", passes=3, method='random')

# Wipe free space
deleter.wipe_free_space("/tmp", size_mb=100)
```

### Artifact Cleaning

```python
from secure_delete import ArtifactCleaner

# Initialize cleaner
cleaner = ArtifactCleaner()

# Comprehensive cleanup
results = cleaner.comprehensive_cleanup()

# Clean specific artifacts
cleaner.clean_temp_files()
cleaner.clean_browser_history()
cleaner.clean_prefetch()  # Windows only
cleaner.clean_mru()       # Windows only
```

### Deletion Methods

```python
from secure_delete import OverwriteMethods

methods = OverwriteMethods()

# Get information about a method
info = methods.get_method_info('dod')
print(info['description'])
print(info['passes'])

# Generate different patterns
random_data = methods.random_data(1024)      # 1 KB random
zero_data = methods.zero_data(1024)          # 1 KB zeros
one_data = methods.one_data(1024)            # 1 KB ones
dod_data = methods.dod_pattern(1024, 0)      # DoD pass 1
gutmann_data = methods.gutmann_pattern(1024, 15)  # Gutmann pass 15
```

## 🔍 Deletion Methods Explained

### Random Data
- **Passes**: User-defined (recommended: 3-7)
- **Security**: High
- **Speed**: Fast
- **Use Case**: General purpose secure deletion

### DoD 5220.22-M
- **Passes**: 3 (ones, zeros, random)
- **Security**: High
- **Speed**: Fast
- **Use Case**: Meets US Department of Defense standard
- **Pattern**:
  - Pass 1: All ones (0xFF)
  - Pass 2: All zeros (0x00)
  - Pass 3: Random data

### Gutmann Method
- **Passes**: 35
- **Security**: Very High
- **Speed**: Slow
- **Use Case**: Maximum security, magnetic media
- **Note**: Designed for older magnetic storage; may be overkill for SSDs

### Zeros/Ones
- **Passes**: User-defined
- **Security**: Low
- **Speed**: Very Fast
- **Use Case**: Quick overwrites, testing

## ⚠️ Important Considerations

### SSD and Modern Storage

**SSDs are different:**
- Wear leveling changes how data is stored
- TRIM commands may prevent overwriting
- Secure erase features are built-in

**Recommendations for SSDs:**
- Use built-in secure erase features
- Enable encryption (then delete encryption key)
- Single pass is usually sufficient

### File System Considerations

**Journaling:**
- ext3/ext4, NTFS, APFS use journaling
- Deleted data may persist in journal
- Consider wiping free space

**Snapshots:**
- Time Machine, Shadow Copies, ZFS snapshots
- Deleted files may remain in snapshots
- Disable or delete snapshots

**Cloud Sync:**
- Dropbox, OneDrive, Google Drive
- Files may persist in cloud
- Delete from cloud separately

## 🛡️ Security Best Practices

### Before Deletion
1. **Verify file path** - Ensure you're deleting the correct file
2. **Check for copies** - Look for backups, temp files, caches
3. **Close applications** - Ensure file isn't in use
4. **Check cloud sync** - Files may be synced to cloud

### During Deletion
1. **Use appropriate method** - Match security level to threat model
2. **Multiple passes** - Use 3-7 passes for critical data
3. **Verify completion** - Check that file is actually deleted

### After Deletion
1. **Wipe free space** - Remove traces from unallocated space
2. **Clean artifacts** - Remove temp files, prefetch, MRU
3. **Verify deletion** - Attempt file recovery to verify
4. **Check backups** - Ensure backups are also cleaned

## 🛠️ Development

### Adding Custom Deletion Method

```python
# In methods/overwrite_methods.py
def custom_method(self, size, pass_num):
    """Your custom deletion method"""
    # Implement your pattern
    return custom_data
```

### Adding Custom Artifact Cleaner

```python
# In cleaners/artifact_cleaner.py
def clean_custom_artifact(self):
    """Clean custom artifact"""
    # Implementation
    pass
```

## 📄 License

For authorized security testing and educational purposes only.

## ⚖️ Legal Disclaimer

This tool is provided for **authorized use only**.

- Destroying evidence may be illegal
- Always obtain written permission
- Understand legal obligations (e.g., data retention laws)
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
  - Multiple deletion methods
  - Artifact cleaning
  - Free space wiping
  - Comprehensive CLI

## 🎯 Roadmap

- [ ] Progress bars for large files
- [ ] Parallel processing for bulk operations
- [ ] Integration with encryption tools
- [ ] Advanced SSD support
- [ ] Network share deletion
- [ ] Scheduled deletion
- [ ] GUI interface

## 🔗 Related Projects

- Linux Log Cleanup Framework
- Windows Log Manipulation Framework
- Timestamp Stomping Toolkit
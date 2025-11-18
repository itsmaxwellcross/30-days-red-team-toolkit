"""
CTF Challenge Generator
Creates all challenge files and structure
"""

import os
import json
import base64
import random
import string
from pathlib import Path
from datetime import datetime


class CTFGenerator:
    """
    Generates complete CTF challenge environment
    """
    
    def __init__(self, output_dir='06-integration/ctf_challenge'):
        self.output_dir = Path(output_dir)
        self.flags = {}
    
    def generate_full_challenge(self):
        """Generate complete challenge"""
        # Create directory structure
        self._create_directories()
        
        # Generate flags
        self._generate_flags()
        
        # Create challenge components
        from ctf.challenges.recon import ReconChallenge
        from ctf.challenges.web_exploit import WebExploitChallenge
        from ctf.challenges.shell_access import ShellAccessChallenge
        from ctf.challenges.enumeration import EnumerationChallenge
        from ctf.challenges.privesc import PrivEscChallenge
        
        ReconChallenge(self.output_dir, self.flags).create()
        WebExploitChallenge(self.output_dir, self.flags).create()
        ShellAccessChallenge(self.output_dir, self.flags).create()
        EnumerationChallenge(self.output_dir, self.flags).create()
        PrivEscChallenge(self.output_dir, self.flags).create()
        
        # Generate documentation
        self._create_documentation()
        
        # Save flags
        self._save_flags()
        
        print(f"[+] Challenge files created in: {self.output_dir}")
    
    def _create_directories(self):
        """Create directory structure"""
        dirs = [
            self.output_dir,
            self.output_dir / 'www',
            self.output_dir / 'www' / 'uploads',
            self.output_dir / 'etc',
            self.output_dir / 'home' / 'admin',
            self.output_dir / 'home' / 'admin' / '.ssh',
            self.output_dir / 'home' / 'backup',
            self.output_dir / 'var' / 'www' / 'html',
            self.output_dir / 'root',
            self.output_dir / 'usr' / 'local' / 'bin',
            self.output_dir / '.git',
            self.output_dir / 'solutions',
        ]
        
        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _generate_flags(self):
        """Generate all flags"""
        self.flags = {
            'flag1_recon': self._generate_flag('RECON'),
            'flag2_exploit': self._generate_flag('EXPLOIT'),
            'flag3_shell': self._generate_flag('SHELL'),
            'flag4_creds': self._generate_flag('CREDENTIALS'),
            'flag5_privesc': self._generate_flag('PRIVESC'),
            'flag6_final': self._generate_flag('COMPLETE')
        }
    
    def _generate_flag(self, prefix):
        """Generate random flag"""
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        return f"FLAG{{{prefix}_{random_part}}}"
    
    def _create_documentation(self):
        """Create README and documentation"""
        readme = f"""# Week 1 CTF Challenge

## Welcome!

This CTF challenge tests all skills learned in Week 1 (Days 1-6) of the Red Team training.

## Quick Start

### Option 1: Use Built-in Server

```bash
# Generate challenge files (if not done)
python3 -m ctf.cli --generate

# Start challenge server
python3 -m ctf.cli --serve

# Access at http://localhost:8080
```

### Option 2: Use Docker

```bash
cd {self.output_dir}
docker-compose up -d

# Access at http://localhost:8080
```

## Objectives

Complete all 6 flags to demonstrate Week 1 mastery:

| Flag | Challenge | Points | Skills Tested |
|------|-----------|--------|---------------|
| 1 | Reconnaissance | 10 | Info gathering, source analysis |
| 2 | Web Exploitation | 15 | SQL injection, vulnerability scanning |
| 3 | Shell Access | 20 | Web shells, reverse shells |
| 4 | Enumeration | 20 | System enumeration, credential harvesting |
| 5 | Privilege Escalation | 25 | SUID exploitation, privilege escalation |
| 6 | Root Access | 10 | Complete attack chain |

**Total: 100 points**

## Challenge Flow

```
[1. Reconnaissance] → [2. Web Exploit] → [3. Shell Access]
                                              ↓
[6. Root Access] ← [5. Privilege Escalation] ← [4. Enumeration]
```

## Flag Format

All flags follow this format:
```
FLAG{{PREFIX_XXXXXXXXXXXXXXXX}}
```

Where:
- PREFIX indicates the challenge type (RECON, EXPLOIT, etc.)
- X's are random alphanumeric characters

## Validation

Submit flags using:
```bash
python3 -m ctf.cli --validate "FLAG{{...}}"
```

Check your progress:
```bash
python3 -m ctf.cli --progress
```

## Hints

Need help? Get hints with:
```bash
python3 -m ctf.cli --hints
```

Or check the detailed walkthrough in `solutions/WALKTHROUGH.md` (try not to cheat!)

## Rules

1. ✅ Use all tools from Week 1 toolkit
2. ✅ Document your methodology
3. ✅ Take screenshots of flags
4. ✅ Time yourself for practice
5. ❌ Don't share flags with others
6. ❌ Don't look at answer key before completing

## Recommended Approach

### Phase 1: Reconnaissance (30 mins)
- Use reconnaissance tools from Day 1-2
- Find Flag 1
- Document findings

### Phase 2: Exploitation (45 mins)
- Use vulnerability scanners
- Exploit web vulnerabilities
- Find Flag 2

### Phase 3: Access (30 mins)
- Upload web shell
- Establish reverse shell
- Find Flag 3

### Phase 4: Enumeration (45 mins)
- Run post-exploitation tools
- Enumerate system thoroughly
- Find Flag 4

### Phase 5: Escalation (60 mins)
- Find privilege escalation vectors
- Exploit to root
- Find Flag 5 and Flag 6

## Tools You'll Need

- `01-reconnaissance/` - All recon tools
- `04-exploitation/` - Exploitation tools
- `05-post-exploitation/` - Post-exploit tools

## Scoring & Time

**Scoring:**
- 100 points total
- 90+ points: Excellent
- 75-89 points: Good
- 60-74 points: Passing
- <60 points: Review Week 1 material

**Time:**
- Beginner: 3-4 hours
- Intermediate: 2-3 hours
- Advanced: 1-2 hours

## Submission

Track your progress:

```
Flag 1 (RECON): _______________
Time: _______________

Flag 2 (EXPLOIT): _______________
Time: _______________

Flag 3 (SHELL): _______________
Time: _______________

Flag 4 (CREDENTIALS): _______________
Time: _______________

Flag 5 (PRIVESC): _______________
Time: _______________

Flag 6 (COMPLETE): _______________
Time: _______________

Total Time: _______________
```

## Troubleshooting

**Server won't start:**
```bash
# Check if port is in use
netstat -tulpn | grep 8080

# Try different port
python3 -m ctf.cli --serve --port 8081
```

**Can't find flags:**
- Check hints: `python3 -m ctf.cli --hints`
- Review Week 1 materials
- Check solutions (last resort)

**Reset challenge:**
```bash
python3 -m ctf.cli --reset
```

## Resources

- Week 1 Materials: `../docs/`
- Tool Documentation: Each tool has `--help`
- Walkthrough: `solutions/WALKTHROUGH.md`
- Hints: Run `--hints` command

## Good Luck!

Remember:
- Document everything
- Try harder before checking hints
- Learn from mistakes
- This is practice for real engagements

---

**Have fun and happy hacking! 🚩**
"""
        
        with open(self.output_dir / 'README.md', 'w') as f:
            f.write(readme)
        
        print("[+] Created README.md")
    
    def _save_flags(self):
        """Save flags to file"""
        flag_data = {
            'generated': datetime.now().isoformat(),
            'flags': self.flags,
            'flag_info': {
                'flag1_recon': {
                    'name': 'Reconnaissance',
                    'points': 10,
                    'description': 'Found through external reconnaissance',
                    'location': 'HTML source code'
                },
                'flag2_exploit': {
                    'name': 'Web Exploitation',
                    'points': 15,
                    'description': 'Found by exploiting SQL injection',
                    'location': 'Login page response'
                },
                'flag3_shell': {
                    'name': 'Shell Access',
                    'points': 20,
                    'description': 'Found after obtaining shell',
                    'location': 'User home directory'
                },
                'flag4_creds': {
                    'name': 'Credential Discovery',
                    'points': 20,
                    'description': 'Found during enumeration',
                    'location': 'Configuration files'
                },
                'flag5_privesc': {
                    'name': 'Privilege Escalation',
                    'points': 25,
                    'description': 'Found through privilege escalation',
                    'location': 'SUID binary exploitation'
                },
                'flag6_final': {
                    'name': 'Complete',
                    'points': 10,
                    'description': 'Final flag as root',
                    'location': '/root/flag.txt'
                }
            }
        }
        
        # Save for validator
        with open(self.output_dir / '.flags.json', 'w') as f:
            json.dump(flag_data, f, indent=2)
        
        # Save answer key (restricted permissions)
        answer_key = "# WEEK 1 CTF - ANSWER KEY\n"
        answer_key += "# DO NOT SHARE WITH PARTICIPANTS\n\n"
        
        for flag_id, flag_value in self.flags.items():
            info = flag_data['flag_info'][flag_id]
            answer_key += f"\n## {info['name']}\n"
            answer_key += f"Flag: {flag_value}\n"
            answer_key += f"Points: {info['points']}\n"
            answer_key += f"Location: {info['location']}\n"
        
        answer_file = self.output_dir / 'solutions' / 'ANSWER_KEY.txt'
        with open(answer_file, 'w') as f:
            f.write(answer_key)
        
        os.chmod(answer_file, 0o600)
        print("[+] Saved flags and answer key")
    
    def reset_challenge(self):
        """Reset challenge to initial state"""
        # Remove progress file if exists
        progress_file = self.output_dir / '.progress.json'
        if progress_file.exists():
            progress_file.unlink()
        
        print("[+] Challenge reset")
    
    def show_all_flags(self):
        """Show all flags (admin only)"""
        flag_file = self.output_dir / '.flags.json'
        
        if not flag_file.exists():
            print("[-] Flags not generated yet")
            return
        
        with open(flag_file, 'r') as f:
            data = json.load(f)
        
        print("\n" + "="*70)
        print("ALL FLAGS (ADMIN VIEW)")
        print("="*70)
        
        for flag_id, flag_value in data['flags'].items():
            info = data['flag_info'][flag_id]
            print(f"\n{info['name']}:")
            print(f"  Flag: {flag_value}")
            print(f"  Points: {info['points']}")
            print(f"  Location: {info['location']}")
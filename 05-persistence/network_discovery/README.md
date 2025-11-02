# Network Discovery & Lateral Movement Reconnaissance

Internal network mapping tool for post-exploitation and red team operations.

## ⚠️ Legal Warning

**This tool is for authorized penetration testing and red team operations ONLY.**

- ✅ Only use on networks with explicit written authorization
- ✅ Follow all applicable laws and regulations
- ❌ Unauthorized network scanning is illegal
- ❌ Tool misuse can result in criminal prosecution

## Installation

```bash
# Method 1: Install as package
pip install -e .

# Method 2: Install with optional dependencies
pip install -e .[full]

# Method 3: Run directly
python3 -m network_discovery
```

## Features

### Network Scanning
- **Interface Discovery**: Detect local network interfaces and IP addresses
- **Host Discovery**: Ping sweep and ARP scanning
- **Port Scanning**: Multi-threaded scanning of common lateral movement ports
- **Service Identification**: Identify services running on discovered ports

### SMB Enumeration
- Enumerate SMB shares on discovered hosts
- Identify admin shares (C$, ADMIN$, IPC$)
- Cross-platform support (Windows net view, Linux smbclient)

### Active Directory Enumeration
- Domain membership detection
- Domain controller identification
- Domain user enumeration
- Domain computer enumeration
- Domain admin discovery

### Output
- JSON results file with all discovery data
- Lateral movement targets file with prioritized systems
- High-value target identification (DCs, databases, admin workstations)

## Usage

### Basic Usage
```bash
# Full discovery
python3 -m network_discovery

# Quick scan (no domain enum)
python3 -m network_discovery --quick

# Limit port scanning
python3 -m network_discovery --max-hosts 5
```

### Programmatic Usage
```python
from network_discovery import NetworkDiscovery

# Create instance
discovery = NetworkDiscovery()

# Run full discovery
discovery.run_network_discovery()

# Access results
print(f"Found {len(discovery.discovered_hosts)} hosts")
print(f"Found {len(discovery.discovered_services)} services")
```

### Use Individual Modules
```python
from network_discovery.scanners import HostDiscovery, PortScanner
from network_discovery.enumeration import SMBEnumerator

# Host discovery only
host_discovery = HostDiscovery()
hosts = host_discovery.ping_sweep('192.168.1.0/24')

# Port scanning only
port_scanner = PortScanner()
services = port_scanner.scan_host('192.168.1.100')

# SMB enumeration only
smb = SMBEnumerator()
shares = smb.enumerate_shares('192.168.1.100')
```

## Module Structure

```
network_discovery/
├── __init__.py                    # Package initialization
├── main.py                        # CLI entry point
├── core/
│   ├── __init__.py
│   ├── base.py                   # Main orchestrator
│   └── utils.py                  # Shared utilities
├── scanners/
│   ├── __init__.py
│   ├── interfaces.py             # Interface discovery
│   ├── host_discovery.py         # Ping/ARP scanning
│   └── port_scanner.py           # Port scanning
├── enumeration/
│   ├── __init__.py
│   ├── smb.py                    # SMB enumeration
│   ├── domain.py                 # Active Directory
│   └── access.py                 # Access checking
└── output/
    ├── __init__.py
    └── formatters.py             # Output formatting
```

## Scanning Workflow

1. **Interface Discovery** - Identify local network interfaces and IPs
2. **ARP Scan** - Quick discovery of hosts on local segment
3. **Ping Sweep** - Discover live hosts on network ranges
4. **Port Scan** - Scan common lateral movement ports on discovered hosts
5. **Service Enumeration** - Enumerate SMB shares and other services
6. **Domain Enumeration** - If domain-joined, enumerate AD objects
7. **Output Generation** - Save JSON results and lateral movement targets

## Output Files

### network_discovery_TIMESTAMP.json
Complete discovery results in JSON format:
```json
{
  "timestamp": "20251030_143215",
  "local_interfaces": [
    {
      "interface": "eth0",
      "ip": "192.168.1.50",
      "netmask": "255.255.255.0"
    }
  ],
  "discovered_hosts": [
    {
      "ip": "192.168.1.1",
      "status": "alive",
      "discovery_method": "ping"
    }
  ],
  "discovered_services": [
    {
      "ip": "192.168.1.100",
      "port": 445,
      "service": "SMB",
      "state": "open"
    }
  ],
  "smb_shares": [...],
  "domain_info": {...}
}
```

### lateral_movement_targets_TIMESTAMP.txt
Prioritized targets for lateral movement:
```
# Lateral Movement Targets
# Generated: 20251030_143215

## High-Value Targets

[Domain Controller]
DC01.CORPORATE.LOCAL

[Systems with Open Admin Shares]
192.168.1.100
192.168.1.150

[RDP Targets]
192.168.1.200
192.168.1.201

[SSH Targets]
192.168.1.10
192.168.1.20

[Database Servers]
192.168.1.50:1433 - MSSQL
192.168.1.60:3306 - MySQL
```

## Common Ports Scanned

| Port | Service | Use Case |
|------|---------|----------|
| 22 | SSH | Remote access, credential reuse |
| 80/443 | HTTP/HTTPS | Web applications, admin panels |
| 135/139/445 | RPC/SMB | File shares, lateral movement |
| 1433 | MSSQL | Database access |
| 3306 | MySQL | Database access |
| 3389 | RDP | Remote desktop access |
| 5432 | PostgreSQL | Database access |
| 5900 | VNC | Remote desktop access |

## Examples

### Example 1: Map Corporate Network
```bash
# Run full discovery
python3 -m network_discovery

# Review results
cat network_discovery_*.json | jq '.discovered_hosts'

# Check targets
cat lateral_movement_targets_*.txt
```

### Example 2: Quick Local Segment Scan
```bash
# Fast scan without domain enumeration
python3 -m network_discovery --quick
```

### Example 3: Target Specific Network
```python
from network_discovery.scanners import HostDiscovery, PortScanner

# Discover hosts on specific network
discovery = HostDiscovery()
hosts = discovery.ping_sweep('10.0.0.0/24')

# Port scan discovered hosts
scanner = PortScanner()
for host in hosts:
    services = scanner.scan_host(host['ip'])
    print(f"Host {host['ip']}: {len(services)} services")
```

### Example 4: SMB Share Enumeration
```python
from network_discovery.enumeration import SMBEnumerator

smb = SMBEnumerator()

# Enumerate shares on multiple hosts
targets = ['192.168.1.100', '192.168.1.150', '192.168.1.200']

for target in targets:
    shares = smb.enumerate_shares(target)
    if shares:
        print(f"Shares on {target}:")
        print(shares['shares'])
```

## Platform Support

- ✅ Linux (Ubuntu, CentOS, Debian, Kali, etc.)
- ✅ Windows (7, 8, 10, 11, Server)
- ⚠️ macOS (partial support)

## Requirements

- Python 3.7+
- Standard library (no required dependencies)
- Optional: netifaces for better interface detection
- Optional: smbclient (Linux) for SMB enumeration

## Best Practices

### 1. Start with Quick Scan
```bash
# Get initial lay of the land
python3 -m network_discovery --quick
```

### 2. Limit Scope
```bash
# Scan only a few hosts initially
python3 -m network_discovery --max-hosts 5
```

### 3. Use OPSEC
- Slow down scans to avoid detection
- Limit concurrent threads
- Scan during business hours when traffic is high
- Use compromised credentials for authenticated scans

### 4. Prioritize Targets
Review the lateral_movement_targets.txt file and focus on:
1. Domain controllers (full AD control)
2. Database servers (sensitive data)
3. Systems with admin shares (lateral movement)
4. Admin workstations (credential theft)

### 5. Document Everything
```bash
# Save all output
python3 -m network_discovery 2>&1 | tee discovery_log.txt
```

## Advanced Usage

### Custom Port List
```python
from network_discovery.scanners import PortScanner

scanner = PortScanner()

# Scan custom ports
custom_ports = [21, 22, 23, 80, 443, 8080, 8443]
services = scanner.scan_host('192.168.1.100', ports=custom_ports)
```

### Parallel Scanning
```python
from network_discovery import NetworkDiscovery
import concurrent.futures

discovery = NetworkDiscovery()

# Scan multiple networks in parallel
networks = ['192.168.1.0/24', '10.0.0.0/24', '172.16.0.0/24']

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(discovery.host_discovery.ping_sweep, net)
        for net in networks
    ]
    
    for future in concurrent.futures.as_completed(futures):
        hosts = future.result()
        print(f"Found {len(hosts)} hosts")
```

### Integration with Other Tools
```bash
# Export to nmap format
python3 -c "
import json
with open('network_discovery_*.json') as f:
    data = json.load(f)
    hosts = [h['ip'] for h in data['discovered_hosts']]
    print(' '.join(hosts))
" > targets.txt

# Scan with nmap
nmap -sV -iL targets.txt -oA detailed_scan
```

## Troubleshooting

### "Permission denied" on port scanning
Some systems require root for raw socket access:
```bash
sudo python3 -m network_discovery
```

### No hosts discovered
- Check if you're on the correct network
- Verify firewall rules aren't blocking ICMP
- Try ARP scan instead (works on local segment)

### SMB enumeration fails
On Linux, install smbclient:
```bash
# Ubuntu/Debian
sudo apt-get install smbclient

# CentOS/RHEL
sudo yum install samba-client
```

### Slow scanning
Reduce max_workers in scanners:
```python
# Edit port_scanner.py
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
```

## Security Considerations

This tool performs active network scanning which can:
- Trigger IDS/IPS alerts
- Be logged by network monitoring tools
- Violate network policies
- Result in legal action if unauthorized

**Always obtain written authorization before scanning any network.**

## Contributing

To add a new scanner or enumerator:

1. Create new file in appropriate directory
2. Implement scanner/enumerator class
3. Add to module `__init__.py`
4. Update base.py to use new module
5. Add tests

Example:
```python
# network_discovery/enumeration/rdp.py
class RDPEnumerator:
    def enumerate_rdp(self, target_ip: str):
        # Your enumeration logic
        pass
```

## License

[Your License Here]

## Disclaimer

This tool is provided for educational and authorized testing purposes only. The authors are not responsible for misuse or illegal use of this tool. Always obtain proper authorization before scanning networks.

---

**Remember**: Unauthorized network scanning is illegal. Always get authorization. Always act ethically.

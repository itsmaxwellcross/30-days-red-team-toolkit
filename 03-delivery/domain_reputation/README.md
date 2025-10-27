# Domain Reputation Builder

Comprehensive toolkit for setting up and verifying email domain reputation and authentication.

## Features

- **DNS Record Verification**: Check SPF, DKIM, DMARC records
- **Blacklist Monitoring**: Check domain against major blacklists
- **DNS Generation**: Generate proper email authentication records
- **Warmup Scheduling**: Progressive email volume recommendations
- **Deliverability Testing**: Send test emails to verify setup
- **Comprehensive Reporting**: Clear summaries and checklists

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```bash
# Full analysis with recommendations
python -m domain_reputation example.com

# Check current status only
python -m domain_reputation example.com --check-only

# Generate records with server IP
python -m domain_reputation example.com --server-ip 192.0.2.1

# Custom warmup schedule
python -m domain_reputation example.com --warmup-days 30

# Test deliverability
python -m domain_reputation example.com --test-email test@example.com
```

## Python API

```python
from domain_reputation import DomainReputationBuilder

# Initialize
builder = DomainReputationBuilder('example.com')

# Run full analysis
domain = builder.run_full_analysis(
    server_ip='192.0.2.1',
    warmup_days=14
)

# Check specific components
builder.check_all()
builder.generate_dns_records('192.0.2.1')
builder.show_warmup_schedule(14)

# Access results
print(f"SPF configured: {domain.spf_record is not None}")
print(f"Clean reputation: {domain.is_clean()}")
print(f"Summary: {domain.get_summary()}")
```

## File Structure

```
domain_reputation/
├── core/              # Core logic
│   ├── builder.py     # Main orchestrator
│   └── domain.py      # Domain data model
├── checkers/          # Verification modules
│   ├── dns_checker.py        # DNS records
│   ├── blacklist_checker.py  # Blacklists
│   └── deliverability.py     # Email testing
├── generators/        # Record generation
│   ├── dns_generator.py      # DNS records
│   └── warmup_scheduler.py   # Warmup plans
├── utils/            # Utilities
│   └── formatters.py  # Output formatting
└── config/           # Configuration
    └── settings.py    # All settings
```

## What Gets Checked

### DNS Records
- **SPF**: Sender Policy Framework
- **DKIM**: DomainKeys Identified Mail
- **DMARC**: Domain-based Message Authentication
- **MX**: Mail exchanger records

### Blacklists
- Spamhaus ZEN
- SpamCop
- SORBS
- Barracuda
- Mail Spike

## Domain Warmup

Progressive email sending schedule to build reputation:

| Day | Volume | Audience |
|-----|--------|----------|
| 1-2 | 10-20 | Internal team |
| 3-4 | 30-50 | Known contacts |
| 5-7 | 75-100 | Newsletter subscribers |
| 8-14 | 150-500 | Broader audience |
| 15-28 | 1000-2000 | Full volume |

## DNS Record Setup

### 1. SPF Record
```
TXT @ "v=spf1 a mx ip4:YOUR_SERVER_IP ~all"
```

### 2. DKIM Record
```bash
# Generate keys
opendkim-genkey -d example.com -s default

# Add TXT record
TXT default._domainkey "v=DKIM1; k=rsa; p=YOUR_PUBLIC_KEY"
```

### 3. DMARC Record
```
TXT _dmarc "v=DMARC1; p=none; rua=mailto:dmarc@example.com"
```

## Interpreting Results

### ✓ Good Configuration
```
Email Authentication:
  SPF:   ✓ Configured
  DKIM:  ✓ Configured
  DMARC: ✓ Configured

Reputation:
  Status: ✓ Clean (not on any blacklists)
```

### ⚠ Needs Attention
```
Email Authentication:
  SPF:   ✗ Not configured
  DKIM:  ✗ Not configured
  DMARC: ✗ Not configured

Reputation:
  Status: ✗ Listed on one or more blacklists
```

## Best Practices

### Initial Setup
1. Configure all three authentication methods (SPF, DKIM, DMARC)
2. Wait 24-48 hours for DNS propagation
3. Verify records with this tool
4. Check blacklist status
5. Begin warmup process

### Ongoing Maintenance
- Monitor blacklist status weekly
- Review DMARC reports regularly
- Maintain consistent sending patterns
- Keep bounce rates below 2%
- Monitor spam complaint rates
- Update DNS records when infrastructure changes

### Common Issues

**Problem**: Listed on blacklists
- **Solution**: Request delisting, improve practices, use authentication

**Problem**: DNS records not found
- **Solution**: Check DNS propagation, verify syntax, wait longer

**Problem**: Poor deliverability
- **Solution**: Complete warmup, improve engagement, check content

## Advanced Usage

### Custom Blacklist Checks
```python
from domain_reputation.checkers import BlacklistChecker

checker = BlacklistChecker('example.com')
results = checker.check_all()

for blacklist, is_listed in results.items():
    if is_listed:
        print(f"Listed on: {blacklist}")
```

### Generate Custom Warmup Schedule
```python
from domain_reputation.generators import WarmupScheduler

scheduler = WarmupScheduler()
schedule = scheduler.generate_schedule(days=30)

for day, volume, audience in schedule:
    print(f"Day {day}: {volume} emails to {audience}")
```

### Check Specific DNS Records
```python
from domain_reputation.checkers import DNSChecker

checker = DNSChecker('example.com')

# Check individual records
spf = checker.check_spf()
dkim = checker.check_dkim(selector='mail')
dmarc = checker.check_dmarc()
mx = checker.check_mx()
```

## Integration Examples

### With Phishing Framework
```python
from domain_reputation import DomainReputationBuilder
from phishing_framework import PhishingFramework

# Verify domain before sending campaign
builder = DomainReputationBuilder('phishing-domain.com')
domain = builder.check_all()

if domain.has_email_auth() and domain.is_clean():
    # Domain is ready for use
    framework = PhishingFramework()
    framework.send_campaign(...)
else:
    print("Domain not ready - complete setup first")
```

### Automated Monitoring
```python
import schedule
import time
from domain_reputation import DomainReputationBuilder

def check_reputation():
    """Daily reputation check"""
    builder = DomainReputationBuilder('example.com')
    domain = builder.check_all()
    
    if not domain.is_clean():
        # Alert on blacklist
        send_alert(f"Domain listed on blacklist!")

# Run daily
schedule.every().day.at("09:00").do(check_reputation)

while True:
    schedule.run_pending()
    time.sleep(3600)
```

### Batch Domain Checks
```python
from domain_reputation import DomainReputationBuilder

domains = ['domain1.com', 'domain2.com', 'domain3.com']

results = {}
for domain_name in domains:
    builder = DomainReputationBuilder(domain_name)
    domain = builder.check_all()
    results[domain_name] = domain.get_summary()

# Find domains needing attention
for name, summary in results.items():
    if not summary['has_email_auth']:
        print(f"{name} needs email authentication setup")
```

## Testing

### Unit Tests
```python
import unittest
from domain_reputation import DomainReputationBuilder
from domain_reputation.core import Domain

class TestDomainReputation(unittest.TestCase):
    def setUp(self):
        self.builder = DomainReputationBuilder('example.com')
    
    def test_check_spf(self):
        """Test SPF record checking"""
        result = self.builder.dns_checker.check_spf()
        self.assertIsNotNone(result)
    
    def test_domain_model(self):
        """Test domain data model"""
        domain = Domain(name='test.com')
        domain.spf_record = 'v=spf1 ~all'
        domain.dkim_record = 'v=DKIM1; p=...'
        domain.dmarc_record = 'v=DMARC1; p=none'
        
        self.assertTrue(domain.has_email_auth())
    
    def test_blacklist_checker(self):
        """Test blacklist checking"""
        results = self.builder.blacklist_checker.check_all()
        self.assertIsInstance(results, dict)
        self.assertTrue(len(results) > 0)

if __name__ == '__main__':
    unittest.main()
```

### Integration Testing
```bash
# Test against real domain
python -m domain_reputation google.com --check-only

# Should show all records configured
```

## Configuration

Edit `config/settings.py` to customize:

```python
class Settings:
    # Add more blacklists
    BLACKLISTS = [
        'zen.spamhaus.org',
        'bl.spamcop.net',
        # Add custom blacklist
        'custom.blacklist.org'
    ]
    
    # Customize warmup schedule
    WARMUP_SCHEDULE = [
        (1, 5, "Test group"),
        (3, 15, "Small group"),
        # ... custom schedule
    ]
    
    # Change defaults
    DEFAULT_DMARC_POLICY = 'quarantine'  # More strict
```

## Troubleshooting

### DNS Not Propagating
```bash
# Check specific nameserver
dig @8.8.8.8 example.com TXT
dig @8.8.8.8 default._domainkey.example.com TXT
dig @8.8.8.8 _dmarc.example.com TXT

# Wait 24-48 hours for full propagation
```

### Blacklist False Positives
```bash
# Check individual blacklist websites
# Most offer lookup tools and delisting forms

# Common delisting:
# Spamhaus: https://www.spamhaus.org/lookup/
# SpamCop: https://www.spamcop.net/bl.shtml
```

### DKIM Issues
```bash
# Verify key format
openssl rsa -in dkim.private -pubout -outform PEM

# Check DNS record
dig default._domainkey.example.com TXT

# Common issues:
# - Incorrect selector
# - Key too long (split into multiple strings)
# - Wrong format in DNS
```

## Performance Considerations

### Async Checks
For checking multiple domains:

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def check_domains_async(domains):
    """Check multiple domains concurrently"""
    loop = asyncio.get_event_loop()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            loop.run_in_executor(
                executor,
                check_domain,
                domain
            )
            for domain in domains
        ]
        results = await asyncio.gather(*futures)
    
    return results

def check_domain(domain_name):
    """Check single domain"""
    builder = DomainReputationBuilder(domain_name)
    return builder.check_all()
```

### Caching Results
```python
import json
from datetime import datetime, timedelta

class CachedReputationBuilder:
    """Cache results to avoid excessive DNS queries"""
    
    def __init__(self, cache_file='reputation_cache.json'):
        self.cache_file = cache_file
        self.cache = self.load_cache()
    
    def get_or_check(self, domain, max_age_hours=24):
        """Get from cache or perform new check"""
        if domain in self.cache:
            cached_time = datetime.fromisoformat(self.cache[domain]['timestamp'])
            age = datetime.now() - cached_time
            
            if age < timedelta(hours=max_age_hours):
                return self.cache[domain]['result']
        
        # Perform new check
        builder = DomainReputationBuilder(domain)
        result = builder.check_all()
        
        # Cache result
        self.cache[domain] = {
            'timestamp': datetime.now().isoformat(),
            'result': result.get_summary()
        }
        self.save_cache()
        
        return result
```

## API Reference

### DomainReputationBuilder

Main class for domain reputation analysis.

**Methods:**
- `check_all()` - Run all verification checks
- `generate_dns_records(server_ip)` - Generate DNS records
- `show_warmup_schedule(days)` - Display warmup schedule
- `test_deliverability(email)` - Send test email
- `run_full_analysis(server_ip, warmup_days)` - Complete analysis

### Domain

Data model for domain information.

**Attributes:**
- `name` - Domain name
- `spf_record` - SPF record (if found)
- `dkim_record` - DKIM record (if found)
- `dmarc_record` - DMARC record (if found)
- `blacklist_status` - Dict of blacklist results

**Methods:**
- `is_clean()` - Check if not blacklisted
- `has_email_auth()` - Check if all auth configured
- `get_summary()` - Get status summary

### DNSChecker

Check DNS records.

**Methods:**
- `check_spf()` - Verify SPF record
- `check_dkim(selector)` - Verify DKIM record
- `check_dmarc()` - Verify DMARC record
- `check_mx()` - Get MX records

### BlacklistChecker

Check domain blacklist status.

**Methods:**
- `check_blacklist(blacklist)` - Check single blacklist
- `check_all()` - Check all configured blacklists

## Contributing

Contributions welcome! Areas for improvement:

- Additional blacklist sources
- More DKIM selector options
- BIMI record support
- Automated delisting requests
- Email validation testing
- Reputation scoring algorithms

## Security Notes

- DNS queries are passive and safe
- Test emails require SMTP configuration
- Store SMTP credentials securely
- Use for authorized domains only
- Follow email sending best practices

## License

MIT License - For authorized security testing and legitimate email infrastructure setup only.

---

## Quick Reference Card


```bash
# Basic check
python -m domain_reputation example.com

# With IP
python -m domain_reputation example.com --server-ip 192.0.2.1

# 30-day warmup
python -m domain_reputation example.com --warmup-days 30

# Just status
python -m domain_reputation example.com --check-only

# Test email
python -m domain_reputation example.com --test-email test@example.com

# Custom DKIM selector
python -m domain_reputation example.com --dkim-selector mail
```

## Support

- Issues: GitHub Issues
- Docs: README.md
- Examples: See examples/ directory

---

**⚠️ Legal Notice**: Use only for domains you own or have authorization to test. Unauthorized testing may violate computer fraud laws
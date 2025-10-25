# Delivery & Social Engineering Tools (Day 4)

Tools for phishing campaigns, credential harvesting, and payload delivery.

## Tools Overview

### phishing_framework.py
Complete phishing infrastructure with tracking and credential harvesting.

**Usage:**
```bash
# Start tracking server
python3 phishing_framework.py --server --port 8080

# Send campaign
python3 phishing_framework.py --send targets.txt --template password_reset

# View statistics
python3 phishing_framework.py --stats
```

**Features:**
- Email template generation
- Unique tracking tokens
- Invisible pixel tracking
- Link click tracking
- Credential harvesting
- Fake login pages
- SQLite database
- Web statistics dashboard

**Templates Available:**
- password_reset
- document_review
- security_update
- hr_benefits
- voicemail

---

### template_generator.py
Personalized email template generator using reconnaissance data.

**Usage:**
```python
from template_generator import TemplateGenerator

target_data = {
    'name': 'John Doe',
    'email': 'john@target.com',
    'title': 'Developer',
    'company_name': 'Target Corp',
    'technologies_used': ['Office 365', 'Slack']
}

generator = TemplateGenerator(target_data)
templates = generator.get_all_templates()
```

**Template Types:**
- CEO Fraud / BEC
- IT Security Alerts
- HR Documents
- Vendor Invoices
- IT Support Requests
- Collaboration Requests
- LinkedIn Notifications

**Personalization:**
- Uses target's name, title, department
- References real company tools
- Adapts to company culture
- Includes recent news/events

---

### domain_reputation.py
Domain setup and reputation checking helper.

**Usage:**
```bash
python3 domain_reputation.py your-domain.com
```

**Features:**
- SPF record checking
- DKIM verification
- DMARC analysis
- Blacklist checking
- DNS record generation
- Warm-up schedule
- Deliverability testing

**Checks:**
- Domain reputation across major blacklists
- Email authentication configuration
- Recommended DNS records

---

### attachment_weaponizer.py
Malicious attachment creation for phishing.

**Usage:**
```bash
python3 attachment_weaponizer.py
```

**Creates:**
- Malicious Office macros
- Password-protected ZIPs
- ISO files
- HTML smuggling files
- LNK shortcuts
- Polyglot files

**Bypass Techniques:**
- Email security evasion
- Sandbox detection
- Content inspection bypass

---

### ab_testing.py
A/B testing framework for campaign optimization.

**Usage:**
```python
from ab_testing import PhishingABTest

tester = PhishingABTest(targets)
tester.test_urgency_levels()
tester.test_sender_types()
```

**Tests:**
- Urgency levels (high vs low)
- Sender types (internal vs external)
- Template variations
- Subject line effectiveness

---

### delivery_scheduler.py
Optimal timing calculator for phishing campaigns.

**Usage:**
```python
from delivery_scheduler import DeliveryScheduler

scheduler = DeliveryScheduler(timezone='America/New_York')
scheduler.get_optimal_send_times()
scheduler.schedule_campaign(start_date, days=5)
```

**Features:**
- Optimal send time calculation
- Times to avoid identification
- Staggered sending schedule
- Timezone-aware scheduling

**Best Times:**
- Tuesday-Thursday, 10 AM
- Wednesday, 2 PM
- End of week, 4 PM

**Avoid:**
- Early mornings
- Lunch hours
- Late evenings
- Weekends
- Holidays

---

### campaign_analytics.py
Comprehensive campaign analysis and reporting.

**Usage:**
```bash
python3 campaign_analytics.py
```

**Analyzes:**
- Funnel conversion rates
- Time-based activity
- Department susceptibility
- Individual target responses

**Reports:**
- Email open rates
- Link click rates
- Credential submission rates
- Hourly activity patterns
- Department breakdowns

**Exports:**
- JSON reports
- CSV data
- Statistics summaries

---

## Configuration

### phishing_config.json
```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your-email@domain.com",
  "sender_password": "app-password",
  "sender_name": "IT Security Team",
  "tracking_domain": "http://your-server.com",
  "landing_page_port": 8080
}
```

**Setup:**
1. Configure SMTP settings
2. Set up tracking domain
3. Configure DNS records (SPF, DKIM, DMARC)
4. Warm up domain (1-2 weeks for new domains)

---

## Target List Format

Create `targets.txt`:
```csv
email,name,title,department
john.doe@target.com,John Doe,Senior Developer,Engineering
jane.smith@target.com,Jane Smith,IT Manager,IT
```

---

## Campaign Workflow

### 1. Infrastructure Setup
```bash
# Start tracking server
python3 phishing_framework.py --server --port 8080 &

# Verify DNS configuration
python3 domain_reputation.py your-domain.com
```

### 2. Template Generation
```bash
# Generate personalized templates
python3 template_generator.py

# Review and customize based on recon data
```

### 3. Testing
```bash
# Create test targets file with YOUR email
echo "your-email@test.com,Your Name,Tester,Testing" > test_targets.txt

# Send test campaign
python3 phishing_framework.py --send test_targets.txt --template security_alert

# Verify:
# - Email delivery
# - Tracking pixel loads
# - Links work
# - Landing page displays
# - Credentials capture
```

### 4. Campaign Execution
```bash
# Send in batches
python3 phishing_framework.py --send batch1.txt --template security_alert
# Wait 24 hours
python3 phishing_framework.py --send batch2.txt --template security_alert
```

### 5. Monitoring
```bash
# Real-time stats
python3 phishing_framework.py --stats

# Web dashboard
http://your-server:8080/stats

# Detailed analysis
python3 campaign_analytics.py
```

---

## Social Engineering Principles

### Psychological Triggers
1. **Authority** - Impersonate trusted figures
2. **Urgency** - Create time pressure
3. **Fear** - Threaten negative consequences
4. **Curiosity** - Promise interesting information
5. **Greed** - Offer rewards or benefits
6. **Helpfulness** - Request assistance

### Effective Pretexts
- Based on reconnaissance
- Relevant to target's role
- Timely and contextual
- Technically plausible
- Emotionally compelling

---

## Tracking and Analytics

### Events Tracked
- **email_sent** - Campaign delivery
- **email_opened** - Tracking pixel loaded
- **link_clicked** - User clicked phishing link
- **credentials_submitted** - Login attempted

### Success Metrics
- **Open Rate** - % who opened email
- **Click Rate** - % who clicked link
- **Success Rate** - % who submitted credentials

### Database Schema
```sql
targets(id, email, name, title, department, token)
events(id, target_id, event_type, ip_address, user_agent, timestamp)
credentials(id, target_id, username, password, timestamp)
```

---

## Legal and Ethical Requirements

### Before ANY Campaign

**Required:**
- ✅ Written authorization from client
- ✅ Clearly defined scope
- ✅ Rules of engagement signed
- ✅ Incident response plan
- ✅ Data protection agreement

**Never:**
- ❌ Test without explicit permission
- ❌ Phish personal email accounts
- ❌ Keep credentials after engagement
- ❌ Use findings maliciously
- ❌ Exceed defined scope

### Data Handling
- Encrypt captured credentials
- Delete data after engagement
- Follow data protection laws
- Document everything
- Provide findings securely

---

## Integration with Other Days

### Using Recon Data (Days 1-2)
```python
# Load reconnaissance findings
recon_data = json.load(open('../01-reconnaissance/target_recon.json'))

# Use in template personalization
target_info = {
    'name': recon_data['employee_name'],
    'company_name': recon_data['company'],
    'technologies': recon_data['tech_stack']
}
```

### Using Payloads (Day 3)
```bash
# Attach weaponized document
python3 phishing_framework.py \
  --send targets.txt \
  --template document_review \
  --attachment ../02-weaponization/payloads/document.docm
```

### Preparing for Exploitation (Day 5)
- Captured credentials for initial access
- Identified susceptible users
- Established C2 callbacks
- Gathered internal information

---

## Troubleshooting

### Emails Going to Spam
1. Check SPF/DKIM/DMARC configuration
2. Verify sender reputation
3. Warm up domain longer
4. Reduce sending volume
5. Improve email content

### Tracking Not Working
1. Verify server is running
2. Check firewall rules
3. Confirm tracking domain matches
4. Test tracking pixel manually

### Low Success Rates
1. Improve personalization
2. Try different templates
3. Adjust timing
4. A/B test variations
5. Review landing page design

---

## Next Steps

After successful delivery:
1. Monitor for callbacks
2. Document successful compromises
3. Proceed to exploitation (Day 5)
4. Establish persistence
5. Begin lateral movement

Remember: The goal is security improvement, not just compromise statistics.
# Phishing Framework

Professional phishing campaign framework with tracking and analytics.

## ⚠️ Legal Disclaimer

**FOR AUTHORIZED SECURITY TESTING ONLY**

This tool is designed for authorized penetration testing and security awareness training. 
Unauthorized use is illegal and unethical. Always obtain written permission before deployment.

## Features

- **Email Campaign Management** - Send targeted phishing emails
- **Event Tracking** - Track opens, clicks, and submissions
- **Credential Harvesting** - Capture credentials via fake login pages
- **Analytics Dashboard** - Real-time campaign statistics
- **Template System** - Multiple customizable email templates
- **Modular Architecture** - Clean, maintainable code structure

## Installation
```bash
# Clone repository
git clone 
cd phishing_framework

# Install dependencies
pip3 install -r requirements.txt

# Configure settings
nano config/phishing_config.json
```

## Configuration

Edit `config/phishing_config.json`:
```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your-email@gmail.com",
  "sender_password": "your-app-password",
  "sender_name": "IT Security Team",
  "tracking_domain": "http://your-server.com",
  "landing_page_port": 8080,
  "database_path": "phishing_campaign.db"
}
```

## Usage

### Start Tracking Server
```bash
python3 main.py --server --port 8080
```

Access statistics at: `http://localhost:8080/stats`

### Send Campaign

Create targets file (`targets.csv`):
```
email,name,title,department
john.doe@example.com,John Doe,Developer,Engineering
jane.smith@example.com,Jane Smith,Manager,IT
```

Send campaign:
```bash
python3 main.py --send targets.csv --template password_reset
```

### With Attachment
```bash
python3 main.py --send targets.csv --template document_review --attachment document.pdf
```

### View Statistics
```bash
python3 main.py --stats
```

## Available Templates

- `password_reset` - Password reset notification
- `document_review` - Document review request
- `security_update` - Critical security update
- `hr_benefits` - Benefits enrollment
- `voicemail` - Voicemail notification

## Security Considerations

1. **Use HTTPS** - Always use SSL for tracking server
2. **Secure Database** - Protect database file with proper permissions
3. **Delete Data** - Remove campaign data after engagement
4. **Authorization** - Obtain written permission before testing
5. **Scope Limits** - Stay within defined engagement scope

## Extending

### Add New Email Template

Edit `templates/email_templates.py`:
```python
def _custom_template(self, target_name: str, token: str) -> dict:
    return {
        "subject": "Your Subject",
        "body": f'''<html>...</html>'''
    }
```

### Add New Landing Page

Edit `templates/landing_pages.py`:
```python
@staticmethod
def custom_login(token: str) -> str:
    return f'''<!DOCTYPE html>...</html>'''
```

## Troubleshooting

**Emails not sending:**
- Check SMTP credentials
- Verify firewall allows SMTP port
- Use app-specific password for Gmail

**Tracking not working:**
- Ensure server is running
- Check firewall allows tracking port
- Verify tracking_domain in config

**Database errors:**
- Check file permissions
- Verify database path exists
- Ensure SQLite is installed

## Testing
```bash
# Test with your own email first
echo "your-email@test.com,Your Name,Tester,Testing" > test.csv
python3 main.py --send test.csv --template password_reset
```

The authors assume no liability for misuse. This tool is for security 
professionals conducting authorized testing only.

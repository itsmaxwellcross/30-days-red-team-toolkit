"""
IT Security alert templates
"""
import random
from datetime import datetime
from .base import BaseTemplate

class SecurityAlertTemplate(BaseTemplate):
    """IT security alert and warning templates"""
    
    def generate(self) -> dict:
        """Generate security alert template"""
        # Use actual tech from fingerprinting
        tech_stack = self.target.technologies_used or ['Office 365', 'Email System']
        platform = random.choice(tech_stack)
        
        locations = [
            "Moscow, Russia",
            "Beijing, China",
            "Lagos, Nigeria",
            "São Paulo, Brazil",
            "Mumbai, India"
        ]
        
        location = random.choice(locations)
        ip_address = f"185.220.{random.randint(1,255)}.{random.randint(1,255)}"
        
        subject = f"Security Alert: Suspicious {platform} Activity Detected"
        
        body = f'''
Dear {self.target.name},

Our security systems have detected unusual login attempts on your {platform} account from the following location:

Location: {location}
IP Address: {ip_address}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
Device: Unknown Windows PC

If this was not you, please verify your account immediately:
[TRACKING_LINK: Verify Account Security]

If you do not verify within 24 hours, your account will be temporarily suspended for security purposes.

Thank you for your prompt attention to this matter.

{self.target.company_name or 'Company'} IT Security Team
security@{self.target.company_domain or 'company.com'}
'''
        
        return self._format_template(
            subject=subject,
            body=body,
            template_type='security_alert',
            urgency='high'
        )
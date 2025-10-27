"""
Social media notification templates
"""
from datetime import datetime
from .base import BaseTemplate

class SocialMediaTemplate(BaseTemplate):
    """Social media platform notification templates"""
    
    def generate(self) -> dict:
        """Generate social media template (LinkedIn)"""
        subject = f"LinkedIn: You appeared in 3 searches this week"
        
        body = f'''
Hi {self.target.name},

You're attracting attention! Your profile appeared in 3 searches this week.

See who's viewing your profile:
[TRACKING_LINK: View Profile Viewers]

These connections could lead to new opportunities.

Best,
The LinkedIn Team

---
© {datetime.now().year} LinkedIn Corporation
'''
        
        return self._format_template(
            subject=subject,
            body=body,
            template_type='linkedin',
            urgency='low'
        )
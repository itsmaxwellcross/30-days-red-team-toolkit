"""
IT support and request templates
"""
import random
from .base import BaseTemplate

class ITRequestTemplate(BaseTemplate):
    """Internal IT support request templates"""
    
    def generate(self) -> dict:
        """Generate IT request template"""
        ticket_num = random.randint(10000, 99999)
        
        subject = f"IT Ticket #{ticket_num}: Software Update Required"
        
        update_types = [
            "critical security update",
            "mandatory compliance update",
            "system patch",
            "security hotfix"
        ]
        
        update_type = random.choice(update_types)
        
        body = f'''
Hi {self.target.name},

We're rolling out a {update_type} to all systems in {self.target.department or 'your department'}.

Ticket: #{ticket_num}
Priority: High
Category: Security Update

Please install the update at your earliest convenience:
[TRACKING_LINK: Download Security Update]

The update addresses several critical vulnerabilities and should be installed before end of business today.

If you experience any issues, please reply to this ticket.

Best regards,
IT Support Team
support@{self.target.company_domain or 'company.com'}
'''
        
        return self._format_template(
            subject=subject,
            body=body,
            template_type='it_request',
            urgency='high'
        )
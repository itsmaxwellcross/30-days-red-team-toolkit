"""
CEO Fraud / Business Email Compromise templates
"""
import random
from .base import BaseTemplate

class CEOFraudTemplate(BaseTemplate):
    """CEO fraud and business email compromise templates"""
    
    def generate(self) -> dict:
        """Generate CEO fraud template"""
        # In real implementation, get CEO name from recon
        ceo_names = ["Michael Chen", "Sarah Johnson", "David Martinez", "Jennifer Lee"]
        ceo_name = random.choice(ceo_names)
        
        subjects = [
            f"Urgent: Confidential Matter - {self.target.name}",
            f"Quick Question - {self.target.name}",
            f"Need Your Help - Confidential",
            f"Time Sensitive: {self.target.name}"
        ]
        
        bodies = [
            f'''
{self.target.name},

I'm in meetings all day but need your help with something time-sensitive and confidential.

I need you to process a wire transfer for an acquisition we're working on. I'll send you the details shortly, but wanted to give you a heads up now.

Please keep this between us until we announce publicly.

Can you handle this today?

{ceo_name}
CEO, {self.target.company_name or 'Company'}

Sent from my iPhone
''',
            f'''
{self.target.name},

Are you available? I need you to handle something urgent but I'm tied up in back-to-back meetings.

It's regarding a vendor payment that needs to go out today. I'll forward you the details in a few minutes.

Please standby and keep this confidential for now.

Thanks,
{ceo_name}

Sent from my iPhone
''',
            f'''
Hi {self.target.name},

I know this is short notice, but we have a time-sensitive payment that needs to be processed before EOD.

Can you help with this? I'll send over the wire transfer details shortly.

This is confidential until we make the announcement next week.

{ceo_name}
{self.target.company_name or 'Company'}
'''
        ]
        
        subject = random.choice(subjects)
        body = random.choice(bodies)
        
        return self._format_template(
            subject=subject,
            body=body,
            template_type='ceo_fraud',
            urgency='high'
        )
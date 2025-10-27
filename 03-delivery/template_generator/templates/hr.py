"""
HR document and benefits templates
"""
import random
from .base import BaseTemplate

class HRDocumentTemplate(BaseTemplate):
    """HR document review and benefits templates"""
    
    def generate(self) -> dict:
        """Generate HR document template"""
        subject = f"Action Required: Review Updated Employee Handbook - {self.target.name}"
        
        updates = [
            "• Remote work policies\n• PTO accrual rates\n• Benefits enrollment procedures\n• Code of conduct updates",
            "• Hybrid work guidelines\n• Health insurance changes\n• 401(k) matching updates\n• Performance review process",
            "• Workplace safety protocols\n• Diversity and inclusion policies\n• Professional development opportunities\n• Leave of absence procedures"
        ]
        
        update_list = random.choice(updates)
        
        body = f'''
Hello {self.target.name},

As part of our annual policy review, we've updated the Employee Handbook with important changes to:

{update_list}

Please review the attached document and acknowledge receipt by EOD Friday.

[TRACKING_LINK: Download Updated Handbook]

If you have questions, please contact HR at hr@{self.target.company_domain or 'company.com'}

Thank you,
Human Resources Department
{self.target.company_name or 'Company'}
'''
        
        return self._format_template(
            subject=subject,
            body=body,
            template_type='hr_document',
            urgency='medium'
        )
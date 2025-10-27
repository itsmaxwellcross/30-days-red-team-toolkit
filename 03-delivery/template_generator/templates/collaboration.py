"""
Collaboration and document sharing templates
"""
import random
from .base import BaseTemplate

class CollaborationTemplate(BaseTemplate):
    """Document collaboration request templates"""
    
    def generate(self) -> dict:
        """Generate collaboration template"""
        # Use real names from recon in production
        colleague_names = ["Sarah Williams", "Mike Chen", "Jennifer Lopez", "David Kim"]
        colleague = random.choice(colleague_names)
        
        documents = [
            "Q4 Planning Document",
            "Budget Review Spreadsheet",
            "Project Proposal",
            "Strategy Presentation",
            "Annual Report Draft"
        ]
        
        doc = random.choice(documents)
        
        subject = f"Collaboration Request: {doc}"
        
        body = f'''
Hi {self.target.name},

{colleague} suggested I reach out to you for input on our {doc}.

I've shared it with you here:
[TRACKING_LINK: View Document]

Would appreciate your thoughts by Wednesday if possible. Let me know if you have any questions.

Thanks!
'''
        
        return self._format_template(
            subject=subject,
            body=body,
            template_type='collaboration',
            urgency='low'
        )
#!/usr/bin/env python3
"""
Email template definitions
"""

from datetime import datetime
from utils.helpers import generate_tracking_pixel, generate_tracking_link

class EmailTemplates:
    """Manage email templates"""
    
    def __init__(self, tracking_domain: str):
        self.tracking_domain = tracking_domain
    
    def get_template(self, template_name: str, target_name: str, token: str) -> dict:
        """Get email template by name"""
        templates = {
            "password_reset": self._password_reset_template,
            "document_review": self._document_review_template,
            "security_update": self._security_update_template,
            "hr_benefits": self._hr_benefits_template,
            "voicemail": self._voicemail_template
        }
        
        template_func = templates.get(template_name, self._password_reset_template)
        return template_func(target_name, token)
    
    def _password_reset_template(self, target_name: str, token: str) -> dict:
        """Password reset template"""
        return {
            "subject": "Password Reset Required - Action Needed",
            "body": f'''
<html>
<body style="font-family: Arial, sans-serif;">
<p>Dear {target_name},</p>

<p>We've detected unusual activity on your account and need you to reset your password immediately for security purposes.</p>

<p>{generate_tracking_link(self.tracking_domain, token, "Reset Password Now")}</p>

<p>This link will expire in 24 hours. If you did not request this reset, please contact IT security immediately.</p>

<p>Best regards,<br>
IT Security Team</p>

{generate_tracking_pixel(self.tracking_domain, token)}
</body>
</html>
'''
        }
    
    def _document_review_template(self, target_name: str, token: str) -> dict:
        """Document review template"""
        return {
            "subject": f"Document Review Request - {target_name}",
            "body": f'''
<html>
<body style="font-family: Arial, sans-serif;">
<p>Hi {target_name},</p>

<p>I need your input on the attached document before our meeting this afternoon. Can you review and provide feedback?</p>

<p>{generate_tracking_link(self.tracking_domain, token, "View Document")}</p>

<p>Thanks for your quick turnaround on this.</p>

<p>Best,<br>
Management Team</p>

{generate_tracking_pixel(self.tracking_domain, token)}
</body>
</html>
'''
        }
    
    def _security_update_template(self, target_name: str, token: str) -> dict:
        """Security update template"""
        return {
            "subject": "Critical Security Update Required",
            "body": f'''
<html>
<body style="font-family: Arial, sans-serif;">
<p>Dear {target_name},</p>

<p>A critical security vulnerability has been identified that affects your system. Please install the attached update immediately.</p>

<p>{generate_tracking_link(self.tracking_domain, token, "Download Security Update")}</p>

<p>Failure to update may leave your system vulnerable to attack.</p>

<p>IT Security Department</p>

{generate_tracking_pixel(self.tracking_domain, token)}
</body>
</html>
'''
        }
    
    def _hr_benefits_template(self, target_name: str, token: str) -> dict:
        """HR benefits template"""
        return {
            "subject": "Annual Benefits Enrollment - Action Required",
            "body": f'''
<html>
<body style="font-family: Arial, sans-serif;">
<p>Hello {target_name},</p>

<p>It's time for annual benefits enrollment. Please review your options and submit your selections by Friday.</p>

<p>{generate_tracking_link(self.tracking_domain, token, "Access Benefits Portal")}</p>

<p>If you have questions, contact HR at extension 5555.</p>

<p>Human Resources<br>
Benefits Team</p>

{generate_tracking_pixel(self.tracking_domain, token)}
</body>
</html>
'''
        }
    
    def _voicemail_template(self, target_name: str, token: str) -> dict:
        """Voicemail notification template"""
        return {
            "subject": "New Voicemail from Unknown Caller",
            "body": f'''
<html>
<body style="font-family: Arial, sans-serif;">
<p>Hi {target_name},</p>

<p>You have a new voicemail message:</p>

<p><strong>From:</strong> Unknown Number<br>
<strong>Duration:</strong> 1:37<br>
<strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>

<p>{generate_tracking_link(self.tracking_domain, token, "Listen to Voicemail")}</p>

<p>Your Voicemail System</p>

{generate_tracking_pixel(self.tracking_domain, token)}
</body>
</html>
'''
        }
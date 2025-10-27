#!/usr/bin/env python3
"""
Email sending functionality
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import Optional

class EmailSender:
    """Handle email sending operations"""
    
    def __init__(self, config):
        self.smtp_server = config.get('smtp_server')
        self.smtp_port = config.get('smtp_port')
        self.sender_email = config.get('sender_email')
        self.sender_password = config.get('sender_password')
        self.sender_name = config.get('sender_name')
    
    def send_email(self, to_email: str, subject: str, html_body: str, 
                   attachment_path: Optional[str] = None) -> bool:
        """
        Send email with optional attachment
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_body: HTML email body
            attachment_path: Optional path to attachment file
            
        Returns:
            True if sent successfully, False otherwise
        """
        # Create email
        msg = MIMEMultipart()
        msg['From'] = f"{self.sender_name} <{self.sender_email}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add HTML body
        msg.attach(MIMEText(html_body, 'html'))
        
        # Add attachment if provided
        if attachment_path:
            try:
                with open(attachment_path, 'rb') as f:
                    attachment = MIMEApplication(f.read())
                    filename = attachment_path.split('/')[-1]
                    attachment.add_header('Content-Disposition', 'attachment', 
                                        filename=filename)
                    msg.attach(attachment)
            except FileNotFoundError:
                print(f"[!] Attachment not found: {attachment_path}")
                return False
        
        # Send email
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"[-] Error sending email: {e}")
            return False
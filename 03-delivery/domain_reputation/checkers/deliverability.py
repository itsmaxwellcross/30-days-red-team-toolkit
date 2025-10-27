"""
Email deliverability tester
"""
import smtplib
from email.mime.text import MIMEText
from typing import Optional

class DeliverabilityTester:
    """Test email deliverability"""
    
    def __init__(self, domain: str):
        """
        Initialize deliverability tester
        
        Args:
            domain: Domain to test
        """
        self.domain = domain
    
    def test(self, recipient_email: str, 
             smtp_server: Optional[str] = None,
             smtp_port: int = 587,
             username: Optional[str] = None,
             password: Optional[str] = None) -> bool:
        """
        Send test email to check deliverability
        
        Args:
            recipient_email: Recipient to test
            smtp_server: SMTP server (optional)
            smtp_port: SMTP port (default: 587)
            username: SMTP username (optional)
            password: SMTP password (optional)
            
        Returns:
            True if successful, False otherwise
        """
        print(f"\n[*] Testing deliverability to {recipient_email}")
        print("[!] This will send a real test email")
        
        if not smtp_server:
            print("[!] No SMTP server configured")
            print("[!] Provide SMTP settings to test deliverability")
            return False
        
        try:
            # Create test message
            msg = MIMEText("This is a test email for deliverability testing.")
            msg['Subject'] = f"Test Email from {self.domain}"
            msg['From'] = f"test@{self.domain}"
            msg['To'] = recipient_email
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                if username and password:
                    server.login(username, password)
                server.send_message(msg)
            
            print("[+] Test email sent successfully")
            return True
            
        except Exception as e:
            print(f"[-] Failed to send test email: {e}")
            return False
    
    def verify_mx(self, domain: str) -> bool:
        """
        Verify MX records exist for a domain
        
        Args:
            domain: Domain to check
            
        Returns:
            True if MX records exist
        """
        import dns.resolver
        try:
            dns.resolver.resolve(domain, 'MX')
            return True
        except:
            return False
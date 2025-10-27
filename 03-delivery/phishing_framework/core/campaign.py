#!/usr/bin/env python3
"""
Campaign orchestration and management
"""

from typing import List, Tuple
from core.database import Database
from core.email_sender import EmailSender
from templates.email_templates import EmailTemplates
from utils.helpers import generate_token

class Campaign:
    """Orchestrate phishing campaign operations"""
    
    def __init__(self, config, database: Database):
        self.config = config
        self.db = database
        self.email_sender = EmailSender(config)
        self.email_templates = EmailTemplates(config.get('tracking_domain'))
    
    def load_targets_from_file(self, filename: str) -> List[Tuple[str, str, str]]:
        """
        Load targets from CSV file
        
        Args:
            filename: Path to CSV file (email,name,title,department)
            
        Returns:
            List of tuples (email, name, token)
        """
        targets = []
        
        try:
            with open(filename, 'r') as f:
                for line in f:
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) >= 2:
                        email = parts[0]
                        name = parts[1]
                        title = parts[2] if len(parts) > 2 else ""
                        department = parts[3] if len(parts) > 3 else ""
                        
                        # Generate unique token and add to database
                        token = generate_token()
                        self.db.add_target(email, name, title, department, token)
                        targets.append((email, name, token))
        except FileNotFoundError:
            print(f"[-] Target file not found: {filename}")
            return []
        
        return targets
    
    def send_campaign(self, targets_file: str, template_name: str, 
                     attachment_path: str = None) -> dict:
        """
        Send phishing campaign to all targets
        
        Args:
            targets_file: Path to targets CSV file
            template_name: Email template to use
            attachment_path: Optional attachment path
            
        Returns:
            Dictionary with campaign results
        """
        targets = self.load_targets_from_file(targets_file)
        
        print(f"[*] Starting phishing campaign: {template_name}")
        print(f"[*] Targets: {len(targets)}")
        
        sent = 0
        failed = 0
        
        for email, name, token in targets:
            print(f"[*] Sending to {name} ({email})...")
            
            # Generate email content
            template = self.email_templates.get_template(template_name, name, token)
            subject = template['subject']
            body = template['body']
            
            # Send email
            if self.email_sender.send_email(email, subject, body, attachment_path):
                # Log sent event
                target_id = self.db.get_target_by_token(token)
                if target_id:
                    self.db.log_event(target_id, 'email_sent')
                sent += 1
                print(f"    [+] Sent successfully")
            else:
                failed += 1
                print(f"    [-] Failed")
        
        print(f"\n[*] Campaign complete:")
        print(f"    Sent: {sent}")
        print(f"    Failed: {failed}")
        
        return {
            'sent': sent,
            'failed': failed,
            'total': len(targets)
        }
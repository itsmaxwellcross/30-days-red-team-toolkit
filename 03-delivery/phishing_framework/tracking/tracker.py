#!/usr/bin/env python3
"""
Event tracking functionality
"""

from core.database import Database

class Tracker:
    """Track campaign events"""
    
    def __init__(self, database: Database):
        self.db = database
    
    def track_event(self, token: str, event_type: str, 
                   ip_address: str = "", user_agent: str = "") -> bool:
        """
        Track an event
        
        Args:
            token: Target tracking token
            event_type: Type of event (email_opened, link_clicked, etc.)
            ip_address: IP address of user
            user_agent: User agent string
            
        Returns:
            True if logged successfully
        """
        target_id = self.db.get_target_by_token(token)
        
        if target_id:
            return self.db.log_event(target_id, event_type, ip_address, user_agent)
        
        return False
    
    def track_credentials(self, token: str, username: str, password: str) -> bool:
        """
        Track captured credentials
        
        Args:
            token: Target tracking token
            username: Captured username
            password: Captured password
            
        Returns:
            True if logged successfully
        """
        target_id = self.db.get_target_by_token(token)
        
        if target_id:
            print(f"\n[+] CREDENTIALS CAPTURED!")
            print(f"    Token: {token}")
            print(f"    Username: {username}")
            print(f"    Password: {password}\n")
            
            return self.db.log_credentials(target_id, username, password)
        
        return False
#!/usr/bin/env python3
"""
Campaign analytics and statistics
"""

from core.database import Database

class Analytics:
    """Campaign statistics and analysis"""
    
    def __init__(self, database: Database):
        self.db = database
    
    def get_campaign_stats(self) -> dict:
        """Get comprehensive campaign statistics"""
        cursor = self.db.conn.cursor()
        
        # Total targets
        cursor.execute('SELECT COUNT(*) FROM targets')
        total_targets = cursor.fetchone()[0]
        
        # Emails opened
        cursor.execute('''
            SELECT COUNT(DISTINCT target_id) FROM events 
            WHERE event_type = 'email_opened'
        ''')
        opened = cursor.fetchone()[0]
        
        # Links clicked
        cursor.execute('''
            SELECT COUNT(DISTINCT target_id) FROM events 
            WHERE event_type = 'link_clicked'
        ''')
        clicked = cursor.fetchone()[0]
        
        # Credentials submitted
        cursor.execute('SELECT COUNT(DISTINCT target_id) FROM credentials')
        submitted = cursor.fetchone()[0]
        
        return {
            'total_targets': total_targets,
            'emails_opened': opened,
            'links_clicked': clicked,
            'credentials_submitted': submitted,
            'open_rate': (opened / total_targets * 100) if total_targets > 0 else 0,
            'click_rate': (clicked / total_targets * 100) if total_targets > 0 else 0,
            'success_rate': (submitted / total_targets * 100) if total_targets > 0 else 0
        }
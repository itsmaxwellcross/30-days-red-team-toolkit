#!/usr/bin/env python3
"""
Funnel Analysis
Analyzes the complete attack funnel from email sent to credentials captured
"""

import sqlite3

class FunnelAnalyzer:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_funnel_counts(self):
        """Get counts at each stage of the funnel"""
        cursor = self.db.cursor()
        
        # Total emails sent
        cursor.execute('SELECT COUNT(*) FROM targets')
        total_sent = cursor.fetchone()[0]
        
        # Emails opened
        cursor.execute('''
            SELECT COUNT(DISTINCT target_id) FROM events 
            WHERE event_type = "email_opened"
        ''')
        opened = cursor.fetchone()[0]
        
        # Links clicked
        cursor.execute('''
            SELECT COUNT(DISTINCT target_id) FROM events 
            WHERE event_type = "link_clicked"
        ''')
        clicked = cursor.fetchone()[0]
        
        # Credentials submitted
        cursor.execute('SELECT COUNT(DISTINCT target_id) FROM credentials')
        submitted = cursor.fetchone()[0]
        
        return {
            'total_sent': total_sent,
            'opened': opened,
            'clicked': clicked,
            'submitted': submitted
        }
    
    def calculate_rates(self, counts):
        """Calculate conversion rates"""
        total = counts['total_sent']
        
        if total == 0:
            return {
                'open_rate': 0.0,
                'click_rate': 0.0,
                'submit_rate': 0.0
            }
        
        return {
            'open_rate': (counts['opened'] / total) * 100,
            'click_rate': (counts['clicked'] / total) * 100,
            'submit_rate': (counts['submitted'] / total) * 100
        }
    
    def calculate_stage_conversion(self, counts):
        """Calculate conversion between stages"""
        conversions = {}
        
        # Open to Click conversion
        if counts['opened'] > 0:
            conversions['open_to_click'] = (counts['clicked'] / counts['opened']) * 100
        else:
            conversions['open_to_click'] = 0.0
        
        # Click to Submit conversion
        if counts['clicked'] > 0:
            conversions['click_to_submit'] = (counts['submitted'] / counts['clicked']) * 100
        else:
            conversions['click_to_submit'] = 0.0
        
        return conversions
    
    def analyze(self):
        """Perform complete funnel analysis"""
        counts = self.get_funnel_counts()
        rates = self.calculate_rates(counts)
        conversions = self.calculate_stage_conversion(counts)
        
        return {
            'counts': counts,
            'rates': rates,
            'conversions': conversions
        }
    
    def print_analysis(self):
        """Print formatted funnel analysis"""
        analysis = self.analyze()
        counts = analysis['counts']
        rates = analysis['rates']
        conversions = analysis['conversions']
        
        print("\n[*] Campaign Funnel Analysis:")
        print("="*60)
        print(f"    Emails Sent:        {counts['total_sent']:>6}")
        print(f"    Emails Opened:      {counts['opened']:>6} ({rates['open_rate']:>5.1f}%)")
        print(f"    Links Clicked:      {counts['clicked']:>6} ({rates['click_rate']:>5.1f}%)")
        print(f"    Credentials Submit: {counts['submitted']:>6} ({rates['submit_rate']:>5.1f}%)")
        print("="*60)
        
        if conversions['open_to_click'] > 0:
            print(f"\n    Open → Click: {conversions['open_to_click']:.1f}%")
        
        if conversions['click_to_submit'] > 0:
            print(f"    Click → Submit: {conversions['click_to_submit']:.1f}%")
        
        return analysis
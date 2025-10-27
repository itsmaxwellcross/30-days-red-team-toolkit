#!/usr/bin/env python3
"""
Time Analysis
Analyzes when victims interacted with phishing emails
"""

import sqlite3
from datetime import datetime
from collections import defaultdict

class TimeAnalyzer:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_all_events(self):
        """Get all events with timestamps"""
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT event_type, timestamp FROM events
            ORDER BY timestamp
        ''')
        return cursor.fetchall()
    
    def analyze_by_hour(self):
        """Analyze activity by hour of day"""
        events = self.get_all_events()
        hour_counts = defaultdict(int)
        
        for event_type, timestamp in events:
            try:
                hour = datetime.fromisoformat(timestamp).hour
                hour_counts[hour] += 1
            except (ValueError, AttributeError):
                continue
        
        return dict(hour_counts)
    
    def analyze_by_day_of_week(self):
        """Analyze activity by day of week"""
        events = self.get_all_events()
        day_counts = defaultdict(int)
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for event_type, timestamp in events:
            try:
                day = datetime.fromisoformat(timestamp).weekday()
                day_counts[days[day]] += 1
            except (ValueError, AttributeError):
                continue
        
        return dict(day_counts)
    
    def analyze_by_event_type(self):
        """Analyze activity by event type over time"""
        events = self.get_all_events()
        event_hours = defaultdict(lambda: defaultdict(int))
        
        for event_type, timestamp in events:
            try:
                hour = datetime.fromisoformat(timestamp).hour
                event_hours[event_type][hour] += 1
            except (ValueError, AttributeError):
                continue
        
        return dict(event_hours)
    
    def get_time_to_action(self):
        """Calculate average time from email sent to action"""
        cursor = self.db.cursor()
        
        # Get targets with their events
        cursor.execute('''
            SELECT t.id, t.created_at,
                   MIN(CASE WHEN e.event_type = 'email_opened' THEN e.timestamp END) as first_open,
                   MIN(CASE WHEN e.event_type = 'link_clicked' THEN e.timestamp END) as first_click,
                   MIN(CASE WHEN e.event_type = 'credentials_submitted' THEN e.timestamp END) as first_submit
            FROM targets t
            LEFT JOIN events e ON t.id = e.target_id
            GROUP BY t.id
        ''')
        
        times = {
            'time_to_open': [],
            'time_to_click': [],
            'time_to_submit': []
        }
        
        for row in cursor.fetchall():
            target_id, created_at, first_open, first_click, first_submit = row
            
            try:
                created = datetime.fromisoformat(created_at)
                
                if first_open:
                    opened = datetime.fromisoformat(first_open)
                    times['time_to_open'].append((opened - created).total_seconds() / 60)
                
                if first_click:
                    clicked = datetime.fromisoformat(first_click)
                    times['time_to_click'].append((clicked - created).total_seconds() / 60)
                
                if first_submit:
                    submitted = datetime.fromisoformat(first_submit)
                    times['time_to_submit'].append((submitted - created).total_seconds() / 60)
            except (ValueError, AttributeError):
                continue
        
        # Calculate averages
        averages = {}
        for key, values in times.items():
            if values:
                averages[key] = sum(values) / len(values)
            else:
                averages[key] = 0.0
        
        return averages
    
    def analyze(self):
        """Perform complete time analysis"""
        return {
            'by_hour': self.analyze_by_hour(),
            'by_day': self.analyze_by_day_of_week(),
            'by_event_type': self.analyze_by_event_type(),
            'time_to_action': self.get_time_to_action()
        }
    
    def print_hourly_analysis(self):
        """Print formatted hourly analysis"""
        hour_counts = self.analyze_by_hour()
        
        if not hour_counts:
            print("\n[*] No activity data available")
            return
        
        print("\n[*] Activity by Hour:")
        for hour in sorted(hour_counts.keys()):
            bar = '█' * (hour_counts[hour] // 2)
            print(f"    {hour:02d}:00 - {bar} ({hour_counts[hour]})")
        
        return hour_counts
    
    def print_time_to_action(self):
        """Print time to action analysis"""
        times = self.get_time_to_action()
        
        print("\n[*] Average Time to Action:")
        print("="*60)
        if times['time_to_open'] > 0:
            print(f"    Time to Open:   {times['time_to_open']:>6.1f} minutes")
        if times['time_to_click'] > 0:
            print(f"    Time to Click:  {times['time_to_click']:>6.1f} minutes")
        if times['time_to_submit'] > 0:
            print(f"    Time to Submit: {times['time_to_submit']:>6.1f} minutes")
        
        return times
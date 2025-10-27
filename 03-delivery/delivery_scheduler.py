#!/usr/bin/env python3
"""
Optimal Delivery Timing
Send emails when targets are most likely to click
"""

from datetime import datetime, timedelta
import pytz

class DeliveryScheduler:
    def __init__(self, timezone='America/New_York'):
        self.tz = pytz.timezone(timezone)
    
    def get_optimal_send_times(self):
        """Calculate optimal send times"""
        now = datetime.now(self.tz)
        
        optimal_times = [
            "Monday 9:00 AM - Start of week, checking email backlog",
            "Tuesday 10:00 AM - Peak productivity time",
            "Wednesday 2:00 PM - Post-lunch, lower attention",
            "Thursday 11:00 AM - Mid-week routine",
            "Friday 4:00 PM - End of week, rushing to finish"
        ]
        
        print("[*] Optimal Phishing Send Times:")
        for time in optimal_times:
            print(f"    • {time}")
        
        return optimal_times
    
    def avoid_these_times(self):
        """Times to avoid sending"""
        avoid = [
            "Early morning (before 8 AM) - Suspicious",
            "Lunch time (12-1 PM) - Not checking email",
            "Late evening (after 6 PM) - Suspicious for business email",
            "Weekends - Unusual for corporate communication",
            "Holidays - Red flag for urgency"
        ]
        
        print("\n[*] Times to Avoid:")
        for time in avoid:
            print(f"    ✗ {time}")
    
    def schedule_campaign(self, start_date, num_days=5, emails_per_day=20):
        """Generate staggered sending schedule"""
        print(f"\n[*] Campaign Schedule:")
        print(f"    Start: {start_date.strftime('%Y-%m-%d')}")
        print(f"    Duration: {num_days} days")
        print(f"    Volume: {emails_per_day} emails/day")
        print(f"    Total: {num_days * emails_per_day} emails\n")
        
        current_date = start_date
        for day in range(num_days):
            send_time = current_date.replace(hour=10, minute=0)
            print(f"    Day {day+1}: {send_time.strftime('%A, %B %d at %I:%M %p')}")
            print(f"           Send {emails_per_day} emails")
            current_date += timedelta(days=1)

if __name__ == "__main__":
    scheduler = DeliveryScheduler()
    scheduler.get_optimal_send_times()
    scheduler.avoid_these_times()
    
    # Schedule campaign starting next Monday
    now = datetime.now(pytz.timezone('America/New_York'))
    days_ahead = 0 - now.weekday()  # Monday
    if days_ahead <= 0:
        days_ahead += 7
    next_monday = now + timedelta(days=days_ahead)
    
    scheduler.schedule_campaign(next_monday, num_days=5, emails_per_day=20)
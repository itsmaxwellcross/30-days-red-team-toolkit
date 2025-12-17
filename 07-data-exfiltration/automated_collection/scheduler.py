#!/usr/bin/env python3
"""
Scheduling functionality
"""

import time
import schedule
from datetime import datetime

class CollectionScheduler:
    """Schedule collection tasks"""
    
    def __init__(self):
        """Initialize scheduler"""
        self.scheduled_rules = []
    
    def schedule_rule(self, rule, collect_function):
        """
        Schedule a collection rule
        
        Args:
            rule: Collection rule dict
            collect_function: Function to call (takes rule as argument)
        """
        interval = rule.get('schedule', 'daily')
        
        if interval == 'hourly':
            schedule.every().hour.do(lambda: collect_function(rule))
        elif interval == 'daily':
            # Run at 2 AM daily
            schedule.every().day.at("02:00").do(lambda: collect_function(rule))
        elif interval == 'weekly':
            # Run at 2 AM every Sunday
            schedule.every().sunday.at("02:00").do(lambda: collect_function(rule))
        else:
            print(f"[-] Unknown schedule interval: {interval}")
            return False
        
        self.scheduled_rules.append({
            'rule': rule,
            'interval': interval
        })
        
        print(f"[+] Scheduled: {rule['name']} ({interval})")
        return True
    
    def schedule_all(self, rules, collect_function):
        """
        Schedule all collection rules
        
        Args:
            rules: List of collection rules
            collect_function: Function to call for collection
        """
        for rule in rules:
            self.schedule_rule(rule, collect_function)
    
    def run(self):
        """Run scheduler loop"""
        print(f"\n[*] Scheduler running")
        print(f"[*] Scheduled tasks: {len(self.scheduled_rules)}")
        print(f"[*] Press Ctrl+C to stop\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        except KeyboardInterrupt:
            print("\n[!] Scheduler stopped")
    
    def get_next_run_times(self):
        """
        Get next run times for all scheduled tasks
        
        Returns:
            List of next run time info
        """
        next_runs = []
        
        for job in schedule.jobs:
            next_runs.append({
                'job': str(job),
                'next_run': job.next_run
            })
        
        return next_runs
    
    def clear_all(self):
        """Clear all scheduled tasks"""
        schedule.clear()
        self.scheduled_rules = []
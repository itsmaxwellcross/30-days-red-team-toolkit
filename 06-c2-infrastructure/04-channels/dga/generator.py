"""
DGA Generator - Core domain generation logic
"""

import hashlib
from datetime import datetime, timedelta


class DGAGenerator:
    """
    Domain Generation Algorithm Generator
    Creates pseudo-random domains based on seeds and dates
    """
    
    def __init__(self, seed=None, tld='.com'):
        """
        Initialize DGA Generator
        
        Args:
            seed (str): Custom seed for generation (default: current date)
            tld (str): Top-level domain (default: .com)
        """
        self.seed = seed or self.get_default_seed()
        self.tld = tld
    
    def get_default_seed(self):
        """
        Generate seed from current date
        
        Returns:
            str: Date-based seed in format YYYYMMDD
        """
        today = datetime.now()
        return f"{today.year}{today.month:02d}{today.day:02d}"
    
    def generate_domain(self, seed=None, length=12):
        """
        Generate single domain from seed
        
        Args:
            seed (str): Seed for domain generation
            length (int): Domain name length
        
        Returns:
            str: Generated domain name
        """
        if not seed:
            seed = self.seed
        
        # Hash seed using MD5
        hash_obj = hashlib.md5(seed.encode())
        hash_hex = hash_obj.hexdigest()
        
        # Generate domain name from hash
        domain = ''
        for i in range(0, length * 2, 2):
            byte_val = int(hash_hex[i:i+2], 16)
            char = chr(97 + (byte_val % 26))  # Convert to a-z
            domain += char
        
        return f"{domain[:length]}{self.tld}"
    
    def generate_daily_domains(self, num_days=7, domains_per_day=10):
        """
        Generate domains for multiple days
        
        Args:
            num_days (int): Number of days to generate domains for
            domains_per_day (int): Number of domains per day
        
        Returns:
            list: List of dicts containing date and domains
        """
        today = datetime.now()
        all_domains = []
        
        for day_offset in range(num_days):
            date = today + timedelta(days=day_offset)
            day_seed = f"{date.year}{date.month:02d}{date.day:02d}"
            
            day_domains = []
            for i in range(domains_per_day):
                seed = f"{day_seed}-{i}"
                domain = self.generate_domain(seed)
                day_domains.append(domain)
            
            all_domains.append({
                'date': date.strftime('%Y-%m-%d'),
                'domains': day_domains
            })
        
        return all_domains
    
    def generate_time_based_domain(self, interval_hours=1):
        """
        Generate domain based on time interval
        Domain changes every N hours
        
        Args:
            interval_hours (int): Interval in hours
        
        Returns:
            str: Generated domain for current time interval
        """
        now = datetime.now()
        interval_num = now.hour // interval_hours
        
        seed = f"{now.year}{now.month:02d}{now.day:02d}-{interval_num}"
        return self.generate_domain(seed)
    
    def generate_weekly_domains(self, num_weeks=4, domains_per_week=50):
        """
        Generate domains for multiple weeks
        
        Args:
            num_weeks (int): Number of weeks to generate domains for
            domains_per_week (int): Number of domains per week
        
        Returns:
            list: List of dicts containing week and domains
        """
        today = datetime.now()
        all_domains = []
        
        for week_offset in range(num_weeks):
            week_start = today + timedelta(weeks=week_offset)
            week_seed = f"{week_start.year}-W{week_start.isocalendar()[1]}"
            
            week_domains = []
            for i in range(domains_per_week):
                seed = f"{week_seed}-{i}"
                domain = self.generate_domain(seed)
                week_domains.append(domain)
            
            all_domains.append({
                'week': week_seed,
                'week_start': week_start.strftime('%Y-%m-%d'),
                'domains': week_domains
            })
        
        return all_domains
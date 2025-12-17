#!/usr/bin/env python3
"""
Timing and jitter control for DNS exfiltration
"""

import time
import random

class TimingController:
    """Control timing between DNS queries"""
    
    def __init__(self, min_delay=0.5, max_delay=2.0, jitter=True):
        """
        Initialize timing controller
        
        Args:
            min_delay: Minimum delay between queries (seconds)
            max_delay: Maximum delay between queries (seconds)
            jitter: Whether to add random jitter
        """
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.jitter = jitter
    
    def wait(self):
        """Wait appropriate time before next query"""
        if self.jitter:
            delay = random.uniform(self.min_delay, self.max_delay)
        else:
            delay = self.min_delay
        
        time.sleep(delay)
    
    def calculate_total_time(self, num_chunks):
        """
        Calculate estimated total exfiltration time
        
        Args:
            num_chunks: Number of chunks to send
            
        Returns:
            Estimated time in seconds
        """
        avg_delay = (self.min_delay + self.max_delay) / 2
        return num_chunks * avg_delay
    
    def set_aggressive_timing(self):
        """Set aggressive timing (faster, more detectable)"""
        self.min_delay = 0.1
        self.max_delay = 0.5
    
    def set_stealth_timing(self):
        """Set stealth timing (slower, less detectable)"""
        self.min_delay = 2.0
        self.max_delay = 5.0
    
    def set_custom_timing(self, min_delay, max_delay):
        """
        Set custom timing parameters
        
        Args:
            min_delay: Minimum delay
            max_delay: Maximum delay
        """
        self.min_delay = min_delay
        self.max_delay = max_delay
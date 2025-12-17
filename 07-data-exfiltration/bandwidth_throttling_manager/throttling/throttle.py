"""
Core bandwidth throttling implementation
"""

import time
import threading
from datetime import datetime

from core.utils import (
    mbps_to_bytes_per_sec,
    is_within_schedule,
    calculate_wait_time,
    bytes_to_mbps
)
from config import THROTTLE_PRECISION, MIN_SLEEP_TIME


class BandwidthThrottle:
    """Core bandwidth throttling engine"""
    
    def __init__(self, max_rate_mbps, schedule=None):
        """
        Initialize bandwidth throttle
        
        Args:
            max_rate_mbps (float): Maximum transfer rate in Mbps
            schedule (dict): Optional schedule with start_hour and end_hour
        """
        self.max_rate_mbps = max_rate_mbps
        self.max_rate_bytes_per_sec = mbps_to_bytes_per_sec(max_rate_mbps)
        self.schedule = schedule
        
        # Transfer tracking
        self.transferred = 0
        self.start_time = None
        self.last_check_time = None
        
        # Thread safety
        self.lock = threading.Lock()
        
        print(f"[+] Bandwidth throttle initialized")
        print(f"[+] Max rate: {max_rate_mbps} Mbps ({self.max_rate_bytes_per_sec} bytes/sec)")
        
        if schedule:
            print(f"[+] Transfer window: {schedule['start_hour']}:00 - {schedule['end_hour']}:00")
    
    def is_transfer_allowed(self):
        """
        Check if current time is within transfer window
        
        Returns:
            bool: True if transfer is allowed
        """
        if not self.schedule:
            return True
        
        current_time = datetime.now()
        
        return is_within_schedule(
            current_time,
            self.schedule['start_hour'],
            self.schedule['end_hour']
        )
    
    def wait_for_transfer_window(self):
        """Wait until transfer window opens"""
        if not self.schedule:
            return
        
        while not self.is_transfer_allowed():
            current_time = datetime.now()
            
            wait_seconds = calculate_wait_time(
                current_time,
                self.schedule['start_hour'],
                self.schedule['end_hour']
            )
            
            wait_minutes = wait_seconds / 60
            wait_hours = wait_minutes / 60
            
            if wait_hours >= 1:
                print(f"[*] Outside transfer window. Waiting {wait_hours:.1f} hours...")
            else:
                print(f"[*] Outside transfer window. Waiting {wait_minutes:.1f} minutes...")
            
            # Sleep in chunks to allow for interruption
            sleep_time = min(300, wait_seconds)  # Max 5 minutes at a time
            time.sleep(sleep_time)
    
    def throttle(self, data_size):
        """
        Apply throttling for data transfer
        
        Args:
            data_size (int): Size of data to transfer in bytes
        """
        with self.lock:
            current_time = time.time()
            
            # Initialize on first transfer
            if self.start_time is None:
                self.start_time = current_time
                self.last_check_time = current_time
            
            # Calculate elapsed time since start
            elapsed = current_time - self.start_time
            
            # Calculate how many bytes we should have transferred by now
            expected_transferred = elapsed * self.max_rate_bytes_per_sec
            
            # Calculate how many bytes we've actually transferred (including current)
            actual_transferred = self.transferred + data_size
            
            # If we're ahead of schedule, sleep to slow down
            if actual_transferred > expected_transferred:
                bytes_ahead = actual_transferred - expected_transferred
                sleep_time = bytes_ahead / self.max_rate_bytes_per_sec
                
                # Only sleep if significant
                if sleep_time > MIN_SLEEP_TIME:
                    time.sleep(sleep_time)
            
            # Update transferred count
            self.transferred += data_size
            self.last_check_time = time.time()
    
    def transfer_with_throttle(self, data, transfer_function):
        """
        Transfer data with throttling applied
        
        Args:
            data (bytes): Data to transfer
            transfer_function (callable): Function to call for actual transfer
            
        Returns:
            Result from transfer_function
        """
        # Wait for transfer window if scheduled
        self.wait_for_transfer_window()
        
        # Get data size
        data_size = len(data)
        
        # Apply throttling (pre-transfer delay)
        start_time = time.time()
        self.throttle(data_size)
        throttle_delay = time.time() - start_time
        
        # Perform actual transfer
        transfer_start = time.time()
        result = transfer_function(data)
        transfer_duration = time.time() - transfer_start
        
        # Calculate actual rate
        total_duration = time.time() - start_time
        actual_rate_mbps = bytes_to_mbps(data_size, total_duration)
        
        print(f"[*] Transferred {data_size:,} bytes in {total_duration:.2f}s ({actual_rate_mbps:.2f} Mbps)")
        
        if throttle_delay > 0.1:
            print(f"    Throttle delay: {throttle_delay:.2f}s")
        
        return result
    
    def get_stats(self):
        """
        Get current transfer statistics
        
        Returns:
            dict: Statistics including total bytes, time, rate
        """
        if self.start_time is None:
            return {
                'total_bytes': 0,
                'elapsed_seconds': 0,
                'avg_rate_mbps': 0,
                'max_rate_mbps': self.max_rate_mbps
            }
        
        elapsed = time.time() - self.start_time
        avg_rate_mbps = bytes_to_mbps(self.transferred, elapsed)
        
        return {
            'total_bytes': self.transferred,
            'total_mb': self.transferred / (1024 * 1024),
            'elapsed_seconds': elapsed,
            'avg_rate_mbps': avg_rate_mbps,
            'max_rate_mbps': self.max_rate_mbps,
            'utilization': (avg_rate_mbps / self.max_rate_mbps * 100) if self.max_rate_mbps > 0 else 0
        }
    
    def reset_stats(self):
        """Reset transfer statistics"""
        with self.lock:
            self.transferred = 0
            self.start_time = None
            self.last_check_time = None
        
        print("[*] Statistics reset")
    
    def update_max_rate(self, new_rate_mbps):
        """
        Update maximum transfer rate
        
        Args:
            new_rate_mbps (float): New maximum rate in Mbps
        """
        with self.lock:
            self.max_rate_mbps = new_rate_mbps
            self.max_rate_bytes_per_sec = mbps_to_bytes_per_sec(new_rate_mbps)
        
        print(f"[*] Max rate updated to {new_rate_mbps} Mbps")
    
    def update_schedule(self, start_hour, end_hour):
        """
        Update transfer schedule
        
        Args:
            start_hour (int): Window start hour (0-23)
            end_hour (int): Window end hour (0-23)
        """
        with self.lock:
            self.schedule = {
                'start_hour': start_hour,
                'end_hour': end_hour
            }
        
        print(f"[*] Schedule updated: {start_hour}:00 - {end_hour}:00")
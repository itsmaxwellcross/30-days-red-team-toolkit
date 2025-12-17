"""
Main orchestrator for Bandwidth Throttling Manager
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from throttling.throttle import BandwidthThrottle
from queue.exfil_queue import TransferQueue
from core.utils import (
    get_rate_preset,
    get_schedule_preset,
    validate_rate,
    validate_hour,
    format_bytes
)
from config import (
    RATE_PRESETS,
    SCHEDULE_PRESETS,
    DEFAULT_MAX_RATE_MBPS
)


class BandwidthOrchestrator:
    """Main coordinator for bandwidth throttling operations"""
    
    def __init__(self):
        self.throttle = None
        self.queue = None
    
    def display_banner(self):
        """Display framework banner"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║         BANDWIDTH THROTTLING MANAGER                      ║
║             Stealth Data Transfer                         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
        print(banner)
    
    def list_presets(self):
        """Display available rate and schedule presets"""
        print("\n" + "="*60)
        print("RATE PRESETS")
        print("="*60 + "\n")
        
        for preset_id, info in RATE_PRESETS.items():
            print(f"[{preset_id.upper()}]")
            print(f"  Name: {info['name']}")
            print(f"  Rate: {info['rate_mbps']} Mbps")
            print(f"  Description: {info['description']}")
            print()
        
        print("="*60)
        print("SCHEDULE PRESETS")
        print("="*60 + "\n")
        
        for preset_id, info in SCHEDULE_PRESETS.items():
            print(f"[{preset_id.upper()}]")
            print(f"  Name: {info['name']}")
            print(f"  Window: {info['start_hour']}:00 - {info['end_hour']}:00")
            print(f"  Description: {info['description']}")
            print()
    
    def initialize_throttle(self, max_rate_mbps=None, rate_preset=None, 
                           schedule=None, schedule_preset=None):
        """
        Initialize bandwidth throttle
        
        Args:
            max_rate_mbps (float): Maximum rate in Mbps
            rate_preset (str): Rate preset name
            schedule (dict): Custom schedule
            schedule_preset (str): Schedule preset name
            
        Returns:
            BandwidthThrottle: Initialized throttle
        """
        # Determine rate
        if rate_preset:
            preset = get_rate_preset(rate_preset)
            if preset:
                max_rate_mbps = preset['rate_mbps']
                print(f"[*] Using rate preset: {preset['name']}")
            else:
                print(f"[!] Unknown rate preset: {rate_preset}")
                max_rate_mbps = DEFAULT_MAX_RATE_MBPS
        
        if max_rate_mbps is None:
            max_rate_mbps = DEFAULT_MAX_RATE_MBPS
        
        # Validate rate
        is_valid, msg = validate_rate(max_rate_mbps)
        if not is_valid:
            print(f"[-] Invalid rate: {msg}")
            return None
        else:
            print(f"[*] {msg}")
        
        # Determine schedule
        if schedule_preset:
            preset = get_schedule_preset(schedule_preset)
            if preset:
                schedule = {
                    'start_hour': preset['start_hour'],
                    'end_hour': preset['end_hour']
                }
                print(f"[*] Using schedule preset: {preset['name']}")
            else:
                print(f"[!] Unknown schedule preset: {schedule_preset}")
        
        # Validate schedule
        if schedule:
            if not validate_hour(schedule['start_hour']):
                print(f"[-] Invalid start hour: {schedule['start_hour']}")
                schedule = None
            elif not validate_hour(schedule['end_hour']):
                print(f"[-] Invalid end hour: {schedule['end_hour']}")
                schedule = None
        
        # Create throttle
        self.throttle = BandwidthThrottle(max_rate_mbps, schedule)
        
        # Create queue
        self.queue = TransferQueue(self.throttle)
        
        return self.throttle
    
    def run_test(self, num_chunks=5, chunk_size_mb=1):
        """
        Run transfer test
        
        Args:
            num_chunks (int): Number of chunks to transfer
            chunk_size_mb (int): Size of each chunk in MB
            
        Returns:
            dict: Test results
        """
        if not self.throttle:
            print("[!] Throttle not initialized")
            return None
        
        print("\n" + "="*60)
        print("RUNNING TRANSFER TEST")
        print("="*60)
        print(f"Chunks: {num_chunks}")
        print(f"Chunk size: {chunk_size_mb} MB")
        print(f"Total: {num_chunks * chunk_size_mb} MB")
        print()
        
        # Mock transfer function
        def mock_transfer(data):
            import time
            time.sleep(0.05)  # Simulate network delay
            return True
        
        # Transfer chunks
        import time
        chunk_size_bytes = chunk_size_mb * 1024 * 1024
        
        for i in range(num_chunks):
            print(f"[*] Chunk {i+1}/{num_chunks}")
            test_data = b'X' * chunk_size_bytes
            self.throttle.transfer_with_throttle(test_data, mock_transfer)
        
        # Get statistics
        stats = self.throttle.get_stats()
        
        print("\n" + "="*60)
        print("TEST COMPLETE")
        print("="*60)
        print(f"Total transferred: {stats['total_mb']:.2f} MB")
        print(f"Duration: {stats['elapsed_seconds']:.2f} seconds")
        print(f"Avg rate: {stats['avg_rate_mbps']:.2f} Mbps")
        print(f"Max rate: {stats['max_rate_mbps']:.2f} Mbps")
        print(f"Utilization: {stats['utilization']:.1f}%")
        print("="*60)
        
        return stats
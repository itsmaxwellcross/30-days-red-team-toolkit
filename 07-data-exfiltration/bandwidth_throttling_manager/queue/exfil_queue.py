"""
File transfer queue with priority scheduling
"""

import os
import time
from datetime import datetime
from pathlib import Path

from core.utils import format_bytes, format_duration, create_progress_bar
from config import (
    PRIORITY_NORMAL,
    MAX_QUEUE_SIZE,
    MAX_RETRIES,
    RETRY_DELAY
)


class TransferQueue:
    """Manages queue of files to transfer"""
    
    def __init__(self, throttle):
        """
        Initialize transfer queue
        
        Args:
            throttle: BandwidthThrottle instance
        """
        self.throttle = throttle
        self.queue = []
        self.completed = []
        self.failed = []
        self.running = False
    
    def add_file(self, filepath, transfer_function, priority=PRIORITY_NORMAL, metadata=None):
        """
        Add file to transfer queue
        
        Args:
            filepath (str): Path to file
            transfer_function (callable): Function to transfer file
            priority (int): Transfer priority (higher = sooner)
            metadata (dict): Optional metadata
            
        Returns:
            bool: True if added successfully
        """
        if len(self.queue) >= MAX_QUEUE_SIZE:
            print(f"[-] Queue full (max {MAX_QUEUE_SIZE} items)")
            return False
        
        path = Path(filepath)
        
        if not path.exists():
            print(f"[-] File not found: {filepath}")
            return False
        
        if not path.is_file():
            print(f"[-] Not a file: {filepath}")
            return False
        
        file_size = path.stat().st_size
        
        item = {
            'filepath': str(path),
            'filename': path.name,
            'size': file_size,
            'transfer_function': transfer_function,
            'priority': priority,
            'status': 'pending',
            'added_time': datetime.now(),
            'attempts': 0,
            'metadata': metadata or {}
        }
        
        self.queue.append(item)
        
        # Sort by priority (descending)
        self.queue.sort(key=lambda x: x['priority'], reverse=True)
        
        print(f"[+] Added to queue: {path.name}")
        print(f"    Size: {format_bytes(file_size)}")
        print(f"    Priority: {priority}")
        print(f"    Queue position: {self._get_item_position(item)}/{len(self.queue)}")
        
        return True
    
    def add_directory(self, directory, transfer_function, priority=PRIORITY_NORMAL, 
                     recursive=True, pattern='*'):
        """
        Add all files from directory to queue
        
        Args:
            directory (str): Directory path
            transfer_function (callable): Transfer function
            priority (int): Priority for all files
            recursive (bool): Include subdirectories
            pattern (str): File pattern (e.g., '*.txt')
            
        Returns:
            int: Number of files added
        """
        dir_path = Path(directory)
        
        if not dir_path.exists() or not dir_path.is_dir():
            print(f"[-] Invalid directory: {directory}")
            return 0
        
        added = 0
        
        if recursive:
            files = dir_path.rglob(pattern)
        else:
            files = dir_path.glob(pattern)
        
        for file_path in files:
            if file_path.is_file():
                if self.add_file(str(file_path), transfer_function, priority):
                    added += 1
        
        print(f"[+] Added {added} file(s) from {directory}")
        
        return added
    
    def remove_item(self, filepath):
        """
        Remove item from queue
        
        Args:
            filepath (str): Path to file
            
        Returns:
            bool: True if removed
        """
        for i, item in enumerate(self.queue):
            if item['filepath'] == filepath:
                self.queue.pop(i)
                print(f"[+] Removed from queue: {filepath}")
                return True
        
        print(f"[-] Not in queue: {filepath}")
        return False
    
    def _get_item_position(self, item):
        """Get position of item in queue"""
        try:
            return self.queue.index(item) + 1
        except ValueError:
            return -1
    
    def _transfer_item(self, item):
        """
        Transfer a single item
        
        Args:
            item (dict): Queue item
            
        Returns:
            bool: True if successful
        """
        print(f"\n[*] Processing: {item['filename']}")
        print(f"    Size: {format_bytes(item['size'])}")
        print(f"    Priority: {item['priority']}")
        
        try:
            # Read file
            with open(item['filepath'], 'rb') as f:
                data = f.read()
            
            # Transfer with throttling
            start_time = time.time()
            result = self.throttle.transfer_with_throttle(data, item['transfer_function'])
            duration = time.time() - start_time
            
            if result:
                item['status'] = 'completed'
                item['completed_time'] = datetime.now()
                item['duration'] = duration
                self.completed.append(item)
                
                print(f"[+] Completed: {item['filename']}")
                print(f"    Duration: {format_duration(duration)}")
                
                return True
            else:
                print(f"[-] Transfer failed: {item['filename']}")
                return False
        
        except Exception as e:
            print(f"[-] Error: {e}")
            return False
    
    def process_queue(self, max_retries=MAX_RETRIES):
        """
        Process entire queue
        
        Args:
            max_retries (int): Maximum retry attempts per file
            
        Returns:
            dict: Processing summary
        """
        if not self.queue:
            print("[!] Queue is empty")
            return None
        
        self.running = True
        
        print("\n" + "="*60)
        print("STARTING QUEUE PROCESSING")
        print("="*60)
        print(f"Queue size: {len(self.queue)} file(s)")
        
        total_size = sum(item['size'] for item in self.queue)
        print(f"Total size: {format_bytes(total_size)}")
        print()
        
        start_time = time.time()
        processed = 0
        
        while self.running and self.queue:
            item = self.queue[0]
            
            # Check retry limit
            if item['attempts'] >= max_retries:
                print(f"[!] Max retries reached for {item['filename']}")
                item['status'] = 'failed'
                self.failed.append(item)
                self.queue.pop(0)
                continue
            
            item['attempts'] += 1
            
            # Show progress
            processed += 1
            progress = create_progress_bar(processed, len(self.queue) + processed)
            print(f"\nProgress: {progress}")
            print(f"Item {processed}/{len(self.queue) + processed}")
            
            # Transfer item
            success = self._transfer_item(item)
            
            if success:
                self.queue.pop(0)
            else:
                # Move to end of queue for retry
                if item['attempts'] < max_retries:
                    print(f"[*] Will retry ({item['attempts']}/{max_retries})")
                    self.queue.pop(0)
                    self.queue.append(item)
                    time.sleep(RETRY_DELAY)
                else:
                    item['status'] = 'failed'
                    self.failed.append(item)
                    self.queue.pop(0)
        
        # Summary
        total_duration = time.time() - start_time
        
        print("\n" + "="*60)
        print("QUEUE PROCESSING COMPLETE")
        print("="*60)
        print(f"Completed: {len(self.completed)} file(s)")
        print(f"Failed: {len(self.failed)} file(s)")
        print(f"Duration: {format_duration(total_duration)}")
        
        # Transfer statistics
        stats = self.throttle.get_stats()
        if stats:
            print(f"\n[*] Transfer Statistics:")
            print(f"    Total: {stats['total_mb']:.2f} MB")
            print(f"    Avg Rate: {stats['avg_rate_mbps']:.2f} Mbps")
            print(f"    Max Rate: {stats['max_rate_mbps']:.2f} Mbps")
            print(f"    Utilization: {stats['utilization']:.1f}%")
        
        return {
            'completed': len(self.completed),
            'failed': len(self.failed),
            'duration': total_duration,
            'stats': stats
        }
    
    def stop(self):
        """Stop queue processing"""
        self.running = False
        print("\n[!] Stopping queue processing...")
    
    def get_status(self):
        """
        Get current queue status
        
        Returns:
            dict: Status information
        """
        return {
            'pending': len(self.queue),
            'completed': len(self.completed),
            'failed': len(self.failed),
            'running': self.running,
            'total_pending_size': sum(item['size'] for item in self.queue)
        }
    
    def list_queue(self):
        """Display queue contents"""
        if not self.queue:
            print("[*] Queue is empty")
            return
        
        print("\n" + "="*60)
        print("TRANSFER QUEUE")
        print("="*60)
        
        for i, item in enumerate(self.queue, 1):
            print(f"\n{i}. {item['filename']}")
            print(f"   Size: {format_bytes(item['size'])}")
            print(f"   Priority: {item['priority']}")
            print(f"   Status: {item['status']}")
            print(f"   Attempts: {item['attempts']}")
        
        print("\n" + "="*60)
        print(f"Total: {len(self.queue)} file(s)")
        print(f"Size: {format_bytes(sum(item['size'] for item in self.queue))}")
        print("="*60)
"""
Utility functions for Bandwidth Throttling Manager
"""

import time
from datetime import datetime, timedelta
from config import RATE_PRESETS, SCHEDULE_PRESETS


def bytes_to_mbps(bytes_count, seconds):
    """
    Convert bytes and time to Mbps
    
    Args:
        bytes_count (int): Number of bytes
        seconds (float): Time duration
        
    Returns:
        float: Rate in Mbps
    """
    if seconds <= 0:
        return 0.0
    
    bits = bytes_count * 8
    mbps = bits / (seconds * 1024 * 1024)
    
    return mbps


def mbps_to_bytes_per_sec(mbps):
    """
    Convert Mbps to bytes per second
    
    Args:
        mbps (float): Rate in Mbps
        
    Returns:
        int: Bytes per second
    """
    return int((mbps * 1024 * 1024) / 8)


def format_bytes(byte_count):
    """
    Format bytes in human-readable format
    
    Args:
        byte_count (int): Bytes
        
    Returns:
        str: Formatted string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if byte_count < 1024.0:
            return f"{byte_count:.2f} {unit}"
        byte_count /= 1024.0
    
    return f"{byte_count:.2f} PB"


def format_duration(seconds):
    """
    Format duration in human-readable format
    
    Args:
        seconds (float): Duration in seconds
        
    Returns:
        str: Formatted duration
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def calculate_eta(bytes_transferred, total_bytes, elapsed_seconds):
    """
    Calculate estimated time to completion
    
    Args:
        bytes_transferred (int): Bytes transferred so far
        total_bytes (int): Total bytes to transfer
        elapsed_seconds (float): Time elapsed
        
    Returns:
        float: Estimated seconds remaining
    """
    if bytes_transferred <= 0 or elapsed_seconds <= 0:
        return 0
    
    rate = bytes_transferred / elapsed_seconds
    remaining_bytes = total_bytes - bytes_transferred
    
    if rate > 0:
        return remaining_bytes / rate
    
    return 0


def is_within_schedule(current_time, start_hour, end_hour):
    """
    Check if current time is within schedule
    
    Args:
        current_time (datetime): Current time
        start_hour (int): Start hour (0-23)
        end_hour (int): End hour (0-23)
        
    Returns:
        bool: True if within schedule
    """
    current_hour = current_time.hour
    
    if start_hour <= end_hour:
        # Normal range (e.g., 9-17)
        return start_hour <= current_hour < end_hour
    else:
        # Overnight range (e.g., 22-6)
        return current_hour >= start_hour or current_hour < end_hour


def get_next_window_start(current_time, start_hour, end_hour):
    """
    Calculate when next transfer window starts
    
    Args:
        current_time (datetime): Current time
        start_hour (int): Window start hour
        end_hour (int): Window end hour
        
    Returns:
        datetime: Next window start time
    """
    current_hour = current_time.hour
    
    if start_hour <= end_hour:
        # Normal range
        if current_hour < start_hour:
            # Today
            next_start = current_time.replace(
                hour=start_hour, minute=0, second=0, microsecond=0
            )
        else:
            # Tomorrow
            next_start = (current_time + timedelta(days=1)).replace(
                hour=start_hour, minute=0, second=0, microsecond=0
            )
    else:
        # Overnight range
        if current_hour < start_hour and current_hour >= end_hour:
            # Later today
            next_start = current_time.replace(
                hour=start_hour, minute=0, second=0, microsecond=0
            )
        else:
            # Tomorrow
            next_start = (current_time + timedelta(days=1)).replace(
                hour=start_hour, minute=0, second=0, microsecond=0
            )
    
    return next_start


def calculate_wait_time(current_time, start_hour, end_hour):
    """
    Calculate seconds to wait until transfer window
    
    Args:
        current_time (datetime): Current time
        start_hour (int): Window start hour
        end_hour (int): Window end hour
        
    Returns:
        float: Seconds to wait
    """
    next_start = get_next_window_start(current_time, start_hour, end_hour)
    wait_seconds = (next_start - current_time).total_seconds()
    
    return max(0, wait_seconds)


def get_rate_preset(preset_name):
    """
    Get rate preset configuration
    
    Args:
        preset_name (str): Preset name
        
    Returns:
        dict: Preset configuration or None
    """
    return RATE_PRESETS.get(preset_name)


def get_schedule_preset(preset_name):
    """
    Get schedule preset configuration
    
    Args:
        preset_name (str): Preset name
        
    Returns:
        dict: Preset configuration or None
    """
    return SCHEDULE_PRESETS.get(preset_name)


def validate_hour(hour):
    """
    Validate hour value
    
    Args:
        hour (int): Hour to validate
        
    Returns:
        bool: True if valid
    """
    return isinstance(hour, int) and 0 <= hour <= 23


def validate_rate(rate_mbps):
    """
    Validate transfer rate
    
    Args:
        rate_mbps (float): Rate in Mbps
        
    Returns:
        tuple: (is_valid, message)
    """
    if rate_mbps <= 0:
        return False, "Rate must be positive"
    
    if rate_mbps > 100:
        return True, "Warning: Very high rate may be detectable"
    
    return True, "Rate valid"


def create_progress_bar(current, total, width=50):
    """
    Create text-based progress bar
    
    Args:
        current (int): Current progress
        total (int): Total items
        width (int): Bar width in characters
        
    Returns:
        str: Progress bar string
    """
    if total <= 0:
        percent = 0
    else:
        percent = min(100, (current / total) * 100)
    
    filled = int(width * current / total) if total > 0 else 0
    bar = '█' * filled + '░' * (width - filled)
    
    return f"[{bar}] {percent:.1f}%"
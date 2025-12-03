"""
Cloud C2 Utilities - Helper functions
"""

import re
import json
from datetime import datetime, timedelta


def validate_bucket_name(bucket_name):
    """
    Validate S3 bucket name
    
    Args:
        bucket_name (str): Bucket name to validate
    
    Returns:
        tuple: (is_valid, error_message)
    """
    # S3 bucket naming rules
    if len(bucket_name) < 3 or len(bucket_name) > 63:
        return False, "Bucket name must be between 3 and 63 characters"
    
    if not re.match(r'^[a-z0-9][a-z0-9\-]*[a-z0-9]$', bucket_name):
        return False, "Bucket name must start and end with lowercase letter or number"
    
    if '..' in bucket_name:
        return False, "Bucket name cannot contain consecutive periods"
    
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', bucket_name):
        return False, "Bucket name cannot be formatted as IP address"
    
    return True, None


def estimate_costs(num_agents, beacon_interval, days=30):
    """
    Estimate AWS S3 costs for C2 operations
    
    Args:
        num_agents (int): Number of agents
        beacon_interval (int): Beacon interval in seconds
        days (int): Number of days
    
    Returns:
        dict: Cost breakdown
    """
    # Average sizes
    task_size = 0.5  # KB
    result_size = 2  # KB
    session_size = 1  # KB
    
    # Calculate operations per day
    beacons_per_day = (86400 / beacon_interval) * num_agents
    
    # Requests
    put_requests = beacons_per_day  # Results
    get_requests = beacons_per_day  # Check for tasks
    
    # Storage (cumulative)
    daily_storage = ((result_size * beacons_per_day) + 
                     (session_size * num_agents)) / 1024 / 1024  # GB
    total_storage = daily_storage * days
    
    # AWS pricing (approximate)
    storage_cost_per_gb = 0.023  # First 50 TB / month
    put_cost_per_1000 = 0.005
    get_cost_per_1000 = 0.0004
    
    # Calculate costs
    storage_cost = total_storage * storage_cost_per_gb
    put_cost = (put_requests * days / 1000) * put_cost_per_1000
    get_cost = (get_requests * days / 1000) * get_cost_per_1000
    
    total_cost = storage_cost + put_cost + get_cost
    
    return {
        'num_agents': num_agents,
        'beacon_interval': beacon_interval,
        'days': days,
        'beacons_per_day': int(beacons_per_day),
        'storage_gb': round(total_storage, 2),
        'put_requests': int(put_requests * days),
        'get_requests': int(get_requests * days),
        'storage_cost': round(storage_cost, 2),
        'put_cost': round(put_cost, 2),
        'get_cost': round(get_cost, 2),
        'total_cost': round(total_cost, 2),
        'cost_per_day': round(total_cost / days, 2)
    }


def list_all_sessions(cloud_c2):
    """
    List all sessions with detailed info
    
    Args:
        cloud_c2: CloudC2 instance
    
    Returns:
        list: List of session info
    """
    session_keys = cloud_c2.list_objects(prefix='sessions/')
    sessions = []
    
    for key in session_keys:
        data = cloud_c2.download_object(key)
        if data:
            try:
                session = json.loads(data)
                
                # Add heartbeat
                session_id = session.get('session_id')
                heartbeat_key = f"heartbeats/{session_id}.txt"
                last_seen = cloud_c2.download_object(heartbeat_key)
                
                if last_seen:
                    session['last_seen'] = last_seen
                    session['is_active'] = is_session_active(last_seen)
                
                sessions.append(session)
            except:
                continue
    
    return sessions


def is_session_active(last_seen, timeout_minutes=10):
    """
    Check if session is considered active
    
    Args:
        last_seen (str): Last seen timestamp (ISO format)
        timeout_minutes (int): Timeout in minutes
    
    Returns:
        bool: True if active, False otherwise
    """
    try:
        last_seen_dt = datetime.fromisoformat(last_seen)
        timeout = timedelta(minutes=timeout_minutes)
        
        return datetime.now() - last_seen_dt < timeout
    except:
        return False


def format_session_table(sessions):
    """
    Format sessions as table
    
    Args:
        sessions (list): List of session dicts
    
    Returns:
        str: Formatted table
    """
    if not sessions:
        return "No sessions found"
    
    lines = []
    lines.append("="*100)
    lines.append(f"{'Session ID':<20} {'Hostname':<20} {'Platform':<15} {'Last Seen':<25}")
    lines.append("="*100)
    
    for session in sessions:
        session_id = session.get('session_id', 'unknown')[:20]
        hostname = session.get('hostname', 'unknown')[:20]
        platform = session.get('platform', 'unknown')[:15]
        last_seen = session.get('last_seen', 'never')[:25]
        
        lines.append(f"{session_id:<20} {hostname:<20} {platform:<15} {last_seen:<25}")
    
    lines.append("="*100)
    
    return '\n'.join(lines)


def export_sessions_json(sessions, filename):
    """
    Export sessions to JSON file
    
    Args:
        sessions (list): List of sessions
        filename (str): Output filename
    """
    with open(filename, 'w') as f:
        json.dump(sessions, f, indent=2)
    
    print(f"[+] Exported {len(sessions)} sessions to {filename}")


def generate_aws_policy(bucket_name):
    """
    Generate minimal AWS IAM policy for C2 operations
    
    Args:
        bucket_name (str): S3 bucket name
    
    Returns:
        dict: IAM policy document
    """
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:GetObject",
                    "s3:DeleteObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    f"arn:aws:s3:::{bucket_name}",
                    f"arn:aws:s3:::{bucket_name}/*"
                ]
            }
        ]
    }
    
    return policy
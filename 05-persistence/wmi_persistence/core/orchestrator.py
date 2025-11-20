"""
Main orchestrator for WMI Persistence Framework
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import check_admin, generate_event_name
from config import EVENT_NAME_COMPONENTS
from methods.interval import create_interval_persistence
from methods.logon import create_logon_persistence
from methods.process import (
    create_process_creation_persistence,
    create_process_deletion_persistence
)
from methods.custom import create_custom_persistence
from detection.scanner import (
    find_suspicious_subscriptions,
    generate_wmi_report,
    list_all_subscriptions
)
from output.removal import (
    remove_wmi_persistence,
    generate_removal_script
)

class WMIPersistenceOrchestrator:
    """Main coordinator for all WMI persistence operations"""
    
    def __init__(self):
        self.is_admin = check_admin()
        self.created_subscriptions = []
    
    def create_persistence(self, payload_command, method='interval', 
                          event_name=None, **kwargs):
        """
        Create WMI persistence using specified method
        
        Args:
            payload_command (str): Command to execute
            method (str): Trigger method (interval/logon/process/custom)
            event_name (str): Custom event name
            **kwargs: Method-specific parameters
            
        Returns:
            dict: Operation result
        """
        # Generate event name if not provided
        if not event_name:
            event_name = generate_event_name(EVENT_NAME_COMPONENTS)
        
        print(f"\n{'='*60}")
        print(f"WMI PERSISTENCE CREATION: {method.upper()}")
        print(f"{'='*60}\n")
        
        result = None
        
        if method == 'interval':
            interval = kwargs.get('interval', 60)
            result = create_interval_persistence(event_name, payload_command, interval)
        
        elif method == 'logon':
            result = create_logon_persistence(event_name, payload_command)
        
        elif method == 'process':
            process_name = kwargs.get('process_name')
            if not process_name:
                return {
                    'success': False,
                    'error': 'process_name required for process method'
                }
            
            trigger_on = kwargs.get('trigger_on', 'creation')
            if trigger_on == 'creation':
                result = create_process_creation_persistence(
                    event_name, payload_command, process_name
                )
            else:
                result = create_process_deletion_persistence(
                    event_name, payload_command, process_name
                )
        
        elif method == 'custom':
            wql_query = kwargs.get('wql_query')
            if not wql_query:
                return {
                    'success': False,
                    'error': 'wql_query required for custom method'
                }
            
            result = create_custom_persistence(event_name, payload_command, wql_query)
        
        else:
            return {
                'success': False,
                'error': f'Unknown method: {method}'
            }
        
        # Track successful creations
        if result and result.get('success'):
            self.created_subscriptions.append(result)
            
            # Generate removal script
            script_path = generate_removal_script(result)
            if script_path:
                result['removal_script_path'] = script_path
                print(f"\n[+] Removal script: {script_path}")
        
        print(f"\n{'='*60}\n")
        return result
    
    def scan_subscriptions(self):
        """
        Scan for suspicious WMI subscriptions
        
        Returns:
            dict: Scan report
        """
        return generate_wmi_report()
    
    def list_all(self):
        """List all WMI event subscriptions"""
        return list_all_subscriptions()
    
    def remove_persistence(self, event_name):
        """
        Remove WMI persistence by event name
        
        Args:
            event_name (str): Event name
            
        Returns:
            dict: Removal result
        """
        print(f"\n{'='*60}")
        print("WMI PERSISTENCE REMOVAL")
        print(f"{'='*60}\n")
        
        result = remove_wmi_persistence(event_name)
        
        print(f"\n{'='*60}\n")
        return result
    
    def remove_all_created(self):
        """
        Remove all WMI subscriptions created by this orchestrator
        
        Returns:
            dict: Removal results
        """
        print(f"\n{'='*60}")
        print("REMOVE ALL CREATED SUBSCRIPTIONS")
        print(f"{'='*60}\n")
        
        results = {
            'removed': [],
            'failed': [],
            'total': len(self.created_subscriptions)
        }
        
        for subscription in self.created_subscriptions:
            event_name = subscription.get('event_name')
            print(f"[*] Removing: {event_name}")
            
            result = remove_wmi_persistence(event_name)
            
            if result.get('success'):
                results['removed'].append(event_name)
            else:
                results['failed'].append(event_name)
        
        print(f"\n[+] Removal complete")
        print(f"    Removed: {len(results['removed'])}")
        print(f"    Failed: {len(results['failed'])}")
        print(f"\n{'='*60}\n")
        
        return results
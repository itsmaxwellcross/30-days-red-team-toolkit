"""
Main orchestrator for Service Persistence Framework
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import check_admin, generate_service_name
from config import SERVICE_NAME_COMPONENTS
from methods.create import (
    create_service,
    create_delayed_service,
    delete_service
)
from methods.wrapper import (
    create_wrapped_service,
    cleanup_wrapper_files
)
from methods.modify import (
    modify_service_binary,
    restore_service_config,
    backup_service_config
)
from detection.scanner import (
    find_suspicious_services,
    generate_service_report,
    list_services
)
from output.removal import (
    generate_removal_script,
    generate_restore_script
)

class ServicePersistenceOrchestrator:
    """Main coordinator for all service persistence operations"""
    
    def __init__(self):
        self.is_admin = check_admin()
        self.created_services = []
        self.modified_services = []
    
    def create_service(self, payload_path=None, payload_command=None, 
                      service_name=None, display_name=None, description=None,
                      method='create', start_type='auto'):
        """
        Create service using specified method
        
        Args:
            payload_path (str): Path to executable (for direct creation)
            payload_command (str): Command to execute (for wrapper method)
            service_name (str): Custom service name
            display_name (str): Display name
            description (str): Description
            method (str): Creation method (create/wrapper)
            start_type (str): Service start type
            
        Returns:
            dict: Operation result
        """
        # Generate service name if not provided
        if not service_name:
            service_name = generate_service_name(SERVICE_NAME_COMPONENTS)
        
        print(f"\n{'='*60}")
        print(f"SERVICE CREATION: {method.upper()}")
        print(f"{'='*60}\n")
        
        if method == 'create':
            if not payload_path:
                return {
                    'success': False,
                    'error': 'payload_path required for direct creation'
                }
            
            if start_type == 'delayed':
                result = create_delayed_service(
                    service_name, payload_path, display_name, description
                )
            else:
                result = create_service(
                    service_name, payload_path, display_name, 
                    description, start_type
                )
        
        elif method == 'wrapper':
            if not payload_command:
                return {
                    'success': False,
                    'error': 'payload_command required for wrapper creation'
                }
            
            result = create_wrapped_service(
                service_name, payload_command, display_name, description
            )
        
        else:
            return {
                'success': False,
                'error': f'Unknown method: {method}'
            }
        
        # Track successful creations
        if result.get('success'):
            self.created_services.append(result)
            
            # Generate removal script
            script_path = generate_removal_script(result)
            if script_path:
                result['removal_script_path'] = script_path
                print(f"\n[+] Removal script: {script_path}")
        
        print(f"\n{'='*60}\n")
        return result
    
    def modify_service(self, service_name, new_binary_path):
        """
        Modify existing service
        
        Args:
            service_name (str): Service name to modify
            new_binary_path (str): New binary path
            
        Returns:
            dict: Operation result
        """
        print(f"\n{'='*60}")
        print(f"SERVICE MODIFICATION")
        print(f"{'='*60}\n")
        
        result = modify_service_binary(service_name, new_binary_path)
        
        if result.get('success'):
            self.modified_services.append(result)
            
            # Generate restore script
            script_path = generate_restore_script(result)
            if script_path:
                result['restore_script_path'] = script_path
                print(f"\n[+] Restore script: {script_path}")
        
        print(f"\n{'='*60}\n")
        return result
    
    def scan_services(self):
        """
        Scan for suspicious services
        
        Returns:
            dict: Scan report
        """
        return generate_service_report()
    
    def list_all_services(self):
        """List all services"""
        return list_services('all')
    
    def list_running_services(self):
        """List running services"""
        return list_services('active')
    
    def delete_service(self, service_name):
        """
        Delete a service
        
        Args:
            service_name (str): Service name
            
        Returns:
            dict: Result
        """
        result = delete_service(service_name)
        return result
    
    def cleanup_all(self):
        """
        Clean up all created/modified services
        
        Returns:
            dict: Cleanup results
        """
        print(f"\n{'='*60}")
        print("CLEANUP ALL SERVICES")
        print(f"{'='*60}\n")
        
        results = {
            'deleted_services': [],
            'restored_services': [],
            'cleaned_wrappers': [],
            'errors': []
        }
        
        # Delete created services
        for service_data in self.created_services:
            service_name = service_data.get('service_name')
            print(f"[*] Deleting: {service_name}")
            
            result = delete_service(service_name)
            if result.get('success'):
                results['deleted_services'].append(service_name)
                
                # Cleanup wrapper files if applicable
                if 'wrapper' in service_data:
                    cleanup_result = cleanup_wrapper_files(service_name)
                    if cleanup_result.get('success'):
                        results['cleaned_wrappers'].append(service_name)
            else:
                results['errors'].append(f"Failed to delete {service_name}")
        
        # Restore modified services
        for service_data in self.modified_services:
            service_name = service_data.get('service_name')
            original_config = service_data.get('original_config')
            
            if original_config:
                print(f"[*] Restoring: {service_name}")
                result = restore_service_config(service_name, original_config)
                
                if result.get('success'):
                    results['restored_services'].append(service_name)
                else:
                    results['errors'].append(f"Failed to restore {service_name}")
        
        print(f"\n[+] Cleanup complete")
        print(f"    Deleted: {len(results['deleted_services'])}")
        print(f"    Restored: {len(results['restored_services'])}")
        print(f"    Errors: {len(results['errors'])}")
        print(f"\n{'='*60}\n")
        
        return results
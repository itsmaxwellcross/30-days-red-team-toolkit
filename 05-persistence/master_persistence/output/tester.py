"""
Testing instructions and validation for persistence mechanisms
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import print_section_header
from config import TESTING_INSTRUCTIONS


class PersistenceTester:
    """Provides testing instructions and validation"""
    
    def display_testing_instructions(self, installed_methods):
        """
        Display instructions for testing installed persistence
        
        Args:
            installed_methods: List of installed persistence method dicts
        """
        if not installed_methods:
            print("[!] No persistence methods installed - nothing to test")
            return
        
        print_section_header("PERSISTENCE TESTING")
        
        self._print_general_instructions()
        self._print_method_specific_instructions(installed_methods)
    
    def _print_general_instructions(self):
        """Print general testing instructions"""
        print("[*] To test persistence:\n")
        print("  1. Reboot the system")
        print("  2. Log off and log back on")
        print("  3. Wait for scheduled tasks to trigger")
        print("  4. Check for incoming connections on your handler\n")
    
    def _print_method_specific_instructions(self, installed_methods):
        """
        Print method-specific testing instructions
        
        Args:
            installed_methods: List of installed persistence method dicts
        """
        print("[*] Expected behaviors:\n")
        
        for method in installed_methods:
            method_type = method.get('method', 'Unknown').lower()
            trigger_info = method.get('trigger', '')
            
            instruction = self._get_method_instruction(method_type, trigger_info)
            print(f"  - {method.get('method', 'Unknown')}: {instruction}")
    
    def _get_method_instruction(self, method_type, trigger_info=''):
        """
        Get testing instruction for a specific method type
        
        Args:
            method_type: Type of persistence method
            trigger_info: Additional trigger information
            
        Returns:
            str: Testing instruction
        """
        # Check for specific method types
        if 'run' in method_type and 'key' in method_type:
            return TESTING_INSTRUCTIONS['run_key']
        
        elif 'scheduled' in method_type or 'task' in method_type:
            if trigger_info:
                return f"Triggers {trigger_info}"
            return TESTING_INSTRUCTIONS['scheduled_task']
        
        elif 'service' in method_type:
            return TESTING_INSTRUCTIONS['service']
        
        elif 'wmi' in method_type:
            return TESTING_INSTRUCTIONS['wmi']
        
        elif 'screensaver' in method_type:
            return TESTING_INSTRUCTIONS['screensaver']
        
        else:
            return "Check method-specific trigger conditions"
    
    def generate_test_checklist(self, installed_methods, output_file='test_checklist.txt'):
        """
        Generate a test checklist file
        
        Args:
            installed_methods: List of installed persistence methods
            output_file: Output filename
            
        Returns:
            str: Path to checklist file
        """
        from datetime import datetime
        
        checklist = f'''PERSISTENCE TESTING CHECKLIST
Generated: {datetime.now().isoformat()}

SETUP:
[ ] Start handler on attacker machine
[ ] Note current time for correlation
[ ] Prepare to monitor network connections

TESTS TO PERFORM:

'''
        
        for i, method in enumerate(installed_methods, 1):
            method_name = method.get('method', 'Unknown')
            method_type = method_name.lower()
            trigger_info = method.get('trigger', '')
            
            instruction = self._get_method_instruction(method_type, trigger_info)
            
            checklist += f'''{i}. {method_name}
   Trigger: {instruction}
   [ ] Tested
   [ ] Connection received
   Notes: ___________________________________________

'''
        
        checklist += '''
POST-TESTING:
[ ] Verify all connections received
[ ] Document any failures
[ ] Run removal script
[ ] Verify all persistence removed

'''
        
        try:
            with open(output_file, 'w') as f:
                f.write(checklist)
            
            print(f"\n[+] Test checklist generated: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"[!] Failed to generate checklist: {e}")
            return None
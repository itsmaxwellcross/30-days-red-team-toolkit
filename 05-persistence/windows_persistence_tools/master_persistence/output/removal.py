"""
Removal script generation for installed persistence methods
"""

import os
from datetime import datetime
from config import REMOVAL_SCRIPT_PREFIX, REMOVAL_SCRIPT_EXTENSION


class RemovalScriptGenerator:
    """Generates batch scripts to remove all installed persistence"""
    
    def generate_removal_script(self, installed_methods):
        """
        Generate batch script to remove all persistence mechanisms
        
        Args:
            installed_methods: List of installed persistence method dicts
        """
        if not installed_methods:
            print("[!] No methods installed - no removal script needed")
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        removal_file = f"{REMOVAL_SCRIPT_PREFIX}_{timestamp}{REMOVAL_SCRIPT_EXTENSION}"
        
        script_content = self._build_script_content(installed_methods)
        
        try:
            with open(removal_file, 'w') as f:
                f.write(script_content)
            
            print(f"[+] Removal script generated: {removal_file}")
            print(f"[!] Run this script to remove all persistence")
            
            return removal_file
            
        except Exception as e:
            print(f"[!] Failed to write removal script: {e}")
            return None
    
    def _build_script_content(self, installed_methods):
        """
        Build the content of the removal script
        
        Args:
            installed_methods: List of installed persistence method dicts
            
        Returns:
            str: Complete batch script content
        """
        script = self._get_script_header()
        
        for i, method in enumerate(installed_methods, 1):
            script += self._format_removal_command(i, method)
        
        script += self._get_script_footer()
        
        return script
    
    def _get_script_header(self):
        """Get batch script header"""
        return f'''@echo off
REM Persistence Removal Script
REM Generated: {datetime.now().isoformat()}
REM 
REM WARNING: This will remove ALL installed persistence mechanisms
REM

echo [*] Removing persistence mechanisms...
echo.

'''
    
    def _format_removal_command(self, number, method):
        """
        Format a single removal command
        
        Args:
            number: Method number
            method: Method dict with 'method' and 'remove_command' keys
            
        Returns:
            str: Formatted removal commands
        """
        method_name = method.get('method', 'Unknown')
        remove_cmd = method.get('remove_command', '')
        
        return f'''echo [{number}] Removing {method_name}...
{remove_cmd}
echo.

'''
    
    def _get_script_footer(self):
        """Get batch script footer"""
        return '''echo [+] All persistence removed
pause
'''
    
    def generate_powershell_removal(self, installed_methods, output_file=None):
        """
        Generate PowerShell removal script (alternative to batch)
        
        Args:
            installed_methods: List of installed persistence method dicts
            output_file: Optional output filename
            
        Returns:
            str: Path to generated script
        """
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"{REMOVAL_SCRIPT_PREFIX}_{timestamp}.ps1"
        
        script = '''# Persistence Removal Script (PowerShell)
# Generated: {timestamp}

Write-Host "[*] Removing persistence mechanisms..." -ForegroundColor Cyan
Write-Host ""

'''.format(timestamp=datetime.now().isoformat())
        
        for i, method in enumerate(installed_methods, 1):
            method_name = method.get('method', 'Unknown')
            # Convert batch commands to PowerShell equivalents
            script += f'''Write-Host "[{i}] Removing {method_name}..." -ForegroundColor Yellow
# {method.get('remove_command', '')}
Write-Host ""

'''
        
        script += '''Write-Host "[+] All persistence removed" -ForegroundColor Green
Read-Host "Press Enter to exit"
'''
        
        try:
            with open(output_file, 'w') as f:
                f.write(script)
            
            return output_file
            
        except Exception as e:
            print(f"[!] Failed to write PowerShell removal script: {e}")
            return None
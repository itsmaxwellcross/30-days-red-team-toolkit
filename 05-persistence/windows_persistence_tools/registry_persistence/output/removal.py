"""
Generate removal scripts for installed persistence mechanisms
"""

import os
from datetime import datetime
from config import DEFAULT_STAGING_DIR


class RemovalScriptGenerator:
    """Generates removal scripts for persistence cleanup"""
    
    def __init__(self, output_dir=DEFAULT_STAGING_DIR):
        self.output_dir = output_dir
    
    def generate_removal_script(self, installed_methods):
        """
        Generate a batch script to remove all installed persistence
        
        Args:
            installed_methods (list): List of installed persistence methods
            
        Returns:
            str: Path to generated removal script
        """
        if not installed_methods:
            print("[!] No persistence methods to remove")
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        script_name = f"remove_persistence_{timestamp}.bat"
        script_path = os.path.join(self.output_dir, script_name)
        
        print(f"[*] Generating removal script: {script_name}")
        
        # Build script content
        script_content = f'''@echo off
REM ============================================================
REM Registry Persistence Removal Script
REM Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
REM Methods: {len(installed_methods)}
REM ============================================================

echo.
echo ========================================
echo Registry Persistence Removal
echo ========================================
echo.
echo This script will remove {len(installed_methods)} persistence mechanism(s)
echo.
pause

'''
        
        # Add removal commands for each method
        for i, method in enumerate(installed_methods, 1):
            method_name = method.get('method', 'unknown')
            
            script_content += f'''
REM ------------------------------------------------------------
REM {i}. Removing {method_name}
REM ------------------------------------------------------------
echo Removing {method_name}...
'''
            
            # Add the removal command
            removal_cmd = method.get('remove_command', '')
            if removal_cmd:
                script_content += f'{removal_cmd}\n'
                script_content += 'if %ERRORLEVEL% EQU 0 (\n'
                script_content += f'    echo [+] {method_name} removed successfully\n'
                script_content += ') else (\n'
                script_content += f'    echo [-] Failed to remove {method_name}\n'
                script_content += ')\n'
            
            # Add file cleanup if applicable
            if 'script' in method:
                script_path_to_delete = method['script']
                script_content += f'\nREM Clean up script file\n'
                script_content += f'if exist "{script_path_to_delete}" (\n'
                script_content += f'    del /f /q "{script_path_to_delete}"\n'
                script_content += f'    echo [+] Deleted {script_path_to_delete}\n'
                script_content += ')\n'
            
            if 'wrapper' in method:
                wrapper_path = method['wrapper']
                script_content += f'\nREM Clean up wrapper file\n'
                script_content += f'if exist "{wrapper_path}" (\n'
                script_content += f'    del /f /q "{wrapper_path}"\n'
                script_content += f'    echo [+] Deleted {wrapper_path}\n'
                script_content += ')\n'
            
            script_content += 'echo.\n'
        
        # Add completion message
        script_content += '''
echo.
echo ========================================
echo Removal Complete
echo ========================================
echo.
echo All persistence mechanisms have been processed.
echo Please verify manually that everything was removed.
echo.
pause
'''
        
        try:
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            print(f"[+] Removal script created: {script_path}")
            print(f"[+] Methods to remove: {len(installed_methods)}")
            print(f"\n[*] To remove persistence, run:")
            print(f"    {script_path}")
            
            return script_path
            
        except Exception as e:
            print(f"[-] Error creating removal script: {e}")
            return None
    
    def generate_powershell_removal(self, installed_methods):
        """
        Generate a PowerShell removal script
        
        Args:
            installed_methods (list): List of installed persistence methods
            
        Returns:
            str: Path to generated PowerShell script
        """
        if not installed_methods:
            print("[!] No persistence methods to remove")
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        script_name = f"remove_persistence_{timestamp}.ps1"
        script_path = os.path.join(self.output_dir, script_name)
        
        print(f"[*] Generating PowerShell removal script: {script_name}")
        
        # Build PowerShell script
        ps_script = f'''# Registry Persistence Removal Script
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Methods: {len(installed_methods)}

Write-Host ""
Write-Host "========================================"
Write-Host "Registry Persistence Removal"
Write-Host "========================================"
Write-Host ""
Write-Host "This script will remove {len(installed_methods)} persistence mechanism(s)"
Write-Host ""
Read-Host "Press Enter to continue"

'''
        
        # Add removal for each method
        for i, method in enumerate(installed_methods, 1):
            method_name = method.get('method', 'unknown')
            
            ps_script += f'''
# ------------------------------------------------------------
# {i}. Removing {method_name}
# ------------------------------------------------------------
Write-Host "Removing {method_name}..." -ForegroundColor Cyan

try {{
'''
            
            # Convert batch commands to PowerShell
            removal_cmd = method.get('remove_command', '')
            
            if 'reg delete' in removal_cmd:
                # Extract reg path and value
                parts = removal_cmd.split('"')
                if len(parts) >= 2:
                    reg_path = parts[1]
                    if '/v' in removal_cmd:
                        value_name = parts[3] if len(parts) >= 4 else ''
                        ps_script += f'    Remove-ItemProperty -Path "Registry::{reg_path}" -Name "{value_name}" -Force -ErrorAction Stop\n'
                    else:
                        ps_script += f'    Remove-Item -Path "Registry::{reg_path}" -Force -Recurse -ErrorAction Stop\n'
            
            ps_script += f'''    Write-Host "[+] {method_name} removed successfully" -ForegroundColor Green
}} catch {{
    Write-Host "[-] Failed to remove {method_name}: $_" -ForegroundColor Red
}}

'''
            
            # File cleanup
            if 'script' in method:
                script_path_to_delete = method['script']
                ps_script += f'''if (Test-Path "{script_path_to_delete}") {{
    Remove-Item "{script_path_to_delete}" -Force
    Write-Host "[+] Deleted {script_path_to_delete}" -ForegroundColor Green
}}

'''
            
            if 'wrapper' in method:
                wrapper_path = method['wrapper']
                ps_script += f'''if (Test-Path "{wrapper_path}") {{
    Remove-Item "{wrapper_path}" -Force
    Write-Host "[+] Deleted {wrapper_path}" -ForegroundColor Green
}}

'''
        
        ps_script += '''
Write-Host ""
Write-Host "========================================"
Write-Host "Removal Complete"
Write-Host "========================================"
Write-Host ""
Write-Host "All persistence mechanisms have been processed."
Write-Host "Please verify manually that everything was removed."
Write-Host ""
Read-Host "Press Enter to exit"
'''
        
        try:
            with open(script_path, 'w') as f:
                f.write(ps_script)
            
            print(f"[+] PowerShell removal script created: {script_path}")
            print(f"[+] Methods to remove: {len(installed_methods)}")
            print(f"\n[*] To remove persistence, run:")
            print(f"    powershell -ExecutionPolicy Bypass -File {script_path}")
            
            return script_path
            
        except Exception as e:
            print(f"[-] Error creating PowerShell removal script: {e}")
            return None
    
    def generate_report(self, installed_methods):
        """
        Generate a detailed report of installed persistence
        
        Args:
            installed_methods (list): List of installed persistence methods
            
        Returns:
            str: Path to generated report
        """
        if not installed_methods:
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_name = f"persistence_report_{timestamp}.txt"
        report_path = os.path.join(self.output_dir, report_name)
        
        print(f"[*] Generating persistence report: {report_name}")
        
        report_content = f'''
{'='*60}
REGISTRY PERSISTENCE INSTALLATION REPORT
{'='*60}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Methods Installed: {len(installed_methods)}

{'='*60}

'''
        
        for i, method in enumerate(installed_methods, 1):
            report_content += f'''
Method #{i}: {method.get('method', 'unknown').upper()}
{'-'*60}
Location: {method.get('path', 'N/A')}
Payload: {method.get('payload', 'N/A')}
Admin Required: {method.get('requires_admin', 'N/A')}
Removal Command: {method.get('remove_command', 'N/A')}

'''
            
            # Add any additional details
            for key, value in method.items():
                if key not in ['method', 'path', 'payload', 'requires_admin', 'remove_command']:
                    report_content += f'{key.replace("_", " ").title()}: {value}\n'
            
            report_content += '\n'
        
        report_content += f'''
{'='*60}
END OF REPORT
{'='*60}
'''
        
        try:
            with open(report_path, 'w') as f:
                f.write(report_content)
            
            print(f"[+] Report generated: {report_path}")
            
            return report_path
            
        except Exception as e:
            print(f"[-] Error generating report: {e}")
            return None
"""
Detection and scanning for existing persistence mechanisms
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.utils import run_command
from config import REGISTRY_PATHS


class PersistenceChecker:
    """Scans for existing persistence mechanisms"""
    
    def __init__(self):
        self.findings = []
    
    def scan_all(self):
        """
        Scan for all types of registry persistence
        
        Returns:
            list: All findings
        """
        print("\n" + "="*60)
        print("SCANNING FOR REGISTRY PERSISTENCE")
        print("="*60 + "\n")
        
        self.findings = []
        
        # Scan each type
        self.scan_run_keys()
        self.scan_runonce_keys()
        self.scan_winlogon()
        self.scan_screensaver()
        self.scan_logon_scripts()
        self.scan_ifeo()
        
        # Summary
        print("\n" + "="*60)
        print(f"SCAN COMPLETE - Found {len(self.findings)} potential persistence mechanism(s)")
        print("="*60 + "\n")
        
        return self.findings
    
    def scan_run_keys(self):
        """Scan HKCU and HKLM Run keys"""
        print("[*] Scanning Run keys...")
        
        locations = [
            ("HKCU Run", REGISTRY_PATHS['hkcu_run']),
            ("HKLM Run", REGISTRY_PATHS['hklm_run'])
        ]
        
        for name, path in locations:
            command = f'reg query "{path}"'
            result = run_command(command)
            
            if result and result['success'] and result['stdout']:
                # Parse entries
                entries = self._parse_reg_output(result['stdout'])
                
                if entries:
                    print(f"[+] {name}: Found {len(entries)} entry/entries")
                    for entry in entries:
                        print(f"    {entry['name']}: {entry['value']}")
                        self.findings.append({
                            'type': name,
                            'location': path,
                            'name': entry['name'],
                            'value': entry['value']
                        })
                else:
                    print(f"[-] {name}: No entries (clean)")
            else:
                print(f"[-] {name}: Cannot access")
        
        print()
    
    def scan_runonce_keys(self):
        """Scan RunOnce keys"""
        print("[*] Scanning RunOnce keys...")
        
        locations = [
            ("HKCU RunOnce", REGISTRY_PATHS['hkcu_run_once']),
            ("HKLM RunOnce", REGISTRY_PATHS['hklm_run_once'])
        ]
        
        for name, path in locations:
            command = f'reg query "{path}"'
            result = run_command(command)
            
            if result and result['success'] and result['stdout']:
                entries = self._parse_reg_output(result['stdout'])
                
                if entries:
                    print(f"[+] {name}: Found {len(entries)} entry/entries")
                    for entry in entries:
                        print(f"    {entry['name']}: {entry['value']}")
                        self.findings.append({
                            'type': name,
                            'location': path,
                            'name': entry['name'],
                            'value': entry['value']
                        })
                else:
                    print(f"[-] {name}: No entries (clean)")
            else:
                print(f"[-] {name}: Cannot access")
        
        print()
    
    def scan_winlogon(self):
        """Scan Winlogon keys"""
        print("[*] Scanning Winlogon...")
        
        path = REGISTRY_PATHS['winlogon']
        
        # Check Userinit
        command = f'reg query "{path}" /v Userinit'
        result = run_command(command)
        
        if result and result['success']:
            userinit = self._extract_value(result['stdout'], 'Userinit')
            print(f"[*] Userinit: {userinit}")
            
            # Check if it's been modified (should be just userinit.exe)
            if userinit and not userinit.strip().endswith('userinit.exe,'):
                print(f"[!] SUSPICIOUS: Userinit has been modified!")
                self.findings.append({
                    'type': 'Winlogon Userinit',
                    'location': path,
                    'name': 'Userinit',
                    'value': userinit,
                    'suspicious': True
                })
        
        # Check Shell
        command = f'reg query "{path}" /v Shell'
        result = run_command(command)
        
        if result and result['success']:
            shell = self._extract_value(result['stdout'], 'Shell')
            print(f"[*] Shell: {shell}")
            
            # Check if it's been modified (should be explorer.exe)
            if shell and shell.strip().lower() != 'explorer.exe':
                print(f"[!] SUSPICIOUS: Shell has been replaced!")
                self.findings.append({
                    'type': 'Winlogon Shell',
                    'location': path,
                    'name': 'Shell',
                    'value': shell,
                    'suspicious': True
                })
        
        print()
    
    def scan_screensaver(self):
        """Scan screensaver settings"""
        print("[*] Scanning Screensaver...")
        
        path = REGISTRY_PATHS['screensaver']
        
        # Get screensaver info
        command = f'reg query "{path}"'
        result = run_command(command)
        
        if result and result['success']:
            output = result['stdout']
            
            active = self._extract_value(output, 'ScreenSaveActive')
            exe = self._extract_value(output, 'SCRNSAVE.EXE')
            timeout = self._extract_value(output, 'ScreenSaveTimeout')
            
            if active == '1' and exe:
                print(f"[*] Screensaver Active: Yes")
                print(f"[*] Executable: {exe}")
                print(f"[*] Timeout: {timeout} seconds")
                
                # Check if it's a suspicious executable
                if exe and not exe.lower().endswith('.scr'):
                    print(f"[!] SUSPICIOUS: Not a standard screensaver file!")
                    self.findings.append({
                        'type': 'Screensaver',
                        'location': path,
                        'name': 'SCRNSAVE.EXE',
                        'value': exe,
                        'suspicious': True
                    })
            else:
                print(f"[-] Screensaver: Disabled or not configured")
        
        print()
    
    def scan_logon_scripts(self):
        """Scan logon script entries"""
        print("[*] Scanning Logon Scripts...")
        
        path = REGISTRY_PATHS['environment']
        
        command = f'reg query "{path}" /v UserInitMprLogonScript'
        result = run_command(command)
        
        if result and result['success'] and 'UserInitMprLogonScript' in result['stdout']:
            script = self._extract_value(result['stdout'], 'UserInitMprLogonScript')
            print(f"[+] Found logon script: {script}")
            
            self.findings.append({
                'type': 'Logon Script',
                'location': path,
                'name': 'UserInitMprLogonScript',
                'value': script
            })
        else:
            print(f"[-] No logon scripts configured")
        
        print()
    
    def scan_ifeo(self):
        """Scan for IFEO debugger hijacks"""
        print("[*] Scanning IFEO (Image File Execution Options)...")
        
        path = REGISTRY_PATHS['ifeo']
        
        command = f'reg query "{path}" /s /v Debugger'
        result = run_command(command)
        
        if result and result['success'] and result['stdout']:
            # Parse IFEO entries
            lines = result['stdout'].split('\n')
            current_key = None
            
            for line in lines:
                if path in line and '\\' in line:
                    current_key = line.strip()
                elif 'Debugger' in line and 'REG_SZ' in line and current_key:
                    debugger = line.split('REG_SZ')[-1].strip()
                    target = current_key.split('\\')[-1]
                    
                    print(f"[+] Found IFEO hijack:")
                    print(f"    Target: {target}")
                    print(f"    Debugger: {debugger}")
                    
                    self.findings.append({
                        'type': 'IFEO Hijack',
                        'location': current_key,
                        'name': 'Debugger',
                        'value': debugger,
                        'target': target
                    })
        else:
            print(f"[-] No IFEO hijacks found")
        
        print()
    
    def _parse_reg_output(self, output):
        """Parse registry query output into entries"""
        entries = []
        
        for line in output.split('\n'):
            if 'REG_SZ' in line or 'REG_EXPAND_SZ' in line:
                parts = line.strip().split(None, 2)
                if len(parts) >= 3:
                    name = parts[0]
                    value = parts[2] if len(parts) > 2 else ''
                    
                    # Skip default values and common system entries
                    if name not in ['(Default)', 'SecurityHealth', 'OneDrive']:
                        entries.append({'name': name, 'value': value})
        
        return entries
    
    def _extract_value(self, output, value_name):
        """Extract a specific value from reg query output"""
        for line in output.split('\n'):
            if value_name in line and 'REG_' in line:
                parts = line.split('REG_SZ' if 'REG_SZ' in line else 'REG_EXPAND_SZ')
                if len(parts) >= 2:
                    return parts[-1].strip()
        return None
"""
File system enumeration
"""

import os
from ..core.utils import run_command


class FileEnumerator:
    """Enumerate interesting files"""
    
    def __init__(self, os_type: str):
        self.os_type = os_type
    
    def enumerate(self) -> dict:
        """Run file enumeration"""
        print("\n[*] Searching for interesting files...")
        
        if self.os_type == 'linux':
            files = self._enumerate_linux_files()
        elif self.os_type == 'windows':
            files = self._enumerate_windows_files()
        else:
            files = {}
        
        self._print_results(files)
        return files
    
    def _enumerate_linux_files(self) -> dict:
        """Linux file enumeration"""
        searches = {
            'config_files': [
                'find / -name "*.conf" -type f 2>/dev/null | head -20',
                'find /etc -type f 2>/dev/null | head -30'
            ],
            'credential_files': [
                'find / -name "*.pem" -o -name "*.key" 2>/dev/null | head -20',
                'find /home -name ".ssh" -type d 2>/dev/null'
            ],
            'scripts': [
                'find / -name "*.sh" -type f 2>/dev/null | head -20'
            ],
            'database_files': [
                'find / -name "*.db" -o -name "*.sqlite" 2>/dev/null | head -20'
            ]
        }
        
        results = {}
        for category, commands in searches.items():
            files = []
            for cmd in commands:
                output = run_command(cmd)
                if output and 'Error' not in output:
                    files.extend(output.strip().split('\n'))
            results[category] = [f for f in files if f]
        
        return results
    
    def _enumerate_windows_files(self) -> dict:
        """Windows file enumeration"""
        searches = {
            'config_files': 'dir C:\\ /s /b *.config 2>nul | findstr /v "Windows"',
            'credential_files': 'dir C:\\ /s /b *.key *.pem 2>nul | findstr /v "Windows"',
            'scripts': 'dir C:\\ /s /b *.ps1 *.bat 2>nul | findstr /v "Windows"'
        }
        
        results = {}
        for category, cmd in searches.items():
            output = run_command(cmd)
            if output:
                results[category] = output.strip().split('\n')[:20]
            else:
                results[category] = []
        
        return results
    
    def check_writable(self) -> list:
        """Check for writable directories"""
        print("\n[*] Checking for writable directories...")
        
        writable = []
        check_paths = self._get_check_paths()
        
        for path in check_paths:
            if path and os.path.exists(path):
                if self._test_write(path):
                    writable.append(path)
                    print(f"  [+] Writable: {path}")
        
        return writable
    
    def _get_check_paths(self) -> list:
        """Get paths to check for writeability"""
        if self.os_type == 'linux':
            return ['/tmp', '/var/tmp', '/dev/shm', '/home', '/opt']
        else:
            return ['C:\\Windows\\Temp', 'C:\\Temp', 
                   os.getenv('TEMP'), os.getenv('TMP')]
    
    def _test_write(self, path: str) -> bool:
        """Test if directory is writable"""
        try:
            test_file = os.path.join(path, '.test_write')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            return True
        except:
            return False
    
    def _print_results(self, files: dict):
        """Print file enumeration results"""
        for category, file_list in files.items():
            if file_list:
                print(f"  {category}: {len(file_list)} files found")
                for f in file_list[:5]:
                    print(f"    - {f}")

"""
Browser data harvesting
"""

import os


class BrowserHarvester:
    """Harvest credentials from browser storage"""
    
    def __init__(self, credentials: dict, os_type: str):
        self.credentials = credentials
        self.os_type = os_type
    
    def harvest(self):
        """Attempt to locate browser credential stores"""
        print("\n[*] Searching for browser data...")
        
        chrome_paths, firefox_paths = self._get_browser_paths()
        
        # Check Chrome/Chromium
        for chrome_path in chrome_paths:
            if os.path.exists(chrome_path):
                print(f"  [+] Found Chrome/Chromium data: {chrome_path}")
                print(f"     [!] Use tools like 'chrome-password-dumper' or 'LaZagne' to extract")
                
                self.credentials['passwords'].append({
                    'source': chrome_path,
                    'type': 'Browser Data',
                    'note': 'Requires decryption tool (LaZagne, chrome-password-dumper)'
                })
        
        # Check Firefox
        for firefox_path in firefox_paths:
            if os.path.exists(firefox_path):
                print(f"  [+] Found Firefox data: {firefox_path}")
                print(f"     [!] Use 'firefox_decrypt.py' to extract passwords")
                
                self.credentials['passwords'].append({
                    'source': firefox_path,
                    'type': 'Browser Data',
                    'note': 'Requires decryption tool (firefox_decrypt.py)'
                })
    
    def _get_browser_paths(self) -> tuple:
        """Get browser storage paths based on OS"""
        if self.os_type == 'posix':
            chrome_paths = [
                os.path.expanduser('~/.config/google-chrome/Default/Login Data'),
                os.path.expanduser('~/.config/chromium/Default/Login Data')
            ]
            firefox_paths = [
                os.path.expanduser('~/.mozilla/firefox/')
            ]
        else:
            chrome_paths = [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Login Data'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Login Data')
            ]
            firefox_paths = [
                os.path.expanduser('~/AppData/Roaming/Mozilla/Firefox/Profiles/')
            ]
        
        return chrome_paths, firefox_paths
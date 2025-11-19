"""Registry persistence method implementations"""

from methods.run_keys import RunKeyPersistence
from methods.winlogon import WinlogonPersistence
from methods.screensaver import ScreensaverPersistence
from methods.logon_script import LogonScriptPersistence
from methods.ifeo import IFEOPersistence

__all__ = [
    'RunKeyPersistence',
    'WinlogonPersistence',
    'ScreensaverPersistence',
    'LogonScriptPersistence',
    'IFEOPersistence'
]
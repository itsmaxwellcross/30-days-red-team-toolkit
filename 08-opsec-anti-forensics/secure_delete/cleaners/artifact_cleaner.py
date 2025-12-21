"""
Artifact Cleaner
Clean common forensic artifacts (temp files, browser history, MRU, prefetch)
"""

import os
import platform
from pathlib import Path

from ..core.constants import TEMP_DIRS, BROWSER_PATHS, WINDOWS_PREFETCH, WINDOWS_MRU_KEYS


class ArtifactCleaner:
    """
    Clean forensic artifacts
    
    Provides functionality to clean:
    - Temporary files
    - Browser history
    - Windows Prefetch
    - Windows MRU (Most Recently Used) lists
    - Recycle Bin
    """
    
    def __init__(self):
        """Initialize artifact cleaner"""
        self.os_type = platform.system()
    
    def clean_temp_files(self):
        """
        Clean temporary files
        
        Returns:
            int: Number of files cleaned
        """
        print(f"[*] Cleaning temporary files")
        
        cleaned_count = 0
        
        # Get temp directories for current platform
        temp_dirs = TEMP_DIRS.get(self.os_type, [])
        
        for temp_dir in temp_dirs:
            # Expand environment variables
            temp_dir = os.path.expandvars(temp_dir)
            temp_dir = os.path.expanduser(temp_dir)
            
            if os.path.exists(temp_dir):
                try:
                    files = list(Path(temp_dir).rglob('*'))
                    
                    for filepath in files:
                        if filepath.is_file():
                            try:
                                os.remove(filepath)
                                cleaned_count += 1
                            except PermissionError:
                                # Skip files we can't delete
                                pass
                            except Exception:
                                pass
                
                except PermissionError:
                    print(f"[-] Permission denied: {temp_dir}")
                except Exception as e:
                    print(f"[-] Error cleaning {temp_dir}: {e}")
        
        print(f"[+] Cleaned {cleaned_count} temp files")
        return cleaned_count
    
    def clean_browser_history(self):
        """
        Clean browser history
        
        Returns:
            int: Number of artifacts cleaned
        """
        print(f"[*] Cleaning browser history")
        
        cleaned_count = 0
        
        # Get browser paths for current platform
        browser_paths = BROWSER_PATHS.get(self.os_type, {})
        
        for browser_name, path in browser_paths.items():
            # Expand environment variables
            path = os.path.expandvars(path)
            path = os.path.expanduser(path)
            
            if os.path.exists(path):
                try:
                    if os.path.isfile(path):
                        os.remove(path)
                        cleaned_count += 1
                        print(f"[+] Cleaned {browser_name} history")
                    
                    elif os.path.isdir(path):
                        # Handle Firefox profiles directory
                        if 'Firefox' in browser_name:
                            files = list(Path(path).rglob('places.sqlite'))
                            for f in files:
                                try:
                                    os.remove(f)
                                    cleaned_count += 1
                                except:
                                    pass
                        
                        # Handle Safari
                        elif 'Safari' in browser_name:
                            try:
                                os.remove(path)
                                cleaned_count += 1
                            except:
                                pass
                
                except PermissionError:
                    print(f"[-] Permission denied: {browser_name}")
                except Exception as e:
                    print(f"[-] Failed to clean {browser_name}: {e}")
        
        print(f"[+] Cleaned {cleaned_count} browser artifacts")
        return cleaned_count
    
    def clean_prefetch(self):
        """
        Clean Windows Prefetch files
        
        Returns:
            int: Number of files cleaned
        """
        if self.os_type != 'Windows':
            print(f"[-] Prefetch cleaning only available on Windows")
            return 0
        
        print(f"[*] Cleaning Prefetch")
        
        if not os.path.exists(WINDOWS_PREFETCH):
            print(f"[-] Prefetch directory not found")
            return 0
        
        try:
            files = list(Path(WINDOWS_PREFETCH).glob('*.pf'))
            cleaned_count = 0
            
            for filepath in files:
                try:
                    os.remove(filepath)
                    cleaned_count += 1
                except PermissionError:
                    pass
                except Exception:
                    pass
            
            print(f"[+] Cleaned {cleaned_count} prefetch files")
            return cleaned_count
        
        except PermissionError:
            print(f"[-] Permission denied: {WINDOWS_PREFETCH}")
            return 0
        except Exception as e:
            print(f"[-] Prefetch cleaning failed: {e}")
            return 0
    
    def clean_mru(self):
        """
        Clean Windows MRU (Most Recently Used) lists
        
        Returns:
            int: Number of registry keys cleaned
        """
        if self.os_type != 'Windows':
            print(f"[-] MRU cleaning only available on Windows")
            return 0
        
        print(f"[*] Cleaning MRU lists")
        
        try:
            import winreg
        except ImportError:
            print(f"[-] winreg module not available")
            return 0
        
        cleaned_count = 0
        
        for key_path in WINDOWS_MRU_KEYS:
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    key_path,
                    0,
                    winreg.KEY_ALL_ACCESS
                )
                
                # Delete all values in the key
                i = 0
                values_deleted = 0
                
                while True:
                    try:
                        value_name = winreg.EnumValue(key, i)[0]
                        winreg.DeleteValue(key, value_name)
                        values_deleted += 1
                    except WindowsError:
                        break
                
                winreg.CloseKey(key)
                
                if values_deleted > 0:
                    print(f"[+] Cleaned: {key_path} ({values_deleted} values)")
                    cleaned_count += 1
            
            except PermissionError:
                print(f"[-] Permission denied: {key_path}")
            except FileNotFoundError:
                # Key doesn't exist, skip
                pass
            except Exception as e:
                print(f"[-] Failed to clean {key_path}: {e}")
        
        print(f"[+] Cleaned {cleaned_count} MRU registry keys")
        return cleaned_count
    
    def clean_recycle_bin(self):
        """
        Clean Recycle Bin (Windows only)
        
        Returns:
            bool: True if successful
        """
        if self.os_type != 'Windows':
            print(f"[-] Recycle Bin cleaning only available on Windows")
            return False
        
        print(f"[*] Cleaning Recycle Bin")
        
        try:
            import ctypes
            
            # SHEmptyRecycleBin
            result = ctypes.windll.shell32.SHEmptyRecycleBinW(
                None,  # Window handle
                None,  # Root path (None = all drives)
                0x0001 | 0x0002 | 0x0004  # Flags: no confirmation, no progress, no sound
            )
            
            if result == 0:
                print(f"[+] Recycle Bin cleaned")
                return True
            else:
                print(f"[-] Failed to clean Recycle Bin (error code: {result})")
                return False
        
        except Exception as e:
            print(f"[-] Recycle Bin cleaning failed: {e}")
            return False
    
    def comprehensive_cleanup(self):
        """
        Run comprehensive artifact cleanup
        
        Returns:
            dict: Results of each cleanup operation
        """
        print("="*60)
        print("COMPREHENSIVE ARTIFACT CLEANUP")
        print("="*60)
        print()
        
        results = {}
        
        # Clean temp files
        results['temp_files'] = self.clean_temp_files()
        print()
        
        # Clean browser history
        results['browser_history'] = self.clean_browser_history()
        print()
        
        # Platform-specific cleaning
        if self.os_type == 'Windows':
            # Clean Prefetch
            results['prefetch'] = self.clean_prefetch()
            print()
            
            # Clean MRU
            results['mru'] = self.clean_mru()
            print()
            
            # Clean Recycle Bin
            results['recycle_bin'] = self.clean_recycle_bin()
        
        print()
        print("="*60)
        print("CLEANUP SUMMARY")
        print("="*60)
        
        for artifact_type, count in results.items():
            if isinstance(count, bool):
                status = "✅" if count else "❌"
                print(f"{status} {artifact_type}")
            else:
                print(f"✅ {artifact_type}: {count} items")
        
        print()
        
        return results
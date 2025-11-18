"""
Practice Lab Definitions
Centralized repository of all available practice labs
"""

LAB_DEFINITIONS = {
    'dvwa': {
        'name': 'Damn Vulnerable Web Application',
        'type': 'docker',
        'description': 'Web application with common vulnerabilities',
        'setup_command': 'docker run -d --name web-dvwa -p 80:80 vulnerables/web-dvwa',
        'access_url': 'http://localhost',
        'default_creds': 'admin/password',
        'difficulty': 'beginner',
        'practice_scenarios': [
            'SQL Injection',
            'XSS (Reflected & Stored)',
            'CSRF',
            'File Upload Vulnerabilities',
            'Command Injection',
            'File Inclusion',
            'Weak Session IDs',
            'Brute Force'
        ],
        'estimated_setup_time': '2 minutes',
        'resources': {
            'github': 'https://github.com/digininja/DVWA',
            'documentation': 'https://github.com/digininja/DVWA#readme'
        }
    },
    
    'juice_shop': {
        'name': 'OWASP Juice Shop',
        'type': 'docker',
        'description': 'Modern web application with OWASP Top 10 vulnerabilities',
        'setup_command': 'docker run -d --name juice-shop -p 3000:3000 bkimminich/juice-shop',
        'access_url': 'http://localhost:3000',
        'default_creds': 'N/A',
        'difficulty': 'beginner-intermediate',
        'practice_scenarios': [
            'Authentication Bypass',
            'Injection Attacks (SQL, XSS, XXE)',
            'Broken Access Control',
            'Security Misconfiguration',
            'API Exploitation',
            'Cryptographic Failures',
            'SSRF',
            'Insecure Deserialization'
        ],
        'estimated_setup_time': '3 minutes',
        'resources': {
            'github': 'https://github.com/juice-shop/juice-shop',
            'documentation': 'https://pwning.owasp-juice.shop/',
            'companion_guide': 'https://pwning.owasp-juice.shop/'
        }
    },
    
    'webgoat': {
        'name': 'OWASP WebGoat',
        'type': 'docker',
        'description': 'Deliberately insecure application with lessons',
        'setup_command': 'docker run -d --name webgoat -p 8080:8080 -p 9090:9090 webgoat/webgoat',
        'access_url': 'http://localhost:8080/WebGoat',
        'default_creds': 'Create your own on first access',
        'difficulty': 'beginner',
        'practice_scenarios': [
            'General Security Awareness',
            'Access Control Flaws',
            'AJAX Security',
            'Authentication Flaws',
            'Client-side Filtering',
            'Code Quality',
            'Concurrency',
            'Cross-Site Scripting (XSS)'
        ],
        'estimated_setup_time': '3 minutes',
        'resources': {
            'github': 'https://github.com/WebGoat/WebGoat',
            'documentation': 'https://owasp.org/www-project-webgoat/'
        }
    },
    
    'metasploitable3': {
        'name': 'Metasploitable 3',
        'type': 'vagrant',
        'description': 'Intentionally vulnerable Linux system for Metasploit practice',
        'setup_command': 'vagrant init rapid7/metasploitable3-ub1404 && vagrant up',
        'access_url': 'ssh vagrant@localhost -p 2222',
        'default_creds': 'vagrant/vagrant',
        'difficulty': 'intermediate',
        'practice_scenarios': [
            'Service Exploitation',
            'Privilege Escalation',
            'Credential Harvesting',
            'Network Service Attacks',
            'Web Application Exploitation',
            'Post-Exploitation',
            'Lateral Movement'
        ],
        'estimated_setup_time': '15-30 minutes',
        'resources': {
            'github': 'https://github.com/rapid7/metasploitable3',
            'documentation': 'https://github.com/rapid7/metasploitable3/wiki'
        }
    },
    
    'bwapp': {
        'name': 'bWAPP (Buggy Web Application)',
        'type': 'docker',
        'description': 'Web application with over 100 vulnerabilities',
        'setup_command': 'docker run -d --name bwapp -p 8081:80 raesene/bwapp',
        'access_url': 'http://localhost:8081',
        'default_creds': 'bee/bug',
        'difficulty': 'beginner-intermediate',
        'practice_scenarios': [
            'A1 - Injection',
            'A2 - Broken Authentication',
            'A3 - Sensitive Data Exposure',
            'A4 - XML External Entities (XXE)',
            'A5 - Broken Access Control',
            'A6 - Security Misconfiguration',
            'A7 - Cross-Site Scripting (XSS)',
            'A8 - Insecure Deserialization'
        ],
        'estimated_setup_time': '2 minutes',
        'resources': {
            'website': 'http://www.itsecgames.com/',
            'documentation': 'http://www.itsecgames.com/'
        }
    },
    
    'vulnhub': {
        'name': 'VulnHub Virtual Machines',
        'type': 'manual',
        'description': 'Collection of vulnerable VMs for complete attack chains',
        'setup_command': 'Download OVA from vulnhub.com and import to VirtualBox/VMware',
        'access_url': 'Varies by VM',
        'default_creds': 'Varies by VM',
        'difficulty': 'beginner-advanced',
        'practice_scenarios': [
            'Complete Attack Chain',
            'Enumeration',
            'Exploitation',
            'Post-Exploitation',
            'Privilege Escalation',
            'CTF-style Challenges'
        ],
        'estimated_setup_time': '10-20 minutes per VM',
        'resources': {
            'website': 'https://www.vulnhub.com',
            'recommended_beginner': [
                'Basic Pentesting: 1',
                'Mr. Robot: 1',
                'Kioptrix: Level 1'
            ]
        }
    },
    
    'hackthebox': {
        'name': 'HackTheBox',
        'type': 'manual',
        'description': 'Online platform with active and retired vulnerable machines',
        'setup_command': 'Sign up at hackthebox.com and connect via VPN',
        'access_url': 'https://www.hackthebox.com',
        'default_creds': 'Create account',
        'difficulty': 'beginner-advanced',
        'practice_scenarios': [
            'Active Machines',
            'Retired Machines (with VIP)',
            'Challenges (Web, Crypto, Reversing)',
            'Fortresses (Multi-machine networks)',
            'Endgames (Red Team simulations)',
            'Pro Labs (Enterprise environments)'
        ],
        'estimated_setup_time': '10 minutes (VPN setup)',
        'resources': {
            'website': 'https://www.hackthebox.com',
            'documentation': 'https://help.hackthebox.com/',
            'forum': 'https://forum.hackthebox.com/'
        }
    },
    
    'tryhackme': {
        'name': 'TryHackMe',
        'type': 'manual',
        'description': 'Guided learning platform with hands-on labs',
        'setup_command': 'Sign up at tryhackme.com and access via browser',
        'access_url': 'https://tryhackme.com',
        'default_creds': 'Create account',
        'difficulty': 'beginner-intermediate',
        'practice_scenarios': [
            'Learning Paths (Structured)',
            'Free Rooms',
            'Premium Rooms',
            'King of the Hill',
            'Challenges',
            'Capture the Flag Events'
        ],
        'estimated_setup_time': '5 minutes',
        'resources': {
            'website': 'https://tryhackme.com',
            'documentation': 'https://docs.tryhackme.com/'
        }
    },
    
    'pentesterlab': {
        'name': 'PentesterLab',
        'type': 'manual',
        'description': 'Focused exercises on specific vulnerabilities',
        'setup_command': 'Sign up at pentesterlab.com and download exercises',
        'access_url': 'https://pentesterlab.com',
        'default_creds': 'Create account',
        'difficulty': 'beginner-advanced',
        'practice_scenarios': [
            'Web Application Vulnerabilities',
            'Network Pivoting',
            'Active Directory',
            'Binary Exploitation',
            'Mobile Security',
            'AWS Security'
        ],
        'estimated_setup_time': 'Varies by exercise',
        'resources': {
            'website': 'https://pentesterlab.com',
            'badge_system': 'Track progress with badges'
        }
    },
    
    'goad': {
        'name': 'Game of Active Directory',
        'type': 'vagrant',
        'description': 'Complete Active Directory lab environment',
        'setup_command': 'Clone repo and run: vagrant up (requires 32GB RAM)',
        'access_url': 'Multiple VMs in domain environment',
        'default_creds': 'Documented in repo',
        'difficulty': 'advanced',
        'practice_scenarios': [
            'Active Directory Enumeration',
            'Kerberoasting',
            'AS-REP Roasting',
            'Domain Privilege Escalation',
            'Lateral Movement',
            'Domain Persistence',
            'Golden/Silver Tickets'
        ],
        'estimated_setup_time': '1-2 hours',
        'resources': {
            'github': 'https://github.com/Orange-Cyberdefense/GOAD',
            'documentation': 'https://github.com/Orange-Cyberdefense/GOAD/wiki'
        }
    }
}


def get_labs_by_difficulty(difficulty):
    """Get labs filtered by difficulty level"""
    return {
        lab_id: lab for lab_id, lab in LAB_DEFINITIONS.items()
        if difficulty.lower() in lab.get('difficulty', '').lower()
    }


def get_labs_by_type(lab_type):
    """Get labs filtered by type"""
    return {
        lab_id: lab for lab_id, lab in LAB_DEFINITIONS.items()
        if lab['type'] == lab_type
    }


def get_docker_labs():
    """Get all Docker-based labs (easiest to set up)"""
    return get_labs_by_type('docker')


def get_beginner_labs():
    """Get beginner-friendly labs"""
    return get_labs_by_difficulty('beginner')
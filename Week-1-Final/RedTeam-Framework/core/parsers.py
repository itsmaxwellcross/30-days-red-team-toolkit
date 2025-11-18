"""
Parsers for extracting structured data from tool outputs
"""


class OutputParsers:
    """Collection of parsers for different tool outputs"""
    
    @staticmethod
    def parse_emails(output):
        """Parse email enumeration output"""
        emails = []
        for line in output.split('\n'):
            if '@' in line and 'Found' not in line:
                email = line.strip()
                if email:
                    emails.append(email)
        return emails
    
    @staticmethod
    def parse_subdomains(output):
        """Parse subdomain enumeration output"""
        subdomains = []
        for line in output.split('\n'):
            if 'Found:' in line:
                subdomain = line.strip()
                if subdomain:
                    subdomains.append(subdomain)
        return subdomains
    
    @staticmethod
    def parse_dork_results(output):
        """Parse Google dork results"""
        results = []
        # Implementation depends on output format
        # This is a placeholder
        for line in output.split('\n'):
            if line.strip() and not line.startswith('['):
                results.append(line.strip())
        return results
    
    @staticmethod
    def parse_tech_stack(output):
        """Parse technology fingerprinting results"""
        tech = {}
        current_category = None
        
        for line in output.split('\n'):
            line = line.strip()
            if ':' in line and not line.startswith('['):
                key, value = line.split(':', 1)
                tech[key.strip()] = value.strip()
        
        return tech
    
    @staticmethod
    def parse_vulnerabilities(output):
        """Parse vulnerability scan results"""
        vulns = []
        keywords = ['FOUND:', 'CRITICAL', 'HIGH', 'MEDIUM', 'VULNERABLE']
        
        for line in output.split('\n'):
            if any(keyword in line.upper() for keyword in keywords):
                vulns.append(line.strip())
        
        return vulns
    
    @staticmethod
    def parse_credentials(output):
        """Parse credential harvesting results"""
        credentials = []
        for line in output.split('\n'):
            if 'username' in line.lower() or 'password' in line.lower():
                credentials.append(line.strip())
        return credentials
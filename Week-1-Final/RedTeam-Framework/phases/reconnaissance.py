"""
Phase 1: Reconnaissance operations
"""

from datetime import datetime
from core.parsers import OutputParsers


class ReconnaissancePhase:
    """Handles reconnaissance operations"""
    
    def __init__(self, config, executor, logger, parsers=None):
        self.config = config
        self.executor = executor
        self.logger = logger
        self.parsers = parsers or OutputParsers()
    
    def execute(self):
        """Execute reconnaissance phase"""
        self.logger.section_header("PHASE 1: RECONNAISSANCE")
        
        phase_results = {
            'start_time': datetime.now().isoformat(),
            'subdomains': [],
            'emails': [],
            'technologies': {},
            'google_dorks': []
        }
        
        domain = self.config.get('target.domain')
        company = self.config.get('target.company_name')
        
        # Subdomain enumeration
        if self.config.get('scope.subdomains'):
            phase_results['subdomains'] = self._enumerate_subdomains(domain)
        
        # Email enumeration
        if self.config.get('scope.email_enum'):
            phase_results['emails'] = self._enumerate_emails(domain, company)
        
        # Google dorking
        phase_results['google_dorks'] = self._run_google_dorking(domain)
        
        # Technology fingerprinting
        phase_results['technologies'] = self._fingerprint_technologies(domain)
        
        phase_results['end_time'] = datetime.now().isoformat()
        self.logger.info("Phase 1 complete")
        
        return phase_results
    
    def _enumerate_subdomains(self, domain):
        """Enumerate subdomains for target domain"""
        self.logger.info("Running subdomain enumeration...")
        
        cmd_args = f"{domain} 01-reconnaissance/wordlists/subdomains.txt"
        result = self.executor.run_python_script(
            '01-reconnaissance/subdomain_enum.py',
            cmd_args
        )
        
        if result['success']:
            subdomains = self.parsers.parse_subdomains(result['stdout'])
            self.logger.info(f"Found {len(subdomains)} subdomains")
            return subdomains
        
        return []
    
    def _enumerate_emails(self, domain, company):
        """Enumerate email addresses"""
        self.logger.info("Running email enumeration...")
        
        cmd_args = f'{domain} "{company}"'
        result = self.executor.run_python_script(
            '01-reconnaissance/email_hunter.py',
            cmd_args
        )
        
        if result['success']:
            emails = self.parsers.parse_emails(result['stdout'])
            self.logger.info(f"Found {len(emails)} emails")
            return emails
        
        return []
    
    def _run_google_dorking(self, domain):
        """Run Google dorking queries"""
        self.logger.info("Running Google dorking...")
        
        result = self.executor.run_python_script(
            '01-reconnaissance/google_dorker.py',
            domain
        )
        
        if result['success']:
            return self.parsers.parse_dork_results(result['stdout'])
        
        return []
    
    def _fingerprint_technologies(self, domain):
        """Fingerprint web technologies"""
        self.logger.info("Running technology fingerprinting...")
        
        result = self.executor.run_python_script(
            '01-reconnaissance/tech_fingerprinter.py',
            f'https://{domain}'
        )
        
        if result['success']:
            return self.parsers.parse_tech_stack(result['stdout'])
        
        return {}
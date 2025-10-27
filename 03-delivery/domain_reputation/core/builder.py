"""
Main domain reputation builder orchestrator
"""
from typing import Optional
from .domain import Domain
from ..checkers import DNSChecker, BlacklistChecker, DeliverabilityTester
from ..generators import DNSGenerator, WarmupScheduler
from ..utils.formatters import OutputFormatter

class DomainReputationBuilder:
    """Main orchestrator for domain reputation analysis"""
    
    def __init__(self, domain_name: str):
        """
        Initialize builder with domain name
        
        Args:
            domain_name: Domain to analyze
        """
        self.domain = Domain(name=domain_name)
        self.dns_checker = DNSChecker(domain_name)
        self.blacklist_checker = BlacklistChecker(domain_name)
        self.deliverability_tester = DeliverabilityTester(domain_name)
        self.dns_generator = DNSGenerator(domain_name)
        self.warmup_scheduler = WarmupScheduler()
        self.formatter = OutputFormatter()
    
    def check_all(self) -> Domain:
        """
        Run all checks on the domain
        
        Returns:
            Updated Domain object with all results
        """
        print(f"[*] Domain Reputation Analysis: {self.domain.name}")
        print("=" * 60)
        print()
        
        # DNS checks
        print("[*] Checking DNS records...")
        self.domain.spf_record = self.dns_checker.check_spf()
        self.domain.dkim_record = self.dns_checker.check_dkim(self.domain.dkim_selector)
        self.domain.dmarc_record = self.dns_checker.check_dmarc()
        print()
        
        # Blacklist checks
        print("[*] Checking blacklists...")
        self.domain.blacklist_status = self.blacklist_checker.check_all()
        print()
        
        return self.domain
    
    def generate_dns_records(self, server_ip: Optional[str] = None):
        """Generate recommended DNS records"""
        self.dns_generator.generate_all(server_ip)
    
    def show_warmup_schedule(self, days: int = 14):
        """Display email warmup schedule"""
        self.warmup_scheduler.generate_schedule(days)
    
    def test_deliverability(self, recipient_email: str):
        """Test email deliverability"""
        self.deliverability_tester.test(recipient_email)
    
    def run_full_analysis(self, server_ip: Optional[str] = None, 
                         warmup_days: int = 14) -> Domain:
        """
        Run complete domain reputation analysis
        
        Args:
            server_ip: Server IP for DNS record generation
            warmup_days: Days for warmup schedule
            
        Returns:
            Completed Domain object
        """
        # Check current state
        self.check_all()
        
        # Generate recommendations
        self.generate_dns_records(server_ip)
        self.show_warmup_schedule(warmup_days)
        
        # Show summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        self.formatter.print_domain_summary(self.domain)
        
        return self.domain
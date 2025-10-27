"""
Output formatting utilities
"""
from ..core.domain import Domain

class OutputFormatter:
    """Format output for display"""
    
    @staticmethod
    def print_domain_summary(domain: Domain):
        """
        Print formatted domain summary
        
        Args:
            domain: Domain object to summarize
        """
        summary = domain.get_summary()
        
        print(f"\nDomain: {summary['domain']}")
        print("-" * 60)
        
        # Email authentication
        print("\nEmail Authentication:")
        print(f"  SPF:   {'✓ Configured' if summary['spf_configured'] else '✗ Not configured'}")
        print(f"  DKIM:  {'✓ Configured' if summary['dkim_configured'] else '✗ Not configured'}")
        print(f"  DMARC: {'✓ Configured' if summary['dmarc_configured'] else '✗ Not configured'}")
        
        # Reputation
        print("\nReputation:")
        if summary['is_clean'] is None:
            print("  Status: Not checked")
        elif summary['is_clean']:
            print("  Status: ✓ Clean (not on any blacklists)")
        else:
            print("  Status: ✗ Listed on one or more blacklists")
        
        # Overall
        print("\nOverall Status:")
        if summary['has_email_auth'] and summary['is_clean']:
            print("  ✓ Domain is properly configured and has good reputation")
        elif summary['has_email_auth']:
            print("  ⚠ Domain is configured but may have reputation issues")
        elif summary['is_clean']:
            print("  ⚠ Domain has clean reputation but lacks proper authentication")
        else:
            print("  ✗ Domain needs configuration and reputation improvement")
    
    @staticmethod
    def print_checklist(domain: Domain):
        """Print setup checklist"""
        print("\n[*] Setup Checklist:")
        print("  " + ("✓" if domain.spf_record else "☐") + " Configure SPF record")
        print("  " + ("✓" if domain.dkim_record else "☐") + " Configure DKIM record")
        print("  " + ("✓" if domain.dmarc_record else "☐") + " Configure DMARC record")
        print("  " + ("✓" if domain.is_clean() else "☐") + " Check blacklist status")
        print("  ☐ Start domain warmup process")
        print("  ☐ Monitor deliverability metrics")
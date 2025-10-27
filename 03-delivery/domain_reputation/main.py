"""
Main entry point for domain reputation builder
"""
import sys
import argparse
from .core.builder import DomainReputationBuilder

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Domain Reputation Builder - Email infrastructure setup and verification'
    )
    parser.add_argument('domain', help='Domain to analyze')
    parser.add_argument('--check-only', action='store_true',
                       help='Only check current status, no recommendations')
    parser.add_argument('--server-ip', help='Server IP for DNS record generation')
    parser.add_argument('--warmup-days', type=int, default=14,
                       help='Days for warmup schedule (default: 14)')
    parser.add_argument('--test-email', help='Send test email to this address')
    parser.add_argument('--dkim-selector', default='default',
                       help='DKIM selector to check (default: default)')
    
    args = parser.parse_args()
    
    # Initialize builder
    builder = DomainReputationBuilder(args.domain)
    builder.domain.dkim_selector = args.dkim_selector
    
    if args.check_only:
        # Just check current status
        domain = builder.check_all()
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        builder.formatter.print_domain_summary(domain)
    else:
        # Full analysis with recommendations
        domain = builder.run_full_analysis(
            server_ip=args.server_ip,
            warmup_days=args.warmup_days
        )
    
    # Test deliverability if requested
    if args.test_email:
        builder.test_deliverability(args.test_email)
    
    # Print checklist
    builder.formatter.print_checklist(domain)

if __name__ == "__main__":
    main()
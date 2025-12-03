"""
DGA Runner - CLI interface for DGA framework
"""

import argparse
import sys
from datetime import datetime
from .generator import DGAGenerator
from .agent import DGAAgent
from .utils import (
    format_output, 
    save_domains_to_file, 
    check_domain_list,
    generate_registration_commands,
    calculate_dga_cost
)


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Domain Generation Algorithm (DGA) Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 10 domains for today
  python -m dga.run --generate 10
  
  # Generate domains for next 7 days
  python -m dga.run --daily 7 --per-day 20
  
  # Generate time-based domain
  python -m dga.run --time-based
  
  # Check domains for availability
  python -m dga.run --check-domains --daily 7
  
  # Save domains to file
  python -m dga.run --daily 7 --output domains.json --format json
  
  # Calculate registration cost
  python -m dga.run --daily 7 --per-day 20 --cost-estimate
        """
    )
    
    # Basic options
    parser.add_argument('--seed', type=str,
                       help='Custom seed (default: current date)')
    parser.add_argument('--tld', type=str, default='.com',
                       help='Top-level domain (default: .com)')
    parser.add_argument('--length', type=int, default=12,
                       help='Domain name length (default: 12)')
    
    # Generation options
    parser.add_argument('--generate', type=int,
                       help='Generate N domains for today')
    parser.add_argument('--daily', type=int,
                       help='Generate domains for N days')
    parser.add_argument('--per-day', type=int, default=10,
                       help='Domains per day (default: 10)')
    parser.add_argument('--weekly', type=int,
                       help='Generate domains for N weeks')
    parser.add_argument('--per-week', type=int, default=50,
                       help='Domains per week (default: 50)')
    parser.add_argument('--time-based', action='store_true',
                       help='Generate time-based domain (hourly)')
    parser.add_argument('--interval-hours', type=int, default=1,
                       help='Time interval in hours (default: 1)')
    
    # Output options
    parser.add_argument('--output', type=str,
                       help='Output file')
    parser.add_argument('--format', type=str, default='text',
                       choices=['text', 'json', 'csv'],
                       help='Output format (default: text)')
    
    # Checking options
    parser.add_argument('--check-domains', action='store_true',
                       help='Check generated domains for availability')
    parser.add_argument('--timeout', type=int, default=2,
                       help='Domain check timeout (default: 2s)')
    
    # Utility options
    parser.add_argument('--registration-commands', action='store_true',
                       help='Generate domain registration commands')
    parser.add_argument('--registrar', type=str, default='namecheap',
                       choices=['namecheap', 'godaddy', 'cli'],
                       help='Domain registrar (default: namecheap)')
    parser.add_argument('--cost-estimate', action='store_true',
                       help='Calculate domain registration cost')
    parser.add_argument('--price-per-domain', type=float, default=10.0,
                       help='Price per domain per year (default: $10)')
    
    # Agent mode
    parser.add_argument('--agent-mode', action='store_true',
                       help='Run in agent mode (find active domains)')
    parser.add_argument('--beacon-interval', type=int, default=300,
                       help='Beacon interval in seconds (default: 300)')
    parser.add_argument('--jitter', type=int, default=60,
                       help='Beacon jitter in seconds (default: 60)')
    
    args = parser.parse_args()
    
    # Initialize generator
    dga = DGAGenerator(seed=args.seed, tld=args.tld)
    
    # Agent mode
    if args.agent_mode:
        agent = DGAAgent(dga, timeout=args.timeout)
        
        print("="*60)
        print("DGA AGENT MODE")
        print("="*60)
        print(f"[*] TLD: {args.tld}")
        print(f"[*] Beacon interval: {args.beacon_interval}s ± {args.jitter}s")
        print("="*60)
        print()
        
        agent.continuous_beacon(interval=args.beacon_interval, jitter=args.jitter)
        return
    
    # Generate single day
    if args.generate:
        print(f"[*] Generating {args.generate} domains for today:")
        print("="*60)
        
        today = datetime.now()
        seed_base = f"{today.year}{today.month:02d}{today.day:02d}"
        
        domains = []
        for i in range(args.generate):
            seed = f"{seed_base}-{i}"
            domain = dga.generate_domain(seed, length=args.length)
            domains.append(domain)
            print(f"{i+1}. {domain}")
        
        print()
        
        # Check domains if requested
        if args.check_domains:
            print("\n[*] Checking domain availability:")
            print("="*60)
            results = check_domain_list(domains, timeout=args.timeout)
            print(f"\n[+] Active: {results['active_count']}/{results['total']}")
            print(f"[-] Inactive: {results['inactive_count']}/{results['total']}")
        
        return
    
    # Time-based domain
    if args.time_based:
        domain = dga.generate_time_based_domain(interval_hours=args.interval_hours)
        print(f"[*] Current time-based domain ({args.interval_hours}h interval): {domain}")
        
        if args.check_domains:
            if check_domain_list([domain], timeout=args.timeout, verbose=False)['active_count'] > 0:
                print(f"[+] Domain is active")
            else:
                print(f"[-] Domain is inactive")
        
        return
    
    # Generate daily domains
    if args.daily:
        domains_data = dga.generate_daily_domains(
            num_days=args.daily,
            domains_per_day=args.per_day
        )
        
        print(f"[*] Generated domains for {args.daily} days:")
        print("="*60)
        print(format_output(domains_data, 'text'))
        print()
        
        # Save to file if requested
        if args.output:
            save_domains_to_file(domains_data, args.output, args.format)
        
        # Check domains if requested
        if args.check_domains:
            all_domains = []
            for day_data in domains_data:
                all_domains.extend(day_data['domains'])
            
            print("\n[*] Checking domain availability:")
            print("="*60)
            results = check_domain_list(all_domains, timeout=args.timeout)
            print(f"\n[+] Active: {results['active_count']}/{results['total']}")
            print(f"[-] Inactive: {results['inactive_count']}/{results['total']}")
        
        # Generate registration commands if requested
        if args.registration_commands:
            all_domains = []
            for day_data in domains_data:
                all_domains.extend(day_data['domains'])
            
            print("\n[*] Domain Registration Commands:")
            print("="*60)
            commands = generate_registration_commands(all_domains, args.registrar)
            for cmd in commands:
                print(cmd)
        
        # Cost estimate if requested
        if args.cost_estimate:
            total_domains = args.daily * args.per_day
            cost_data = calculate_dga_cost(total_domains, args.price_per_domain)
            
            print("\n[*] Cost Estimate:")
            print("="*60)
            print(f"Domains: {cost_data['num_domains']}")
            print(f"Price per domain: ${cost_data['price_per_domain']:.2f}/year")
            print(f"Total cost: ${cost_data['total_cost']:.2f}")
            print(f"Cost per month: ${cost_data['cost_per_month']:.2f}")
            print(f"Cost per day: ${cost_data['cost_per_day']:.2f}")
        
        return
    
    # Generate weekly domains
    if args.weekly:
        domains_data = dga.generate_weekly_domains(
            num_weeks=args.weekly,
            domains_per_week=args.per_week
        )
        
        print(f"[*] Generated domains for {args.weekly} weeks:")
        print("="*60)
        
        for week_data in domains_data:
            print(f"\n{week_data['week']} (Starting {week_data['week_start']}):")
            for i, domain in enumerate(week_data['domains'], 1):
                print(f"  {i}. {domain}")
        
        print()
        
        return
    
    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()
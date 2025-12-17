#!/usr/bin/env python3
"""
Command-line interface for automated collection
"""

import argparse
import sys
from .core import AutomatedCollector
from .filter import DataFilter
from .config import ConfigManager

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Automated Collection Framework - Schedule data collection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add collection rule
  automated_collection.py --add-rule --name "office_docs" \\
    --sources /home/user/Documents --patterns "*.docx" "*.xlsx" \\
    --schedule daily
  
  # Run collector (scheduled)
  automated_collection.py --run
  
  # Run collection immediately
  automated_collection.py --collect-now "office_docs"
  
  # Filter collected data
  automated_collection.py --filter collection_staging/office_docs/20250103_120000 \\
    --min-priority 7
  
  # List configured rules
  automated_collection.py --list-rules
        """
    )
    
    parser.add_argument('--add-rule', action='store_true',
                       help='Add collection rule')
    parser.add_argument('--name', type=str,
                       help='Rule name')
    parser.add_argument('--sources', nargs='+',
                       help='Source paths')
    parser.add_argument('--patterns', nargs='+',
                       help='File patterns (e.g., *.txt *.pdf)')
    parser.add_argument('--schedule', type=str, default='daily',
                       choices=['hourly', 'daily', 'weekly'],
                       help='Collection schedule (default: daily)')
    parser.add_argument('--max-age', type=int,
                       help='Maximum file age in days')
    
    parser.add_argument('--run', action='store_true',
                       help='Run collector with scheduling')
    parser.add_argument('--run-once', action='store_true',
                       help='Run all collections once (no scheduling)')
    parser.add_argument('--collect-now', type=str, metavar='RULE_NAME',
                       help='Run specific collection immediately')
    
    parser.add_argument('--filter', type=str, metavar='COLLECTION_DIR',
                       help='Filter collection by priority')
    parser.add_argument('--min-priority', type=int, default=5,
                       help='Minimum priority for filtering (default: 5)')
    
    parser.add_argument('--list-rules', action='store_true',
                       help='List all configured rules')
    parser.add_argument('--remove-rule', type=str, metavar='RULE_NAME',
                       help='Remove rule from configuration')
    
    parser.add_argument('--config', type=str,
                       help='Configuration file (default: collection_config.json)')
    parser.add_argument('--staging-dir', type=str, default='collection_staging',
                       help='Staging directory (default: collection_staging)')
    
    args = parser.parse_args()
    
    try:
        collector = AutomatedCollector(staging_dir=args.staging_dir)
        
        if args.add_rule:
            if not all([args.name, args.sources, args.patterns]):
                print("[!] --add-rule requires --name, --sources, and --patterns")
                return 1
            
            collector.add_collection_rule(
                args.name,
                args.sources,
                args.patterns,
                args.schedule,
                args.max_age
            )
            
            # Save to config
            collector.save_config(args.config)
        
        elif args.run:
            # Load configuration
            collector.load_config(args.config)
            
            if not collector.collections:
                print("[!] No collection rules configured")
                return 1
            
            collector.run()
        
        elif args.run_once:
            # Load and run once
            collector.load_config(args.config)
            
            if not collector.collections:
                print("[!] No collection rules configured")
                return 1
            
            collector.run_once()
        
        elif args.collect_now:
            # Load configuration
            collector.load_config(args.config)
            
            # Find and run specific rule
            rule = next((r for r in collector.collections if r['name'] == args.collect_now), None)
            
            if rule:
                collector.collect_files(rule)
            else:
                print(f"[-] Rule not found: {args.collect_now}")
                return 1
        
        elif args.filter:
            DataFilter.filter_collection(args.filter, args.min_priority)
        
        elif args.list_rules:
            rules = ConfigManager.list_rules(args.config)
            
            if rules:
                print(f"\n[*] Configured Rules:")
                print("="*60)
                for i, rule_name in enumerate(rules, 1):
                    print(f"{i}. {rule_name}")
                print()
            else:
                print("[*] No rules configured")
        
        elif args.remove_rule:
            ConfigManager.remove_rule_from_config(args.remove_rule, args.config)
        
        else:
            parser.print_help()
            return 1
        
        return 0
    
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        return 1
    except Exception as e:
        print(f"\n[-] Error: {e}", file=sys.stderr)
        return 1
if __name__ == "__main__":
    sys.exit(main())
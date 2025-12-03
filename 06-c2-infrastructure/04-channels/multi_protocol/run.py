"""
Multi-Protocol C2 Agent Runner
Main entry point for the agent
"""

import json
import argparse
from .agent import MultiProtocolAgent


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Multi-Protocol C2 Agent with automatic failover",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example configuration file (config.json):
{
    "protocol_order": ["http", "dns", "cloud", "icmp"],
    "http_server": "https://c2.example.com",
    "http_token": "your-auth-token",
    "dns_domain": "c2.example.com",
    "dns_server": "8.8.8.8",
    "icmp_server": "192.168.1.100",
    "cloud_bucket": "my-c2-bucket",
    "cloud_access_key": "AKIAIOSFODNN7EXAMPLE",
    "cloud_secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    "cloud_region": "us-east-1"
}

Usage examples:
    python -m multi_protocol.run --config config.json
    python run.py --config /path/to/config.json
        """
    )
    
    parser.add_argument(
        '--config',
        type=str,
        required=True,
        help='Path to configuration file (JSON format)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"[!] Error: Configuration file not found: {args.config}")
        return 1
    except json.JSONDecodeError as e:
        print(f"[!] Error: Invalid JSON in configuration file: {e}")
        return 1
    
    # Initialize and run agent
    try:
        agent = MultiProtocolAgent(config)
        agent.run()
    except KeyboardInterrupt:
        print("\n[!] Agent stopped by user")
        return 0
    except Exception as e:
        print(f"[!] Fatal error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
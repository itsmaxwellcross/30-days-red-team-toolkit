#!/usr/bin/env python3
"""
Phishing Framework - Main Entry Point
Modular organized version
"""

import sys
import argparse
from core.config_manager import ConfigManager
from core.database import Database
from core.campaign import Campaign
from tracking.analytics import Analytics
from server import start_server

def send_campaign(args):
    """Send phishing campaign"""
    # Load configuration
    config = ConfigManager()
    
    # Initialize database
    database = Database(config.get('database_path'))
    
    # Create campaign
    campaign = Campaign(config, database)
    
    # Send campaign
    results = campaign.send_campaign(
        args.send,
        args.template,
        args.attachment
    )
    
    print(f"\n[*] Campaign Results:")
    print(f"    Total: {results['total']}")
    print(f"    Sent: {results['sent']}")
    print(f"    Failed: {results['failed']}")
    
    database.close()

def show_stats():
    """Display campaign statistics"""
    # Load configuration
    config = ConfigManager()
    
    # Initialize database
    database = Database(config.get('database_path'))
    
    # Get analytics
    analytics = Analytics(database)
    stats = analytics.get_campaign_stats()
    
    print("\n[*] Campaign Statistics:")
    print("=" * 50)
    print(f"    Total Targets: {stats['total_targets']}")
    print(f"    Emails Opened: {stats['emails_opened']} ({stats['open_rate']:.1f}%)")
    print(f"    Links Clicked: {stats['links_clicked']} ({stats['click_rate']:.1f}%)")
    print(f"    Credentials: {stats['credentials_submitted']} ({stats['success_rate']:.1f}%)")
    print("=" * 50)
    
    database.close()

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Phishing Campaign Framework - Modular Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start tracking server
  python3 main.py --server --port 8080
  
  # Send campaign
  python3 main.py --send targets.txt --template password_reset
  
  # Send with attachment
  python3 main.py --send targets.txt --template document_review --attachment doc.pdf
  
  # View statistics
  python3 main.py --stats

Templates available:
  - password_reset
  - document_review
  - security_update
  - hr_benefits
  - voicemail
        """
    )
    
    parser.add_argument('--server', action='store_true', 
                       help='Start tracking server')
    parser.add_argument('--port', type=int, default=8080, 
                       help='Server port (default: 8080)')
    parser.add_argument('--send', type=str, 
                       help='Send campaign to targets file (CSV format)')
    parser.add_argument('--template', type=str, default='password_reset',
                       help='Email template to use (default: password_reset)')
    parser.add_argument('--attachment', type=str, 
                       help='Path to attachment file')
    parser.add_argument('--stats', action='store_true', 
                       help='Show campaign statistics')
    
    args = parser.parse_args()
    
    # Determine action
    if args.server:
        start_server(args.port)
    elif args.send:
        send_campaign(args)
    elif args.stats:
        show_stats()
    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
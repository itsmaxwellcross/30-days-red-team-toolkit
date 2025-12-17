"""
Bandwidth Throttling Manager - Main CLI
"""

import argparse
import time
from core.orchestrator import BandwidthOrchestrator
from config import (
    DEFAULT_MAX_RATE_MBPS,
    PRIORITY_HIGH,
    PRIORITY_NORMAL,
    PRIORITY_LOW
)


def main():
    parser = argparse.ArgumentParser(
        description="Bandwidth Throttling Manager - Stealth data transfer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List presets
  python main.py --list-presets
  
  # Run test with 1 Mbps limit
  python main.py --test --max-rate 1.0
  
  # Test with rate preset
  python main.py --test --rate-preset stealth
  
  # Test with schedule (night hours)
  python main.py --test --schedule-preset night
  
  # Test with custom schedule
  python main.py --test --max-rate 2.0 --start-hour 22 --end-hour 6
  
  # Queue files for transfer
  python main.py --queue file1.txt file2.txt --max-rate 1.0
  
  # Queue directory (recursive)
  python main.py --queue-dir /path/to/data --max-rate 0.5 --recursive
        """
    )
    
    # Rate settings
    rate_group = parser.add_mutually_exclusive_group()
    rate_group.add_argument('--max-rate', type=float,
                           help=f'Maximum transfer rate in Mbps (default: {DEFAULT_MAX_RATE_MBPS})')
    rate_group.add_argument('--rate-preset', type=str,
                           choices=['stealth', 'conservative', 'normal', 'moderate', 'aggressive', 'maximum'],
                           help='Use rate preset')
    
    # Schedule settings
    schedule_group = parser.add_argument_group('Schedule settings')
    schedule_group.add_argument('--start-hour', type=int,
                               help='Transfer window start hour (0-23)')
    schedule_group.add_argument('--end-hour', type=int,
                               help='Transfer window end hour (0-23)')
    schedule_group.add_argument('--schedule-preset', type=str,
                               choices=['night', 'lunch', 'off_hours', 'business', 'weekend'],
                               help='Use schedule preset')
    
    # Actions
    action_group = parser.add_argument_group('Actions')
    action_group.add_argument('--list-presets', action='store_true',
                             help='List available presets')
    action_group.add_argument('--test', action='store_true',
                             help='Run transfer test')
    action_group.add_argument('--test-chunks', type=int, default=5,
                             help='Number of chunks for test (default: 5)')
    action_group.add_argument('--test-size', type=int, default=1,
                             help='Chunk size in MB for test (default: 1)')
    
    # Queue operations
    queue_group = parser.add_argument_group('Queue operations')
    queue_group.add_argument('--queue', nargs='+',
                            help='Files to add to transfer queue')
    queue_group.add_argument('--queue-dir', type=str,
                            help='Directory to add to queue')
    queue_group.add_argument('--recursive', action='store_true',
                            help='Include subdirectories (with --queue-dir)')
    queue_group.add_argument('--priority', type=str, default='normal',
                            choices=['high', 'normal', 'low'],
                            help='Transfer priority (default: normal)')
    queue_group.add_argument('--process-queue', action='store_true',
                            help='Process the transfer queue')
    
    # Output settings
    parser.add_argument('--no-banner', action='store_true',
                       help='Suppress banner')
    
    args = parser.parse_args()
    
    orchestrator = BandwidthOrchestrator()
    
    if not args.no_banner:
        orchestrator.display_banner()
    
    # List presets
    if args.list_presets:
        orchestrator.list_presets()
        return 0
    
    # Determine schedule
    schedule = None
    if args.start_hour is not None and args.end_hour is not None:
        schedule = {
            'start_hour': args.start_hour,
            'end_hour': args.end_hour
        }
    
    # Initialize throttle
    orchestrator.initialize_throttle(
        max_rate_mbps=args.max_rate,
        rate_preset=args.rate_preset,
        schedule=schedule,
        schedule_preset=args.schedule_preset
    )
    
    if not orchestrator.throttle:
        print("[-] Failed to initialize throttle")
        return 1
    
    # Run test
    if args.test:
        orchestrator.run_test(args.test_chunks, args.test_size)
        return 0
    
    # Queue operations
    if args.queue or args.queue_dir:
        # Mock transfer function
        def mock_transfer(data):
            time.sleep(0.01)
            return True
        
        # Determine priority
        priority_map = {
            'high': PRIORITY_HIGH,
            'normal': PRIORITY_NORMAL,
            'low': PRIORITY_LOW
        }
        priority = priority_map[args.priority]
        
        # Add files to queue
        if args.queue:
            for filepath in args.queue:
                orchestrator.queue.add_file(filepath, mock_transfer, priority)
        
        # Add directory to queue
        if args.queue_dir:
            orchestrator.queue.add_directory(
                args.queue_dir,
                mock_transfer,
                priority,
                recursive=args.recursive
            )
        
        # Show queue status
        status = orchestrator.queue.get_status()
        print(f"\n[*] Queue status:")
        print(f"    Pending: {status['pending']} file(s)")
        
        # Process queue if requested
        if args.process_queue:
            orchestrator.queue.process_queue()
        else:
            print("\n[*] Use --process-queue to start transfers")
        
        return 0
    
    # List queue
    if args.process_queue and orchestrator.queue:
        orchestrator.queue.list_queue()
        orchestrator.queue.process_queue()
        return 0
    
    # No action specified
    parser.print_help()
    return 0


if __name__ == "__main__":
    import sys
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
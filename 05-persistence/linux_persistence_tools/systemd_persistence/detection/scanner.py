from ..utils.helpers import run_command
import os

class SystemdScanner:
    @staticmethod
    def list_services():
        print("[SYSTEM SERVICES]")
        res = run_command("systemctl list-units --type=service --all")
        print(res['stdout'][:3000] if res['success'] else "Error")

        print("\n[USER SERVICES]")
        res = run_command("systemctl --user list-units --type=service --all")
        print(res['stdout'][:3000] if res['success'] else "Error")

    @staticmethod
    def check_suspicious():
        patterns = ['bash -i', '/dev/tcp/', 'nc ', 'netcat', 'curl', 'wget', '/tmp/', 'sh -']
        dirs = ['/etc/systemd/system', '/lib/systemd/system', '/usr/lib/systemd/system']

        print("[*] Scanning for suspicious systemd services...")
        for d in dirs:
            if os.path.exists(d):
                res = run_command(f"grep -rE '({'|'.join(patterns)})' {d} 2>/dev/null")
                if res['success'] and res['stdout']:
                    for line in res['stdout'].splitlines():
                        if any(p in line.lower() for p in patterns):
                            print(f"[!] SUSPICIOUS → {line.strip()}")
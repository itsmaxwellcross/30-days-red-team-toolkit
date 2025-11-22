from ..utils.helpers import run_command
import os

class CronScanner:
    @staticmethod
    def list_all():
        print("[*] Listing all cron jobs...\n")
        # User crontab
        print("[USER CRONTAB]")
        r = run_command("crontab -l 2>/dev/null")
        print(r['stdout'] if r['success'] and r['stdout'].strip() else "(none)")

        # System directories
        dirs = ["/etc/cron.d", "/etc/cron.hourly", "/etc/cron.daily",
                "/etc/cron.weekly", "/etc/cron.monthly"]
        for d in dirs:
            if os.path.exists(d):
                print(f"\n[{d.upper()}]")
                r = run_command(f"ls -la {d}")
                print(r['stdout'] if r['success'] else "(error)")

    @staticmethod
    def check_suspicious():
        patterns = ['bash -i', '/dev/tcp/', 'nc ', 'netcat', 'curl.*sh',
                    'wget.*sh', 'python.*socket', 'perl.*socket',
                    '/tmp/', 'base64', 'eval']

        print("[*] Scanning for suspicious entries...")
        # User crontab
        r = run_command("crontab -l 2>/dev/null")
        if r['success']:
            for line in r['stdout'].splitlines():
                if any(p in line.lower() for p in patterns):
                    print(f"[!] USER: {line}")

        # System crons
        r = run_command('grep -rE "(bash|sh|curl|wget|nc|python|perl)" /etc/cron.* 2>/dev/null || true')
        if r['success']:
            for line in r['stdout'].splitlines():
                if any(p in line.lower() for p in patterns):
                    print(f"[!] SYSTEM: {line}")
